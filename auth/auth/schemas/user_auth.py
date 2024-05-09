from pydantic import BaseModel, Field


class UserCredentials(BaseModel):
    username: str = Field(max_length=32)
    password: str = Field(max_length=164)


class UserRefresh(BaseModel):
    refresh_token: str


class UserLogout(BaseModel):
    refresh_token: str
