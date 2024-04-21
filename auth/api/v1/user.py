from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException

from auth.schemas.user import Credentials
from auth.services.user import UserService, get_user_service

from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.exceptions import JWTDecodeError
from async_fastapi_jwt_auth.auth_jwt import AuthJWTBearer

router = APIRouter()
auth_dep = AuthJWTBearer()


@router.post("/", status_code=HTTPStatus.CREATED)
async def new_user(
    credentials: Credentials, user_service: UserService = Depends(get_user_service)
) -> dict:
    status = await user_service.create(credentials)
    if status:
        return {"detail": "Created"}
    raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Username in use")


@router.post("/login")
async def user_login(
    credentials: Credentials,
    user_service: UserService = Depends(get_user_service),
    authorize: AuthJWT = Depends(auth_dep),
) -> dict:
    """Проверить логин и пароль"""

    if await user_service.check_creds(credentials):
        access_token = await authorize.create_access_token(subject=credentials.username)
        refresh_token = await authorize.create_refresh_token(subject=credentials.username)
        return {"access_token": access_token, "refresh_token": refresh_token}
    raise HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED, detail="Incorrect username or password"
    )


@router.post("/refresh")
async def user_refresh(refresh_token: str, authorize: AuthJWT = Depends(auth_dep)):
    try:
        payload = await authorize.get_raw_jwt(refresh_token)
    except JWTDecodeError:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Your refresh token is shit")

    username = payload["sub"]
    access_token = await authorize.create_access_token(subject=username)
    refresh_token = await authorize.create_refresh_token(subject=username)
    return {"access_token": access_token, "refresh_token": refresh_token}
