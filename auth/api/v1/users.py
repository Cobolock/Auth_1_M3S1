from typing import Annotated

from fastapi import APIRouter, Depends, status

from auth.services.user import UserService

router = APIRouter()


@router.put(
    "/{username}/roles/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Назначить роль пользователю",
)
async def add_role_to_user(
    username: str, role_id: str, user_service: Annotated[UserService, Depends()]
) -> None:
    await user_service.add_role(username, role_id)


@router.delete(
    "/{username}/roles/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Снять роль с пользователя",
)
async def remove_role_from_user(
    username: str, role_id: str, user_service: Annotated[UserService, Depends()]
) -> None:
    await user_service.remove_role(username, role_id)
