from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="DtoWorldStaker")


@attr.s(auto_attribs=True)
class DtoWorldStaker:
    """
    Attributes:
        avatar_hash (Union[Unset, str]):
        name (Union[Unset, str]):
        stake (Union[Unset, str]):
        user_id (Union[Unset, str]):
    """

    avatar_hash: Unset | str = UNSET
    name: Unset | str = UNSET
    stake: Unset | str = UNSET
    user_id: Unset | str = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        avatar_hash = self.avatar_hash
        name = self.name
        stake = self.stake
        user_id = self.user_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if avatar_hash is not UNSET:
            field_dict["avatarHash"] = avatar_hash
        if name is not UNSET:
            field_dict["name"] = name
        if stake is not UNSET:
            field_dict["stake"] = stake
        if user_id is not UNSET:
            field_dict["user_id"] = user_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        avatar_hash = d.pop("avatarHash", UNSET)

        name = d.pop("name", UNSET)

        stake = d.pop("stake", UNSET)

        user_id = d.pop("user_id", UNSET)

        dto_world_staker = cls(
            avatar_hash=avatar_hash,
            name=name,
            stake=stake,
            user_id=user_id,
        )

        dto_world_staker.additional_properties = d
        return dto_world_staker

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
