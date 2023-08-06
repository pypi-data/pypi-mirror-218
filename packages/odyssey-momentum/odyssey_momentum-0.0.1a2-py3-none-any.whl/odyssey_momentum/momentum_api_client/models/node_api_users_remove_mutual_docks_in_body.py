from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="NodeApiUsersRemoveMutualDocksInBody")


@attr.s(auto_attribs=True)
class NodeApiUsersRemoveMutualDocksInBody:
    """
    Attributes:
        wallet_a (str):
        wallet_b (str):
    """

    wallet_a: str
    wallet_b: str
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        wallet_a = self.wallet_a
        wallet_b = self.wallet_b

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "walletA": wallet_a,
                "walletB": wallet_b,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        wallet_a = d.pop("walletA")

        wallet_b = d.pop("walletB")

        node_api_users_remove_mutual_docks_in_body = cls(
            wallet_a=wallet_a,
            wallet_b=wallet_b,
        )

        node_api_users_remove_mutual_docks_in_body.additional_properties = d
        return node_api_users_remove_mutual_docks_in_body

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
