from __future__ import annotations

import contextlib
import logging
import typing
import uuid

import anyio
import anyio.abc

from odyssey_momentum import api, posbus

from . import coords, world

logger = logging.getLogger(__name__)

_MsgHandlerType = typing.Callable[[posbus.MsgType, posbus.InMessage], typing.Awaitable[None]]

STREAM_BUFFER_SIZE = 0


class Bot:
    """
    A bot represents a single, automated user in Momentum.

    It is work-in-progress, not feature complete and no compatibility guarantees.

    This wraps the low level sync communication libray into a more traditional, object oriented, stateful model.

    The functionality is still inherently async, so the bot should run inside an (anyio) async context.
    So instaces are to be used as a AsycnContextManager.
    """

    _base_url: str
    _auth: posbus.auth.Auth
    _posbus_connected = False
    _posbus_send: posbus.SendFunc
    _exit_stack: contextlib.AsyncExitStack
    _task_group: anyio.abc.TaskGroup
    _world: world.World | None = None
    _set_world: anyio.Event
    _transform: coords.Transform | None = None
    _set_transform: anyio.Event
    _subscribers: typing.MutableMapping[posbus.MsgType, list[_MsgHandlerType]]
    _api: api.API | None = None

    def __init__(self, server_url: str):
        server_url = server_url.rstrip("/")
        self.server_url = server_url
        self._subscribers = {}
        self._setup_handlers()

    @property
    def server_url(self):
        return self._base_url

    @server_url.setter
    def server_url(self, url: str):
        """Set the remote server to connect to."""
        self._base_url = url
        # TODO: disconnect+reconnect when needed.

    @property
    def auth(self) -> posbus.Auth:
        return self._auth

    @property
    def user_id(self) -> str:
        return self.auth["id"]

    @property
    def uid(self) -> uuid.UUID:
        return uuid.UUID(self.user_id)

    @property
    def transform(self) -> tuple[coords.Position, coords.Rotation]:
        assert self._transform is not None  # TODO, make async everywhere
        return self._transform.position, self._transform.rotation

    @property
    def api(self) -> api.API:
        assert self._api is not None
        return self._api

    async def authenticate_guest(self, *, cache=False):
        """
        Authenticate as a (new) guest user.

        Guest authentication can be cached (in a file on disk) to avoid creating a lot of accounts.
        """
        self._auth = await posbus.authenticate_guest(self.server_url, cache=cache)
        self._api = api.API(self.server_url, self._auth["token"])
        # TODO: disconnect+reconnect when needed.

    async def authenticate(self, account_key: str):
        """
        Authenticate as an existing user.

        args:
          account_key: Private key of an ethereum account, either hexadecimal or mnemonic words.
        """
        account = posbus.web3_account(account_key)
        self._auth = await posbus.authenticate_web3(self.server_url, account)
        self._api = api.API(self.server_url, self._auth["token"])

    async def teleport(self, world_id: str):
        """
        Teleport to a world.

        args:
        world_id: Identifier of the world in UUID syntax (e.g. "00000000-0000-8000-8000-000000000001").
        """
        await self._ensure_connection()
        logger.debug("Teleport to world %s", world_id)
        await self._posbus_send(posbus.teleport_request(world_id))
        world = await self.world()
        await self.get_transform()
        return world

    async def world(self) -> world.World:
        if self._set_world.is_set():
            assert self._world is not None
            return self._world
        logger.debug("Waiting for world...")
        await self._set_world.wait()
        assert self._world is not None
        return self._world

    async def get_transform(self) -> coords.Transform:
        """
        Return the transformation of this account 3D representation (a.k.a the wisp).

        Async, this waits for the transformation to arrive from the remote server.

        """
        if self._set_transform.is_set():
            assert self._transform is not None
            return self._transform
        logger.debug("Waiting for transform...")
        await self._set_transform.wait()
        assert self._transform is not None
        return self._transform

    async def _ensure_connection(self):
        if not self._posbus_connected:
            await self._connect()

    async def _connect(self):
        logger.debug("Connecting to %s", self.server_url)
        send, stream = await self._exit_stack.enter_async_context(posbus.connect(self.server_url, self.auth))
        self._posbus_send = send

        self._task_group.start_soon(self._posbus_reader, stream, name="posbus reader")
        self._posbus_connected = True

    async def _posbus_reader(self, stream: posbus.InGenerator):
        logger.debug("Start posbus reader task...")
        async for (msg_type, msg) in stream:
            await self._handle_message(msg_type, msg)

    async def _handle_message(self, type_: posbus.MsgType, msg: posbus.InMessage):
        # logger.debug("Handle message %s", msg)
        # type_ = msg.get_type()
        for handler in self._subscribers.get(type_, []):
            try:
                await handler(type_, msg)
            except Exception as e:
                logger.error("Handler %s for type %s", handler, type_, exc_info=e)

    def _setup_handlers(self):
        self._add_handler(posbus.MsgType.TypeSetWorld, self._handle_world)
        self._add_handler(posbus.MsgType.TypeMyTransform, self._handle_my_transform)
        self._add_handler(posbus.MsgType.TypeUsersTransformList, self._handle_user_transform_list)

    async def _handle_world(self, _type, msg: posbus.InMessage):
        self._world = world.World.from_msg(self, msg)
        self._set_world.set()

    async def _handle_my_transform(self, _type, msg: posbus.InMessage):
        pos = msg["position"]
        rot = msg["rotation"]
        self._transform = coords.Transform(coords.Position.from_dict(pos), coords.Rotation.from_dict(rot))
        self._set_transform.set()

    async def _handle_user_transform_list(self, _type, msg: posbus.InMessage):
        for value in msg["value"]:
            if value["id"] == self.user_id:
                # bah, own position also comes in here, next to the initial my_transform...
                transform = value["transform"]
                self._transform = coords.Transform(
                    coords.Position.from_dict(transform["position"]),
                    coords.Rotation.from_dict(transform["rotation"]),
                )

    def _add_handler(self, type_: posbus.MsgType, handler: _MsgHandlerType):
        hs = self._subscribers.get(type_, [])
        hs.append(handler)
        self._subscribers[type_] = hs

    def _remove_handler(self, type_: posbus.MsgType, handler: _MsgHandlerType):
        hs = self._subscribers.get(type_, None)
        if hs is not None:
            hs.remove(handler)

    async def send(self, msg: posbus.OutMessage):
        """Send a message to the remote server."""
        await self._ensure_connection()
        await self._posbus_send(msg)

    @contextlib.asynccontextmanager
    async def messages(self, msg_types: typing.Iterable[posbus.MsgType]):
        """Return stream of message for given types."""
        # logging.debug("Messages %s", type_)
        send_stream, recv_stream = anyio.create_memory_object_stream(
            STREAM_BUFFER_SIZE, tuple[posbus.MsgType, posbus.InMessage]
        )

        async def handler(msg_type: posbus.MsgType, msg: posbus.InMessage):
            try:
                await send_stream.send((msg_type, msg))
            except anyio.BrokenResourceError:
                logger.debug("Broken stream")
                return

        for type_ in msg_types:
            self._add_handler(type_, handler)
        yield recv_stream
        for type_ in msg_types:
            self._remove_handler(type_, handler)

    async def move_to(self, pos: coords.Position):
        """
        Move this bot to specific coordinates.

        Async, returns when to move is complete.
        """
        origin, _ = self.transform
        target = pos
        distance = coords.distance(origin, pos)
        update_time = 0.5  # seconds
        speed = 16  # TODO
        amount = update_time * speed
        while distance > amount:  # TODO: seperate fuzzy value, not speed.
            origin, _ = self.transform
            distance = coords.distance(origin, pos)
            logger.debug("Move distance left: %s", distance)
            move = coords.move(origin, target, amount)
            msg = posbus.my_transform(move, (0, 0, 0))  # TODO: rotation
            await self._posbus_send(msg)
            await anyio.sleep(update_time)

    async def profile(self) -> api.User:
        """Return the bot's account profile."""
        assert self._api is not None
        return await self._api.current_user()

    async def update_profile(self, name: str, image: typing.IO[bytes]):
        """Update the name and image of the account."""
        assert self._api is not None
        return await self._api.update_profile(name, image)

    async def asset_list(self):
        """Return list of 3D assets"""
        assert self._api is not None
        return await self._api.asset_list()

    async def asset_upload(self, name: str, file: typing.IO[bytes]):
        """
        Upload a new 3D model (GLB) file.
        """
        assert self._api is not None
        return await self._api.asset_upload(name=name, asset=file)

    async def __aenter__(self):
        self._exit_stack = contextlib.AsyncExitStack()
        await self._exit_stack.__aenter__()
        self._task_group = await self._exit_stack.enter_async_context(anyio.create_task_group())
        self._set_world = anyio.Event()
        self._set_transform = anyio.Event()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        logger.debug("Exit bot context.")
        await self._exit_stack.__aexit__(exc_type, exc, tb)
