from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.entry_user_profile import EntryUserProfile
    from ..models.node_node_js_out import NodeNodeJSOut


T = TypeVar("T", bound="NodeApiProfileUpdateCheckJobOut")


@attr.s(auto_attribs=True)
class NodeApiProfileUpdateCheckJobOut:
    """
    Attributes:
        error (Union[Unset, str]):
        job_id (Union[Unset, str]):
        node_js_out (Union[Unset, NodeNodeJSOut]):
        profile (Union[Unset, EntryUserProfile]):
        status (Union[Unset, str]):
        user_id (Union[Unset, str]):
    """

    error: Unset | str = UNSET
    job_id: Unset | str = UNSET
    node_js_out: Union[Unset, "NodeNodeJSOut"] = UNSET
    profile: Union[Unset, "EntryUserProfile"] = UNSET
    status: Unset | str = UNSET
    user_id: Unset | str = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        error = self.error
        job_id = self.job_id
        node_js_out: Unset | dict[str, Any] = UNSET
        if not isinstance(self.node_js_out, Unset):
            node_js_out = self.node_js_out.to_dict()

        profile: Unset | dict[str, Any] = UNSET
        if not isinstance(self.profile, Unset):
            profile = self.profile.to_dict()

        status = self.status
        user_id = self.user_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if error is not UNSET:
            field_dict["error"] = error
        if job_id is not UNSET:
            field_dict["job_id"] = job_id
        if node_js_out is not UNSET:
            field_dict["nodeJSOut"] = node_js_out
        if profile is not UNSET:
            field_dict["profile"] = profile
        if status is not UNSET:
            field_dict["status"] = status
        if user_id is not UNSET:
            field_dict["user_id"] = user_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.entry_user_profile import EntryUserProfile
        from ..models.node_node_js_out import NodeNodeJSOut

        d = src_dict.copy()
        error = d.pop("error", UNSET)

        job_id = d.pop("job_id", UNSET)

        _node_js_out = d.pop("nodeJSOut", UNSET)
        node_js_out: Unset | NodeNodeJSOut
        if isinstance(_node_js_out, Unset):
            node_js_out = UNSET
        else:
            node_js_out = NodeNodeJSOut.from_dict(_node_js_out)

        _profile = d.pop("profile", UNSET)
        profile: Unset | EntryUserProfile
        if isinstance(_profile, Unset):
            profile = UNSET
        else:
            profile = EntryUserProfile.from_dict(_profile)

        status = d.pop("status", UNSET)

        user_id = d.pop("user_id", UNSET)

        node_api_profile_update_check_job_out = cls(
            error=error,
            job_id=job_id,
            node_js_out=node_js_out,
            profile=profile,
            status=status,
            user_id=user_id,
        )

        node_api_profile_update_check_job_out.additional_properties = d
        return node_api_profile_update_check_job_out

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
