from typing import Annotated

from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from auth.schemas.user import Credentials
from auth.services.user import UserService

router = APIRouter()


@router.post("/", status_code=HTTPStatus.CREATED)
async def new_user(
    credentials: Credentials, user_service: Annotated[UserService, Depends()]
) -> dict:
    status = await user_service.create(credentials)
    if status:
        return {"detail": "Created"}
    raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Username in use")


@router.post("/login")
async def user_login(
    credentials: Credentials, user_service: Annotated[UserService, Depends()]
) -> dict:
    """Проверить логин и пароль, выдать в ответ JWT."""
    jwt = await user_service.login(credentials)
    return {"access_token": jwt.AT, "refresh_token": jwt.RT}


@router.post("/refresh")
async def user_refresh(refresh_token: str, user_service: Annotated[UserService, Depends()]):
    """Обновить Refresh Token, если он валидный."""
    jwt = await user_service.refresh(refresh_token)
    return {"access_token": jwt.AT, "refresh_token": jwt.RT}
