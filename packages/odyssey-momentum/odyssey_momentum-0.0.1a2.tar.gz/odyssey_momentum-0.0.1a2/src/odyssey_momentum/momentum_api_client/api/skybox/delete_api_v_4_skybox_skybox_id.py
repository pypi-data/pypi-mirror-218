from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.api_http_error import ApiHTTPError
from ...models.node_api_remove_skybox_by_id_body import NodeApiRemoveSkyboxByIDBody
from ...types import Response


def _get_kwargs(
    skybox_id: str,
    *,
    client: Client,
    json_body: NodeApiRemoveSkyboxByIDBody,
) -> dict[str, Any]:
    url = f"{client.base_url}/api/v4/skybox/{skybox_id}"

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


def _parse_response(*, client: Client, response: httpx.Response) -> ApiHTTPError | int | None:
    if response.status_code == HTTPStatus.OK:
        response_200 = cast(int, response.json())
        return response_200
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = ApiHTTPError.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[ApiHTTPError | int]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    skybox_id: str,
    *,
    client: Client,
    json_body: NodeApiRemoveSkyboxByIDBody,
) -> Response[ApiHTTPError | int]:
    """Delete skybox by ID

     Delete skybox by ID

    Args:
        skybox_id (str):
        json_body (NodeApiRemoveSkyboxByIDBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiHTTPError, int]]
    """

    kwargs = _get_kwargs(
        skybox_id=skybox_id,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    skybox_id: str,
    *,
    client: Client,
    json_body: NodeApiRemoveSkyboxByIDBody,
) -> ApiHTTPError | int | None:
    """Delete skybox by ID

     Delete skybox by ID

    Args:
        skybox_id (str):
        json_body (NodeApiRemoveSkyboxByIDBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiHTTPError, int]
    """

    return sync_detailed(
        skybox_id=skybox_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    skybox_id: str,
    *,
    client: Client,
    json_body: NodeApiRemoveSkyboxByIDBody,
) -> Response[ApiHTTPError | int]:
    """Delete skybox by ID

     Delete skybox by ID

    Args:
        skybox_id (str):
        json_body (NodeApiRemoveSkyboxByIDBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiHTTPError, int]]
    """

    kwargs = _get_kwargs(
        skybox_id=skybox_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    skybox_id: str,
    *,
    client: Client,
    json_body: NodeApiRemoveSkyboxByIDBody,
) -> ApiHTTPError | int | None:
    """Delete skybox by ID

     Delete skybox by ID

    Args:
        skybox_id (str):
        json_body (NodeApiRemoveSkyboxByIDBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiHTTPError, int]
    """

    return (
        await asyncio_detailed(
            skybox_id=skybox_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
