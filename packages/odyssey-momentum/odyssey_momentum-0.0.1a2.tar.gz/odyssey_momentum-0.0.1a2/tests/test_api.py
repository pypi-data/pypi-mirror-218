import pytest

from odyssey_momentum import api


@pytest.fixture
def user():
    return {
        "id": "0187e1be-70fa-7fc5-ba9f-cabe3126ecb1",
        "userTypeId": "00000000-0000-0000-0000-000000000006",
        "name": "me",
        "wallet": "0x32cdd7EBF43B773472333B255521Df472b5B9638",
        "profile": {"avatarHash": "92f8f94a67c1ee05df8562beab611c85"},
        "createdAt": "2023-05-03T13:12:47Z",
        "updatedAt": "2023-05-05T11:52:04Z",
        "isGuest": False,
    }


@pytest.mark.asyncio
async def test_current_user(httpx_mock, user):
    # yeah, not testing much here. But it's a start :p
    httpx_mock.add_response(url="http://example.com/api/v4/users/me", method="GET", json=user)

    client = api.API("http://example.com", "dummy.token")
    response = await client.current_user()
    assert response.id == user["id"]
