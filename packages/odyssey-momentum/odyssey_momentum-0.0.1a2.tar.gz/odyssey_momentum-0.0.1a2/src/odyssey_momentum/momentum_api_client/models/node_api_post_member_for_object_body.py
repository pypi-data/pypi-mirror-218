from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="NodeApiPostMemberForObjectBody")


@attr.s(auto_attribs=True)
class NodeApiPostMemberForObjectBody:
    """
    Attributes:
        role (str):
        user_id (Union[Unset, str]):
        wallet (Union[Unset, str]):
    """

    role: str
    user_id: Unset | str = UNSET
    wallet: Unset | str = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        role = self.role
        user_id = self.user_id
        wallet = self.wallet

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "role": role,
            }
        )
        if user_id is not UNSET:
            field_dict["user_id"] = user_id
        if wallet is not UNSET:
            field_dict["wallet"] = wallet

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        role = d.pop("role")

        user_id = d.pop("user_id", UNSET)

        wallet = d.pop("wallet", UNSET)

        node_api_post_member_for_object_body = cls(
            role=role,
            user_id=user_id,
            wallet=wallet,
        )

        node_api_post_member_for_object_body.additional_properties = d
        return node_api_post_member_for_object_body

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
