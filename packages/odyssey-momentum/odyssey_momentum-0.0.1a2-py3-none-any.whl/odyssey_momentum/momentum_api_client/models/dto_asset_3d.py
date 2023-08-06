from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dto_asset_3d_meta import DtoAsset3DMeta


T = TypeVar("T", bound="DtoAsset3D")


@attr.s(auto_attribs=True)
class DtoAsset3D:
    """
    Attributes:
        created_at (Union[Unset, str]):
        id (Union[Unset, str]):
        is_private (Union[Unset, bool]):
        meta (Union[Unset, DtoAsset3DMeta]):
        name (Union[Unset, str]):
        updated_at (Union[Unset, str]):
        user_id (Union[Unset, str]):
    """

    created_at: Unset | str = UNSET
    id: Unset | str = UNSET
    is_private: Unset | bool = UNSET
    meta: Union[Unset, "DtoAsset3DMeta"] = UNSET
    name: Unset | str = UNSET
    updated_at: Unset | str = UNSET
    user_id: Unset | str = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at
        id = self.id
        is_private = self.is_private
        meta: Unset | dict[str, Any] = UNSET
        if not isinstance(self.meta, Unset):
            meta = self.meta.to_dict()

        name = self.name
        updated_at = self.updated_at
        user_id = self.user_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if id is not UNSET:
            field_dict["id"] = id
        if is_private is not UNSET:
            field_dict["is_private"] = is_private
        if meta is not UNSET:
            field_dict["meta"] = meta
        if name is not UNSET:
            field_dict["name"] = name
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if user_id is not UNSET:
            field_dict["user_id"] = user_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.dto_asset_3d_meta import DtoAsset3DMeta

        d = src_dict.copy()
        created_at = d.pop("createdAt", UNSET)

        id = d.pop("id", UNSET)

        is_private = d.pop("is_private", UNSET)

        _meta = d.pop("meta", UNSET)
        meta: Unset | DtoAsset3DMeta
        if isinstance(_meta, Unset):
            meta = UNSET
        else:
            meta = DtoAsset3DMeta.from_dict(_meta)

        name = d.pop("name", UNSET)

        updated_at = d.pop("updatedAt", UNSET)

        user_id = d.pop("user_id", UNSET)

        dto_asset_3d = cls(
            created_at=created_at,
            id=id,
            is_private=is_private,
            meta=meta,
            name=name,
            updated_at=updated_at,
            user_id=user_id,
        )

        dto_asset_3d.additional_properties = d
        return dto_asset_3d

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
