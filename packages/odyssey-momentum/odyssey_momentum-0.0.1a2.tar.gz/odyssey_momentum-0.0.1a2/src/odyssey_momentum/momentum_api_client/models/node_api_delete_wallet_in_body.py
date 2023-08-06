from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="NodeApiDeleteWalletInBody")


@attr.s(auto_attribs=True)
class NodeApiDeleteWalletInBody:
    """
    Attributes:
        wallet (str):
    """

    wallet: str
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        wallet = self.wallet

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "wallet": wallet,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        wallet = d.pop("wallet")

        node_api_delete_wallet_in_body = cls(
            wallet=wallet,
        )

        node_api_delete_wallet_in_body.additional_properties = d
        return node_api_delete_wallet_in_body

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
