from __future__ import annotations

import typing
import uuid
from dataclasses import dataclass, field

from odyssey_momentum import posbus

from .coords import Position, Rotation, Transform

if typing.TYPE_CHECKING:
    from .world import World


@dataclass
class User:
    world: World = field(repr=False, compare=False)
    uid: uuid.UUID
    name: str = field(compare=False)
    avatar: str = field(compare=False, repr=False)
    is_guest: bool = field(compare=False, repr=False)

    @classmethod
    def from_msg(cls, world: World, msg: posbus.InMessage) -> User:
        user = cls(
            world=world,
            uid=uuid.UUID(msg["id"]),
            name=msg["name"],
            avatar=msg["avatar"],
            is_guest=msg["is_guest"],  # type: ignore
        )
        user.transform = msg["transform"]
        return user

    @property
    def transform(self) -> Transform:
        return self._transform

    @transform.setter
    def transform(self, transform):
        if isinstance(transform, Transform):
            self._transform = transform
        else:
            self._transform = Transform(Position(**transform["position"]), Rotation(**transform["rotation"]))
