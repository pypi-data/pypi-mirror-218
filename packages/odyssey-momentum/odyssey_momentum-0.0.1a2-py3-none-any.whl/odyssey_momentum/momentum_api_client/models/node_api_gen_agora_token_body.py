from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="NodeApiGenAgoraTokenBody")


@attr.s(auto_attribs=True)
class NodeApiGenAgoraTokenBody:
    """
    Attributes:
        screenshare (Union[Unset, bool]):
    """

    screenshare: Unset | bool = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        screenshare = self.screenshare

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if screenshare is not UNSET:
            field_dict["screenshare"] = screenshare

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        screenshare = d.pop("screenshare", UNSET)

        node_api_gen_agora_token_body = cls(
            screenshare=screenshare,
        )

        node_api_gen_agora_token_body.additional_properties = d
        return node_api_gen_agora_token_body

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
