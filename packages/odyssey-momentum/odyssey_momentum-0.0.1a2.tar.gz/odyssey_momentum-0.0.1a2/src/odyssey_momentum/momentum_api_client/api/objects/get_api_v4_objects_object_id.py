from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.api_http_error import ApiHTTPError
from ...models.dto_object import DtoObject
from ...types import UNSET, Response, Unset


def _get_kwargs(
    object_id: str,
    *,
    client: Client,
    effective: Unset | None | bool = UNSET,
) -> dict[str, Any]:
    url = f"{client.base_url}/api/v4/objects/{object_id}"

    headers: dict[str, str] = client.get_headers()
    cookies: dict[str, Any] = client.get_cookies()

    params: dict[str, Any] = {}
    params["effective"] = effective

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


def _parse_response(*, client: Client, response: httpx.Response) -> ApiHTTPError | DtoObject | None:
    if response.status_code == HTTPStatus.ACCEPTED:
        response_202 = DtoObject.from_dict(response.json())

        return response_202
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


def _build_response(*, client: Client, response: httpx.Response) -> Response[ApiHTTPError | DtoObject]:
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
    effective: Unset | None | bool = UNSET,
) -> Response[ApiHTTPError | DtoObject]:
    """Get object by UMID

     Returns a object info based on UMID and query

    Args:
        object_id (str):
        effective (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiHTTPError, DtoObject]]
    """

    kwargs = _get_kwargs(
        object_id=object_id,
        client=client,
        effective=effective,
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
    effective: Unset | None | bool = UNSET,
) -> ApiHTTPError | DtoObject | None:
    """Get object by UMID

     Returns a object info based on UMID and query

    Args:
        object_id (str):
        effective (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiHTTPError, DtoObject]
    """

    return sync_detailed(
        object_id=object_id,
        client=client,
        effective=effective,
    ).parsed


async def asyncio_detailed(
    object_id: str,
    *,
    client: Client,
    effective: Unset | None | bool = UNSET,
) -> Response[ApiHTTPError | DtoObject]:
    """Get object by UMID

     Returns a object info based on UMID and query

    Args:
        object_id (str):
        effective (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiHTTPError, DtoObject]]
    """

    kwargs = _get_kwargs(
        object_id=object_id,
        client=client,
        effective=effective,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    object_id: str,
    *,
    client: Client,
    effective: Unset | None | bool = UNSET,
) -> ApiHTTPError | DtoObject | None:
    """Get object by UMID

     Returns a object info based on UMID and query

    Args:
        object_id (str):
        effective (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiHTTPError, DtoObject]
    """

    return (
        await asyncio_detailed(
            object_id=object_id,
            client=client,
            effective=effective,
        )
    ).parsed
