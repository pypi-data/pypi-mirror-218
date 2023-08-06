from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="NodeApiResolveNodeOut")


@attr.s(auto_attribs=True)
class NodeApiResolveNodeOut:
    """
    Attributes:
        node_id (Union[Unset, str]):
        url (Union[Unset, str]):
    """

    node_id: Unset | str = UNSET
    url: Unset | str = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        node_id = self.node_id
        url = self.url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if node_id is not UNSET:
            field_dict["node_id"] = node_id
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        node_id = d.pop("node_id", UNSET)

        url = d.pop("url", UNSET)

        node_api_resolve_node_out = cls(
            node_id=node_id,
            url=url,
        )

        node_api_resolve_node_out.additional_properties = d
        return node_api_resolve_node_out

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
