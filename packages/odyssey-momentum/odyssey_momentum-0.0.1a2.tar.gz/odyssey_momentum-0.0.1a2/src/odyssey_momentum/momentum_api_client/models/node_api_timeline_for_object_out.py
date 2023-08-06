from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dto_activity import DtoActivity


T = TypeVar("T", bound="NodeApiTimelineForObjectOut")


@attr.s(auto_attribs=True)
class NodeApiTimelineForObjectOut:
    """
    Attributes:
        activities (Union[Unset, List['DtoActivity']]):
        page_size (Union[Unset, int]):
        start_index (Union[Unset, int]):
        total_count (Union[Unset, int]):
    """

    activities: Unset | list["DtoActivity"] = UNSET
    page_size: Unset | int = UNSET
    start_index: Unset | int = UNSET
    total_count: Unset | int = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        activities: Unset | list[dict[str, Any]] = UNSET
        if not isinstance(self.activities, Unset):
            activities = []
            for activities_item_data in self.activities:
                activities_item = activities_item_data.to_dict()

                activities.append(activities_item)

        page_size = self.page_size
        start_index = self.start_index
        total_count = self.total_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if activities is not UNSET:
            field_dict["activities"] = activities
        if page_size is not UNSET:
            field_dict["pageSize"] = page_size
        if start_index is not UNSET:
            field_dict["startIndex"] = start_index
        if total_count is not UNSET:
            field_dict["totalCount"] = total_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.dto_activity import DtoActivity

        d = src_dict.copy()
        activities = []
        _activities = d.pop("activities", UNSET)
        for activities_item_data in _activities or []:
            activities_item = DtoActivity.from_dict(activities_item_data)

            activities.append(activities_item)

        page_size = d.pop("pageSize", UNSET)

        start_index = d.pop("startIndex", UNSET)

        total_count = d.pop("totalCount", UNSET)

        node_api_timeline_for_object_out = cls(
            activities=activities,
            page_size=page_size,
            start_index=start_index,
            total_count=total_count,
        )

        node_api_timeline_for_object_out.additional_properties = d
        return node_api_timeline_for_object_out

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
