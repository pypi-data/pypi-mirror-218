from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="EntryObjectChildPlacementOptions")


@attr.s(auto_attribs=True)
class EntryObjectChildPlacementOptions:
    """ """

    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        entry_object_child_placement_options = cls()

        entry_object_child_placement_options.additional_properties = d
        return entry_object_child_placement_options

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
