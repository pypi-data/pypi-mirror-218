from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.api_http_error_payload import ApiHTTPErrorPayload


T = TypeVar("T", bound="ApiHTTPError")


@attr.s(auto_attribs=True)
class ApiHTTPError:
    """
    Attributes:
        error (Union[Unset, ApiHTTPErrorPayload]):
    """

    error: Union[Unset, "ApiHTTPErrorPayload"] = UNSET
    additional_properties: dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        error: Unset | dict[str, Any] = UNSET
        if not isinstance(self.error, Unset):
            error = self.error.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.api_http_error_payload import ApiHTTPErrorPayload

        d = src_dict.copy()
        _error = d.pop("error", UNSET)
        error: Unset | ApiHTTPErrorPayload
        if isinstance(_error, Unset):
            error = UNSET
        else:
            error = ApiHTTPErrorPayload.from_dict(_error)

        api_http_error = cls(
            error=error,
        )

        api_http_error.additional_properties = d
        return api_http_error

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
