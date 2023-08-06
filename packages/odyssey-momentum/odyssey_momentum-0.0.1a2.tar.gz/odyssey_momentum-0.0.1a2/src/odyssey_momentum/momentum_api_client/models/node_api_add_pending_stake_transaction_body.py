from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="NodeApiAddPendingStakeTransactionBody")


@attr.s(auto_attribs=True)
class NodeApiAddPendingStakeTransactionBody:
    """
    Attributes:
        amount (str):
        comment (str):
        kind (str):
        odyssey_id (str):
        transaction_id (str):
        wallet (str):
    """

    amount: str
    comment: str
    kind: str
    odyssey_id: str
    transaction_id: str
    wallet: str
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        amount = self.amount
        comment = self.comment
        kind = self.kind
        odyssey_id = self.odyssey_id
        transaction_id = self.transaction_id
        wallet = self.wallet

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "amount": amount,
                "comment": comment,
                "kind": kind,
                "odyssey_id": odyssey_id,
                "transaction_id": transaction_id,
                "wallet": wallet,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        amount = d.pop("amount")

        comment = d.pop("comment")

        kind = d.pop("kind")

        odyssey_id = d.pop("odyssey_id")

        transaction_id = d.pop("transaction_id")

        wallet = d.pop("wallet")

        node_api_add_pending_stake_transaction_body = cls(
            amount=amount,
            comment=comment,
            kind=kind,
            odyssey_id=odyssey_id,
            transaction_id=transaction_id,
            wallet=wallet,
        )

        node_api_add_pending_stake_transaction_body.additional_properties = d
        return node_api_add_pending_stake_transaction_body

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
