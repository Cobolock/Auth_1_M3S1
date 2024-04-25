from datetime import datetime
from ipaddress import ip_address
from random import choice, randint
from string import ascii_lowercase
from httpx import AsyncClient
from pytest_unordered import unordered
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models.role import Role
from tests.fixtures.db_entities import user_in_db

from auth.models.user import User

async def test_create_entry(test_client: AsyncClient, session: AsyncSession) -> None:
    # Act
    response = await test_client.post(
        "/api/v1/user", json={"username": "user", "password": "password"}
    )

    # Assert
    assert response.status_code == 201

    user = response.json()

    # Arrange
    role_data = {
        "created": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "ip_address": str(ip_address(randint(1, 0xffffffff))),
        "location": "".join(choice(ascii_lowercase) for _ in range(randint(6, 16))),
        "user_agent": "".join(choice(ascii_lowercase) for _ in range(randint(6, 16))),
        "user_id": user["id"]
    }

    # Act
    response = await test_client.post("/api/v1/user/entry", json=role_data)

    # Assert
    assert response.status_code == 201

async def test_get_entries(test_client: AsyncClient, session: AsyncSession) -> None:
    # Act
    response = await test_client.get(f"/api/v1/user/entries?username=user")

    # Assert
    assert response.status_code == 200
    assert len(response) == 1
