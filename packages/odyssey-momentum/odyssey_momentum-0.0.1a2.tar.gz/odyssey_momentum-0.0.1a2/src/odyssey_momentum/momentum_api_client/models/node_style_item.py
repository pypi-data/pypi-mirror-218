from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="NodeStyleItem")


@attr.s(auto_attribs=True)
class NodeStyleItem:
    """
    Attributes:
        id (Union[Unset, int]):
        image (Union[Unset, Any]):
        max_char (Union[Unset, int]):
        name (Union[Unset, str]):
        negative_text_max_char (Union[Unset, int]):
        premium (Union[Unset, int]):
        skybox_style_families (Union[Unset, List[Any]]):
        sort_order (Union[Unset, int]):
    """

    id: Unset | int = UNSET
    image: Unset | Any = UNSET
    max_char: Unset | int = UNSET
    name: Unset | str = UNSET
    negative_text_max_char: Unset | int = UNSET
    premium: Unset | int = UNSET
    skybox_style_families: Unset | list[Any] = UNSET
    sort_order: Unset | int = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id
        image = self.image
        max_char = self.max_char
        name = self.name
        negative_text_max_char = self.negative_text_max_char
        premium = self.premium
        skybox_style_families: Unset | list[Any] = UNSET
        if not isinstance(self.skybox_style_families, Unset):
            skybox_style_families = self.skybox_style_families

        sort_order = self.sort_order

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if image is not UNSET:
            field_dict["image"] = image
        if max_char is not UNSET:
            field_dict["max-char"] = max_char
        if name is not UNSET:
            field_dict["name"] = name
        if negative_text_max_char is not UNSET:
            field_dict["negative-text-max-char"] = negative_text_max_char
        if premium is not UNSET:
            field_dict["premium"] = premium
        if skybox_style_families is not UNSET:
            field_dict["skybox_style_families"] = skybox_style_families
        if sort_order is not UNSET:
            field_dict["sort_order"] = sort_order

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        image = d.pop("image", UNSET)

        max_char = d.pop("max-char", UNSET)

        name = d.pop("name", UNSET)

        negative_text_max_char = d.pop("negative-text-max-char", UNSET)

        premium = d.pop("premium", UNSET)

        skybox_style_families = cast(list[Any], d.pop("skybox_style_families", UNSET))

        sort_order = d.pop("sort_order", UNSET)

        node_style_item = cls(
            id=id,
            image=image,
            max_char=max_char,
            name=name,
            negative_text_max_char=negative_text_max_char,
            premium=premium,
            skybox_style_families=skybox_style_families,
            sort_order=sort_order,
        )

        node_style_item.additional_properties = d
        return node_style_item

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
