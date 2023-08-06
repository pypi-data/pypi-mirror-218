from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.node_api_get_version_out_api import NodeApiGetVersionOutApi
    from ..models.node_api_get_version_out_controller import NodeApiGetVersionOutController


T = TypeVar("T", bound="NodeApiGetVersionOut")


@attr.s(auto_attribs=True)
class NodeApiGetVersionOut:
    """
    Attributes:
        api (Union[Unset, NodeApiGetVersionOutApi]):
        controller (Union[Unset, NodeApiGetVersionOutController]):
    """

    api: Union[Unset, "NodeApiGetVersionOutApi"] = UNSET
    controller: Union[Unset, "NodeApiGetVersionOutController"] = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        api: Unset | dict[str, Any] = UNSET
        if not isinstance(self.api, Unset):
            api = self.api.to_dict()

        controller: Unset | dict[str, Any] = UNSET
        if not isinstance(self.controller, Unset):
            controller = self.controller.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if api is not UNSET:
            field_dict["api"] = api
        if controller is not UNSET:
            field_dict["controller"] = controller

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.node_api_get_version_out_api import NodeApiGetVersionOutApi
        from ..models.node_api_get_version_out_controller import NodeApiGetVersionOutController

        d = src_dict.copy()
        _api = d.pop("api", UNSET)
        api: Unset | NodeApiGetVersionOutApi
        if isinstance(_api, Unset):
            api = UNSET
        else:
            api = NodeApiGetVersionOutApi.from_dict(_api)

        _controller = d.pop("controller", UNSET)
        controller: Unset | NodeApiGetVersionOutController
        if isinstance(_controller, Unset):
            controller = UNSET
        else:
            controller = NodeApiGetVersionOutController.from_dict(_controller)

        node_api_get_version_out = cls(
            api=api,
            controller=controller,
        )

        node_api_get_version_out.additional_properties = d
        return node_api_get_version_out

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
