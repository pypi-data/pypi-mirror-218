from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.api_http_error import ApiHTTPError
from ...models.dto_object_sub_attributes import DtoObjectSubAttributes
from ...types import UNSET, Response


def _get_kwargs(
    object_id: str,
    *,
    client: Client,
    attribute_name: str,
    plugin_id: str,
    sub_attribute_key: str,
) -> dict[str, Any]:
    url = f"{client.base_url}/api/v4/objects/{object_id}/attributes/sub"

    headers: dict[str, str] = client.get_headers()
    cookies: dict[str, Any] = client.get_cookies()

    params: dict[str, Any] = {}
    params["attribute_name"] = attribute_name

    params["plugin_id"] = plugin_id

    params["subAttributeKey"] = sub_attribute_key

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> ApiHTTPError | DtoObjectSubAttributes | None:
    if response.status_code == HTTPStatus.OK:
        response_200 = DtoObjectSubAttributes.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ApiHTTPError.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = ApiHTTPError.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = ApiHTTPError.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[ApiHTTPError | DtoObjectSubAttributes]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    object_id: str,
    *,
    client: Client,
    attribute_name: str,
    plugin_id: str,
    sub_attribute_key: str,
) -> Response[ApiHTTPError | DtoObjectSubAttributes]:
    """Get object sub attributes

     Returns object sub attributes

    Args:
        object_id (str):
        attribute_name (str):
        plugin_id (str):
        sub_attribute_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiHTTPError, DtoObjectSubAttributes]]
    """

    kwargs = _get_kwargs(
        object_id=object_id,
        client=client,
        attribute_name=attribute_name,
        plugin_id=plugin_id,
        sub_attribute_key=sub_attribute_key,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    object_id: str,
    *,
    client: Client,
    attribute_name: str,
    plugin_id: str,
    sub_attribute_key: str,
) -> ApiHTTPError | DtoObjectSubAttributes | None:
    """Get object sub attributes

     Returns object sub attributes

    Args:
        object_id (str):
        attribute_name (str):
        plugin_id (str):
        sub_attribute_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiHTTPError, DtoObjectSubAttributes]
    """

    return sync_detailed(
        object_id=object_id,
        client=client,
        attribute_name=attribute_name,
        plugin_id=plugin_id,
        sub_attribute_key=sub_attribute_key,
    ).parsed


async def asyncio_detailed(
    object_id: str,
    *,
    client: Client,
    attribute_name: str,
    plugin_id: str,
    sub_attribute_key: str,
) -> Response[ApiHTTPError | DtoObjectSubAttributes]:
    """Get object sub attributes

     Returns object sub attributes

    Args:
        object_id (str):
        attribute_name (str):
        plugin_id (str):
        sub_attribute_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiHTTPError, DtoObjectSubAttributes]]
    """

    kwargs = _get_kwargs(
        object_id=object_id,
        client=client,
        attribute_name=attribute_name,
        plugin_id=plugin_id,
        sub_attribute_key=sub_attribute_key,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    object_id: str,
    *,
    client: Client,
    attribute_name: str,
    plugin_id: str,
    sub_attribute_key: str,
) -> ApiHTTPError | DtoObjectSubAttributes | None:
    """Get object sub attributes

     Returns object sub attributes

    Args:
        object_id (str):
        attribute_name (str):
        plugin_id (str):
        sub_attribute_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiHTTPError, DtoObjectSubAttributes]
    """

    return (
        await asyncio_detailed(
            object_id=object_id,
            client=client,
            attribute_name=attribute_name,
            plugin_id=plugin_id,
            sub_attribute_key=sub_attribute_key,
        )
    ).parsed
