from typing import Annotated

from dataclasses import dataclass

from fastapi import Depends
from opentelemetry import trace

from auth.models.permission import Permission
from auth.repositories.permission import PermissionRepository
from auth.schemas.permission import PermissionCreate

tracer = trace.get_tracer(__name__)


@dataclass
class PermissionService:
    _permission_repo: Annotated[PermissionRepository, Depends()]

    @tracer.start_as_current_span("create_permission")
    async def create_permission(self, permission_data: PermissionCreate) -> Permission:
        current_span = trace.get_current_span()
        current_span.set_attribute("permission_name", permission_data.name)
        permission = Permission(**permission_data.model_dump())
        return await self._permission_repo.add(permission)

    @tracer.start_as_current_span("get_permission_by_id")
    async def get_permission_by_id(self, permission_id: str) -> Permission:
        current_span = trace.get_current_span()
        current_span.set_attribute("permission_id", permission_id)
        return await self._permission_repo.get(permission_id)

    @tracer.start_as_current_span("get_all_permissions")
    async def get_all_permissions(self) -> list[Permission]:
        return await self._permission_repo.get_all()

    @tracer.start_as_current_span("update_permission_by_id")
    async def update_permission_by_id(
        self, permission_id: str, permission_data: PermissionCreate
    ) -> Permission:
        current_span = trace.get_current_span()
        current_span.set_attribute("permission_id", permission_id)
        permission = await self._permission_repo.get(permission_id)
        permission.name = permission_data.name
        if permission_data.description:
            permission.description = permission_data.description
        if permission_data.resource:
            permission.resource = permission_data.resource
        return await self._permission_repo.update(permission)

    @tracer.start_as_current_span("delete_permission_by_id")
    async def delete_permission_by_id(self, permission_id: str) -> None:
        current_span = trace.get_current_span()
        current_span.set_attribute("permission_id", permission_id)
        permission = await self._permission_repo.get(permission_id)
        await self._permission_repo.delete(permission)
