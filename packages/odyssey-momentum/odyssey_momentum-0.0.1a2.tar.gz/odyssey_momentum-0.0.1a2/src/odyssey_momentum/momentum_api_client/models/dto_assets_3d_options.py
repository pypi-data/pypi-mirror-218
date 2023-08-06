from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.dto_asset_3d_options import DtoAsset3DOptions


T = TypeVar("T", bound="DtoAssets3DOptions")


@attr.s(auto_attribs=True)
class DtoAssets3DOptions:
    """ """

    additional_properties: dict[str, "DtoAsset3DOptions"] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pass

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.dto_asset_3d_options import DtoAsset3DOptions

        d = src_dict.copy()
        dto_assets_3d_options = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = DtoAsset3DOptions.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        dto_assets_3d_options.additional_properties = additional_properties
        return dto_assets_3d_options

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "DtoAsset3DOptions":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "DtoAsset3DOptions") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
