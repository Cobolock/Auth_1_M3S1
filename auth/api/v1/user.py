from fastapi import APIRouter, Depends

from auth.schemas.user import UserCreate
from auth.models.user import User, get_user_service

router = APIRouter()


@router.post("/", response_model=UserCreate)
async def new_user(
    username: str,
    password: str,
    # params: dict = Depends(UserCreate),
    # user_service: User = Depends(get_user_service)
) -> dict:
    new_user = User(username, password)
    bl = await new_user.create_user()
    print(bl)
    return new_user
