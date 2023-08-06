from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.entry_asset_3d_meta import EntryAsset3DMeta


T = TypeVar("T", bound="Assets3DApiUpdateAsset3DByIDInBody")


@attr.s(auto_attribs=True)
class Assets3DApiUpdateAsset3DByIDInBody:
    """
    Attributes:
        is_private (Union[Unset, bool]):
        meta (Union[Unset, EntryAsset3DMeta]):
    """

    is_private: Unset | bool = UNSET
    meta: Union[Unset, "EntryAsset3DMeta"] = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        is_private = self.is_private
        meta: Unset | dict[str, Any] = UNSET
        if not isinstance(self.meta, Unset):
            meta = self.meta.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if is_private is not UNSET:
            field_dict["is_private"] = is_private
        if meta is not UNSET:
            field_dict["meta"] = meta

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.entry_asset_3d_meta import EntryAsset3DMeta

        d = src_dict.copy()
        is_private = d.pop("is_private", UNSET)

        _meta = d.pop("meta", UNSET)
        meta: Unset | EntryAsset3DMeta
        if isinstance(_meta, Unset):
            meta = UNSET
        else:
            meta = EntryAsset3DMeta.from_dict(_meta)

        assets_3d_api_update_asset_3d_by_id_in_body = cls(
            is_private=is_private,
            meta=meta,
        )

        assets_3d_api_update_asset_3d_by_id_in_body.additional_properties = d
        return assets_3d_api_update_asset_3d_by_id_in_body

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
