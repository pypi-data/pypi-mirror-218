from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dto_profile import DtoProfile


T = TypeVar("T", bound="DtoUser")


@attr.s(auto_attribs=True)
class DtoUser:
    """
    Attributes:
        created_at (Union[Unset, str]):
        id (Union[Unset, str]):
        is_guest (Union[Unset, bool]):
        name (Union[Unset, str]):
        profile (Union[Unset, DtoProfile]):
        token (Union[Unset, str]):
        updated_at (Union[Unset, str]):
        user_type_id (Union[Unset, str]):
        wallet (Union[Unset, str]):
    """

    created_at: Unset | str = UNSET
    id: Unset | str = UNSET
    is_guest: Unset | bool = UNSET
    name: Unset | str = UNSET
    profile: Union[Unset, "DtoProfile"] = UNSET
    token: Unset | str = UNSET
    updated_at: Unset | str = UNSET
    user_type_id: Unset | str = UNSET
    wallet: Unset | str = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at
        id = self.id
        is_guest = self.is_guest
        name = self.name
        profile: Unset | dict[str, Any] = UNSET
        if not isinstance(self.profile, Unset):
            profile = self.profile.to_dict()

        token = self.token
        updated_at = self.updated_at
        user_type_id = self.user_type_id
        wallet = self.wallet

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if id is not UNSET:
            field_dict["id"] = id
        if is_guest is not UNSET:
            field_dict["isGuest"] = is_guest
        if name is not UNSET:
            field_dict["name"] = name
        if profile is not UNSET:
            field_dict["profile"] = profile
        if token is not UNSET:
            field_dict["token"] = token
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if user_type_id is not UNSET:
            field_dict["userTypeId"] = user_type_id
        if wallet is not UNSET:
            field_dict["wallet"] = wallet

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.dto_profile import DtoProfile

        d = src_dict.copy()
        created_at = d.pop("createdAt", UNSET)

        id = d.pop("id", UNSET)

        is_guest = d.pop("isGuest", UNSET)

        name = d.pop("name", UNSET)

        _profile = d.pop("profile", UNSET)
        profile: Unset | DtoProfile
        if isinstance(_profile, Unset):
            profile = UNSET
        else:
            profile = DtoProfile.from_dict(_profile)

        token = d.pop("token", UNSET)

        updated_at = d.pop("updatedAt", UNSET)

        user_type_id = d.pop("userTypeId", UNSET)

        wallet = d.pop("wallet", UNSET)

        dto_user = cls(
            created_at=created_at,
            id=id,
            is_guest=is_guest,
            name=name,
            profile=profile,
            token=token,
            updated_at=updated_at,
            user_type_id=user_type_id,
            wallet=wallet,
        )

        dto_user.additional_properties = d
        return dto_user

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
