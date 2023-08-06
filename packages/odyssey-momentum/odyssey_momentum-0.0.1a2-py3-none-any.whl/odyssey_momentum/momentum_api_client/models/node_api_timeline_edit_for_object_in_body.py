from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="NodeApiTimelineEditForObjectInBody")


@attr.s(auto_attribs=True)
class NodeApiTimelineEditForObjectInBody:
    """
    Attributes:
        description (Union[Unset, str]):
        hash_ (Union[Unset, str]):
        type (Union[Unset, str]):
    """

    description: Unset | str = UNSET
    hash_: Unset | str = UNSET
    type: Unset | str = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description = self.description
        hash_ = self.hash_
        type = self.type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if hash_ is not UNSET:
            field_dict["hash"] = hash_
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        description = d.pop("description", UNSET)

        hash_ = d.pop("hash", UNSET)

        type = d.pop("type", UNSET)

        node_api_timeline_edit_for_object_in_body = cls(
            description=description,
            hash_=hash_,
            type=type,
        )

        node_api_timeline_edit_for_object_in_body.additional_properties = d
        return node_api_timeline_edit_for_object_in_body

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
