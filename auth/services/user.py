from typing import Annotated

from dataclasses import dataclass

from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.exceptions import JWTDecodeError
from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from auth.core.exceptions import BadRefreshTokenError, NotAuthorizedError
from auth.db.postgres import get_session as pg_get_session
from auth.db.redis import get_redis
from auth.models.user import User
from auth.schemas.user import Credentials
from auth.services.jwt import JWTPair, get_jwt


@dataclass
class UserService:
    db_session: Annotated[AsyncSession, Depends(pg_get_session)]
    cache_session: Annotated[Redis, Depends(get_redis)]
    jwt_service: Annotated[AuthJWT, Depends(get_jwt)]

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

    async def refresh(self, refresh_token) -> JWTPair:
        try:
            payload = await JWTPair.get_payload(refresh_token)
        except JWTDecodeError:
            raise BadRefreshTokenError from None

        username = payload["sub"]
        return await JWTPair.generate(subject=username)

    async def login(self, creds: Credentials) -> JWTPair:
        if await self.check_creds(creds):
            return await JWTPair.generate(subject=creds.username)
        raise NotAuthorizedError from None
