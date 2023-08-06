from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.api_http_error import ApiHTTPError
from ...models.dto_object_sub_attributes import DtoObjectSubAttributes
from ...models.node_api_set_object_user_attribute_sub_value_body import NodeApiSetObjectUserAttributeSubValueBody
from ...types import Response


def _get_kwargs(
    object_id: str,
    user_id: str,
    *,
    client: Client,
    json_body: NodeApiSetObjectUserAttributeSubValueBody,
) -> dict[str, Any]:
    url = "{}/api/v4/objects/{object_id}/{user_id}/attributes/sub".format(
        client.base_url, object_id=object_id, user_id=user_id
    )

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


def _parse_response(*, client: Client, response: httpx.Response) -> ApiHTTPError | DtoObjectSubAttributes | None:
    if response.status_code == HTTPStatus.ACCEPTED:
        response_202 = DtoObjectSubAttributes.from_dict(response.json())

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


def _build_response(*, client: Client, response: httpx.Response) -> Response[ApiHTTPError | DtoObjectSubAttributes]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    object_id: str,
    user_id: str,
    *,
    client: Client,
    json_body: NodeApiSetObjectUserAttributeSubValueBody,
) -> Response[ApiHTTPError | DtoObjectSubAttributes]:
    """Set object sub attribute

     Sets a object sub attribute

    Args:
        object_id (str):
        user_id (str):
        json_body (NodeApiSetObjectUserAttributeSubValueBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiHTTPError, DtoObjectSubAttributes]]
    """

    kwargs = _get_kwargs(
        object_id=object_id,
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
    object_id: str,
    user_id: str,
    *,
    client: Client,
    json_body: NodeApiSetObjectUserAttributeSubValueBody,
) -> ApiHTTPError | DtoObjectSubAttributes | None:
    """Set object sub attribute

     Sets a object sub attribute

    Args:
        object_id (str):
        user_id (str):
        json_body (NodeApiSetObjectUserAttributeSubValueBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiHTTPError, DtoObjectSubAttributes]
    """

    return sync_detailed(
        object_id=object_id,
        user_id=user_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    object_id: str,
    user_id: str,
    *,
    client: Client,
    json_body: NodeApiSetObjectUserAttributeSubValueBody,
) -> Response[ApiHTTPError | DtoObjectSubAttributes]:
    """Set object sub attribute

     Sets a object sub attribute

    Args:
        object_id (str):
        user_id (str):
        json_body (NodeApiSetObjectUserAttributeSubValueBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiHTTPError, DtoObjectSubAttributes]]
    """

    kwargs = _get_kwargs(
        object_id=object_id,
        user_id=user_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    object_id: str,
    user_id: str,
    *,
    client: Client,
    json_body: NodeApiSetObjectUserAttributeSubValueBody,
) -> ApiHTTPError | DtoObjectSubAttributes | None:
    """Set object sub attribute

     Sets a object sub attribute

    Args:
        object_id (str):
        user_id (str):
        json_body (NodeApiSetObjectUserAttributeSubValueBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiHTTPError, DtoObjectSubAttributes]
    """

    return (
        await asyncio_detailed(
            object_id=object_id,
            user_id=user_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
