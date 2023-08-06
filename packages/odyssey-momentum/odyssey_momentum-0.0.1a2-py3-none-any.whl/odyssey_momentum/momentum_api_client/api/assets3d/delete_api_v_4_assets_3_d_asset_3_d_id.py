from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.api_http_error import ApiHTTPError
from ...types import Response


def _get_kwargs(
    asset_3_d_id: str,
    *,
    client: Client,
) -> dict[str, Any]:
    url = f"{client.base_url}/api/v4/assets-3d/{asset_3_d_id}"

    headers: dict[str, str] = client.get_headers()
    cookies: dict[str, Any] = client.get_cookies()

    return {
        "method": "delete",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Any | ApiHTTPError | None:
    if response.status_code == HTTPStatus.OK:
        response_200 = cast(Any, None)
        return response_200
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = ApiHTTPError.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Any | ApiHTTPError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    asset_3_d_id: str,
    *,
    client: Client,
) -> Response[Any | ApiHTTPError]:
    """Delete a 3d asset by its umid

     Deletes 3d asset by its umid

    Args:
        asset_3_d_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ApiHTTPError]]
    """

    kwargs = _get_kwargs(
        asset_3_d_id=asset_3_d_id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    asset_3_d_id: str,
    *,
    client: Client,
) -> Any | ApiHTTPError | None:
    """Delete a 3d asset by its umid

     Deletes 3d asset by its umid

    Args:
        asset_3_d_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ApiHTTPError]
    """

    return sync_detailed(
        asset_3_d_id=asset_3_d_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    asset_3_d_id: str,
    *,
    client: Client,
) -> Response[Any | ApiHTTPError]:
    """Delete a 3d asset by its umid

     Deletes 3d asset by its umid

    Args:
        asset_3_d_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ApiHTTPError]]
    """

    kwargs = _get_kwargs(
        asset_3_d_id=asset_3_d_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    asset_3_d_id: str,
    *,
    client: Client,
) -> Any | ApiHTTPError | None:
    """Delete a 3d asset by its umid

     Deletes 3d asset by its umid

    Args:
        asset_3_d_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ApiHTTPError]
    """

    return (
        await asyncio_detailed(
            asset_3_d_id=asset_3_d_id,
            client=client,
        )
    ).parsed
