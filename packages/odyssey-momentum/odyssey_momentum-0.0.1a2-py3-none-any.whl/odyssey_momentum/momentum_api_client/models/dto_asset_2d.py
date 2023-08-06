from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dto_asset_2d_meta import DtoAsset2DMeta
    from ..models.dto_asset_2d_options import DtoAsset2DOptions


T = TypeVar("T", bound="DtoAsset2D")


@attr.s(auto_attribs=True)
class DtoAsset2D:
    """
    Attributes:
        meta (Union[Unset, DtoAsset2DMeta]):
        options (Union[Unset, DtoAsset2DOptions]):
    """

    meta: Union[Unset, "DtoAsset2DMeta"] = UNSET
    options: Union[Unset, "DtoAsset2DOptions"] = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        meta: Unset | dict[str, Any] = UNSET
        if not isinstance(self.meta, Unset):
            meta = self.meta.to_dict()

        options: Unset | dict[str, Any] = UNSET
        if not isinstance(self.options, Unset):
            options = self.options.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if meta is not UNSET:
            field_dict["meta"] = meta
        if options is not UNSET:
            field_dict["options"] = options

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.dto_asset_2d_meta import DtoAsset2DMeta
        from ..models.dto_asset_2d_options import DtoAsset2DOptions

        d = src_dict.copy()
        _meta = d.pop("meta", UNSET)
        meta: Unset | DtoAsset2DMeta
        if isinstance(_meta, Unset):
            meta = UNSET
        else:
            meta = DtoAsset2DMeta.from_dict(_meta)

        _options = d.pop("options", UNSET)
        options: Unset | DtoAsset2DOptions
        if isinstance(_options, Unset):
            options = UNSET
        else:
            options = DtoAsset2DOptions.from_dict(_options)

        dto_asset_2d = cls(
            meta=meta,
            options=options,
        )

        dto_asset_2d.additional_properties = d
        return dto_asset_2d

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
