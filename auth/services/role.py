from typing import Annotated

from dataclasses import dataclass

from fastapi import Depends

from auth.core.exceptions import RoleDeletionProhibitedError
from auth.models.role import Role
from auth.repositories.role import RoleRepository
from auth.schemas.role import RoleCreate, RoleUpdate


@dataclass
class RoleService:
    _role_repo: Annotated[RoleRepository, Depends()]

    async def create_role(self, role_data: RoleCreate) -> Role:
        role = Role(**role_data.model_dump())
        return await self._role_repo.add(role)

    async def get_role_by_id(self, role_id: str) -> Role:
        return await self._role_repo.get(role_id)

    async def get_all_roles(self) -> list[Role]:
        return await self._role_repo.get_all()

    async def update_role_by_id(self, role_id: str, role_data: RoleUpdate) -> Role:
        role = await self._role_repo.get(role_id)
        role.name = role_data.name
        return await self._role_repo.update(role)

    async def delete_role_by_id(self, role_id: str) -> None:
        role = await self._role_repo.get(role_id)
        self.check_role_allowed_to_delete(role)
        await self._role_repo.delete(role)

    @staticmethod
    def check_role_allowed_to_delete(role: Role) -> None:
        if role.id == "admin":
            raise RoleDeletionProhibitedError
