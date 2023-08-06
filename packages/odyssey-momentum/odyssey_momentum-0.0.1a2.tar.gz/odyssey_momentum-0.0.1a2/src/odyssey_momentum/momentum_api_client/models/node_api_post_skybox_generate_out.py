from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.node_skybox_status import NodeSkyboxStatus


T = TypeVar("T", bound="NodeApiPostSkyboxGenerateOut")


@attr.s(auto_attribs=True)
class NodeApiPostSkyboxGenerateOut:
    """
    Attributes:
        data (Union[Unset, NodeSkyboxStatus]):
        success (Union[Unset, bool]):
    """

    data: Union[Unset, "NodeSkyboxStatus"] = UNSET
    success: Unset | bool = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data: Unset | dict[str, Any] = UNSET
        if not isinstance(self.data, Unset):
            data = self.data.to_dict()

        success = self.success

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if data is not UNSET:
            field_dict["data"] = data
        if success is not UNSET:
            field_dict["success"] = success

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.node_skybox_status import NodeSkyboxStatus

        d = src_dict.copy()
        _data = d.pop("data", UNSET)
        data: Unset | NodeSkyboxStatus
        if isinstance(_data, Unset):
            data = UNSET
        else:
            data = NodeSkyboxStatus.from_dict(_data)

        success = d.pop("success", UNSET)

        node_api_post_skybox_generate_out = cls(
            data=data,
            success=success,
        )

        node_api_post_skybox_generate_out.additional_properties = d
        return node_api_post_skybox_generate_out

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
