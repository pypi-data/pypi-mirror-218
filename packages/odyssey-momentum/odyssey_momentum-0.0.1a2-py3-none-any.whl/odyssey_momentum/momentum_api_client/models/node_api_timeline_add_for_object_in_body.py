from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="NodeApiTimelineAddForObjectInBody")


@attr.s(auto_attribs=True)
class NodeApiTimelineAddForObjectInBody:
    """
    Attributes:
        hash_ (str):
        type (str):
        description (Union[Unset, str]):
    """

    hash_: str
    type: str
    description: Unset | str = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        hash_ = self.hash_
        type = self.type
        description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "hash": hash_,
                "type": type,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        hash_ = d.pop("hash")

        type = d.pop("type")

        description = d.pop("description", UNSET)

        node_api_timeline_add_for_object_in_body = cls(
            hash_=hash_,
            type=type,
            description=description,
        )

        node_api_timeline_add_for_object_in_body.additional_properties = d
        return node_api_timeline_add_for_object_in_body

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
