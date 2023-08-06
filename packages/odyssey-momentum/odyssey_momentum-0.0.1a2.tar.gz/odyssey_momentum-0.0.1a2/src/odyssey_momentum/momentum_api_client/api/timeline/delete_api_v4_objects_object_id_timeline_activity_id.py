from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.api_http_error import ApiHTTPError
from ...models.node_api_timeline_for_object_out import NodeApiTimelineForObjectOut
from ...types import Response


def _get_kwargs(
    object_id: str,
    activity_id: str,
    *,
    client: Client,
) -> dict[str, Any]:
    url = "{}/api/v4/objects/{object_id}/timeline/{activity_id}".format(
        client.base_url, object_id=object_id, activity_id=activity_id
    )

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


def _parse_response(*, client: Client, response: httpx.Response) -> ApiHTTPError | NodeApiTimelineForObjectOut | None:
    if response.status_code == HTTPStatus.OK:
        response_200 = NodeApiTimelineForObjectOut.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = ApiHTTPError.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[ApiHTTPError | NodeApiTimelineForObjectOut]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    object_id: str,
    activity_id: str,
    *,
    client: Client,
) -> Response[ApiHTTPError | NodeApiTimelineForObjectOut]:
    """Remove an item from a timeline

     Removes an item from the timeline of an object

    Args:
        object_id (str):
        activity_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiHTTPError, NodeApiTimelineForObjectOut]]
    """

    kwargs = _get_kwargs(
        object_id=object_id,
        activity_id=activity_id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    object_id: str,
    activity_id: str,
    *,
    client: Client,
) -> ApiHTTPError | NodeApiTimelineForObjectOut | None:
    """Remove an item from a timeline

     Removes an item from the timeline of an object

    Args:
        object_id (str):
        activity_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiHTTPError, NodeApiTimelineForObjectOut]
    """

    return sync_detailed(
        object_id=object_id,
        activity_id=activity_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    object_id: str,
    activity_id: str,
    *,
    client: Client,
) -> Response[ApiHTTPError | NodeApiTimelineForObjectOut]:
    """Remove an item from a timeline

     Removes an item from the timeline of an object

    Args:
        object_id (str):
        activity_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiHTTPError, NodeApiTimelineForObjectOut]]
    """

    kwargs = _get_kwargs(
        object_id=object_id,
        activity_id=activity_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    object_id: str,
    activity_id: str,
    *,
    client: Client,
) -> ApiHTTPError | NodeApiTimelineForObjectOut | None:
    """Remove an item from a timeline

     Removes an item from the timeline of an object

    Args:
        object_id (str):
        activity_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiHTTPError, NodeApiTimelineForObjectOut]
    """

    return (
        await asyncio_detailed(
            object_id=object_id,
            activity_id=activity_id,
            client=client,
        )
    ).parsed
