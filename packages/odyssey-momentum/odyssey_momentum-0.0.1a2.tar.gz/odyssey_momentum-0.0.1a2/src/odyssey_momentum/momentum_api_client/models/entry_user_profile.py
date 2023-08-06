from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="EntryUserProfile")


@attr.s(auto_attribs=True)
class EntryUserProfile:
    """
    Attributes:
        avatar_hash (Union[Unset, str]):
        bio (Union[Unset, str]):
        location (Union[Unset, str]):
        name (Union[Unset, str]):
        onboarded (Union[Unset, bool]):
        profile_link (Union[Unset, str]):
    """

    avatar_hash: Unset | str = UNSET
    bio: Unset | str = UNSET
    location: Unset | str = UNSET
    name: Unset | str = UNSET
    onboarded: Unset | bool = UNSET
    profile_link: Unset | str = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        avatar_hash = self.avatar_hash
        bio = self.bio
        location = self.location
        name = self.name
        onboarded = self.onboarded
        profile_link = self.profile_link

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if avatar_hash is not UNSET:
            field_dict["avatar_hash"] = avatar_hash
        if bio is not UNSET:
            field_dict["bio"] = bio
        if location is not UNSET:
            field_dict["location"] = location
        if name is not UNSET:
            field_dict["name"] = name
        if onboarded is not UNSET:
            field_dict["onboarded"] = onboarded
        if profile_link is not UNSET:
            field_dict["profile_link"] = profile_link

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        avatar_hash = d.pop("avatar_hash", UNSET)

        bio = d.pop("bio", UNSET)

        location = d.pop("location", UNSET)

        name = d.pop("name", UNSET)

        onboarded = d.pop("onboarded", UNSET)

        profile_link = d.pop("profile_link", UNSET)

        entry_user_profile = cls(
            avatar_hash=avatar_hash,
            bio=bio,
            location=location,
            name=name,
            onboarded=onboarded,
            profile_link=profile_link,
        )

        entry_user_profile.additional_properties = d
        return entry_user_profile

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
