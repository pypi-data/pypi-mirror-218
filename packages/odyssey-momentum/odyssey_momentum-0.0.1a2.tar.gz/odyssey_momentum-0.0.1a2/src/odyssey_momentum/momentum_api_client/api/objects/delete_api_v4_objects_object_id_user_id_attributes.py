from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.api_http_error import ApiHTTPError
from ...models.node_api_remove_object_user_attribute_value_body import NodeApiRemoveObjectUserAttributeValueBody
from ...types import Response


def _get_kwargs(
    object_id: str,
    user_id: str,
    *,
    client: Client,
    json_body: NodeApiRemoveObjectUserAttributeValueBody,
) -> dict[str, Any]:
    url = "{}/api/v4/objects/{object_id}/{user_id}/attributes".format(
        client.base_url, object_id=object_id, user_id=user_id
    )

    headers: dict[str, str] = client.get_headers()
    cookies: dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "delete",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_json_body,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Any | ApiHTTPError | None:
    if response.status_code == HTTPStatus.OK:
        response_200 = cast(Any, None)
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


def _build_response(*, client: Client, response: httpx.Response) -> Response[Any | ApiHTTPError]:
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
    json_body: NodeApiRemoveObjectUserAttributeValueBody,
) -> Response[Any | ApiHTTPError]:
    """Delete object user attribute

     Deletes a object attribute

    Args:
        object_id (str):
        user_id (str):
        json_body (NodeApiRemoveObjectUserAttributeValueBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ApiHTTPError]]
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
    json_body: NodeApiRemoveObjectUserAttributeValueBody,
) -> Any | ApiHTTPError | None:
    """Delete object user attribute

     Deletes a object attribute

    Args:
        object_id (str):
        user_id (str):
        json_body (NodeApiRemoveObjectUserAttributeValueBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ApiHTTPError]
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
    json_body: NodeApiRemoveObjectUserAttributeValueBody,
) -> Response[Any | ApiHTTPError]:
    """Delete object user attribute

     Deletes a object attribute

    Args:
        object_id (str):
        user_id (str):
        json_body (NodeApiRemoveObjectUserAttributeValueBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ApiHTTPError]]
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
    json_body: NodeApiRemoveObjectUserAttributeValueBody,
) -> Any | ApiHTTPError | None:
    """Delete object user attribute

     Deletes a object attribute

    Args:
        object_id (str):
        user_id (str):
        json_body (NodeApiRemoveObjectUserAttributeValueBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ApiHTTPError]
    """

    return (
        await asyncio_detailed(
            object_id=object_id,
            user_id=user_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
