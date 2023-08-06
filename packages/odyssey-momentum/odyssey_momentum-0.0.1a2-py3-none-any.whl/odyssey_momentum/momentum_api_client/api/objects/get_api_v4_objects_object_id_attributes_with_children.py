from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.api_http_error import ApiHTTPError
from ...models.dto_object_attribute_values import DtoObjectAttributeValues
from ...types import UNSET, Response


def _get_kwargs(
    object_id: str,
    *,
    client: Client,
    attribute_name: str,
    plugin_id: str,
) -> dict[str, Any]:
    url = f"{client.base_url}/api/v4/objects/{object_id}/attributes-with-children"

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


def _parse_response(*, client: Client, response: httpx.Response) -> ApiHTTPError | DtoObjectAttributeValues | None:
    if response.status_code == HTTPStatus.OK:
        response_200 = DtoObjectAttributeValues.from_dict(response.json())

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


def _build_response(*, client: Client, response: httpx.Response) -> Response[ApiHTTPError | DtoObjectAttributeValues]:
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
) -> Response[ApiHTTPError | DtoObjectAttributeValues]:
    """Get object and all subobject attributes

     Returns object and all subobject attributes

    Args:
        object_id (str):
        attribute_name (str):
        plugin_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiHTTPError, DtoObjectAttributeValues]]
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
) -> ApiHTTPError | DtoObjectAttributeValues | None:
    """Get object and all subobject attributes

     Returns object and all subobject attributes

    Args:
        object_id (str):
        attribute_name (str):
        plugin_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiHTTPError, DtoObjectAttributeValues]
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
) -> Response[ApiHTTPError | DtoObjectAttributeValues]:
    """Get object and all subobject attributes

     Returns object and all subobject attributes

    Args:
        object_id (str):
        attribute_name (str):
        plugin_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiHTTPError, DtoObjectAttributeValues]]
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
) -> ApiHTTPError | DtoObjectAttributeValues | None:
    """Get object and all subobject attributes

     Returns object and all subobject attributes

    Args:
        object_id (str):
        attribute_name (str):
        plugin_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiHTTPError, DtoObjectAttributeValues]
    """

    return (
        await asyncio_detailed(
            object_id=object_id,
            client=client,
            attribute_name=attribute_name,
            plugin_id=plugin_id,
        )
    ).parsed
