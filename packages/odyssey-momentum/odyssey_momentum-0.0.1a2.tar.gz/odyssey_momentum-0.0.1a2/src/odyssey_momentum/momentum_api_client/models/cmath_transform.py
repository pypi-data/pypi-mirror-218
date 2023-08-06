from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cmath_vec_3 import CmathVec3


T = TypeVar("T", bound="CmathTransform")


@attr.s(auto_attribs=True)
class CmathTransform:
    """
    Attributes:
        position (Union[Unset, CmathVec3]):
        rotation (Union[Unset, CmathVec3]):
        scale (Union[Unset, CmathVec3]):
    """

    position: Union[Unset, "CmathVec3"] = UNSET
    rotation: Union[Unset, "CmathVec3"] = UNSET
    scale: Union[Unset, "CmathVec3"] = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        position: Unset | dict[str, Any] = UNSET
        if not isinstance(self.position, Unset):
            position = self.position.to_dict()

        rotation: Unset | dict[str, Any] = UNSET
        if not isinstance(self.rotation, Unset):
            rotation = self.rotation.to_dict()

        scale: Unset | dict[str, Any] = UNSET
        if not isinstance(self.scale, Unset):
            scale = self.scale.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if position is not UNSET:
            field_dict["position"] = position
        if rotation is not UNSET:
            field_dict["rotation"] = rotation
        if scale is not UNSET:
            field_dict["scale"] = scale

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.cmath_vec_3 import CmathVec3

        d = src_dict.copy()
        _position = d.pop("position", UNSET)
        position: Unset | CmathVec3
        if isinstance(_position, Unset):
            position = UNSET
        else:
            position = CmathVec3.from_dict(_position)

        _rotation = d.pop("rotation", UNSET)
        rotation: Unset | CmathVec3
        if isinstance(_rotation, Unset):
            rotation = UNSET
        else:
            rotation = CmathVec3.from_dict(_rotation)

        _scale = d.pop("scale", UNSET)
        scale: Unset | CmathVec3
        if isinstance(_scale, Unset):
            scale = UNSET
        else:
            scale = CmathVec3.from_dict(_scale)

        cmath_transform = cls(
            position=position,
            rotation=rotation,
            scale=scale,
        )

        cmath_transform.additional_properties = d
        return cmath_transform

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
