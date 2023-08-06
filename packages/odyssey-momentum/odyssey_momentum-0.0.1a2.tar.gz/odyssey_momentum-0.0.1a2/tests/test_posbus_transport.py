import logging

import httpx
import pytest
import pytest_asyncio
from httpx_ws.transport import ASGIWebSocketAsyncNetworkStream
from odyssey_posbus_client import posbus as pbc  # type: ignore

from odyssey_momentum import posbus

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_connect(websocket_mock, auth):
    url = "http://example.com"
    async with posbus.connect(url, auth) as (send, stream):
        msg_type1, msg1 = await anext(stream)
        assert msg_type1 == posbus.MsgType.TypeSignal
        await send(posbus.teleport_request("00000000-0000-8000-8000-000000000002"))
        msg_type2, msg2 = await anext(stream)
        assert msg_type2 == posbus.MsgType.TypeSignal


@pytest_asyncio.fixture
async def websocket_mock(httpx_mock):
    stream = ASGIWebSocketAsyncNetworkStream(app, {})

    async def mock_response(request: httpx.Request):
        await stream.__aenter__()
        return httpx.Response(101, extensions={"network_stream": stream})

    httpx_mock.add_callback(mock_response)
    yield httpx_mock
    await stream.__aexit__()


async def app(scope, receive, send):
    """ASGI app mocking the websocket backend."""
    while True:
        event = await receive()
        match event["type"]:
            case "websocket.connect":
                await send({"type": "websocket.accept"})
            case "websocket.close":
                logger.debug("close")
                return
            case "websocket.receive":
                msg_type, msg = posbus.decode(event["bytes"])
                match msg_type:
                    case posbus.MsgType.TypeHandShake:
                        sig = pbc.Signal()
                        sig.value = pbc.SignalConnected
                        await send({"type": "websocket.send", "bytes": posbus.encode(sig)})
                    case posbus.MsgType.TypeTeleportRequest:
                        sig = pbc.Signal()
                        sig.value = pbc.SignalWorldDoesNotExist
                        await send({"type": "websocket.send", "bytes": posbus.encode(sig)})
                    case _:
                        logger.debug(msg_type)
            case _:
                logger.debug(event)


@pytest.fixture
def auth() -> posbus.auth.Auth:
    return {
        "id": "0189274b-f068-7f1c-aac0-f8817cea29c9",
        "name": "Graham Chapman",
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
        ".eyJleHAiOjE2ODkxODcyNzUsImlhdCI6MTY4ODU4MjQ3NSwiaXNzIjoidWJlcmNvbnRyb2xsZXIiLCJzdWIiOiIwMTg5Mjc1Yi1jZTkwLTdmMWMtYjAwMi0zYjZlNjM3NTRkNjkifQ"
        ".Wy10ZaCKvrSWosGbzt_eK7jcUq3Jf2qJhY60797dXVU",
        "iat": 1688582475,
        "isGuest": "false",
    }
