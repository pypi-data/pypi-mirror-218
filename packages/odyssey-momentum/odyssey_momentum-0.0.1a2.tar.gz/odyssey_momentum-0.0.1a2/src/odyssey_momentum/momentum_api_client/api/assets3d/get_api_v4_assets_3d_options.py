from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.api_http_error import ApiHTTPError
from ...models.dto_assets_3d_options import DtoAssets3DOptions
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: Client,
    assets_3_d_i_ds: list[str],
) -> dict[str, Any]:
    url = f"{client.base_url}/api/v4/assets-3d/options"

    headers: dict[str, str] = client.get_headers()
    cookies: dict[str, Any] = client.get_cookies()

    params: dict[str, Any] = {}
    json_assets_3_d_i_ds = assets_3_d_i_ds

    params["assets3dIDs"] = json_assets_3_d_i_ds

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


def _parse_response(*, client: Client, response: httpx.Response) -> ApiHTTPError | DtoAssets3DOptions | None:
    if response.status_code == HTTPStatus.OK:
        response_200 = DtoAssets3DOptions.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ApiHTTPError.from_dict(response.json())

        return response_400
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[ApiHTTPError | DtoAssets3DOptions]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    assets_3_d_i_ds: list[str],
) -> Response[ApiHTTPError | DtoAssets3DOptions]:
    """Get 3d assets options

     Returns list of 3d assets options

    Args:
        assets_3_d_i_ds (List[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiHTTPError, DtoAssets3DOptions]]
    """

    kwargs = _get_kwargs(
        client=client,
        assets_3_d_i_ds=assets_3_d_i_ds,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    assets_3_d_i_ds: list[str],
) -> ApiHTTPError | DtoAssets3DOptions | None:
    """Get 3d assets options

     Returns list of 3d assets options

    Args:
        assets_3_d_i_ds (List[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiHTTPError, DtoAssets3DOptions]
    """

    return sync_detailed(
        client=client,
        assets_3_d_i_ds=assets_3_d_i_ds,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    assets_3_d_i_ds: list[str],
) -> Response[ApiHTTPError | DtoAssets3DOptions]:
    """Get 3d assets options

     Returns list of 3d assets options

    Args:
        assets_3_d_i_ds (List[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiHTTPError, DtoAssets3DOptions]]
    """

    kwargs = _get_kwargs(
        client=client,
        assets_3_d_i_ds=assets_3_d_i_ds,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    assets_3_d_i_ds: list[str],
) -> ApiHTTPError | DtoAssets3DOptions | None:
    """Get 3d assets options

     Returns list of 3d assets options

    Args:
        assets_3_d_i_ds (List[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiHTTPError, DtoAssets3DOptions]
    """

    return (
        await asyncio_detailed(
            client=client,
            assets_3_d_i_ds=assets_3_d_i_ds,
        )
    ).parsed
