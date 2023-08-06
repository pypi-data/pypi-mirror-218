from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.api_http_error import ApiHTTPError
from ...models.dto_explore_option import DtoExploreOption
from ...types import UNSET, Response


def _get_kwargs(
    world_id: str,
    *,
    client: Client,
    object_id: str,
) -> dict[str, Any]:
    url = f"{client.base_url}/api/v4/worlds/{world_id}/explore"

    headers: dict[str, str] = client.get_headers()
    cookies: dict[str, Any] = client.get_cookies()

    params: dict[str, Any] = {}
    params["objectID"] = object_id

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


def _parse_response(*, client: Client, response: httpx.Response) -> ApiHTTPError | DtoExploreOption | None:
    if response.status_code == HTTPStatus.OK:
        response_200 = DtoExploreOption.from_dict(response.json())

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


def _build_response(*, client: Client, response: httpx.Response) -> Response[ApiHTTPError | DtoExploreOption]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    world_id: str,
    *,
    client: Client,
    object_id: str,
) -> Response[ApiHTTPError | DtoExploreOption]:
    """Returns objects and one level of children

     Returns object information and one level of children based on world_id (used in explore widget)

    Args:
        world_id (str):
        object_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiHTTPError, DtoExploreOption]]
    """

    kwargs = _get_kwargs(
        world_id=world_id,
        client=client,
        object_id=object_id,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    world_id: str,
    *,
    client: Client,
    object_id: str,
) -> ApiHTTPError | DtoExploreOption | None:
    """Returns objects and one level of children

     Returns object information and one level of children based on world_id (used in explore widget)

    Args:
        world_id (str):
        object_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiHTTPError, DtoExploreOption]
    """

    return sync_detailed(
        world_id=world_id,
        client=client,
        object_id=object_id,
    ).parsed


async def asyncio_detailed(
    world_id: str,
    *,
    client: Client,
    object_id: str,
) -> Response[ApiHTTPError | DtoExploreOption]:
    """Returns objects and one level of children

     Returns object information and one level of children based on world_id (used in explore widget)

    Args:
        world_id (str):
        object_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiHTTPError, DtoExploreOption]]
    """

    kwargs = _get_kwargs(
        world_id=world_id,
        client=client,
        object_id=object_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    world_id: str,
    *,
    client: Client,
    object_id: str,
) -> ApiHTTPError | DtoExploreOption | None:
    """Returns objects and one level of children

     Returns object information and one level of children based on world_id (used in explore widget)

    Args:
        world_id (str):
        object_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiHTTPError, DtoExploreOption]
    """

    return (
        await asyncio_detailed(
            world_id=world_id,
            client=client,
            object_id=object_id,
        )
    ).parsed
