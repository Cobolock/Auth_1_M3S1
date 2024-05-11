from enum import StrEnum, auto

from jose import jwt

from core.settings import settings


class UserRoles(StrEnum):
    SUBSCRIBER = auto()


class JWTAuth:
    def check_user_role(self, access_token: str | None, user_role_enum: str) -> bool:
        if not access_token:
            return False
        self.data = jwt.decode(
            token=access_token,
            key=settings.jwt_secret,
            algorithms="HS256",
        )
        return user_role_enum in self.data.get("roles")
