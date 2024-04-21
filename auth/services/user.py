from typing import Annotated

from dataclasses import dataclass

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
from auth.services.jwt import JWTPair, JWTService


@dataclass
class UserService:
    db_session: Annotated[AsyncSession, Depends(pg_get_session)]
    cache_session: Annotated[Redis, Depends(get_redis)]
    jwt_service: Annotated[JWTService, Depends()]

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
        username = await self.jwt_service.get_sub(refresh_token)
        if await self.revoke_token(username, refresh_token):
            jwt = await self.jwt_service.generate(subject=username)
            await self.cache_token(username, jwt.RT)
        else:
            raise BadRefreshTokenError
        return jwt

    async def login(self, creds: Credentials) -> JWTPair:
        if await self.check_creds(creds):
            jwt = await self.jwt_service.generate(subject=creds.username)
            await self.cache_token(creds.username, jwt.RT)
            return jwt
        raise NotAuthorizedError from None

    async def revoke_token(self, username, refresh_token) -> bool:
        if await self.cache_session.sismember(f"user:{username}", refresh_token):
            await self.cache_session.srem(f"user:{username}", refresh_token)
        else:
            return False
        return True

    async def cache_token(self, username, token) -> None:
        await self.cache_session.sadd(f"user:{username}", token)
