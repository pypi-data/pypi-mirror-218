import math

import pytest
from pytest import approx
from pytest_httpx import HTTPXMock

from odyssey_momentum import bot
from odyssey_momentum.bot import coords


@pytest.mark.asyncio
async def test_bot(guest_account):
    url = "http://example.com"
    async with bot.Bot(url) as b:
        await b.authenticate_guest(cache=False)


def test_look_at():
    s = coords.Position(0, 0, 0)
    t = (1, 0, 1)
    result = coords.look_at(s, t)
    assert math.degrees(result.y) == approx(45)


@pytest.fixture
def guest_account(httpx_mock: HTTPXMock):
    guest = {
        "id": "0189274b-f068-7f1c-aac0-f8817cea29c9",
        "userTypeId": "76802331-37b3-44fa-9010-35008b0cbaec",
        "name": "Visitor_5128915",
        "profile": {},
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
        ".eyJleHAiOjE2ODkxODYyMzUsImlhdCI6MTY4ODU4MTQzNSwiaXNzIjoidWJlcmNvbnRyb2xsZXIiLCJzdWIiOiIwMTg5Mjc0Yi1mMDY4LTdmMWMtYWFjMC1mODgxN2NlYTI5YzkifQ"
        ".m2kMKeK4ALSjOScfxxqS-twOE2sdHv8es2KfyudsKNI",
        "createdAt": "0001-01-01T00:00:00Z",
        "updatedAt": "0001-01-01T00:00:00Z",
        "isGuest": True,
    }
    httpx_mock.add_response(url="http://example.com/api/v4/auth/guest-token", json=guest)
    return guest
