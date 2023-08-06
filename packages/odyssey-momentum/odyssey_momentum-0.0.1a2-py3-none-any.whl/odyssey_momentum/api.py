"""
Momentum API library.

Wraps the automatically generated code to expose a (hopefully) easier to user API and replace it at some point.

TODO: find a better code generator or write our own implementation :)

TODO: move this into package namespace
"""
import http
import logging
import typing
import uuid
from urllib.parse import urljoin

import httpx

from .momentum_api_client import AuthenticatedClient, models
from .momentum_api_client.api.assets3d import get_api_v4_assets_3d
from .momentum_api_client.api.objects import (
    delete_api_v4_objects_object_id,
    post_api_v4_objects,
    post_api_v4_objects_object_id_attributes,
)
from .momentum_api_client.api.profile import patch_api_v4_profile
from .momentum_api_client.api.users import get_api_v4_users_me
from .momentum_api_client.models.api_http_error import ApiHTTPError
from .momentum_api_client.types import Response

T = typing.TypeVar("T")
ResponseType = Response[ApiHTTPError | T]

User: typing.TypeAlias = models.DtoUser

BASE_PATH = "api/v4"
PLUGIN_CORE = "f0f0f0f0-0f0f-4ff0-af0f-f0f0f0f0f0f0"
OBJECT_TYPE_CUSTOM = "4ed3a5bb-53f8-4511-941b-07902982c31c"


logger = logging.getLogger(__name__)


class APIException(Exception):
    def __init__(self, message, response):
        super().__init__(message)
        self.response = response


class APIPermissionDenied(APIException):
    pass


class API:
    def __init__(self, base_url, auth_token: str):
        self.base_url = base_url
        self.client = AuthenticatedClient(base_url, auth_token)  # type: ignore
        self.httpx_client = httpx.AsyncClient(http2=True, headers={"Authorization": f"Bearer {auth_token}"})

    async def current_user(self) -> User:
        response: ResponseType[models.DtoUser] = await get_api_v4_users_me.asyncio_detailed(client=self.client)
        user = raise_for_status(response)
        return user  # TODO: don't expose Dto type

    async def update_profile(self, name: str, image_file: typing.IO[bytes]):
        image_id = await self.upload_image(image_file)
        profile = models.NodeApiProfileUpdateBodyProfile(avatar_hash=image_id)
        body = models.NodeApiProfileUpdateBody(name, profile)
        response = await patch_api_v4_profile.asyncio_detailed(client=self.client, json_body=body)
        if is_success(response.status_code) and isinstance(response.parsed, models.NodeApiProfileUpdateOut):
            return response.parsed
        msg = "Update profile"
        raise APIException(msg, response)

    async def upload_image(self, f: typing.IO[bytes]) -> str:
        # bah, auto generated code doesn't like our (valid) openapi syntax for these EPs :/
        url = urljoin(self.base_url, (BASE_PATH + "/media/upload/image"))
        files = {"file": f}
        response = await self.httpx_client.post(url, files=files)
        response.raise_for_status()
        return response.json()["hash"]

    async def create_object(
        self,
        name: str,
        world_oid: uuid.UUID,
        asset_3d_id: str,
        position: tuple[float, float, float] | None = None,
        rotation: tuple[float, float, float] | None = None,
        scale: tuple[float, float, float] | None = None,
    ):
        args: dict[str, typing.Any] = {
            "object_name": name,
            "object_type_id": OBJECT_TYPE_CUSTOM,
            "parent_id": str(world_oid),
            "asset_3d_id": asset_3d_id,
        }
        if position:
            transform = args.setdefault("transform", {})
            transform["position"] = _coords_to_dict(position)
        if rotation:
            transform = args.setdefault("transform", {})
            transform["rotation"] = _coords_to_dict(rotation)

        # hmm, scale defaults to 0,0,0... :/
        if scale is None:
            scale = (1, 1, 1)
        transform = args.setdefault("transform", {})
        transform["scale"] = _coords_to_dict(scale)

        args["transform"] = transform
        body = models.NodeApiObjectsCreateObjectInBody.from_dict(args)
        response = await post_api_v4_objects.asyncio_detailed(client=self.client, json_body=body)
        result = raise_for_status(response)
        if result.object_id:
            return uuid.UUID(result.object_id)
        msg = "Create object"
        raise APIException(msg, response)

    async def remove_object(self, oid: uuid.UUID):
        response = await delete_api_v4_objects_object_id.asyncio_detailed(client=self.client, object_id=str(oid))
        raise_for_status(response)

    async def set_object_attr(
        self, oid: uuid.UUID, name: str, value: typing.Mapping[str, typing.Any], plugin_uid: uuid.UUID | None = None
    ):
        plugin_id = str(plugin_uid) if plugin_uid else PLUGIN_CORE

        body = models.NodeApiSetObjectAttributesValueInBody(
            plugin_id=plugin_id,
            attribute_name=name,
            attribute_value=models.NodeApiSetObjectAttributesValueInBodyAttributeValue.from_dict(value),  # type: ignore
        )
        response = await post_api_v4_objects_object_id_attributes.asyncio_detailed(
            str(oid), client=self.client, json_body=body
        )
        raise_for_status(response)

    async def asset_list(self, category="custom") -> typing.Iterable[models.DtoAsset3D]:
        """Return a list of 3D assets (a.k.a. models) available."""
        response = await get_api_v4_assets_3d.asyncio_detailed(
            client=self.client,
            category=category,
        )
        result = raise_for_status(response)
        return result

    async def asset_upload(
        self,
        name: str,
        asset: typing.IO[bytes],
        *,
        private=True,
        preview: str | None = None,
    ):
        url = urljoin(self.base_url, (BASE_PATH + "/assets-3d/upload"))
        files = {"asset": asset}
        body = {"name": name, "is_private": private}
        if preview:
            body["preview_hash"] = preview

        response = await self.httpx_client.post(url, data=body, files=files)
        response.raise_for_status()
        return response.json()


def raise_for_status(response: ResponseType[T]) -> T:
    if response.status_code == http.HTTPStatus.FORBIDDEN:
        msg = "API permission denied"
        raise APIPermissionDenied(msg, response)
    if not is_success(response.status_code):
        msg = "API error"
        raise APIException(msg, response)
    if isinstance(response.parsed, ApiHTTPError):
        __import__("pdb").set_trace()
        msg = "API error"
        raise APIException(msg, response)
    # assert response.parsed is not None
    # TODO: 200 with responses ...
    return response.parsed  # type: ignore


def is_success(status: http.HTTPStatus) -> bool:
    return 200 <= status.value <= 299


def _coords_to_dict(t: tuple[float, float, float]):
    return {"x": t[0], "y": t[1], "z": t[2]}
