from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException

from auth.schemas.user import UserCreate
from auth.models.user import User
from auth.services.user import UserService, get_user_service

router = APIRouter()


@router.post("/", status_code=HTTPStatus.CREATED)
async def new_user(
    username: str,
    password: str,
    # params: dict = Depends(UserCreate),
    user_service: UserService = Depends(get_user_service),
) -> dict:
    status = await user_service.create(username, password)
    if status:
        return {"detail": "Created"}
    raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Username in use")


@router.post("/login")
async def user_login(
    username: str, password: str, user_service: UserService = Depends(get_user_service)
) -> dict:
    """Проверить логин и пароль"""
    # сформировать JWT
    # сформировать RT
    # положить RT в Redis
    # в формате UUID_RT: UUID_User
    # существует ли Set.UUID_User? Создать.
    # добавить UUID_RT в Redis Set[UUID_User]:
    ## Set.SISMEMBER?
    ## Set.SCARD (длина набора, не должна выходить за рамки)
    ## Set.SADD
    ## Обновить срок хранения Set
