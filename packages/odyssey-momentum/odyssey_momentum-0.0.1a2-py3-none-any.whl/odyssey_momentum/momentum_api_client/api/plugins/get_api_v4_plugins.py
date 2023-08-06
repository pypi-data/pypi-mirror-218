from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.api_http_error import ApiHTTPError
from ...models.dto_plugins import DtoPlugins
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    ids: Unset | None | list[str] = UNSET,
    type: Unset | None | str = UNSET,
) -> dict[str, Any]:
    url = f"{client.base_url}/api/v4/plugins"

    headers: dict[str, str] = client.get_headers()
    cookies: dict[str, Any] = client.get_cookies()

    params: dict[str, Any] = {}
    json_ids: Unset | None | list[str] = UNSET
    if not isinstance(ids, Unset):
        if ids is None:
            json_ids = None
        else:
            json_ids = ids

    params["ids"] = json_ids

    params["type"] = type

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


def _parse_response(*, client: Client, response: httpx.Response) -> ApiHTTPError | DtoPlugins | None:
    if response.status_code == HTTPStatus.OK:
        response_200 = DtoPlugins.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ApiHTTPError.from_dict(response.json())

        return response_400
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[ApiHTTPError | DtoPlugins]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    ids: Unset | None | list[str] = UNSET,
    type: Unset | None | str = UNSET,
) -> Response[ApiHTTPError | DtoPlugins]:
    """Get plugins

     Returns a list of plugins filtered by parameters

    Args:
        ids (Union[Unset, None, List[str]]):
        type (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiHTTPError, DtoPlugins]]
    """

    kwargs = _get_kwargs(
        client=client,
        ids=ids,
        type=type,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    ids: Unset | None | list[str] = UNSET,
    type: Unset | None | str = UNSET,
) -> ApiHTTPError | DtoPlugins | None:
    """Get plugins

     Returns a list of plugins filtered by parameters

    Args:
        ids (Union[Unset, None, List[str]]):
        type (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiHTTPError, DtoPlugins]
    """

    return sync_detailed(
        client=client,
        ids=ids,
        type=type,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    ids: Unset | None | list[str] = UNSET,
    type: Unset | None | str = UNSET,
) -> Response[ApiHTTPError | DtoPlugins]:
    """Get plugins

     Returns a list of plugins filtered by parameters

    Args:
        ids (Union[Unset, None, List[str]]):
        type (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiHTTPError, DtoPlugins]]
    """

    kwargs = _get_kwargs(
        client=client,
        ids=ids,
        type=type,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    ids: Unset | None | list[str] = UNSET,
    type: Unset | None | str = UNSET,
) -> ApiHTTPError | DtoPlugins | None:
    """Get plugins

     Returns a list of plugins filtered by parameters

    Args:
        ids (Union[Unset, None, List[str]]):
        type (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiHTTPError, DtoPlugins]
    """

    return (
        await asyncio_detailed(
            client=client,
            ids=ids,
            type=type,
        )
    ).parsed
