from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="DtoWalletInfo")


@attr.s(auto_attribs=True)
class DtoWalletInfo:
    """
    Attributes:
        balance (Union[Unset, str]):
        blockchain_name (Union[Unset, str]):
        contract_id (Union[Unset, str]):
        reward (Union[Unset, str]):
        staked (Union[Unset, str]):
        transferable (Union[Unset, str]):
        unbonding (Union[Unset, str]):
        updated_at (Union[Unset, str]):
        wallet_id (Union[Unset, str]):
    """

    balance: Unset | str = UNSET
    blockchain_name: Unset | str = UNSET
    contract_id: Unset | str = UNSET
    reward: Unset | str = UNSET
    staked: Unset | str = UNSET
    transferable: Unset | str = UNSET
    unbonding: Unset | str = UNSET
    updated_at: Unset | str = UNSET
    wallet_id: Unset | str = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        balance = self.balance
        blockchain_name = self.blockchain_name
        contract_id = self.contract_id
        reward = self.reward
        staked = self.staked
        transferable = self.transferable
        unbonding = self.unbonding
        updated_at = self.updated_at
        wallet_id = self.wallet_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if balance is not UNSET:
            field_dict["balance"] = balance
        if blockchain_name is not UNSET:
            field_dict["blockchain_name"] = blockchain_name
        if contract_id is not UNSET:
            field_dict["contract_id"] = contract_id
        if reward is not UNSET:
            field_dict["reward"] = reward
        if staked is not UNSET:
            field_dict["staked"] = staked
        if transferable is not UNSET:
            field_dict["transferable"] = transferable
        if unbonding is not UNSET:
            field_dict["unbonding"] = unbonding
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if wallet_id is not UNSET:
            field_dict["wallet_id"] = wallet_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        balance = d.pop("balance", UNSET)

        blockchain_name = d.pop("blockchain_name", UNSET)

        contract_id = d.pop("contract_id", UNSET)

        reward = d.pop("reward", UNSET)

        staked = d.pop("staked", UNSET)

        transferable = d.pop("transferable", UNSET)

        unbonding = d.pop("unbonding", UNSET)

        updated_at = d.pop("updated_at", UNSET)

        wallet_id = d.pop("wallet_id", UNSET)

        dto_wallet_info = cls(
            balance=balance,
            blockchain_name=blockchain_name,
            contract_id=contract_id,
            reward=reward,
            staked=staked,
            transferable=transferable,
            unbonding=unbonding,
            updated_at=updated_at,
            wallet_id=wallet_id,
        )

        dto_wallet_info.additional_properties = d
        return dto_wallet_info

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
