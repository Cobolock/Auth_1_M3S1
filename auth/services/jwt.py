from typing import Any

from dataclasses import dataclass

from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.auth_jwt import AuthJWTBearer
from async_fastapi_jwt_auth.exceptions import JWTDecodeError

from auth.core.config import JWTSettings
from auth.core.exceptions import TokenMalformedError

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

    def __init__(self) -> None:
        self._jwt_service = get_jwt()

    @classmethod
    async def generate(cls, subject) -> "JWTPair":
        self = cls()
        self.AT = await self._jwt_service.create_access_token(subject=subject)
        self.RT = await self._jwt_service.create_refresh_token(subject=subject)
        return self

    @classmethod
    async def get_payload(cls, refresh_token) -> dict[str, Any]:
        temp_jwt = get_jwt()
        try:
            return await temp_jwt.get_raw_jwt(refresh_token)
        except JWTDecodeError:
            raise JWTDecodeError from None
        except ValueError:
            raise TokenMalformedError from None
