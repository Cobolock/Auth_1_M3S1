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
