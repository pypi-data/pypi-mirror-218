from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="NodeNodeJSOut")


@attr.s(auto_attribs=True)
class NodeNodeJSOut:
    """
    Attributes:
        data (Union[Unset, Any]):
        error (Union[Unset, str]):
        logs (Union[Unset, List[str]]):
    """

    data: Unset | Any = UNSET
    error: Unset | str = UNSET
    logs: Unset | list[str] = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = self.data
        error = self.error
        logs: Unset | list[str] = UNSET
        if not isinstance(self.logs, Unset):
            logs = self.logs

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if data is not UNSET:
            field_dict["data"] = data
        if error is not UNSET:
            field_dict["error"] = error
        if logs is not UNSET:
            field_dict["logs"] = logs

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        data = d.pop("data", UNSET)

        error = d.pop("error", UNSET)

        logs = cast(list[str], d.pop("logs", UNSET))

        node_node_js_out = cls(
            data=data,
            error=error,
            logs=logs,
        )

        node_node_js_out.additional_properties = d
        return node_node_js_out

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
