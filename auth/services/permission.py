from typing import Annotated

from dataclasses import dataclass

from fastapi import Depends

from auth.core.exceptions import RoleDeletionProhibitedError
from auth.models.permission import Permission
from auth.repositories.permission import PermissionRepository
from auth.schemas.permission import PermissionCreate, PermissionUpdate, PermissionRead


@dataclass
class PermissionService:
    _permission_repo: Annotated[PermissionRepository, Depends()]

    async def create_permission(self, permission_data: PermissionCreate) -> Permission:
        permission = Permission(**permission_data.model_dump())
        return await self._permission_repo.add(permission)

    async def get_permission_by_id(self, permission_id: str) -> Permission:
        return await self._permission_repo.get(permission_id)

    async def get_all_permissions(self) -> list[Permission]:
        return await self._permission_repo.get_all()

    async def update_permission_by_id(
        self, permission_id: str, permission_data: PermissionUpdate
    ) -> Permission:
        permission = await self._permission_repo.get(permission_id)
        permission.name = permission_data.name
        permission.description = permission_data.description
        permission.resource = permission_data.resource
        return await self._permission_repo.update(permission)

    async def delete_permission_by_id(self, permission_id: str) -> None:
        permission = await self._permission_repo.get(permission_id)
        await self._permission_repo.delete(permission)
