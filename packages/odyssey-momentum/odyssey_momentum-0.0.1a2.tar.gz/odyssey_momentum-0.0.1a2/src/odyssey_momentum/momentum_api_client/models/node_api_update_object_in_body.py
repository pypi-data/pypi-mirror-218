from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="NodeApiUpdateObjectInBody")


@attr.s(auto_attribs=True)
class NodeApiUpdateObjectInBody:
    """
    Attributes:
        asset_2d_id (Union[Unset, str]):
        asset_3d_id (Union[Unset, str]):
        object_name (Union[Unset, str]):
    """

    asset_2d_id: Unset | str = UNSET
    asset_3d_id: Unset | str = UNSET
    object_name: Unset | str = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        asset_2d_id = self.asset_2d_id
        asset_3d_id = self.asset_3d_id
        object_name = self.object_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if asset_2d_id is not UNSET:
            field_dict["asset_2d_id"] = asset_2d_id
        if asset_3d_id is not UNSET:
            field_dict["asset_3d_id"] = asset_3d_id
        if object_name is not UNSET:
            field_dict["object_name"] = object_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        asset_2d_id = d.pop("asset_2d_id", UNSET)

        asset_3d_id = d.pop("asset_3d_id", UNSET)

        object_name = d.pop("object_name", UNSET)

        node_api_update_object_in_body = cls(
            asset_2d_id=asset_2d_id,
            asset_3d_id=asset_3d_id,
            object_name=object_name,
        )

        node_api_update_object_in_body.additional_properties = d
        return node_api_update_object_in_body

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
