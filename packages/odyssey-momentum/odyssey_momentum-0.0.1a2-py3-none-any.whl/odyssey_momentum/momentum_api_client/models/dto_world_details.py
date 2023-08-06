from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dto_world_staker import DtoWorldStaker


T = TypeVar("T", bound="DtoWorldDetails")


@attr.s(auto_attribs=True)
class DtoWorldDetails:
    """
    Attributes:
        avatar_hash (Union[Unset, str]):
        created_at (Union[Unset, str]):
        description (Union[Unset, str]):
        id (Union[Unset, str]):
        last_staking_comment (Union[Unset, str]):
        name (Union[Unset, str]):
        owner_id (Union[Unset, str]):
        owner_name (Union[Unset, str]):
        stake_total (Union[Unset, str]):
        stakers (Union[Unset, List['DtoWorldStaker']]):
        updated_at (Union[Unset, str]):
        website_link (Union[Unset, str]):
    """

    avatar_hash: Unset | str = UNSET
    created_at: Unset | str = UNSET
    description: Unset | str = UNSET
    id: Unset | str = UNSET
    last_staking_comment: Unset | str = UNSET
    name: Unset | str = UNSET
    owner_id: Unset | str = UNSET
    owner_name: Unset | str = UNSET
    stake_total: Unset | str = UNSET
    stakers: Unset | list["DtoWorldStaker"] = UNSET
    updated_at: Unset | str = UNSET
    website_link: Unset | str = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        avatar_hash = self.avatar_hash
        created_at = self.created_at
        description = self.description
        id = self.id
        last_staking_comment = self.last_staking_comment
        name = self.name
        owner_id = self.owner_id
        owner_name = self.owner_name
        stake_total = self.stake_total
        stakers: Unset | list[dict[str, Any]] = UNSET
        if not isinstance(self.stakers, Unset):
            stakers = []
            for stakers_item_data in self.stakers:
                stakers_item = stakers_item_data.to_dict()

                stakers.append(stakers_item)

        updated_at = self.updated_at
        website_link = self.website_link

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if avatar_hash is not UNSET:
            field_dict["avatarHash"] = avatar_hash
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if description is not UNSET:
            field_dict["description"] = description
        if id is not UNSET:
            field_dict["id"] = id
        if last_staking_comment is not UNSET:
            field_dict["last_staking_comment"] = last_staking_comment
        if name is not UNSET:
            field_dict["name"] = name
        if owner_id is not UNSET:
            field_dict["owner_id"] = owner_id
        if owner_name is not UNSET:
            field_dict["owner_name"] = owner_name
        if stake_total is not UNSET:
            field_dict["stake_total"] = stake_total
        if stakers is not UNSET:
            field_dict["stakers"] = stakers
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if website_link is not UNSET:
            field_dict["website_link"] = website_link

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.dto_world_staker import DtoWorldStaker

        d = src_dict.copy()
        avatar_hash = d.pop("avatarHash", UNSET)

        created_at = d.pop("createdAt", UNSET)

        description = d.pop("description", UNSET)

        id = d.pop("id", UNSET)

        last_staking_comment = d.pop("last_staking_comment", UNSET)

        name = d.pop("name", UNSET)

        owner_id = d.pop("owner_id", UNSET)

        owner_name = d.pop("owner_name", UNSET)

        stake_total = d.pop("stake_total", UNSET)

        stakers = []
        _stakers = d.pop("stakers", UNSET)
        for stakers_item_data in _stakers or []:
            stakers_item = DtoWorldStaker.from_dict(stakers_item_data)

            stakers.append(stakers_item)

        updated_at = d.pop("updatedAt", UNSET)

        website_link = d.pop("website_link", UNSET)

        dto_world_details = cls(
            avatar_hash=avatar_hash,
            created_at=created_at,
            description=description,
            id=id,
            last_staking_comment=last_staking_comment,
            name=name,
            owner_id=owner_id,
            owner_name=owner_name,
            stake_total=stake_total,
            stakers=stakers,
            updated_at=updated_at,
            website_link=website_link,
        )

        dto_world_details.additional_properties = d
        return dto_world_details

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
