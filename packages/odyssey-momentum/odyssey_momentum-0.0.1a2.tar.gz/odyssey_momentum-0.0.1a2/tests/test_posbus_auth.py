import pytest
from eth_account import Account
from pytest_httpx import HTTPXMock

from odyssey_momentum import posbus


@pytest.mark.asyncio
async def test_authenticate_guest(httpx_mock: HTTPXMock, guest):
    httpx_mock.add_response(url="http://example.com/api/v4/auth/guest-token", json=guest)
    response = await posbus.authenticate_guest("http://example.com", cache=False)
    assert response["isGuest"]


@pytest.mark.asyncio
async def test_authenticate_web3(httpx_mock, web3_account, web3_challenge, web3_token):
    httpx_mock.add_response(
        url="http://example.com/api/v4/auth/challenge?wallet=0x5ce9454909639D2D17A3F753ce7d93fa0b9aB12E",
        json=web3_challenge,
    )
    httpx_mock.add_response(url="http://example.com/api/v4/auth/token", method="POST", json=web3_token)
    response = await posbus.authenticate_web3("http://example.com", web3_account)
    assert response["isGuest"] == "false"


@pytest.fixture
def guest():
    return {
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


@pytest.fixture
def web3_account():
    return Account.from_key("0xb25c7db31feed9122727bf0939dc769a96564b2de4c4726d035b36ecf1e5b364")


@pytest.fixture
def web3_challenge():
    return {
        "challenge": "Please sign this message with the private key for address "
        "0x5ce9454909639D2D17A3F753ce7d93fa0b9aB12E to prove that you own it. 0189275b-b390-7f1c-b886-13406f814037"
    }


@pytest.fixture
def web3_token():
    return {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
        ".eyJleHAiOjE2ODkxODcyNzUsImlhdCI6MTY4ODU4MjQ3NSwiaXNzIjoidWJlcmNvbnRyb2xsZXIiLCJzdWIiOiIwMTg5Mjc1Yi1jZTkwLTdmMWMtYjAwMi0zYjZlNjM3NTRkNjkifQ"
        ".Wy10ZaCKvrSWosGbzt_eK7jcUq3Jf2qJhY60797dXVU"
    }
