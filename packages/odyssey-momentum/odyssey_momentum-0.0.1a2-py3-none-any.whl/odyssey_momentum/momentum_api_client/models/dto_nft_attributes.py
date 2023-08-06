from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="DtoNFTAttributes")


@attr.s(auto_attribs=True)
class DtoNFTAttributes:
    """
    Attributes:
        trait_type (Union[Unset, str]):
        value (Union[Unset, str]):
    """

    trait_type: Unset | str = UNSET
    value: Unset | str = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        trait_type = self.trait_type
        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if trait_type is not UNSET:
            field_dict["trait_type"] = trait_type
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        trait_type = d.pop("trait_type", UNSET)

        value = d.pop("value", UNSET)

        dto_nft_attributes = cls(
            trait_type=trait_type,
            value=value,
        )

        dto_nft_attributes.additional_properties = d
        return dto_nft_attributes

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
