from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.entry_activity_type import EntryActivityType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.entry_activity_data import EntryActivityData


T = TypeVar("T", bound="DtoActivity")


@attr.s(auto_attribs=True)
class DtoActivity:
    """
    Attributes:
        activity_id (Union[Unset, str]):
        avatar_hash (Union[Unset, str]):
        created_at (Union[Unset, str]):
        data (Union[Unset, EntryActivityData]):
        object_id (Union[Unset, str]):
        type (Union[Unset, EntryActivityType]):
        user_id (Union[Unset, str]):
        user_name (Union[Unset, str]):
        world_avatar_hash (Union[Unset, str]):
        world_name (Union[Unset, str]):
    """

    activity_id: Unset | str = UNSET
    avatar_hash: Unset | str = UNSET
    created_at: Unset | str = UNSET
    data: Union[Unset, "EntryActivityData"] = UNSET
    object_id: Unset | str = UNSET
    type: Unset | EntryActivityType = UNSET
    user_id: Unset | str = UNSET
    user_name: Unset | str = UNSET
    world_avatar_hash: Unset | str = UNSET
    world_name: Unset | str = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        activity_id = self.activity_id
        avatar_hash = self.avatar_hash
        created_at = self.created_at
        data: Unset | dict[str, Any] = UNSET
        if not isinstance(self.data, Unset):
            data = self.data.to_dict()

        object_id = self.object_id
        type: Unset | str = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        user_id = self.user_id
        user_name = self.user_name
        world_avatar_hash = self.world_avatar_hash
        world_name = self.world_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if activity_id is not UNSET:
            field_dict["activity_id"] = activity_id
        if avatar_hash is not UNSET:
            field_dict["avatar_hash"] = avatar_hash
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if data is not UNSET:
            field_dict["data"] = data
        if object_id is not UNSET:
            field_dict["object_id"] = object_id
        if type is not UNSET:
            field_dict["type"] = type
        if user_id is not UNSET:
            field_dict["user_id"] = user_id
        if user_name is not UNSET:
            field_dict["user_name"] = user_name
        if world_avatar_hash is not UNSET:
            field_dict["world_avatar_hash"] = world_avatar_hash
        if world_name is not UNSET:
            field_dict["world_name"] = world_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: dict[str, Any]) -> T:
        from ..models.entry_activity_data import EntryActivityData

        d = src_dict.copy()
        activity_id = d.pop("activity_id", UNSET)

        avatar_hash = d.pop("avatar_hash", UNSET)

        created_at = d.pop("created_at", UNSET)

        _data = d.pop("data", UNSET)
        data: Unset | EntryActivityData
        if isinstance(_data, Unset):
            data = UNSET
        else:
            data = EntryActivityData.from_dict(_data)

        object_id = d.pop("object_id", UNSET)

        _type = d.pop("type", UNSET)
        type: Unset | EntryActivityType
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = EntryActivityType(_type)

        user_id = d.pop("user_id", UNSET)

        user_name = d.pop("user_name", UNSET)

        world_avatar_hash = d.pop("world_avatar_hash", UNSET)

        world_name = d.pop("world_name", UNSET)

        dto_activity = cls(
            activity_id=activity_id,
            avatar_hash=avatar_hash,
            created_at=created_at,
            data=data,
            object_id=object_id,
            type=type,
            user_id=user_id,
            user_name=user_name,
            world_avatar_hash=world_avatar_hash,
            world_name=world_name,
        )

        dto_activity.additional_properties = d
        return dto_activity

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
