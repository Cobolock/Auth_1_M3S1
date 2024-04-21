from typing import Any

from dataclasses import dataclass

from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.auth_jwt import AuthJWTBearer
from async_fastapi_jwt_auth.exceptions import JWTDecodeError

from auth.core.config import JWTSettings
from auth.core.exceptions import BadRefreshTokenError, TokenMalformedError

auth_dep = AuthJWTBearer()


@AuthJWT.load_config
def get_config():
    return JWTSettings()


def get_jwt() -> AuthJWT:
    return auth_dep()


@dataclass
class JWTPair:
    AT: str
    RT: str

    def format(self) -> dict:
        return {"access_token": self.AT, "refresh_token": self.RT}


class JWTService:
    def __init__(self) -> None:
        self._jwt_service = get_jwt()
        self.AT: str
        self.RT: str

    async def generate(self, subject) -> JWTPair:
        self.AT = await self._jwt_service.create_access_token(subject=subject)
        self.RT = await self._jwt_service.create_refresh_token(subject=subject)
        return JWTPair(self.AT, self.RT)

    async def get_payload(self, refresh_token) -> dict[str, Any]:
        try:
            return await self._jwt_service.get_raw_jwt(refresh_token)
        except JWTDecodeError:
            raise JWTDecodeError from None
        except ValueError:
            raise TokenMalformedError from None

    async def get_sub(self, refresh_token) -> str:
        try:
            payload = await self.get_payload(refresh_token)
        except JWTDecodeError:
            raise BadRefreshTokenError from None

        return payload["sub"]
