from typing import Annotated

from dataclasses import dataclass

from fastapi import Depends
from redis.asyncio import Redis

from auth.core.exceptions import ObjectAlreadyExistsError
from auth.db.redis import get_redis
from auth.models.user import User
from auth.repositories.role import RoleRepository
from auth.repositories.user import UserRepository
from auth.schemas.user import Credentials


@dataclass
class UserService:
    user_repo: Annotated[UserRepository, Depends()]
    role_repo: Annotated[RoleRepository, Depends()]
    cache_session: Annotated[Redis, Depends(get_redis)]

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
