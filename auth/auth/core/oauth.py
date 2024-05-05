import base64
from typing import List
from pydantic import BaseModel

from auth.core.config import jwt_settings


class OAuthJWT(BaseModel):
    algorithm: str = jwt_settings.jwt_algorithm
    decode_algorithms: List[str] = [jwt_settings.jwt_algorithm]
    token_location: set = {"cookies", "headers"}
    private_key: str = base64.b64decode(jwt_settings.jwt_private_key).decode("utf-8")
    public_key: str = base64.b64decode(jwt_settings.jwt_public_key).decode("utf-8")
    access_cookie_key: str = "access_token"
    refresh_cookie_key: str = "refresh_token"
    cookie_csrf_protect: bool = True


oauthjwt = OAuthJWT()
