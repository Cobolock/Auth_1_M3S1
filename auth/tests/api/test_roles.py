from http import HTTPStatus
from unittest.mock import ANY

from httpx import AsyncClient
from pytest_unordered import unordered
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models.role import Role


async def test_create_role(test_client: AsyncClient, session: AsyncSession) -> None:
    # Arrange
    role_data = {"id": "moderator", "name": "Модератор"}

    # Act
    response = await test_client.post("/api/v1/roles", json=role_data)

    # Assert
    assert response.status_code == HTTPStatus.CREATED
    body = response.json()
    assert body["id"] == role_data["id"]
    assert body["name"] == role_data["name"]

    role = await session.get(Role, role_data["id"])
    assert role is not None
    assert role.name == role_data["name"]


async def test_get_role(test_client: AsyncClient, role_in_db: Role) -> None:
    # Act
    response = await test_client.get(f"/api/v1/roles/{role_in_db.id}")

    # Assert
    assert response.status_code == HTTPStatus.OK
    body = response.json()
    assert body["id"] == str(role_in_db.id)
    assert body["name"] == role_in_db.name


async def test_get_nonexistent_role(test_client: AsyncClient) -> None:
    # Act
    response = await test_client.get("/api/v1/roles/nonexistent")

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Role not found"}


async def test_get_all_roles(
    test_client: AsyncClient, roles_in_db: list[Role], admin_role_in_db: Role
) -> None:
    # Act
    response = await test_client.get("/api/v1/roles")

    # Assert
    assert response.status_code == HTTPStatus.OK
    body = response.json()

    assert body == unordered(
        [
            {
                "id": str(admin_role_in_db.id),
                "name": admin_role_in_db.name,
                "updated_at": ANY,
                "created_at": ANY,
                "permissions": [
                    {
                        "id": str(permission.id),
                        "name": permission.name,
                        "description": permission.description,
                        "resource": "all",
                    }
                    for permission in admin_role_in_db.permissions
                ],
            }
        ]
        + [
            {
                "id": str(role.id),
                "name": role.name,
                "updated_at": ANY,
                "created_at": ANY,
                "permissions": [],
            }
            for role in roles_in_db
        ]
    )


async def test_update_role(test_client: AsyncClient, role_in_db: Role) -> None:
    # Arrange
    new_role_data = {"name": "Карбюратор"}

    # Act
    response = await test_client.patch(f"/api/v1/roles/{role_in_db.id}", json=new_role_data)

    # Assert
    assert response.status_code == HTTPStatus.OK
    body = response.json()
    assert body["id"] == str(role_in_db.id)
    assert body["name"] == new_role_data["name"]

    assert role_in_db.name == new_role_data["name"]


async def test_delete_role(test_client: AsyncClient, role_in_db: Role) -> None:
    # Act
    response = await test_client.delete(f"/api/v1/roles/{role_in_db.id}")

    # Assert
    assert response.status_code == HTTPStatus.NO_CONTENT

    # Act
    response = await test_client.delete(f"/api/v1/roles/{role_in_db.id}")

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Role not found"}
