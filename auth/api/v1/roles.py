from typing import Annotated

from fastapi import APIRouter, Depends, status

from auth.models.role import Role
from auth.schemas.role import RoleCreate, RoleRead, RoleUpdate
from auth.services.role import RoleService

router = APIRouter(tags=["Роли"])


@router.post(
    "",
    response_model=RoleRead,
    response_description="Информация о созданной роли",
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую роль",
)
async def create_role(
    role_data: RoleCreate, role_service: Annotated[RoleService, Depends()]
) -> Role:
    return await role_service.create_role(role_data)


@router.get(
    "/{role_id}",
    response_model=RoleRead,
    response_description="Информация о роли",
    status_code=status.HTTP_200_OK,
    summary="Получить информацию о роли",
)
async def get_role(role_id: str, role_service: Annotated[RoleService, Depends()]) -> Role:
    return await role_service.get_role_by_id(role_id)


@router.get(
    "",
    response_model=list[RoleRead],
    response_description="Информацию о всех ролях",
    status_code=status.HTTP_200_OK,
    summary="Получить информацию о всех ролях",
)
async def get_all_roles(role_service: Annotated[RoleService, Depends()]) -> list[Role]:
    return await role_service.get_all_roles()


@router.patch(
    "/{role_id}",
    response_model=RoleRead,
    response_description="Информация об обновлённой роли",
    status_code=status.HTTP_200_OK,
    summary="Обновить информацию о роли",
)
async def update_role(
    role_id: str, role_data: RoleUpdate, role_service: Annotated[RoleService, Depends()]
) -> Role:
    return await role_service.update_role_by_id(role_id, role_data)


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить роль")
async def delete_role(role_id: str, role_service: Annotated[RoleService, Depends()]) -> None:
    await role_service.delete_role_by_id(role_id)
