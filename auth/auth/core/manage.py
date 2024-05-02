from asyncio import run as aiorun

import typer

from async_fastapi_jwt_auth.auth_jwt import AuthJWTBearer

from auth.db.postgres import get_session as aget_asession
from auth.db.redis import get_redis
from auth.repositories.entry import EntryRepository
from auth.repositories.permission import PermissionRepository
from auth.repositories.role import RoleRepository
from auth.repositories.user import UserRepository
from auth.schemas.user import UserCreate
from auth.services.jwt import JWTService
from auth.services.role import RoleService
from auth.services.user import UserService

app = typer.Typer()


async def _run(username: str, password: str):
    _session = await anext(aget_asession())
    _cache = await get_redis()
    _jwt = AuthJWTBearer()

    permission_repo = PermissionRepository(_session)
    role_repo = RoleRepository(_session)
    user_repo = UserRepository(_session)
    entry_repo = EntryRepository(_session)
    jwt_service = JWTService(_jwt)

    role_service = RoleService(_role_repo=role_repo, _permission_repo=permission_repo)
    user_service = UserService(
        user_repo=user_repo,
        role_repo=role_repo,
        entry_repo=entry_repo,
        cache_session=_cache,
        jwt_service=jwt_service,
    )

    admin_role = await role_service.get_role_by_id("admin")

    user_data = UserCreate(username=username, password=password)

    await user_service.create_user(user_data)

    await user_service.add_role(username, admin_role.id)


def main(username: str, password: str):
    aiorun(_run(username=username, password=password))


if __name__ == "__main__":
    typer.run(main)
