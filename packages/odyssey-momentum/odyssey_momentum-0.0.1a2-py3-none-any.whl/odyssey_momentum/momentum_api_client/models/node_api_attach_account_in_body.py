from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="NodeApiAttachAccountInBody")


@attr.s(auto_attribs=True)
class NodeApiAttachAccountInBody:
    """
    Attributes:
        signed_challenge (str):
        wallet (str):
        network (Union[Unset, str]):
    """

    signed_challenge: str
    wallet: str
    network: Unset | str = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        signed_challenge = self.signed_challenge
        wallet = self.wallet
        network = self.network

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "signedChallenge": signed_challenge,
                "wallet": wallet,
            }
        )
        if network is not UNSET:
            field_dict["network"] = network

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        signed_challenge = d.pop("signedChallenge")

        wallet = d.pop("wallet")

        network = d.pop("network", UNSET)

        node_api_attach_account_in_body = cls(
            signed_challenge=signed_challenge,
            wallet=wallet,
            network=network,
        )

        node_api_attach_account_in_body.additional_properties = d
        return node_api_attach_account_in_body

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
