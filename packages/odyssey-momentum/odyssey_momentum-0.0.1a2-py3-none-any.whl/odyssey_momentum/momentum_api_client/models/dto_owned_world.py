from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="DtoOwnedWorld")


@attr.s(auto_attribs=True)
class DtoOwnedWorld:
    """
    Attributes:
        avatar_hash (Union[Unset, str]):
        description (Union[Unset, str]):
        id (Union[Unset, str]):
        name (Union[Unset, str]):
        owner_id (Union[Unset, str]):
        owner_name (Union[Unset, str]):
        website_link (Union[Unset, str]):
    """

    avatar_hash: Unset | str = UNSET
    description: Unset | str = UNSET
    id: Unset | str = UNSET
    name: Unset | str = UNSET
    owner_id: Unset | str = UNSET
    owner_name: Unset | str = UNSET
    website_link: Unset | str = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        avatar_hash = self.avatar_hash
        description = self.description
        id = self.id
        name = self.name
        owner_id = self.owner_id
        owner_name = self.owner_name
        website_link = self.website_link

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if avatar_hash is not UNSET:
            field_dict["avatarHash"] = avatar_hash
        if description is not UNSET:
            field_dict["description"] = description
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if owner_id is not UNSET:
            field_dict["owner_id"] = owner_id
        if owner_name is not UNSET:
            field_dict["owner_name"] = owner_name
        if website_link is not UNSET:
            field_dict["website_link"] = website_link

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        avatar_hash = d.pop("avatarHash", UNSET)

        description = d.pop("description", UNSET)

        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        owner_id = d.pop("owner_id", UNSET)

        owner_name = d.pop("owner_name", UNSET)

        website_link = d.pop("website_link", UNSET)

        dto_owned_world = cls(
            avatar_hash=avatar_hash,
            description=description,
            id=id,
            name=name,
            owner_id=owner_id,
            owner_name=owner_name,
            website_link=website_link,
        )

        dto_owned_world.additional_properties = d
        return dto_owned_world

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
