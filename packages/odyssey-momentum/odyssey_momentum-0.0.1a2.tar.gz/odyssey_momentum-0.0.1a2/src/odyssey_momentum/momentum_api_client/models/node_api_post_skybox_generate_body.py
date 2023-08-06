from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="NodeApiPostSkyboxGenerateBody")


@attr.s(auto_attribs=True)
class NodeApiPostSkyboxGenerateBody:
    """
    Attributes:
        prompt (str):
        skybox_style_id (int):
        world_id (str):
    """

    prompt: str
    skybox_style_id: int
    world_id: str
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        prompt = self.prompt
        skybox_style_id = self.skybox_style_id
        world_id = self.world_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "prompt": prompt,
                "skybox_style_id": skybox_style_id,
                "world_id": world_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        prompt = d.pop("prompt")

        skybox_style_id = d.pop("skybox_style_id")

        world_id = d.pop("world_id")

        node_api_post_skybox_generate_body = cls(
            prompt=prompt,
            skybox_style_id=skybox_style_id,
            world_id=world_id,
        )

        node_api_post_skybox_generate_body.additional_properties = d
        return node_api_post_skybox_generate_body

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
