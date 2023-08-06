from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConfigUIFeatureFlags")


@attr.s(auto_attribs=True)
class ConfigUIFeatureFlags:
    """
    Attributes:
        newsfeed (Union[Unset, bool]):
    """

    newsfeed: Unset | bool = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        newsfeed = self.newsfeed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if newsfeed is not UNSET:
            field_dict["newsfeed"] = newsfeed

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        newsfeed = d.pop("newsfeed", UNSET)

        config_ui_feature_flags = cls(
            newsfeed=newsfeed,
        )

        config_ui_feature_flags.additional_properties = d
        return config_ui_feature_flags

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
