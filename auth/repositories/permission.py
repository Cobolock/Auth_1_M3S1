from typing import Annotated

from dataclasses import dataclass

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from auth.core.exceptions import ObjectAlreadyExistsError, ObjectNotFoundError
from auth.db.postgres import get_session
from auth.models.permission import Permission


@dataclass
class PermissionRepository:
    _session: Annotated[AsyncSession, Depends(get_session)]

    async def add(self, permission: Permission) -> Permission:
        self._session.add(permission)
        try:
            await self._session.commit()
        except IntegrityError:
            raise ObjectAlreadyExistsError(Permission) from None
        return permission

    async def get_or_none(self, permission_id: str) -> Permission | None:
        return await self._session.get(Permission, permission_id)

    async def get(self, permission_id: str) -> Permission:
        if permission := await self.get_or_none(permission_id):
            return permission
        raise ObjectNotFoundError(Permission)

    async def get_all(self) -> list[Permission]:
        return list(await self._session.scalars(select(Permission)))

    async def update(self, permission: Permission) -> Permission:
        await self._session.merge(permission)
        await self._session.commit()
        return permission

    async def delete(self, permission: Permission) -> None:
        await self._session.delete(permission)
        await self._session.commit()
