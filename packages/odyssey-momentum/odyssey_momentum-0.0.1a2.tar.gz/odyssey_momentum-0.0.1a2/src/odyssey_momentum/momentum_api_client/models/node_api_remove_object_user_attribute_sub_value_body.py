from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="NodeApiRemoveObjectUserAttributeSubValueBody")


@attr.s(auto_attribs=True)
class NodeApiRemoveObjectUserAttributeSubValueBody:
    """
    Attributes:
        attribute_name (str):
        plugin_id (str):
        sub_attribute_key (str):
    """

    attribute_name: str
    plugin_id: str
    sub_attribute_key: str
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        attribute_name = self.attribute_name
        plugin_id = self.plugin_id
        sub_attribute_key = self.sub_attribute_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "attribute_name": attribute_name,
                "plugin_id": plugin_id,
                "sub_attribute_key": sub_attribute_key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        attribute_name = d.pop("attribute_name")

        plugin_id = d.pop("plugin_id")

        sub_attribute_key = d.pop("sub_attribute_key")

        node_api_remove_object_user_attribute_sub_value_body = cls(
            attribute_name=attribute_name,
            plugin_id=plugin_id,
            sub_attribute_key=sub_attribute_key,
        )

        node_api_remove_object_user_attribute_sub_value_body.additional_properties = d
        return node_api_remove_object_user_attribute_sub_value_body

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
