from typing import Annotated

from fastapi import APIRouter, Depends, status

from auth.models.permission import Permission
from auth.schemas.permission import PermissionCreate, PermissionRead
from auth.services.permission import PermissionService

router = APIRouter()


@router.post(
    "",
    response_model=PermissionRead,
    response_description="Информация о созданном ограничении",
    status_code=status.HTTP_201_CREATED,
    summary="Создать новое ограничение",
)
async def create_permission(
    permission_data: PermissionCreate, permission_service: Annotated[PermissionService, Depends()]
) -> Permission:
    return await permission_service.create_permission(permission_data)


@router.get(
    "/{permission_id}",
    response_model=PermissionRead,
    response_description="Информация об ограничении",
    status_code=status.HTTP_200_OK,
    summary="Получить информацию об ограничении",
)
async def get_permission(
    permission_id: str, permission_service: Annotated[PermissionService, Depends()]
) -> Permission:
    return await permission_service.get_permission_by_id(permission_id)


@router.get(
    "",
    response_model=list[PermissionRead],
    response_description="Информацию о всех ограничениях",
    status_code=status.HTTP_200_OK,
    summary="Получить информацию о всех ограничениях",
)
async def get_all_permissions(
    permission_service: Annotated[PermissionService, Depends()],
) -> list[Permission]:
    return await permission_service.get_all_permissions()


@router.patch(
    "/{permission_id}",
    response_model=PermissionRead,
    response_description="Информация об обновлённом ограничении",
    status_code=status.HTTP_200_OK,
    summary="Обновить информацию об ограничении",
)
async def update_permission(
    permission_id: str,
    permission_data: PermissionCreate,
    permission_service: Annotated[PermissionService, Depends()],
) -> Permission:
    return await permission_service.update_permission_by_id(permission_id, permission_data)


@router.delete(
    "/{permission_id}",
    response_description="Информация об удалении ограничения",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить роль",
)
async def delete_role(
    permission_id: str, permission_service: Annotated[PermissionService, Depends()]
) -> None:
    await permission_service.delete_permission_by_id(permission_id)
