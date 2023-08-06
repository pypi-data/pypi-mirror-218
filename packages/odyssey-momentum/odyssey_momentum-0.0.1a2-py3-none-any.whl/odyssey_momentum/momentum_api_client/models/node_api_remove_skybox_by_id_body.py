from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="NodeApiRemoveSkyboxByIDBody")


@attr.s(auto_attribs=True)
class NodeApiRemoveSkyboxByIDBody:
    """
    Attributes:
        world_id (str):
    """

    world_id: str
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        world_id = self.world_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "world_id": world_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        world_id = d.pop("world_id")

        node_api_remove_skybox_by_id_body = cls(
            world_id=world_id,
        )

        node_api_remove_skybox_by_id_body.additional_properties = d
        return node_api_remove_skybox_by_id_body

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
