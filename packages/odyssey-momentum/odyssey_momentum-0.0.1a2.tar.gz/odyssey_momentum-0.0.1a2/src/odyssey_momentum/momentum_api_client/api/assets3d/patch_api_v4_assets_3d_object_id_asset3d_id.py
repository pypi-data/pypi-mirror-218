from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.api_http_error import ApiHTTPError
from ...models.assets_3d_api_update_asset_3d_by_id_in_body import Assets3DApiUpdateAsset3DByIDInBody
from ...models.dto_asset_3d import DtoAsset3D
from ...types import Response


def _get_kwargs(
    object_id: str,
    asset3d_id: str,
    *,
    client: Client,
    json_body: Assets3DApiUpdateAsset3DByIDInBody,
) -> dict[str, Any]:
    url = "{}/api/v4/assets-3d/{object_id}/{asset3d_id}".format(
        client.base_url, object_id=object_id, asset3d_id=asset3d_id
    )

    headers: dict[str, str] = client.get_headers()
    cookies: dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "patch",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_json_body,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> ApiHTTPError | DtoAsset3D | None:
    if response.status_code == HTTPStatus.OK:
        response_200 = DtoAsset3D.from_dict(response.json())

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


def _build_response(*, client: Client, response: httpx.Response) -> Response[ApiHTTPError | DtoAsset3D]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    object_id: str,
    asset3d_id: str,
    *,
    client: Client,
    json_body: Assets3DApiUpdateAsset3DByIDInBody,
) -> Response[ApiHTTPError | DtoAsset3D]:
    """Update 3d asset meta by its umid

     Update 3d asset meta by its umid

    Args:
        object_id (str):
        asset3d_id (str):
        json_body (Assets3DApiUpdateAsset3DByIDInBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiHTTPError, DtoAsset3D]]
    """

    kwargs = _get_kwargs(
        object_id=object_id,
        asset3d_id=asset3d_id,
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
    asset3d_id: str,
    *,
    client: Client,
    json_body: Assets3DApiUpdateAsset3DByIDInBody,
) -> ApiHTTPError | DtoAsset3D | None:
    """Update 3d asset meta by its umid

     Update 3d asset meta by its umid

    Args:
        object_id (str):
        asset3d_id (str):
        json_body (Assets3DApiUpdateAsset3DByIDInBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiHTTPError, DtoAsset3D]
    """

    return sync_detailed(
        object_id=object_id,
        asset3d_id=asset3d_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    object_id: str,
    asset3d_id: str,
    *,
    client: Client,
    json_body: Assets3DApiUpdateAsset3DByIDInBody,
) -> Response[ApiHTTPError | DtoAsset3D]:
    """Update 3d asset meta by its umid

     Update 3d asset meta by its umid

    Args:
        object_id (str):
        asset3d_id (str):
        json_body (Assets3DApiUpdateAsset3DByIDInBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiHTTPError, DtoAsset3D]]
    """

    kwargs = _get_kwargs(
        object_id=object_id,
        asset3d_id=asset3d_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    object_id: str,
    asset3d_id: str,
    *,
    client: Client,
    json_body: Assets3DApiUpdateAsset3DByIDInBody,
) -> ApiHTTPError | DtoAsset3D | None:
    """Update 3d asset meta by its umid

     Update 3d asset meta by its umid

    Args:
        object_id (str):
        asset3d_id (str):
        json_body (Assets3DApiUpdateAsset3DByIDInBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiHTTPError, DtoAsset3D]
    """

    return (
        await asyncio_detailed(
            object_id=object_id,
            asset3d_id=asset3d_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
