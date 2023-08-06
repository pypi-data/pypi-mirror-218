from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.api_http_error import ApiHTTPError
from ...models.node_api_add_pending_stake_transaction_body import NodeApiAddPendingStakeTransactionBody
from ...models.node_api_add_pending_stake_transaction_out import NodeApiAddPendingStakeTransactionOut
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: NodeApiAddPendingStakeTransactionBody,
) -> dict[str, Any]:
    url = f"{client.base_url}/api/v4/users/me/stakes"

    headers: dict[str, str] = client.get_headers()
    cookies: dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_json_body,
    }


def _parse_response(
    *, client: Client, response: httpx.Response
) -> ApiHTTPError | NodeApiAddPendingStakeTransactionOut | None:
    if response.status_code == HTTPStatus.OK:
        response_200 = NodeApiAddPendingStakeTransactionOut.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ApiHTTPError.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = ApiHTTPError.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[ApiHTTPError | NodeApiAddPendingStakeTransactionOut]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: NodeApiAddPendingStakeTransactionBody,
) -> Response[ApiHTTPError | NodeApiAddPendingStakeTransactionOut]:
    """Add pending stake transaction

     Add pending transaction

    Args:
        json_body (NodeApiAddPendingStakeTransactionBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiHTTPError, NodeApiAddPendingStakeTransactionOut]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    json_body: NodeApiAddPendingStakeTransactionBody,
) -> ApiHTTPError | NodeApiAddPendingStakeTransactionOut | None:
    """Add pending stake transaction

     Add pending transaction

    Args:
        json_body (NodeApiAddPendingStakeTransactionBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiHTTPError, NodeApiAddPendingStakeTransactionOut]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: NodeApiAddPendingStakeTransactionBody,
) -> Response[ApiHTTPError | NodeApiAddPendingStakeTransactionOut]:
    """Add pending stake transaction

     Add pending transaction

    Args:
        json_body (NodeApiAddPendingStakeTransactionBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiHTTPError, NodeApiAddPendingStakeTransactionOut]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    json_body: NodeApiAddPendingStakeTransactionBody,
) -> ApiHTTPError | NodeApiAddPendingStakeTransactionOut | None:
    """Add pending stake transaction

     Add pending transaction

    Args:
        json_body (NodeApiAddPendingStakeTransactionBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiHTTPError, NodeApiAddPendingStakeTransactionOut]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
