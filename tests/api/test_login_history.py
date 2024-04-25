from datetime import UTC, datetime
from http import HTTPStatus
from ipaddress import ip_address
from random import choice, randint
from string import ascii_lowercase

from httpx import AsyncClient


async def test_create_and_get_entries(test_client: AsyncClient) -> None:
    num = 3

    # Act
    response = await test_client.post(
        "/api/v1/user", json={"username": "user", "password": "password"}
    )

    # Assert
    assert response.status_code == HTTPStatus.CREATED

    user = response.json()

    # Arrange
    for _ in range(num):
        role_data = {
            "created": datetime.now(tz=UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "ip_address": str(ip_address(randint(1, 0xFFFFFFFF))),  # noqa: S311
            "location": "".join(choice(ascii_lowercase) for _ in range(randint(6, 16))),  # noqa: S311
            "user_agent": "".join(choice(ascii_lowercase) for _ in range(randint(6, 16))),  # noqa: S311
            "user_id": user["id"],
        }

        response = await test_client.post("/api/v1/user/entry?username=user", json=role_data)

        assert response.status_code == HTTPStatus.CREATED

    # Act
    response = await test_client.get("/api/v1/user/entries?username=user")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == num
