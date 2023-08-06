import pytest

from odyssey_momentum import posbus


def test_encode(auth):
    msg = posbus.handshake(auth)
    encoded = posbus.encode(msg)
    # handshake has random session ID, so test:
    msg_type, result = posbus.decode(encoded)
    assert msg_type == posbus.MsgType.TypeHandShake
    assert result.keys() == {"handshake_version", "protocol_version", "token", "user_id", "session_id"}
    assert result["user_id"] == auth["id"]


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
