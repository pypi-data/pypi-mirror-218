from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="StreamchatApiChannelTokenResponse")


@attr.s(auto_attribs=True)
class StreamchatApiChannelTokenResponse:
    """
    Attributes:
        channel (Union[Unset, str]):
        channel_type (Union[Unset, str]):
        token (Union[Unset, str]):
    """

    channel: Unset | str = UNSET
    channel_type: Unset | str = UNSET
    token: Unset | str = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        channel = self.channel
        channel_type = self.channel_type
        token = self.token

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if channel is not UNSET:
            field_dict["channel"] = channel
        if channel_type is not UNSET:
            field_dict["channel_type"] = channel_type
        if token is not UNSET:
            field_dict["token"] = token

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        channel = d.pop("channel", UNSET)

        channel_type = d.pop("channel_type", UNSET)

        token = d.pop("token", UNSET)

        streamchat_api_channel_token_response = cls(
            channel=channel,
            channel_type=channel_type,
            token=token,
        )

        streamchat_api_channel_token_response.additional_properties = d
        return streamchat_api_channel_token_response

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
