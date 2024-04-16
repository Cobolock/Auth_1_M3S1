from typing import Annotated

from dataclasses import dataclass

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from auth.core.exceptions import ObjectAlreadyExistsError, ObjectNotFoundError
from auth.db.postgres import get_session
from auth.models.role import Role


@dataclass
class RoleRepository:
    _session: Annotated[AsyncSession, Depends(get_session)]

    async def add(self, role: Role) -> Role:
        self._session.add(role)
        try:
            await self._session.commit()
        except IntegrityError:
            raise ObjectAlreadyExistsError(Role) from None
        return role

    async def get_or_none(self, role_id: str) -> Role | None:
        return await self._session.get(Role, role_id)

    async def get(self, role_id: str) -> Role:
        if role := await self.get_or_none(role_id):
            return role
        raise ObjectNotFoundError(Role)

    async def get_all(self) -> list[Role]:
        return list(await self._session.scalars(select(Role)))

    async def update(self, role: Role) -> None:
        await self._session.merge(role)
        await self._session.commit()

    async def delete(self, role: Role) -> None:
        await self._session.delete(role)
        await self._session.commit()
