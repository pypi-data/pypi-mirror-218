from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="DtoStake")


@attr.s(auto_attribs=True)
class DtoStake:
    """
    Attributes:
        amount (Union[Unset, str]):
        avatar_hash (Union[Unset, str]):
        blockchain_id (Union[Unset, str]):
        last_comment (Union[Unset, str]):
        name (Union[Unset, str]):
        object_id (Union[Unset, str]):
        reward (Union[Unset, str]):
        updated_at (Union[Unset, str]):
        wallet_id (Union[Unset, str]):
    """

    amount: Unset | str = UNSET
    avatar_hash: Unset | str = UNSET
    blockchain_id: Unset | str = UNSET
    last_comment: Unset | str = UNSET
    name: Unset | str = UNSET
    object_id: Unset | str = UNSET
    reward: Unset | str = UNSET
    updated_at: Unset | str = UNSET
    wallet_id: Unset | str = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        amount = self.amount
        avatar_hash = self.avatar_hash
        blockchain_id = self.blockchain_id
        last_comment = self.last_comment
        name = self.name
        object_id = self.object_id
        reward = self.reward
        updated_at = self.updated_at
        wallet_id = self.wallet_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if amount is not UNSET:
            field_dict["amount"] = amount
        if avatar_hash is not UNSET:
            field_dict["avatar_hash"] = avatar_hash
        if blockchain_id is not UNSET:
            field_dict["blockchain_id"] = blockchain_id
        if last_comment is not UNSET:
            field_dict["last_comment"] = last_comment
        if name is not UNSET:
            field_dict["name"] = name
        if object_id is not UNSET:
            field_dict["object_id"] = object_id
        if reward is not UNSET:
            field_dict["reward"] = reward
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if wallet_id is not UNSET:
            field_dict["wallet_id"] = wallet_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        amount = d.pop("amount", UNSET)

        avatar_hash = d.pop("avatar_hash", UNSET)

        blockchain_id = d.pop("blockchain_id", UNSET)

        last_comment = d.pop("last_comment", UNSET)

        name = d.pop("name", UNSET)

        object_id = d.pop("object_id", UNSET)

        reward = d.pop("reward", UNSET)

        updated_at = d.pop("updated_at", UNSET)

        wallet_id = d.pop("wallet_id", UNSET)

        dto_stake = cls(
            amount=amount,
            avatar_hash=avatar_hash,
            blockchain_id=blockchain_id,
            last_comment=last_comment,
            name=name,
            object_id=object_id,
            reward=reward,
            updated_at=updated_at,
            wallet_id=wallet_id,
        )

        dto_stake.additional_properties = d
        return dto_stake

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
