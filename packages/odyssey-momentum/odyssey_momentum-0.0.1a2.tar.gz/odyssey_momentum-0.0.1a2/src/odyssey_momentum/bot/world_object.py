from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field

import anyio

from odyssey_momentum import api, posbus

from . import coords, world

logger = logging.getLogger(__name__)


@dataclass
class Object:  # hmm, not the best naming wise...
    """An object in a world."""

    world: world.World = field(repr=False, compare=False)
    oid: uuid.UUID
    name: str = field(compare=False)
    # parent_id: uuid.UUID = field(repr=False, compare=False)
    asset_type: uuid.UUID = field(repr=False, compare=False)
    asset_format: int = field(repr=False, compare=False)
    # is_editable
    # thethered_to_parent
    # show_on_minimap

    @classmethod
    def from_msg(cls, world, msg) -> Object:
        user = cls(
            world=world,
            oid=uuid.UUID(msg["id"]),
            name=msg["name"],
            # parent_id=uuid.UUID(msg["parent_id"]),
            asset_format=msg["asset_format"],
            asset_type=msg["asset_type"],
        )
        user.transform = msg["transform"]
        return user

    @property
    def api(self) -> api.API:
        return self.world.api

    @property
    def transform(self) -> coords.Transform:
        return self._transform

    @transform.setter
    def transform(self, transform: coords.Transform):
        if isinstance(transform, coords.Transform):
            self._transform = transform
        else:
            self._transform = coords.Transform(
                coords.Position(**transform["position"]),
                coords.Rotation(**transform["rotation"]),
                coords.Scale(**transform["scale"]),
            )

    async def change_color(self, color: str) -> None:
        """
        Change the color of the object.

        This only works for objects with models from the standard library,
        not for custom uploaded GLB files.
        """
        await self.api.set_object_attr(self.oid, "object_color", {"value": color})

    async def move_to(self, pos: tuple[float, float, float], speed=8):
        """
        Move this object to a new location.

        Async, returns when the move is complete.
        """
        # TODO: refactor, reuse in user movement
        origin = self.transform.position
        target = coords.Position(*pos)
        distance = coords.distance(origin, target)
        update_time = 0.5  # seconds
        amount = update_time * speed
        while distance > amount:  # TODO: seperate fuzzy value, not speed.
            origin = self.transform.position
            distance = coords.distance(origin, target)
            # logger.debug("Move distance left: %s", distance)
            move = coords.move(origin, target, amount)
            rot = coords.look_at(origin, move)
            scale = self.transform.scale.to_tuple() if self.transform.scale else None
            msg = posbus.object_transform(self.oid, move, rot, scale)
            await self.world.bot._posbus_send(msg)
            await anyio.sleep(update_time)
