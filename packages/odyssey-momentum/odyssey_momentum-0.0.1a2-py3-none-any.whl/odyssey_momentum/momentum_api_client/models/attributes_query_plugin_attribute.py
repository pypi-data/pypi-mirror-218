from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="AttributesQueryPluginAttribute")


@attr.s(auto_attribs=True)
class AttributesQueryPluginAttribute:
    """
    Attributes:
        attribute_name (str):
        plugin_id (str):
    """

    attribute_name: str
    plugin_id: str
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        attribute_name = self.attribute_name
        plugin_id = self.plugin_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "attribute_name": attribute_name,
                "plugin_id": plugin_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        attribute_name = d.pop("attribute_name")

        plugin_id = d.pop("plugin_id")

        attributes_query_plugin_attribute = cls(
            attribute_name=attribute_name,
            plugin_id=plugin_id,
        )

        attributes_query_plugin_attribute.additional_properties = d
        return attributes_query_plugin_attribute

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
