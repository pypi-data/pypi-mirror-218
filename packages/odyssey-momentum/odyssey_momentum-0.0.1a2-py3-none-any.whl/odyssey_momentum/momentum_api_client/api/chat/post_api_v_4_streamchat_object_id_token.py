from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.api_http_error import ApiHTTPError
from ...models.streamchat_api_channel_token_response import StreamchatApiChannelTokenResponse
from ...types import Response


def _get_kwargs(
    object_id: str,
    *,
    client: Client,
) -> dict[str, Any]:
    url = f"{client.base_url}/api/v4/streamchat/{object_id}/token"

    headers: dict[str, str] = client.get_headers()
    cookies: dict[str, Any] = client.get_cookies()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
    }


def _parse_response(
    *, client: Client, response: httpx.Response
) -> ApiHTTPError | StreamchatApiChannelTokenResponse | None:
    if response.status_code == HTTPStatus.OK:
        response_200 = StreamchatApiChannelTokenResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ApiHTTPError.from_dict(response.json())

        return response_400
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[ApiHTTPError | StreamchatApiChannelTokenResponse]:
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
) -> Response[ApiHTTPError | StreamchatApiChannelTokenResponse]:
    """Get a authorization token

     Request a chat authorization token for current user and given object (world or object)
    The user is required to be connected to the world/object.
    This also automatically joins the user as a member to the channel, so the join endpoint does not
    have to be called.

    Args:
        object_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiHTTPError, StreamchatApiChannelTokenResponse]]
    """

    kwargs = _get_kwargs(
        object_id=object_id,
        client=client,
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
) -> ApiHTTPError | StreamchatApiChannelTokenResponse | None:
    """Get a authorization token

     Request a chat authorization token for current user and given object (world or object)
    The user is required to be connected to the world/object.
    This also automatically joins the user as a member to the channel, so the join endpoint does not
    have to be called.

    Args:
        object_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiHTTPError, StreamchatApiChannelTokenResponse]
    """

    return sync_detailed(
        object_id=object_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    object_id: str,
    *,
    client: Client,
) -> Response[ApiHTTPError | StreamchatApiChannelTokenResponse]:
    """Get a authorization token

     Request a chat authorization token for current user and given object (world or object)
    The user is required to be connected to the world/object.
    This also automatically joins the user as a member to the channel, so the join endpoint does not
    have to be called.

    Args:
        object_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiHTTPError, StreamchatApiChannelTokenResponse]]
    """

    kwargs = _get_kwargs(
        object_id=object_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    object_id: str,
    *,
    client: Client,
) -> ApiHTTPError | StreamchatApiChannelTokenResponse | None:
    """Get a authorization token

     Request a chat authorization token for current user and given object (world or object)
    The user is required to be connected to the world/object.
    This also automatically joins the user as a member to the channel, so the join endpoint does not
    have to be called.

    Args:
        object_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiHTTPError, StreamchatApiChannelTokenResponse]
    """

    return (
        await asyncio_detailed(
            object_id=object_id,
            client=client,
        )
    ).parsed
