from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="DtoMember")


@attr.s(auto_attribs=True)
class DtoMember:
    """
    Attributes:
        avatar_hash (Union[Unset, str]):
        name (Union[Unset, str]):
        object_id (Union[Unset, str]):
        role (Union[Unset, str]):
        user_id (Union[Unset, str]):
    """

    avatar_hash: Unset | str = UNSET
    name: Unset | str = UNSET
    object_id: Unset | str = UNSET
    role: Unset | str = UNSET
    user_id: Unset | str = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        avatar_hash = self.avatar_hash
        name = self.name
        object_id = self.object_id
        role = self.role
        user_id = self.user_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if avatar_hash is not UNSET:
            field_dict["avatar_hash"] = avatar_hash
        if name is not UNSET:
            field_dict["name"] = name
        if object_id is not UNSET:
            field_dict["object_id"] = object_id
        if role is not UNSET:
            field_dict["role"] = role
        if user_id is not UNSET:
            field_dict["user_id"] = user_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        avatar_hash = d.pop("avatar_hash", UNSET)

        name = d.pop("name", UNSET)

        object_id = d.pop("object_id", UNSET)

        role = d.pop("role", UNSET)

        user_id = d.pop("user_id", UNSET)

        dto_member = cls(
            avatar_hash=avatar_hash,
            name=name,
            object_id=object_id,
            role=role,
            user_id=user_id,
        )

        dto_member.additional_properties = d
        return dto_member

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
