from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.api_http_error import ApiHTTPError
from ...models.dto_plugins_meta import DtoPluginsMeta
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: Client,
    ids: list[str],
) -> dict[str, Any]:
    url = f"{client.base_url}/api/v4/plugins/meta"

    headers: dict[str, str] = client.get_headers()
    cookies: dict[str, Any] = client.get_cookies()

    params: dict[str, Any] = {}
    json_ids = ids

    params["ids"] = json_ids

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


def _parse_response(*, client: Client, response: httpx.Response) -> ApiHTTPError | DtoPluginsMeta | None:
    if response.status_code == HTTPStatus.OK:
        response_200 = DtoPluginsMeta.from_dict(response.json())

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


def _build_response(*, client: Client, response: httpx.Response) -> Response[ApiHTTPError | DtoPluginsMeta]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    ids: list[str],
) -> Response[ApiHTTPError | DtoPluginsMeta]:
    """Get plugins meta

     Returns a list of plugins meta filtered by parameters

    Args:
        ids (List[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiHTTPError, DtoPluginsMeta]]
    """

    kwargs = _get_kwargs(
        client=client,
        ids=ids,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    ids: list[str],
) -> ApiHTTPError | DtoPluginsMeta | None:
    """Get plugins meta

     Returns a list of plugins meta filtered by parameters

    Args:
        ids (List[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiHTTPError, DtoPluginsMeta]
    """

    return sync_detailed(
        client=client,
        ids=ids,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    ids: list[str],
) -> Response[ApiHTTPError | DtoPluginsMeta]:
    """Get plugins meta

     Returns a list of plugins meta filtered by parameters

    Args:
        ids (List[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiHTTPError, DtoPluginsMeta]]
    """

    kwargs = _get_kwargs(
        client=client,
        ids=ids,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    ids: list[str],
) -> ApiHTTPError | DtoPluginsMeta | None:
    """Get plugins meta

     Returns a list of plugins meta filtered by parameters

    Args:
        ids (List[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiHTTPError, DtoPluginsMeta]
    """

    return (
        await asyncio_detailed(
            client=client,
            ids=ids,
        )
    ).parsed
