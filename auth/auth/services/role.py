from typing import Annotated

from dataclasses import dataclass

from fastapi import Depends
from opentelemetry import trace

from auth.core.exceptions import RoleDeletionProhibitedError
from auth.models.role import Role
from auth.repositories.permission import PermissionRepository
from auth.repositories.role import RoleRepository
from auth.schemas.role import RoleCreate, RoleUpdate

tracer = trace.get_tracer(__name__)


@dataclass
class RoleService:
    _role_repo: Annotated[RoleRepository, Depends()]
    _permission_repo: Annotated[PermissionRepository, Depends()]

    @tracer.start_as_current_span("create_role")
    async def create_role(self, role_data: RoleCreate) -> Role:
        current_span = trace.get_current_span()
        current_span.set_attribute("role_id", role_data.id)
        perms = [
            await self._permission_repo.get(permission_id=perm.id) for perm in role_data.permissions
        ]
        role = Role(**role_data.model_dump())
        role.permissions = perms
        return await self._role_repo.add(role)

    @tracer.start_as_current_span("get_role_by_id")
    async def get_role_by_id(self, role_id: str) -> Role:
        current_span = trace.get_current_span()
        current_span.set_attribute("role_id", role_id)
        return await self._role_repo.get(role_id)

    @tracer.start_as_current_span("get_all_roles")
    async def get_all_roles(self) -> list[Role]:
        return await self._role_repo.get_all()

    @tracer.start_as_current_span("update_role_by_id")
    async def update_role_by_id(self, role_id: str, role_data: RoleUpdate) -> Role:
        current_span = trace.get_current_span()
        current_span.set_attribute("role_id", role_id)
        role = await self._role_repo.get(role_id)
        if role_data.name is not None:
            role.name = role_data.name
        if role_data.permissions is not None:
            perms = [
                await self._permission_repo.get(permission_id=perm.id)
                for perm in role_data.permissions
            ]
            role.permissions = perms
        return await self._role_repo.update(role)

    @tracer.start_as_current_span("delete_role_by_id")
    async def delete_role_by_id(self, role_id: str) -> None:
        current_span = trace.get_current_span()
        current_span.set_attribute("role_id", role_id)
        role = await self._role_repo.get(role_id)
        self._check_role_allowed_to_delete(role)
        await self._role_repo.delete(role)

    @staticmethod
    def _check_role_allowed_to_delete(role: Role) -> None:
        if role.id == "admin":
            raise RoleDeletionProhibitedError
