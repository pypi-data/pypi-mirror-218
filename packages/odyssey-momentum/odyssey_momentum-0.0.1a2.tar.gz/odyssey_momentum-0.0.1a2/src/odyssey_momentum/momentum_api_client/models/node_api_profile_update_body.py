from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.node_api_profile_update_body_profile import NodeApiProfileUpdateBodyProfile


T = TypeVar("T", bound="NodeApiProfileUpdateBody")


@attr.s(auto_attribs=True)
class NodeApiProfileUpdateBody:
    """
    Attributes:
        name (Union[Unset, str]):
        profile (Union[Unset, NodeApiProfileUpdateBodyProfile]):
    """

    name: Unset | str = UNSET
    profile: Union[Unset, "NodeApiProfileUpdateBodyProfile"] = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name
        profile: Unset | dict[str, Any] = UNSET
        if not isinstance(self.profile, Unset):
            profile = self.profile.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if profile is not UNSET:
            field_dict["profile"] = profile

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.node_api_profile_update_body_profile import NodeApiProfileUpdateBodyProfile

        d = src_dict.copy()
        name = d.pop("name", UNSET)

        _profile = d.pop("profile", UNSET)
        profile: Unset | NodeApiProfileUpdateBodyProfile
        if isinstance(_profile, Unset):
            profile = UNSET
        else:
            profile = NodeApiProfileUpdateBodyProfile.from_dict(_profile)

        node_api_profile_update_body = cls(
            name=name,
            profile=profile,
        )

        node_api_profile_update_body.additional_properties = d
        return node_api_profile_update_body

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
