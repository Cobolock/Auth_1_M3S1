from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models.role import Role
from auth.models.user import User


async def test_add_role_to_user(
    test_client: AsyncClient, session: AsyncSession, role_in_db: Role, user_in_db: User
) -> None:
    # Act
    response = await test_client.put(f"/api/v1/users/{user_in_db.username}/roles/{role_in_db.id}")

    # Assert
    assert response.status_code == 204

    await session.refresh(user_in_db, ["roles"])
    assert role_in_db in user_in_db.roles


async def test_remove_role_from_user(
    test_client: AsyncClient, session: AsyncSession, role_in_db: Role, user_in_db: User
) -> None:
    # Arrange
    await session.refresh(user_in_db, ["roles"])
    user_in_db.roles.add(role_in_db)
    await session.commit()

    # Act
    response = await test_client.delete(
        f"/api/v1/users/{user_in_db.username}/roles/{role_in_db.id}"
    )

    # Assert
    assert response.status_code == 204

    await session.refresh(user_in_db, ["roles"])
    assert role_in_db not in user_in_db.roles
