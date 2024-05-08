from enum import StrEnum, auto
from jose import jwt, JWTError

from core.settings import settings


class user_roles(StrEnum):
    SUBSCRIBER = auto()


class JWTAuth:
    def check_user_role(self, access_token, user_role_enum) -> bool:
        print(user_role_enum, access_token, flush=True)
        if not access_token:
            return False
        try:
            self.data = jwt.decode(
                token=access_token,
                key=settings.jwt_secret,
                algorithms='HS256',
            )
        except JWTError:
            raise
        print(self.data.get('roles'), user_role_enum, flush=True)
        return user_role_enum in self.data.get('roles')
