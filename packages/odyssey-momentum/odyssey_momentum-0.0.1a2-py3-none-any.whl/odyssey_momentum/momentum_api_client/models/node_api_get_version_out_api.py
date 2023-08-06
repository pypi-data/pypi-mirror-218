from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="NodeApiGetVersionOutApi")


@attr.s(auto_attribs=True)
class NodeApiGetVersionOutApi:
    """
    Attributes:
        major (Union[Unset, int]):
        minor (Union[Unset, int]):
        patch (Union[Unset, int]):
    """

    major: Unset | int = UNSET
    minor: Unset | int = UNSET
    patch: Unset | int = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        major = self.major
        minor = self.minor
        patch = self.patch

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if major is not UNSET:
            field_dict["major"] = major
        if minor is not UNSET:
            field_dict["minor"] = minor
        if patch is not UNSET:
            field_dict["patch"] = patch

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        major = d.pop("major", UNSET)

        minor = d.pop("minor", UNSET)

        patch = d.pop("patch", UNSET)

        node_api_get_version_out_api = cls(
            major=major,
            minor=minor,
            patch=patch,
        )

        node_api_get_version_out_api.additional_properties = d
        return node_api_get_version_out_api

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
