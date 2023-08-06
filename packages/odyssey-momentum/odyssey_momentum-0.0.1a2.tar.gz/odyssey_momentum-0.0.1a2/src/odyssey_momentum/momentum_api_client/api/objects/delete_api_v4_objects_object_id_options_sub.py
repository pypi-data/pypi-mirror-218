from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.api_http_error import ApiHTTPError
from ...models.node_api_objects_remove_object_sub_option_body import NodeApiObjectsRemoveObjectSubOptionBody
from ...types import Response


def _get_kwargs(
    object_id: str,
    *,
    client: Client,
    json_body: NodeApiObjectsRemoveObjectSubOptionBody,
) -> dict[str, Any]:
    url = f"{client.base_url}/api/v4/objects/{object_id}/options/sub"

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
    object_id: str,
    *,
    client: Client,
    json_body: NodeApiObjectsRemoveObjectSubOptionBody,
) -> Response[Any | ApiHTTPError]:
    """Delete object sub option by object UMID

     Deletes a object sub option by object UMID

    Args:
        object_id (str):
        json_body (NodeApiObjectsRemoveObjectSubOptionBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ApiHTTPError]]
    """

    kwargs = _get_kwargs(
        object_id=object_id,
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
    *,
    client: Client,
    json_body: NodeApiObjectsRemoveObjectSubOptionBody,
) -> Any | ApiHTTPError | None:
    """Delete object sub option by object UMID

     Deletes a object sub option by object UMID

    Args:
        object_id (str):
        json_body (NodeApiObjectsRemoveObjectSubOptionBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ApiHTTPError]
    """

    return sync_detailed(
        object_id=object_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    object_id: str,
    *,
    client: Client,
    json_body: NodeApiObjectsRemoveObjectSubOptionBody,
) -> Response[Any | ApiHTTPError]:
    """Delete object sub option by object UMID

     Deletes a object sub option by object UMID

    Args:
        object_id (str):
        json_body (NodeApiObjectsRemoveObjectSubOptionBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ApiHTTPError]]
    """

    kwargs = _get_kwargs(
        object_id=object_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    object_id: str,
    *,
    client: Client,
    json_body: NodeApiObjectsRemoveObjectSubOptionBody,
) -> Any | ApiHTTPError | None:
    """Delete object sub option by object UMID

     Deletes a object sub option by object UMID

    Args:
        object_id (str):
        json_body (NodeApiObjectsRemoveObjectSubOptionBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ApiHTTPError]
    """

    return (
        await asyncio_detailed(
            object_id=object_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
