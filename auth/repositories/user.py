from typing import Annotated

from dataclasses import dataclass

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from auth.core.exceptions import ObjectAlreadyExistsError, ObjectNotFoundError
from auth.db.postgres import get_session
from auth.models.user import User


@dataclass
class UserRepository:
    _session: Annotated[AsyncSession, Depends(get_session)]

    async def add(self, user: User) -> User:
        self._session.add(user)
        try:
            await self._session.commit()
        except IntegrityError:
            raise ObjectAlreadyExistsError(User) from None
        return user

    async def get_by_username_or_none(
        self, username: str, *, with_roles: bool = False
    ) -> User | None:
        query = select(User).where(User.username == username)
        if with_roles:
            query = query.options(selectinload(User.roles))
        return (await self._session.execute(query)).scalar_one_or_none()

    async def get_by_username(self, username: str, *, with_roles: bool = False) -> User:
        if user := await self.get_by_username_or_none(username, with_roles=with_roles):
            return user
        raise ObjectNotFoundError(User)

    async def update(self, user: User) -> User:
        await self._session.merge(user)
        await self._session.commit()
        return user
