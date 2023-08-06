import base64
import json
import logging
import pathlib
import random
import string
import tempfile
import time
from typing import TypedDict

import anyio
import httpx
from eth_account import Account
from eth_account.messages import encode_defunct
from eth_account.signers.local import LocalAccount

from .urls import auth_challenge_url, auth_guest_url, auth_token_url

logger = logging.getLogger(__name__)

_TMP_AUTH = "pyposbus_auth.json"
_ONE_DAY = 60 * 60 * 24
_15_MIN = 60 * 15


class Auth(TypedDict):
    id: str
    name: str
    token: str
    iat: int
    isGuest: str


# legacy for when substrate was used, might need it back to support that again
# class Keypair:
#    public_key: str
#    private_key: str


async def authenticate_guest(base_url: str, *, cache=False) -> Auth:
    """
    Authenticate to the server as a guest account.

    Guest accounts are temporary and will be removed when not used anymore.
    """
    cached_auth = await _read_cache() if cache else None
    if cached_auth and not _expired(cached_auth):
        logger.debug("Using cached auth %s (%s)", cached_auth["id"], cached_auth["name"])
        return cached_auth
    else:
        auth = await _get_guest_auth(base_url)
        logger.debug("Authenticated %s (%s)", auth["id"], auth["name"])
        if cache:
            await _write_cache(auth)
        return auth


async def authenticate_web3(base_url: str, account: LocalAccount) -> Auth:
    """
    Authenticate with an etherium account.
    """
    try:
        challenge = await _get_challenge(base_url, account)
        token = await _get_token(base_url, account, challenge)
        jwt = json.loads(_base64url_decode(token.split(".")[1]))
        return {
            "id": jwt["sub"],
            "iat": jwt["iat"],
            "name": "",  # TODO
            "token": token,
            "isGuest": "false",
        }
    except httpx.HTTPStatusError as e:
        logger.error(e.request)
        logger.error(e.response.json())
        raise


def web3_account(private_key: str) -> LocalAccount:
    """
    Create an ethereum account from a private key.
    """
    if " " in private_key:
        return Account.from_mnemonic(private_key)
    return Account.from_key(private_key)


async def _get_guest_auth(base_url):
    async with httpx.AsyncClient(http2=True) as client:
        url = auth_guest_url(base_url)
        name = "guest_" + _name_suffix()
        http_response = await client.post(url, json={"name": name})
        http_response.raise_for_status()
        response = http_response.json()
        response["iat"] = int(time.time())
        return response


async def _get_challenge(base_url: str, account: LocalAccount) -> str:
    async with httpx.AsyncClient(http2=True) as client:
        url = auth_challenge_url(base_url)
        http_response = await client.get(url, params={"wallet": account.address})
        http_response.raise_for_status()
        response = http_response.json()
        return response["challenge"]


async def _get_token(base_url, account: LocalAccount, challenge):
    # sig = key_pair.sign(challenge)
    # pubkey = key_pair.public_key
    url = auth_token_url(base_url)
    msg = encode_defunct(text=challenge)
    signed_msg = account.sign_message(msg)
    sig = signed_msg.signature
    pubkey = account.address
    async with httpx.AsyncClient(http2=True) as client:
        post_data = {
            "wallet": pubkey,
            "signedChallenge": sig.hex(),
            "network": "ethereum",
        }
        http_response = await client.post(url, json=post_data)
        http_response.raise_for_status()

        response = http_response.json()
        return response["token"]


async def _read_cache():
    try:
        tmp_file = pathlib.PurePath(tempfile.gettempdir(), _TMP_AUTH)
        async with await anyio.open_file(tmp_file, encoding="utf-8") as f:
            cached_auth = json.loads(await f.read())
            return cached_auth
    except FileNotFoundError as e:
        logger.debug("Cache file not found %s", e)
        return None


async def _write_cache(auth):
    tmp_file = pathlib.PurePath(tempfile.gettempdir(), _TMP_AUTH)
    async with await anyio.open_file(tmp_file, "w", encoding="utf-8") as f:
        await f.write(json.dumps(auth, indent=2))


def _expired(auth: Auth):
    exp = _15_MIN if auth["isGuest"] else _ONE_DAY
    now = int(time.time())
    return (now - auth["iat"]) > exp


def _name_suffix():
    return "".join(random.sample(string.ascii_lowercase + string.digits, 7))


def _base64url_decode(s: str) -> bytes:
    rem = len(s) % 4
    if (len(s) % 4) > 0:
        padded = s + "=" * (4 - rem)
    else:
        padded = s

    return base64.urlsafe_b64decode(padded)
