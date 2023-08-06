from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="NodeWalletMeta")


@attr.s(auto_attribs=True)
class NodeWalletMeta:
    """
    Attributes:
        avatar (Union[Unset, str]):
        user_id (Union[Unset, str]):
        username (Union[Unset, str]):
        wallet (Union[Unset, str]):
    """

    avatar: Unset | str = UNSET
    user_id: Unset | str = UNSET
    username: Unset | str = UNSET
    wallet: Unset | str = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        avatar = self.avatar
        user_id = self.user_id
        username = self.username
        wallet = self.wallet

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if avatar is not UNSET:
            field_dict["avatar"] = avatar
        if user_id is not UNSET:
            field_dict["userID"] = user_id
        if username is not UNSET:
            field_dict["username"] = username
        if wallet is not UNSET:
            field_dict["wallet"] = wallet

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        avatar = d.pop("avatar", UNSET)

        user_id = d.pop("userID", UNSET)

        username = d.pop("username", UNSET)

        wallet = d.pop("wallet", UNSET)

        node_wallet_meta = cls(
            avatar=avatar,
            user_id=user_id,
            username=username,
            wallet=wallet,
        )

        node_wallet_meta.additional_properties = d
        return node_wallet_meta

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
