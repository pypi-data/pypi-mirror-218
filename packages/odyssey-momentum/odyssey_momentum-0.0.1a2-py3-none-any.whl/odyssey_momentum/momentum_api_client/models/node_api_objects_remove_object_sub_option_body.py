from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="NodeApiObjectsRemoveObjectSubOptionBody")


@attr.s(auto_attribs=True)
class NodeApiObjectsRemoveObjectSubOptionBody:
    """
    Attributes:
        sub_option_key (str):
    """

    sub_option_key: str
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        sub_option_key = self.sub_option_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "sub_option_key": sub_option_key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        sub_option_key = d.pop("sub_option_key")

        node_api_objects_remove_object_sub_option_body = cls(
            sub_option_key=sub_option_key,
        )

        node_api_objects_remove_object_sub_option_body.additional_properties = d
        return node_api_objects_remove_object_sub_option_body

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
