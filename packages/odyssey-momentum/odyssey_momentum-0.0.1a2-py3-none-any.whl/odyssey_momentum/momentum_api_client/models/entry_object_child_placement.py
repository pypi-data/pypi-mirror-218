from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.entry_object_child_placement_options import EntryObjectChildPlacementOptions


T = TypeVar("T", bound="EntryObjectChildPlacement")


@attr.s(auto_attribs=True)
class EntryObjectChildPlacement:
    """
    Attributes:
        algo (Union[Unset, str]):
        options (Union[Unset, EntryObjectChildPlacementOptions]):
    """

    algo: Unset | str = UNSET
    options: Union[Unset, "EntryObjectChildPlacementOptions"] = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        algo = self.algo
        options: Unset | dict[str, Any] = UNSET
        if not isinstance(self.options, Unset):
            options = self.options.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if algo is not UNSET:
            field_dict["algo"] = algo
        if options is not UNSET:
            field_dict["options"] = options

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.entry_object_child_placement_options import EntryObjectChildPlacementOptions

        d = src_dict.copy()
        algo = d.pop("algo", UNSET)

        _options = d.pop("options", UNSET)
        options: Unset | EntryObjectChildPlacementOptions
        if isinstance(_options, Unset):
            options = UNSET
        else:
            options = EntryObjectChildPlacementOptions.from_dict(_options)

        entry_object_child_placement = cls(
            algo=algo,
            options=options,
        )

        entry_object_child_placement.additional_properties = d
        return entry_object_child_placement

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
