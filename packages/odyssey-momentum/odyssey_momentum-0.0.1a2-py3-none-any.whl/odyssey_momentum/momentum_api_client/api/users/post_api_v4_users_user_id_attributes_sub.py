from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.api_http_error import ApiHTTPError
from ...models.dto_user_sub_attributes import DtoUserSubAttributes
from ...models.node_api_set_user_attribute_sub_value_body import NodeApiSetUserAttributeSubValueBody
from ...types import Response


def _get_kwargs(
    user_id: str,
    *,
    client: Client,
    json_body: NodeApiSetUserAttributeSubValueBody,
) -> dict[str, Any]:
    url = f"{client.base_url}/api/v4/users/{user_id}/attributes/sub"

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


def _parse_response(*, client: Client, response: httpx.Response) -> ApiHTTPError | DtoUserSubAttributes | None:
    if response.status_code == HTTPStatus.ACCEPTED:
        response_202 = DtoUserSubAttributes.from_dict(response.json())

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


def _build_response(*, client: Client, response: httpx.Response) -> Response[ApiHTTPError | DtoUserSubAttributes]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    user_id: str,
    *,
    client: Client,
    json_body: NodeApiSetUserAttributeSubValueBody,
) -> Response[ApiHTTPError | DtoUserSubAttributes]:
    """Set user sub attribute

     Sets a user sub attribute

    Args:
        user_id (str):
        json_body (NodeApiSetUserAttributeSubValueBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiHTTPError, DtoUserSubAttributes]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    user_id: str,
    *,
    client: Client,
    json_body: NodeApiSetUserAttributeSubValueBody,
) -> ApiHTTPError | DtoUserSubAttributes | None:
    """Set user sub attribute

     Sets a user sub attribute

    Args:
        user_id (str):
        json_body (NodeApiSetUserAttributeSubValueBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiHTTPError, DtoUserSubAttributes]
    """

    return sync_detailed(
        user_id=user_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    user_id: str,
    *,
    client: Client,
    json_body: NodeApiSetUserAttributeSubValueBody,
) -> Response[ApiHTTPError | DtoUserSubAttributes]:
    """Set user sub attribute

     Sets a user sub attribute

    Args:
        user_id (str):
        json_body (NodeApiSetUserAttributeSubValueBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiHTTPError, DtoUserSubAttributes]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    user_id: str,
    *,
    client: Client,
    json_body: NodeApiSetUserAttributeSubValueBody,
) -> ApiHTTPError | DtoUserSubAttributes | None:
    """Set user sub attribute

     Sets a user sub attribute

    Args:
        user_id (str):
        json_body (NodeApiSetUserAttributeSubValueBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiHTTPError, DtoUserSubAttributes]
    """

    return (
        await asyncio_detailed(
            user_id=user_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
