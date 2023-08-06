from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.api_http_error import ApiHTTPError
from ...models.dto_asset_3d import DtoAsset3D
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    category: Unset | None | str = UNSET,
) -> dict[str, Any]:
    url = f"{client.base_url}/api/v4/assets-3d"

    headers: dict[str, str] = client.get_headers()
    cookies: dict[str, Any] = client.get_cookies()

    params: dict[str, Any] = {}
    params["category"] = category

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


def _parse_response(*, client: Client, response: httpx.Response) -> ApiHTTPError | list["DtoAsset3D"] | None:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = DtoAsset3D.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ApiHTTPError.from_dict(response.json())

        return response_400
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[ApiHTTPError | list["DtoAsset3D"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    category: Unset | None | str = UNSET,
) -> Response[ApiHTTPError | list["DtoAsset3D"]]:
    """Get 3d assets

     Returns a filtered list of 3d assets

    Args:
        category (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiHTTPError, List['DtoAsset3D']]]
    """

    kwargs = _get_kwargs(
        client=client,
        category=category,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    category: Unset | None | str = UNSET,
) -> ApiHTTPError | list["DtoAsset3D"] | None:
    """Get 3d assets

     Returns a filtered list of 3d assets

    Args:
        category (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiHTTPError, List['DtoAsset3D']]
    """

    return sync_detailed(
        client=client,
        category=category,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    category: Unset | None | str = UNSET,
) -> Response[ApiHTTPError | list["DtoAsset3D"]]:
    """Get 3d assets

     Returns a filtered list of 3d assets

    Args:
        category (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiHTTPError, List['DtoAsset3D']]]
    """

    kwargs = _get_kwargs(
        client=client,
        category=category,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    category: Unset | None | str = UNSET,
) -> ApiHTTPError | list["DtoAsset3D"] | None:
    """Get 3d assets

     Returns a filtered list of 3d assets

    Args:
        category (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiHTTPError, List['DtoAsset3D']]
    """

    return (
        await asyncio_detailed(
            client=client,
            category=category,
        )
    ).parsed
