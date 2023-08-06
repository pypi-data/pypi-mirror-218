from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.api_http_error import ApiHTTPError
from ...models.entry_attribute_value import EntryAttributeValue
from ...types import UNSET, Response


def _get_kwargs(
    user_id: str,
    *,
    client: Client,
    attribute_name: str,
    plugin_id: str,
) -> dict[str, Any]:
    url = f"{client.base_url}/api/v4/users/{user_id}/attributes"

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


def _parse_response(*, client: Client, response: httpx.Response) -> ApiHTTPError | EntryAttributeValue | None:
    if response.status_code == HTTPStatus.OK:
        response_200 = EntryAttributeValue.from_dict(response.json())

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


def _build_response(*, client: Client, response: httpx.Response) -> Response[ApiHTTPError | EntryAttributeValue]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    user_id: str,
    *,
    client: Client,
    attribute_name: str,
    plugin_id: str,
) -> Response[ApiHTTPError | EntryAttributeValue]:
    """Get user attribute

     Returns user attribute

    Args:
        user_id (str):
        attribute_name (str):
        plugin_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiHTTPError, EntryAttributeValue]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
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
    user_id: str,
    *,
    client: Client,
    attribute_name: str,
    plugin_id: str,
) -> ApiHTTPError | EntryAttributeValue | None:
    """Get user attribute

     Returns user attribute

    Args:
        user_id (str):
        attribute_name (str):
        plugin_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiHTTPError, EntryAttributeValue]
    """

    return sync_detailed(
        user_id=user_id,
        client=client,
        attribute_name=attribute_name,
        plugin_id=plugin_id,
    ).parsed


async def asyncio_detailed(
    user_id: str,
    *,
    client: Client,
    attribute_name: str,
    plugin_id: str,
) -> Response[ApiHTTPError | EntryAttributeValue]:
    """Get user attribute

     Returns user attribute

    Args:
        user_id (str):
        attribute_name (str):
        plugin_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiHTTPError, EntryAttributeValue]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        client=client,
        attribute_name=attribute_name,
        plugin_id=plugin_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    user_id: str,
    *,
    client: Client,
    attribute_name: str,
    plugin_id: str,
) -> ApiHTTPError | EntryAttributeValue | None:
    """Get user attribute

     Returns user attribute

    Args:
        user_id (str):
        attribute_name (str):
        plugin_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiHTTPError, EntryAttributeValue]
    """

    return (
        await asyncio_detailed(
            user_id=user_id,
            client=client,
            attribute_name=attribute_name,
            plugin_id=plugin_id,
        )
    ).parsed
