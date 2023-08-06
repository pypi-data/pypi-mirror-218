from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dto_nft_attributes import DtoNFTAttributes


T = TypeVar("T", bound="DtoWorldNFTMeta")


@attr.s(auto_attribs=True)
class DtoWorldNFTMeta:
    """
    Attributes:
        name (str):
        attributes (Union[Unset, List['DtoNFTAttributes']]):
        description (Union[Unset, str]):
        external_url (Union[Unset, str]):
        image (Union[Unset, str]):
    """

    name: str
    attributes: Unset | list["DtoNFTAttributes"] = UNSET
    description: Unset | str = UNSET
    external_url: Unset | str = UNSET
    image: Unset | str = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name
        attributes: Unset | list[dict[str, Any]] = UNSET
        if not isinstance(self.attributes, Unset):
            attributes = []
            for attributes_item_data in self.attributes:
                attributes_item = attributes_item_data.to_dict()

                attributes.append(attributes_item)

        description = self.description
        external_url = self.external_url
        image = self.image

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if attributes is not UNSET:
            field_dict["attributes"] = attributes
        if description is not UNSET:
            field_dict["description"] = description
        if external_url is not UNSET:
            field_dict["external_url"] = external_url
        if image is not UNSET:
            field_dict["image"] = image

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.dto_nft_attributes import DtoNFTAttributes

        d = src_dict.copy()
        name = d.pop("name")

        attributes = []
        _attributes = d.pop("attributes", UNSET)
        for attributes_item_data in _attributes or []:
            attributes_item = DtoNFTAttributes.from_dict(attributes_item_data)

            attributes.append(attributes_item)

        description = d.pop("description", UNSET)

        external_url = d.pop("external_url", UNSET)

        image = d.pop("image", UNSET)

        dto_world_nft_meta = cls(
            name=name,
            attributes=attributes,
            description=description,
            external_url=external_url,
            image=image,
        )

        dto_world_nft_meta.additional_properties = d
        return dto_world_nft_meta

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
