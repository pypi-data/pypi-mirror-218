from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cmath_transform import CmathTransform


T = TypeVar("T", bound="NodeApiObjectsCreateObjectInBody")


@attr.s(auto_attribs=True)
class NodeApiObjectsCreateObjectInBody:
    """
    Attributes:
        object_name (str):
        object_type_id (str):
        parent_id (str):
        asset_2d_id (Union[Unset, str]):
        asset_3d_id (Union[Unset, str]):
        minimap (Union[Unset, bool]):
        transform (Union[Unset, CmathTransform]):
    """

    object_name: str
    object_type_id: str
    parent_id: str
    asset_2d_id: Unset | str = UNSET
    asset_3d_id: Unset | str = UNSET
    minimap: Unset | bool = UNSET
    transform: Union[Unset, "CmathTransform"] = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        object_name = self.object_name
        object_type_id = self.object_type_id
        parent_id = self.parent_id
        asset_2d_id = self.asset_2d_id
        asset_3d_id = self.asset_3d_id
        minimap = self.minimap
        transform: Unset | dict[str, Any] = UNSET
        if not isinstance(self.transform, Unset):
            transform = self.transform.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object_name": object_name,
                "object_type_id": object_type_id,
                "parent_id": parent_id,
            }
        )
        if asset_2d_id is not UNSET:
            field_dict["asset_2d_id"] = asset_2d_id
        if asset_3d_id is not UNSET:
            field_dict["asset_3d_id"] = asset_3d_id
        if minimap is not UNSET:
            field_dict["minimap"] = minimap
        if transform is not UNSET:
            field_dict["transform"] = transform

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.cmath_transform import CmathTransform

        d = src_dict.copy()
        object_name = d.pop("object_name")

        object_type_id = d.pop("object_type_id")

        parent_id = d.pop("parent_id")

        asset_2d_id = d.pop("asset_2d_id", UNSET)

        asset_3d_id = d.pop("asset_3d_id", UNSET)

        minimap = d.pop("minimap", UNSET)

        _transform = d.pop("transform", UNSET)
        transform: Unset | CmathTransform
        if isinstance(_transform, Unset):
            transform = UNSET
        else:
            transform = CmathTransform.from_dict(_transform)

        node_api_objects_create_object_in_body = cls(
            object_name=object_name,
            object_type_id=object_type_id,
            parent_id=parent_id,
            asset_2d_id=asset_2d_id,
            asset_3d_id=asset_3d_id,
            minimap=minimap,
            transform=transform,
        )

        node_api_objects_create_object_in_body.additional_properties = d
        return node_api_objects_create_object_in_body

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
