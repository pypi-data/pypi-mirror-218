from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cmath_vec_3 import CmathVec3


T = TypeVar("T", bound="EntryActivityData")


@attr.s(auto_attribs=True)
class EntryActivityData:
    """
    Attributes:
        bc_log_index (Union[Unset, str]):
        bc_tx_hash (Union[Unset, str]):
        description (Union[Unset, str]):
        hash_ (Union[Unset, str]):
        position (Union[Unset, CmathVec3]):
        token_amount (Union[Unset, str]):
        token_symbol (Union[Unset, str]):
    """

    bc_log_index: Unset | str = UNSET
    bc_tx_hash: Unset | str = UNSET
    description: Unset | str = UNSET
    hash_: Unset | str = UNSET
    position: Union[Unset, "CmathVec3"] = UNSET
    token_amount: Unset | str = UNSET
    token_symbol: Unset | str = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        bc_log_index = self.bc_log_index
        bc_tx_hash = self.bc_tx_hash
        description = self.description
        hash_ = self.hash_
        position: Unset | dict[str, Any] = UNSET
        if not isinstance(self.position, Unset):
            position = self.position.to_dict()

        token_amount = self.token_amount
        token_symbol = self.token_symbol

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if bc_log_index is not UNSET:
            field_dict["bc_log_index"] = bc_log_index
        if bc_tx_hash is not UNSET:
            field_dict["bc_tx_hash"] = bc_tx_hash
        if description is not UNSET:
            field_dict["description"] = description
        if hash_ is not UNSET:
            field_dict["hash"] = hash_
        if position is not UNSET:
            field_dict["position"] = position
        if token_amount is not UNSET:
            field_dict["token_amount"] = token_amount
        if token_symbol is not UNSET:
            field_dict["token_symbol"] = token_symbol

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.cmath_vec_3 import CmathVec3

        d = src_dict.copy()
        bc_log_index = d.pop("bc_log_index", UNSET)

        bc_tx_hash = d.pop("bc_tx_hash", UNSET)

        description = d.pop("description", UNSET)

        hash_ = d.pop("hash", UNSET)

        _position = d.pop("position", UNSET)
        position: Unset | CmathVec3
        if isinstance(_position, Unset):
            position = UNSET
        else:
            position = CmathVec3.from_dict(_position)

        token_amount = d.pop("token_amount", UNSET)

        token_symbol = d.pop("token_symbol", UNSET)

        entry_activity_data = cls(
            bc_log_index=bc_log_index,
            bc_tx_hash=bc_tx_hash,
            description=description,
            hash_=hash_,
            position=position,
            token_amount=token_amount,
            token_symbol=token_symbol,
        )

        entry_activity_data.additional_properties = d
        return entry_activity_data

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
