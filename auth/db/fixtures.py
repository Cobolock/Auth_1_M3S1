from contextlib import asynccontextmanager, suppress

from sqlalchemy.exc import IntegrityError

from auth.db.postgres import get_session
from auth.models.role import Role


async def create_roles() -> None:
    """Создаёт базовые роли."""
    async with asynccontextmanager(get_session)() as session:
        admin_role = Role(id="admin", name="Администратор")
        session.add(admin_role)
        with suppress(IntegrityError):
            await session.commit()
