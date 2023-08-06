from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.api_http_error import ApiHTTPError
from ...models.dto_asset_2d import DtoAsset2D
from ...types import Response


def _get_kwargs(
    asset_2_d_id: str,
    *,
    client: Client,
) -> dict[str, Any]:
    url = f"{client.base_url}/api/v4/assets-2d/{asset_2_d_id}"

    headers: dict[str, str] = client.get_headers()
    cookies: dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> ApiHTTPError | list["DtoAsset2D"] | None:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = DtoAsset2D.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ApiHTTPError.from_dict(response.json())

        return response_400
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[ApiHTTPError | list["DtoAsset2D"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    asset_2_d_id: str,
    *,
    client: Client,
) -> Response[ApiHTTPError | list["DtoAsset2D"]]:
    """Get 2d asset

     Returns a 2d asset

    Args:
        asset_2_d_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiHTTPError, List['DtoAsset2D']]]
    """

    kwargs = _get_kwargs(
        asset_2_d_id=asset_2_d_id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    asset_2_d_id: str,
    *,
    client: Client,
) -> ApiHTTPError | list["DtoAsset2D"] | None:
    """Get 2d asset

     Returns a 2d asset

    Args:
        asset_2_d_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiHTTPError, List['DtoAsset2D']]
    """

    return sync_detailed(
        asset_2_d_id=asset_2_d_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    asset_2_d_id: str,
    *,
    client: Client,
) -> Response[ApiHTTPError | list["DtoAsset2D"]]:
    """Get 2d asset

     Returns a 2d asset

    Args:
        asset_2_d_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiHTTPError, List['DtoAsset2D']]]
    """

    kwargs = _get_kwargs(
        asset_2_d_id=asset_2_d_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    asset_2_d_id: str,
    *,
    client: Client,
) -> ApiHTTPError | list["DtoAsset2D"] | None:
    """Get 2d asset

     Returns a 2d asset

    Args:
        asset_2_d_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiHTTPError, List['DtoAsset2D']]
    """

    return (
        await asyncio_detailed(
            asset_2_d_id=asset_2_d_id,
            client=client,
        )
    ).parsed
