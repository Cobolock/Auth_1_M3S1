from http import HTTPStatus

import pytest

from httpx import AsyncClient
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models.user import User


async def test_create_new_user(test_client: AsyncClient, session: AsyncSession) -> None:
    # Arrange
    user_data = {
        "username": "user",
        "password": "password",
        "first_name": "John",
        "last_name": "Doe",
    }

    # Act
    response = await test_client.post("/api/v1/user", json=user_data)
    body = response.json()
    assert body["username"] == user_data["username"]
    assert body["first_name"] == user_data["first_name"]
    assert body["last_name"] == user_data["last_name"]

    # Assert
    assert response.status_code == HTTPStatus.CREATED

    user = await session.get(User, body["id"])
    assert user is not None
    assert user.first_name == user_data["first_name"]
    assert user.last_name == user_data["last_name"]


@pytest.mark.usefixtures("user_in_db")
async def test_create_new_user_already_exists(test_client: AsyncClient) -> None:
    # Arrange
    user_data = {"username": "user", "password": "password"}

    # Act
    response = await test_client.post("/api/v1/user", json=user_data)

    # Assert
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Username in use"}


async def test_user_login(test_client: AsyncClient, user_in_db: User, redis_client: Redis) -> None:
    # Act
    response = await test_client.post(
        "/api/v1/user/login", json={"username": user_in_db.username, "password": "password"}
    )

    # Assert
    assert response.status_code == HTTPStatus.OK
    body = response.json()
    assert body.get("access_token") is not None
    assert body.get("refresh_token") is not None

    assert await redis_client.smembers(f"user:{user_in_db.username}") == {
        body["refresh_token"].encode("utf-8")
    }


async def test_user_logout(test_client: AsyncClient, user_in_db: User, redis_client: Redis) -> None:
    # Act
    response = await test_client.post(
        "/api/v1/user/login", json={"username": user_in_db.username, "password": "password"}
    )
    # Assert
    assert response.status_code == HTTPStatus.OK

    # Act
    refresh_token = response.json()["refresh_token"]
    response = await test_client.post("/api/v1/user/logout", json={"refresh_token": refresh_token})

    # Assert
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert await redis_client.smembers(f"user:{user_in_db.username}") == set()


async def test_user_refresh(
    test_client: AsyncClient, user_in_db: User, redis_client: Redis
) -> None:
    # Act
    response = await test_client.post(
        "/api/v1/user/login", json={"username": user_in_db.username, "password": "password"}
    )

    # Assert
    assert response.status_code == HTTPStatus.OK

    # Act
    refresh_token = response.json()["refresh_token"]
    response = await test_client.post("/api/v1/user/refresh", json={"refresh_token": refresh_token})

    # Assert
    assert response.status_code == HTTPStatus.OK
    body = response.json()
    assert body.get("access_token") is not None
    assert body.get("refresh_token") is not None

    assert await redis_client.smembers(f"user:{user_in_db.username}") == {
        body["refresh_token"].encode("utf-8")
    }
