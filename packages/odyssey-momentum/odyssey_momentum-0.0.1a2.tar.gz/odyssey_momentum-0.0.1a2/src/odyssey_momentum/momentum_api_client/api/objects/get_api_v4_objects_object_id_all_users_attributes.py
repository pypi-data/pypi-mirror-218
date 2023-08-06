from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.api_http_error import ApiHTTPError
from ...models.get_api_v4_objects_object_id_all_users_attributes_response_200 import (
    GetApiV4ObjectsObjectIdAllUsersAttributesResponse200,
)
from ...types import UNSET, Response


def _get_kwargs(
    object_id: str,
    *,
    client: Client,
    attribute_name: str,
    plugin_id: str,
) -> dict[str, Any]:
    url = f"{client.base_url}/api/v4/objects/{object_id}/all-users/attributes"

    headers: dict[str, str] = client.get_headers()
    cookies: dict[str, Any] = client.get_cookies()

    params: dict[str, Any] = {}
    params["attribute_name"] = attribute_name

    params["plugin_id"] = plugin_id

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


def _parse_response(
    *, client: Client, response: httpx.Response
) -> ApiHTTPError | GetApiV4ObjectsObjectIdAllUsersAttributesResponse200 | None:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetApiV4ObjectsObjectIdAllUsersAttributesResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ApiHTTPError.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = ApiHTTPError.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[ApiHTTPError | GetApiV4ObjectsObjectIdAllUsersAttributesResponse200]:
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
) -> Response[ApiHTTPError | GetApiV4ObjectsObjectIdAllUsersAttributesResponse200]:
    """Get list of attributes for all users limited by object, plugin and attribute_name

     Returns map with key as userID and value as Attribute Value

    Args:
        object_id (str):
        attribute_name (str):
        plugin_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiHTTPError, GetApiV4ObjectsObjectIdAllUsersAttributesResponse200]]
    """

    kwargs = _get_kwargs(
        object_id=object_id,
        client=client,
        attribute_name=attribute_name,
        plugin_id=plugin_id,
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
) -> ApiHTTPError | GetApiV4ObjectsObjectIdAllUsersAttributesResponse200 | None:
    """Get list of attributes for all users limited by object, plugin and attribute_name

     Returns map with key as userID and value as Attribute Value

    Args:
        object_id (str):
        attribute_name (str):
        plugin_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiHTTPError, GetApiV4ObjectsObjectIdAllUsersAttributesResponse200]
    """

    return sync_detailed(
        object_id=object_id,
        client=client,
        attribute_name=attribute_name,
        plugin_id=plugin_id,
    ).parsed


async def asyncio_detailed(
    object_id: str,
    *,
    client: Client,
    attribute_name: str,
    plugin_id: str,
) -> Response[ApiHTTPError | GetApiV4ObjectsObjectIdAllUsersAttributesResponse200]:
    """Get list of attributes for all users limited by object, plugin and attribute_name

     Returns map with key as userID and value as Attribute Value

    Args:
        object_id (str):
        attribute_name (str):
        plugin_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiHTTPError, GetApiV4ObjectsObjectIdAllUsersAttributesResponse200]]
    """

    kwargs = _get_kwargs(
        object_id=object_id,
        client=client,
        attribute_name=attribute_name,
        plugin_id=plugin_id,
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
) -> ApiHTTPError | GetApiV4ObjectsObjectIdAllUsersAttributesResponse200 | None:
    """Get list of attributes for all users limited by object, plugin and attribute_name

     Returns map with key as userID and value as Attribute Value

    Args:
        object_id (str):
        attribute_name (str):
        plugin_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiHTTPError, GetApiV4ObjectsObjectIdAllUsersAttributesResponse200]
    """

    return (
        await asyncio_detailed(
            object_id=object_id,
            client=client,
            attribute_name=attribute_name,
            plugin_id=plugin_id,
        )
    ).parsed
