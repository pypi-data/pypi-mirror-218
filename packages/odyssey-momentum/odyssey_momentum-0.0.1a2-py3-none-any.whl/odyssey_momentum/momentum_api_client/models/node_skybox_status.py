from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="NodeSkyboxStatus")


@attr.s(auto_attribs=True)
class NodeSkyboxStatus:
    """
    Attributes:
        created_at (Union[Unset, str]):
        depth_map_url (Union[Unset, str]):
        error_message (Union[Unset, Any]):
        file_url (Union[Unset, str]):
        id (Union[Unset, int]):
        is_my_favorite (Union[Unset, bool]):
        message (Union[Unset, str]):
        negative_text (Union[Unset, Any]):
        obfuscated_id (Union[Unset, str]):
        prompt (Union[Unset, str]):
        pusher_channel (Union[Unset, str]):
        pusher_event (Union[Unset, str]):
        queue_position (Union[Unset, int]):
        remix_imagine_id (Union[Unset, Any]):
        remix_obfuscated_id (Union[Unset, Any]):
        seed (Union[Unset, int]):
        skybox_id (Union[Unset, int]):
        skybox_name (Union[Unset, str]):
        skybox_style_id (Union[Unset, int]):
        skybox_style_name (Union[Unset, str]):
        status (Union[Unset, str]):
        thumb_url (Union[Unset, str]):
        title (Union[Unset, str]):
        type (Union[Unset, str]):
        updated_at (Union[Unset, str]):
        user_id (Union[Unset, int]):
        username (Union[Unset, str]):
    """

    created_at: Unset | str = UNSET
    depth_map_url: Unset | str = UNSET
    error_message: Unset | Any = UNSET
    file_url: Unset | str = UNSET
    id: Unset | int = UNSET
    is_my_favorite: Unset | bool = UNSET
    message: Unset | str = UNSET
    negative_text: Unset | Any = UNSET
    obfuscated_id: Unset | str = UNSET
    prompt: Unset | str = UNSET
    pusher_channel: Unset | str = UNSET
    pusher_event: Unset | str = UNSET
    queue_position: Unset | int = UNSET
    remix_imagine_id: Unset | Any = UNSET
    remix_obfuscated_id: Unset | Any = UNSET
    seed: Unset | int = UNSET
    skybox_id: Unset | int = UNSET
    skybox_name: Unset | str = UNSET
    skybox_style_id: Unset | int = UNSET
    skybox_style_name: Unset | str = UNSET
    status: Unset | str = UNSET
    thumb_url: Unset | str = UNSET
    title: Unset | str = UNSET
    type: Unset | str = UNSET
    updated_at: Unset | str = UNSET
    user_id: Unset | int = UNSET
    username: Unset | str = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at
        depth_map_url = self.depth_map_url
        error_message = self.error_message
        file_url = self.file_url
        id = self.id
        is_my_favorite = self.is_my_favorite
        message = self.message
        negative_text = self.negative_text
        obfuscated_id = self.obfuscated_id
        prompt = self.prompt
        pusher_channel = self.pusher_channel
        pusher_event = self.pusher_event
        queue_position = self.queue_position
        remix_imagine_id = self.remix_imagine_id
        remix_obfuscated_id = self.remix_obfuscated_id
        seed = self.seed
        skybox_id = self.skybox_id
        skybox_name = self.skybox_name
        skybox_style_id = self.skybox_style_id
        skybox_style_name = self.skybox_style_name
        status = self.status
        thumb_url = self.thumb_url
        title = self.title
        type = self.type
        updated_at = self.updated_at
        user_id = self.user_id
        username = self.username

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if depth_map_url is not UNSET:
            field_dict["depth_map_url"] = depth_map_url
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if file_url is not UNSET:
            field_dict["file_url"] = file_url
        if id is not UNSET:
            field_dict["id"] = id
        if is_my_favorite is not UNSET:
            field_dict["isMyFavorite"] = is_my_favorite
        if message is not UNSET:
            field_dict["message"] = message
        if negative_text is not UNSET:
            field_dict["negative_text"] = negative_text
        if obfuscated_id is not UNSET:
            field_dict["obfuscated_id"] = obfuscated_id
        if prompt is not UNSET:
            field_dict["prompt"] = prompt
        if pusher_channel is not UNSET:
            field_dict["pusher_channel"] = pusher_channel
        if pusher_event is not UNSET:
            field_dict["pusher_event"] = pusher_event
        if queue_position is not UNSET:
            field_dict["queue_position"] = queue_position
        if remix_imagine_id is not UNSET:
            field_dict["remix_imagine_id"] = remix_imagine_id
        if remix_obfuscated_id is not UNSET:
            field_dict["remix_obfuscated_id"] = remix_obfuscated_id
        if seed is not UNSET:
            field_dict["seed"] = seed
        if skybox_id is not UNSET:
            field_dict["skybox_id"] = skybox_id
        if skybox_name is not UNSET:
            field_dict["skybox_name"] = skybox_name
        if skybox_style_id is not UNSET:
            field_dict["skybox_style_id"] = skybox_style_id
        if skybox_style_name is not UNSET:
            field_dict["skybox_style_name"] = skybox_style_name
        if status is not UNSET:
            field_dict["status"] = status
        if thumb_url is not UNSET:
            field_dict["thumb_url"] = thumb_url
        if title is not UNSET:
            field_dict["title"] = title
        if type is not UNSET:
            field_dict["type"] = type
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if user_id is not UNSET:
            field_dict["user_id"] = user_id
        if username is not UNSET:
            field_dict["username"] = username

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        created_at = d.pop("created_at", UNSET)

        depth_map_url = d.pop("depth_map_url", UNSET)

        error_message = d.pop("error_message", UNSET)

        file_url = d.pop("file_url", UNSET)

        id = d.pop("id", UNSET)

        is_my_favorite = d.pop("isMyFavorite", UNSET)

        message = d.pop("message", UNSET)

        negative_text = d.pop("negative_text", UNSET)

        obfuscated_id = d.pop("obfuscated_id", UNSET)

        prompt = d.pop("prompt", UNSET)

        pusher_channel = d.pop("pusher_channel", UNSET)

        pusher_event = d.pop("pusher_event", UNSET)

        queue_position = d.pop("queue_position", UNSET)

        remix_imagine_id = d.pop("remix_imagine_id", UNSET)

        remix_obfuscated_id = d.pop("remix_obfuscated_id", UNSET)

        seed = d.pop("seed", UNSET)

        skybox_id = d.pop("skybox_id", UNSET)

        skybox_name = d.pop("skybox_name", UNSET)

        skybox_style_id = d.pop("skybox_style_id", UNSET)

        skybox_style_name = d.pop("skybox_style_name", UNSET)

        status = d.pop("status", UNSET)

        thumb_url = d.pop("thumb_url", UNSET)

        title = d.pop("title", UNSET)

        type = d.pop("type", UNSET)

        updated_at = d.pop("updated_at", UNSET)

        user_id = d.pop("user_id", UNSET)

        username = d.pop("username", UNSET)

        node_skybox_status = cls(
            created_at=created_at,
            depth_map_url=depth_map_url,
            error_message=error_message,
            file_url=file_url,
            id=id,
            is_my_favorite=is_my_favorite,
            message=message,
            negative_text=negative_text,
            obfuscated_id=obfuscated_id,
            prompt=prompt,
            pusher_channel=pusher_channel,
            pusher_event=pusher_event,
            queue_position=queue_position,
            remix_imagine_id=remix_imagine_id,
            remix_obfuscated_id=remix_obfuscated_id,
            seed=seed,
            skybox_id=skybox_id,
            skybox_name=skybox_name,
            skybox_style_id=skybox_style_id,
            skybox_style_name=skybox_style_name,
            status=status,
            thumb_url=thumb_url,
            title=title,
            type=type,
            updated_at=updated_at,
            user_id=user_id,
            username=username,
        )

        node_skybox_status.additional_properties = d
        return node_skybox_status

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
