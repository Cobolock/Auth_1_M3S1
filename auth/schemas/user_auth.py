from pydantic import BaseModel


class UserCredentials(BaseModel):
    username: str
    password: str


class UserRefresh(BaseModel):
    refresh_token: str


class UserLogout(BaseModel):
    refresh_token: str
