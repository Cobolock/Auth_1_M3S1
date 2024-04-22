from typing import Annotated

from dataclasses import dataclass

from fastapi import Depends
from redis.asyncio import Redis

from auth.core.exceptions import BadRefreshTokenError, NotAuthorizedError, ObjectAlreadyExistsError
from auth.db.redis import get_redis
from auth.models.user import User
from auth.repositories.role import RoleRepository
from auth.repositories.user import UserRepository
from auth.schemas.user import Credentials
from auth.services.jwt import JWTPair, JWTService


@dataclass
class UserService:
    user_repo: Annotated[UserRepository, Depends()]
    role_repo: Annotated[RoleRepository, Depends()]
    cache_session: Annotated[Redis, Depends(get_redis)]
    jwt_service: Annotated[JWTService, Depends()]

    async def create_user(self, creds: Credentials) -> bool:
        new_user = User(creds.username, creds.password)
        try:
            await self.user_repo.add(new_user)
        except ObjectAlreadyExistsError:
            return False
        return True

    async def check_creds(self, creds: Credentials) -> bool:
        if user := await self.user_repo.get_by_username_or_none(creds.username):
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

    async def add_role(self, username: str, role_id: str) -> User:
        user = await self.user_repo.get_by_username(username, with_roles=True)
        role = await self.role_repo.get(role_id)
        user.roles.add(role)
        return await self.user_repo.update(user)

    async def remove_role(self, username: str, role_id: str) -> User:
        user = await self.user_repo.get_by_username(username, with_roles=True)
        role = await self.role_repo.get(role_id)
        if role in user.roles:
            user.roles.remove(role)
        return await self.user_repo.update(user)
