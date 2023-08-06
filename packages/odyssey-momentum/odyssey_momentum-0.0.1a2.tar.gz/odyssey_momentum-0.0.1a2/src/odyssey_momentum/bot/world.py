from __future__ import annotations

import contextlib
import logging
import typing
import uuid
from dataclasses import dataclass, field

import anyio

from odyssey_momentum import api, posbus

from . import coords
from .bot import Bot
from .user import User
from .world_object import Object

logger = logging.getLogger(__name__)


@dataclass
class HighFive:
    sender: uuid.UUID
    receiver: uuid.UUID
    # message

    @classmethod
    def from_msg(cls, _world: World, msg: posbus.InMessage):
        # TODO: _world, so we can implement an 'easy' respond/send back h5?
        return HighFive(sender=uuid.UUID(msg["sender_id"]), receiver=uuid.UUID(msg["receiver_id"]))


@dataclass
class World:
    """Represents the world a user is in."""

    bot: Bot = field(repr=False, compare=False)
    wid: uuid.UUID
    name: str = field(compare=False)
    # avatar
    # owner
    # avatar_3d_asset_id

    # variable world state tracking attrs:
    _users: typing.MutableMapping[uuid.UUID, User] = field(init=False, repr=False, compare=False, default_factory=dict)
    _objects: typing.MutableMapping[uuid.UUID, Object] = field(
        init=False, repr=False, compare=False, default_factory=dict
    )

    def __post_init__(self):
        # user_send, user_recv = anyio.create_memory_object_stream(0, User)
        pass

    @property
    def api(self) -> api.API:
        return self.bot.api

    @classmethod
    def from_msg(cls, bot: Bot, msg: posbus.InMessage) -> World:
        assert msg["id"] is not None
        return cls(
            bot=bot,
            wid=uuid.UUID(msg["id"]),  # type: ignore
            name=msg["name"],
        )

    @contextlib.asynccontextmanager
    async def user_stream(
        self,
    ) -> typing.AsyncIterator[typing.AsyncGenerator[User, None]]:
        """Users entering the world."

        Async context manager that yields a async generator of users when they enter the world.
        """
        async with self.bot.messages([posbus.MsgType.TypeAddUsers]) as stream:
            yield self._user_generator(stream)

    async def _user_generator(self, stream):
        async for (_, msg) in stream:
            for u in (e for e in msg["users"] if not e["id"] == self.bot.user_id):
                yield User.from_msg(self, u)

    @contextlib.asynccontextmanager
    async def high_five_stream(
        self,
    ) -> typing.AsyncIterator[typing.AsyncGenerator[HighFive, None]]:
        """High five events in the world."""
        async with self.bot.messages([posbus.MsgType.TypeHighFive]) as stream:
            yield self._h5_generator(stream)

    async def _h5_generator(self, stream):
        async for (_, msg) in stream:
            yield HighFive.from_msg(self, msg)

    async def move_bot(self, pos: coords.Position, speed=32):
        """
        Move this bot to specific coordinates.

        Async, returns when the move is complete.
        """
        origin, _ = self.bot.transform
        target = pos
        distance = coords.distance(origin, pos)
        update_time = 0.5  # seconds
        amount = update_time * speed
        while distance > amount:  # TODO: seperate fuzzy value, not speed.
            origin, _ = self.bot.transform
            distance = coords.distance(origin, pos)
            logger.debug("Move distance left: %s", distance)
            move = coords.move(origin, target, amount)
            msg = posbus.my_transform(move, (0, 0, 0))  # TODO: rotation
            await self.bot.send(msg)
            await anyio.sleep(update_time)

    async def move_bot_to_user(self, usr: User):
        """
        Move this bot towards a user.

        Since an user can move itself, this 'chases' after them.

        Async, returns when the bot is 'near' the user.
        """
        tracked_usr = self._users.get(usr.uid, usr)  # TODO: get fallback, handle as error?

        # TODO: refacor, share with move_bot
        origin, _ = self.bot.transform
        target = tracked_usr.transform.position
        distance = coords.distance(origin, target)
        update_time = 0.5  # seconds
        speed = 16  # TODO
        amount = update_time * speed
        while distance > amount:  # TODO: seperate fuzzy value, not speed.
            tracked_usr = self._users.get(usr.uid, usr)
            origin, _ = self.bot.transform
            target = tracked_usr.transform.position
            distance = coords.distance(origin, target)
            logger.debug("Move distance left: %s", distance)
            move = coords.move(origin, target, amount)
            msg = posbus.my_transform(move, (0, 0, 0))  # TODO: rotation
            await self.bot.send(msg)
            await anyio.sleep(update_time)

    async def track_objects(self):
        """
        Async task to track all objects in a world.

        Means we keep the state of all objects in the world.
        Should be run as an async task.
        """
        async with self.bot.messages([posbus.MsgType.TypeAddObjects, posbus.MsgType.TypeObjectTransform]) as stream:
            async for (type_, msg) in stream:
                if type_ == posbus.MsgType.TypeAddObjects:
                    for obj in msg["objects"]:
                        o = Object.from_msg(self, obj)
                        await self._update_object(o)
                elif type_ == posbus.MsgType.TypeObjectTransform:
                    oid = uuid.UUID(msg["id"])
                    obj = self._objects.get(oid, None)
                    if obj is None:
                        logger.warning("Transform for unknown object %s", oid)
                        return
                    obj.transform = msg["object_transform"]

    async def _update_object(self, obj: Object):
        o = self._objects.get(obj.oid, None)
        if o is None:
            o = obj
        # currently, only deals with AddObject, so:
        self._objects[obj.oid] = o

    async def track_users(self):
        """
        Async task to track all users in a world.

        Means we keep the state of all users in the world.
        Should be run as an async task.
        """
        # TODO: TypeAddUser/RemoveUser. Need bot.messages to handle multiple types?
        async with self.bot.messages([posbus.MsgType.TypeUsersTransformList]) as stream:
            async for (_type, msg) in stream:
                for value in msg["value"]:
                    user_id = value["id"]
                    if user_id != self.bot.user_id:
                        transform = value["transform"]
                        uid = uuid.UUID(user_id)
                        trans = coords.Transform(
                            coords.Position.from_dict(transform["position"]),
                            coords.Rotation.from_dict(transform["rotation"]),
                        )
                        await self._update_user_transform(uid, trans)

    async def _update_user_transform(self, uid: uuid.UUID, transform: coords.Transform):
        usr = self._users.get(uid, None)
        if usr is None:
            usr = User(self, uid, "", "", is_guest=False)  # TODO: track addusers
            self._users[uid] = usr
        usr.transform = transform

    async def high_five(self, usr: User):
        """Send a high-five event to a user."""
        msg = posbus.high_five(self.bot.uid, usr.uid)
        await self.bot.send(msg)

    async def spawn_object(
        self,
        name: str,
        asset_id: str,
        position: tuple[float, float, float] | None = None,
        rotation: tuple[float, float, float] | None = None,
        scale: tuple[float, float, float] | None = None,
    ) -> uuid.UUID:
        oid = await self.api.create_object(name, self.wid, asset_id, position, rotation, scale)
        # TODO: assuming object tracker is running, wait for it to arrive...
        return oid

    async def remove_object(self, oid: uuid.UUID) -> None:
        await self.api.remove_object(oid)

    async def get_object(self, oid: uuid.UUID) -> Object:
        try:
            return self._objects[oid]
        except KeyError as e:
            # TODO: await for new object?
            msg = "World object not found"
            raise ValueError(msg) from e

    def object_list(self) -> typing.Iterable[Object]:
        """
        Return sequence of known objects.

        Synchronous, returns current state.
        """
        return self._objects.values()
