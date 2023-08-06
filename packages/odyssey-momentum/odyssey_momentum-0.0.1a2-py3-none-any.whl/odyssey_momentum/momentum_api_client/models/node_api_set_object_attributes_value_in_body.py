from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.node_api_set_object_attributes_value_in_body_attribute_value import (
        NodeApiSetObjectAttributesValueInBodyAttributeValue,
    )


T = TypeVar("T", bound="NodeApiSetObjectAttributesValueInBody")


@attr.s(auto_attribs=True)
class NodeApiSetObjectAttributesValueInBody:
    """
    Attributes:
        attribute_name (str):
        attribute_value (NodeApiSetObjectAttributesValueInBodyAttributeValue):
        plugin_id (str):
    """

    attribute_name: str
    attribute_value: "NodeApiSetObjectAttributesValueInBodyAttributeValue"
    plugin_id: str
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        attribute_name = self.attribute_name
        attribute_value = self.attribute_value.to_dict()

        plugin_id = self.plugin_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "attribute_name": attribute_name,
                "attribute_value": attribute_value,
                "plugin_id": plugin_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.node_api_set_object_attributes_value_in_body_attribute_value import (
            NodeApiSetObjectAttributesValueInBodyAttributeValue,
        )

        d = src_dict.copy()
        attribute_name = d.pop("attribute_name")

        attribute_value = NodeApiSetObjectAttributesValueInBodyAttributeValue.from_dict(d.pop("attribute_value"))

        plugin_id = d.pop("plugin_id")

        node_api_set_object_attributes_value_in_body = cls(
            attribute_name=attribute_name,
            attribute_value=attribute_value,
            plugin_id=plugin_id,
        )

        node_api_set_object_attributes_value_in_body.additional_properties = d
        return node_api_set_object_attributes_value_in_body

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
