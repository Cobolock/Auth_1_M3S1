from typing import Annotated

from dataclasses import dataclass

from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from auth.db.postgres import get_session as pg_get_session
from auth.db.redis import get_redis
from auth.models.user import User
from auth.schemas.user import Credentials


@dataclass
class UserService:
    db_session: Annotated[AsyncSession, Depends(pg_get_session)]
    cache_session: Annotated[Redis, Depends(get_redis)]

    async def create(self, creds: Credentials) -> bool:
        new_user = User(creds.username, creds.password)
        self.db_session.add(new_user)
        try:
            await self.db_session.commit()
        except IntegrityError:
            return False
        except:
            raise
        return True

    async def get(self, username: str) -> User | None:
        query = select(User).where(User.username == username)
        if user_rows := await self.db_session.execute(query):
            return user_rows.scalar()
        return None

    async def check_creds(self, creds: Credentials) -> bool:
        if user := await self.get(creds.username):
            return user.check_password(creds.password)
        return False
