from async_fastapi_jwt_auth import AuthJWT

from auth.core.config import JWTSettings


@AuthJWT.load_config
def get_config():
    return JWTSettings()
