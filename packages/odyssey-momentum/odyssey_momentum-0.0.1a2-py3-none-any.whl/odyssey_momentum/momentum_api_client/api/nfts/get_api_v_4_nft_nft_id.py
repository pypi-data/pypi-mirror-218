from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.api_http_error import ApiHTTPError
from ...models.dto_world_nft_meta import DtoWorldNFTMeta
from ...types import Response


def _get_kwargs(
    nft_id: str,
    *,
    client: Client,
) -> dict[str, Any]:
    url = f"{client.base_url}/api/v4/nft/{nft_id}"

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


def _parse_response(*, client: Client, response: httpx.Response) -> ApiHTTPError | DtoWorldNFTMeta | None:
    if response.status_code == HTTPStatus.OK:
        response_200 = DtoWorldNFTMeta.from_dict(response.json())

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


def _build_response(*, client: Client, response: httpx.Response) -> Response[ApiHTTPError | DtoWorldNFTMeta]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    nft_id: str,
    *,
    client: Client,
) -> Response[ApiHTTPError | DtoWorldNFTMeta]:
    """Get NFT metadata.

     Returns ERC721 metadata.

    Args:
        nft_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiHTTPError, DtoWorldNFTMeta]]
    """

    kwargs = _get_kwargs(
        nft_id=nft_id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    nft_id: str,
    *,
    client: Client,
) -> ApiHTTPError | DtoWorldNFTMeta | None:
    """Get NFT metadata.

     Returns ERC721 metadata.

    Args:
        nft_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiHTTPError, DtoWorldNFTMeta]
    """

    return sync_detailed(
        nft_id=nft_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    nft_id: str,
    *,
    client: Client,
) -> Response[ApiHTTPError | DtoWorldNFTMeta]:
    """Get NFT metadata.

     Returns ERC721 metadata.

    Args:
        nft_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiHTTPError, DtoWorldNFTMeta]]
    """

    kwargs = _get_kwargs(
        nft_id=nft_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    nft_id: str,
    *,
    client: Client,
) -> ApiHTTPError | DtoWorldNFTMeta | None:
    """Get NFT metadata.

     Returns ERC721 metadata.

    Args:
        nft_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiHTTPError, DtoWorldNFTMeta]
    """

    return (
        await asyncio_detailed(
            nft_id=nft_id,
            client=client,
        )
    ).parsed
