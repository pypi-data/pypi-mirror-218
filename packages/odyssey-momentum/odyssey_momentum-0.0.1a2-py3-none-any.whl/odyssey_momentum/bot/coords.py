"""Module provides support for 3D transformation."""
import typing
from dataclasses import dataclass

# TODO: what is the good vector math lib in python? or should we just go numpy based, but that pulls in 'big' c lib...
import mathutils  # type: ignore

Vec3: typing.TypeAlias = tuple[float, float, float]


class Vec3Map(typing.TypedDict):
    x: float
    y: float
    z: float


@dataclass(frozen=True, slots=True)
class Position:
    """Represents a location in 3D."""

    x: float
    y: float
    z: float

    @classmethod
    def from_dict(cls, d: Vec3Map):
        return cls(d["x"], d["y"], d["z"])

    def to_tuple(self) -> Vec3:
        return (self.x, self.y, self.z)

    def __str__(self):
        return f"⊹{self.to_tuple()}"


@dataclass(frozen=True, slots=True)
class Rotation:
    """Represents a rotation in 3D as euler angles."""

    x: float
    y: float
    z: float

    @classmethod
    def from_dict(cls, d: Vec3Map):
        return cls(d["x"], d["y"], d["z"])

    def to_tuple(self) -> Vec3:
        return (self.x, self.y, self.z)

    def __str__(self):
        return f"∡{self.to_tuple()}"


@dataclass(frozen=True, slots=True)
class Scale:
    """Represents scaling in 3D."""

    x: float
    y: float
    z: float

    @classmethod
    def from_dict(cls, d: Vec3Map):
        return cls(d["x"], d["y"], d["z"])

    def to_tuple(self) -> Vec3:
        return (self.x, self.y, self.z)

    def __str__(self):
        return f"⇲{self.to_tuple()}"


@dataclass(frozen=True, slots=True)
class Transform:
    """Represents the combined transformation in 3D."""

    position: Position
    rotation: Rotation
    scale: Scale | None = None

    def __str__(self):
        return f"{self.position} {self.rotation} {self.scale}"


def distance(pos1: Position, pos2: Position) -> float:
    """Return the distance between two points in 3D space."""
    # return _vec3(pos1).distance_to(_vec3(pos2))
    return (_vec3(pos1) - _vec3(pos2)).magnitude


def move(src: Position, target: Position, dist: float) -> Vec3:
    """Return coordinates between src and target with given distance."""
    s = _vec3(src)
    t = _vec3(target)
    factor = dist / (t - s).magnitude
    return s.lerp(t, factor).to_tuple()


def look_at(src: Position, target: Vec3) -> Vec3:
    """
    Returns rotation along the vector from src to target.
    """
    # TODO: not sure we should keep this. Devs should pick an existing lib to do stuff like this for them.
    s = _vec3(src)
    t = mathutils.Vector(target)
    direction = t - s
    return direction.to_track_quat("-X", "Z").to_euler()  # hmm, blender vs babylon orientation...


def _vec3(pos: Position) -> mathutils.Vector:
    return mathutils.Vector(pos.to_tuple())
