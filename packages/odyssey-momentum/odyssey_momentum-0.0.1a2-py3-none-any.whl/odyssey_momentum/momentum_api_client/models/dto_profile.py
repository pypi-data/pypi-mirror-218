from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="DtoProfile")


@attr.s(auto_attribs=True)
class DtoProfile:
    """
    Attributes:
        avatar_hash (Union[Unset, str]):
        bio (Union[Unset, str]):
        location (Union[Unset, str]):
        profile_link (Union[Unset, str]):
    """

    avatar_hash: Unset | str = UNSET
    bio: Unset | str = UNSET
    location: Unset | str = UNSET
    profile_link: Unset | str = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        avatar_hash = self.avatar_hash
        bio = self.bio
        location = self.location
        profile_link = self.profile_link

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if avatar_hash is not UNSET:
            field_dict["avatarHash"] = avatar_hash
        if bio is not UNSET:
            field_dict["bio"] = bio
        if location is not UNSET:
            field_dict["location"] = location
        if profile_link is not UNSET:
            field_dict["profileLink"] = profile_link

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        avatar_hash = d.pop("avatarHash", UNSET)

        bio = d.pop("bio", UNSET)

        location = d.pop("location", UNSET)

        profile_link = d.pop("profileLink", UNSET)

        dto_profile = cls(
            avatar_hash=avatar_hash,
            bio=bio,
            location=location,
            profile_link=profile_link,
        )

        dto_profile.additional_properties = d
        return dto_profile

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
