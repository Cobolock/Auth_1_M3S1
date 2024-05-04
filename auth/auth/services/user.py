from typing import Annotated

from dataclasses import dataclass

from fastapi import Depends
from opentelemetry import trace
from redis.asyncio import Redis
from werkzeug.security import check_password_hash

from auth.core.config import extra_config
from auth.core.exceptions import (
    BadRefreshTokenError,
    NotAuthorizedError,
    ObjectAlreadyExistsError,
    ObjectNotFoundError,
    UsernameInUseError,
)
from auth.db.redis import get_redis
from auth.models.entry import Entry as EntryModel
from auth.models.user import User
from auth.repositories.entry import EntryRepository
from auth.repositories.role import RoleRepository
from auth.repositories.user import UserRepository
from auth.schemas.user import EntrySchema, UserCreate
from auth.schemas.user_auth import UserCredentials
from auth.services.jwt import JWTPair, JWTService

tracer = trace.get_tracer(__name__)


@dataclass
class UserService:
    user_repo: Annotated[UserRepository, Depends()]
    role_repo: Annotated[RoleRepository, Depends()]
    entry_repo: Annotated[EntryRepository, Depends()]
    cache_session: Annotated[Redis, Depends(get_redis)]
    jwt_service: Annotated[JWTService, Depends()]

    @tracer.start_as_current_span("create_user")
    async def create_user(self, user_data: UserCreate) -> User:
        current_span = trace.get_current_span()
        current_span.set_attribute("username", user_data.username)
        new_user = User(
            user_data.username, user_data.password, user_data.first_name, user_data.last_name
        )
        try:
            return await self.user_repo.add(new_user)
        except ObjectAlreadyExistsError:
            raise UsernameInUseError from None

    @tracer.start_as_current_span("change_auth")
    async def change_auth(self, username: str, creds: UserCredentials) -> None:
        current_span = trace.get_current_span()
        current_span.set_attribute("username", username)
        if user := await self.user_repo.get_by_username_or_none(username):
            if creds.username != "":
                user.username = creds.username
            if creds.password != "":
                user.password = user.make_password(creds.password)
            await self.user_repo.update(user)
            await self._revoke_all_tokens(username)

    @tracer.start_as_current_span("refresh")
    async def refresh(self, refresh_token) -> JWTPair:
        username = await self.jwt_service.get_sub(refresh_token)
        current_span = trace.get_current_span()
        current_span.set_attribute("username", username)
        if await self._revoke_token(username, refresh_token):
            jwt = await self.jwt_service.generate(subject=username)
            await self._cache_token(username, jwt.RT)
        else:
            raise BadRefreshTokenError
        return jwt

    @tracer.start_as_current_span("login")
    async def login(self, creds: UserCredentials) -> JWTPair:
        current_span = trace.get_current_span()
        current_span.set_attribute("username", creds.username)
        await self._check_creds(creds)
        jwt = await self.jwt_service.generate(subject=creds.username)
        await self._cache_token(creds.username, jwt.RT)
        return jwt

    @tracer.start_as_current_span("logout")
    async def logout(self, refresh_token: str) -> bool:
        if username := await self.jwt_service.get_sub(refresh_token):
            current_span = trace.get_current_span()
            current_span.set_attribute("username", username)
            return await self._revoke_token(username, refresh_token)
        raise ObjectNotFoundError(User) from None

    @tracer.start_as_current_span("add_role")
    async def add_role(self, username: str, role_id: str) -> User:
        current_span = trace.get_current_span()
        current_span.set_attribute("username", username)
        user = await self.user_repo.get_by_username(username, with_roles=True)
        role = await self.role_repo.get(role_id)
        user.roles.add(role)
        return await self.user_repo.update(user)

    @tracer.start_as_current_span("remove_role")
    async def remove_role(self, username: str, role_id: str) -> User:
        current_span = trace.get_current_span()
        current_span.set_attribute("username", username)
        user = await self.user_repo.get_by_username(username, with_roles=True)
        role = await self.role_repo.get(role_id)
        if role in user.roles:
            user.roles.remove(role)
        return await self.user_repo.update(user)

    @tracer.start_as_current_span("add_login_entry")
    async def add_login_entry(self, username: str, entry: EntrySchema) -> None:
        current_span = trace.get_current_span()
        current_span.set_attribute("username", username)
        user = await self.user_repo.get_by_username(username)
        entry.user_id = user.id
        new_entry = EntryModel(**entry.model_dump())
        await self.entry_repo.add(new_entry)

    @tracer.start_as_current_span("add_login_entry")
    async def get_entries(self, username: str) -> list[EntryModel]:
        current_span = trace.get_current_span()
        current_span.set_attribute("username", username)
        user = await self.user_repo.get_by_username(username)
        return await self.entry_repo.get_last_10(user.id)

    async def _check_creds(self, creds: UserCredentials) -> None:
        user = await self.user_repo.get_by_username_or_none(creds.username)
        if not user:
            raise NotAuthorizedError
        if not check_password_hash(user.password, creds.password + extra_config.salt):
            raise NotAuthorizedError

    async def _revoke_token(self, username, refresh_token) -> bool:
        if await self.cache_session.sismember(f"user:{username}", refresh_token):
            await self.cache_session.srem(f"user:{username}", refresh_token)
        else:
            raise BadRefreshTokenError
        return True

    async def _revoke_all_tokens(self, username) -> None:
        await self.cache_session.delete(f"user:{username}")

    async def _cache_token(self, username, token) -> None:
        await self.cache_session.sadd(f"user:{username}", token)
