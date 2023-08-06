from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dto_profile import DtoProfile


T = TypeVar("T", bound="DtoRecentUser")


@attr.s(auto_attribs=True)
class DtoRecentUser:
    """
    Attributes:
        id (Union[Unset, str]):
        name (Union[Unset, str]):
        profile (Union[Unset, DtoProfile]):
        wallet (Union[Unset, str]):
    """

    id: Unset | str = UNSET
    name: Unset | str = UNSET
    profile: Union[Unset, "DtoProfile"] = UNSET
    wallet: Unset | str = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id
        name = self.name
        profile: Unset | dict[str, Any] = UNSET
        if not isinstance(self.profile, Unset):
            profile = self.profile.to_dict()

        wallet = self.wallet

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if profile is not UNSET:
            field_dict["profile"] = profile
        if wallet is not UNSET:
            field_dict["wallet"] = wallet

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.dto_profile import DtoProfile

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        _profile = d.pop("profile", UNSET)
        profile: Unset | DtoProfile
        if isinstance(_profile, Unset):
            profile = UNSET
        else:
            profile = DtoProfile.from_dict(_profile)

        wallet = d.pop("wallet", UNSET)

        dto_recent_user = cls(
            id=id,
            name=name,
            profile=profile,
            wallet=wallet,
        )

        dto_recent_user.additional_properties = d
        return dto_recent_user

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
