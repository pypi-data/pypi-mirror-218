from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cmath_transform import CmathTransform


T = TypeVar("T", bound="DtoObject")


@attr.s(auto_attribs=True)
class DtoObject:
    """
    Attributes:
        asset_2d_id (Union[Unset, str]):
        asset_3d_id (Union[Unset, str]):
        object_type_id (Union[Unset, str]):
        owner_id (Union[Unset, str]):
        parent_id (Union[Unset, str]):
        transform (Union[Unset, CmathTransform]):
    """

    asset_2d_id: Unset | str = UNSET
    asset_3d_id: Unset | str = UNSET
    object_type_id: Unset | str = UNSET
    owner_id: Unset | str = UNSET
    parent_id: Unset | str = UNSET
    transform: Union[Unset, "CmathTransform"] = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        asset_2d_id = self.asset_2d_id
        asset_3d_id = self.asset_3d_id
        object_type_id = self.object_type_id
        owner_id = self.owner_id
        parent_id = self.parent_id
        transform: Unset | dict[str, Any] = UNSET
        if not isinstance(self.transform, Unset):
            transform = self.transform.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if asset_2d_id is not UNSET:
            field_dict["asset_2d_id"] = asset_2d_id
        if asset_3d_id is not UNSET:
            field_dict["asset_3d_id"] = asset_3d_id
        if object_type_id is not UNSET:
            field_dict["object_type_id"] = object_type_id
        if owner_id is not UNSET:
            field_dict["owner_id"] = owner_id
        if parent_id is not UNSET:
            field_dict["parent_id"] = parent_id
        if transform is not UNSET:
            field_dict["transform"] = transform

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.cmath_transform import CmathTransform

        d = src_dict.copy()
        asset_2d_id = d.pop("asset_2d_id", UNSET)

        asset_3d_id = d.pop("asset_3d_id", UNSET)

        object_type_id = d.pop("object_type_id", UNSET)

        owner_id = d.pop("owner_id", UNSET)

        parent_id = d.pop("parent_id", UNSET)

        _transform = d.pop("transform", UNSET)
        transform: Unset | CmathTransform
        if isinstance(_transform, Unset):
            transform = UNSET
        else:
            transform = CmathTransform.from_dict(_transform)

        dto_object = cls(
            asset_2d_id=asset_2d_id,
            asset_3d_id=asset_3d_id,
            object_type_id=object_type_id,
            owner_id=owner_id,
            parent_id=parent_id,
            transform=transform,
        )

        dto_object.additional_properties = d
        return dto_object

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
