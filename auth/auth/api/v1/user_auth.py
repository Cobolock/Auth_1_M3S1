from typing import Annotated

from fastapi import APIRouter, Depends, status

from auth.models.user import User
from auth.schemas.user import UserCreate, UserInDB
from auth.schemas.user_auth import UserCredentials, UserLogout, UserRefresh
from auth.services.user import UserService

router = APIRouter()


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=UserInDB,
    description="Создать нового пользователя",
    response_description="Данные о созданном пользователе",
)
async def new_user(user_data: UserCreate, user_service: Annotated[UserService, Depends()]) -> User:
    return await user_service.create_user(user_data)


@router.post("/login", status_code=status.HTTP_200_OK)
async def user_login(
    credentials: UserCredentials, user_service: Annotated[UserService, Depends()]
) -> dict:
    """Проверить логин и пароль, выдать в ответ JWT."""
    jwt = await user_service.login(credentials)
    return jwt.format()


@router.post("/refresh", status_code=status.HTTP_200_OK)
async def user_refresh(body: UserRefresh, user_service: Annotated[UserService, Depends()]) -> dict:
    """Обновить Refresh Token, если он валидный."""
    jwt = await user_service.refresh(body.refresh_token)
    return jwt.format()


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def user_logout(body: UserLogout, user_service: Annotated[UserService, Depends()]) -> None:
    """Удаляет RT из кэша."""
    await user_service.logout(body.refresh_token)
