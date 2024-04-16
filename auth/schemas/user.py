from uuid import UUID

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str
    first_name: str | None
    last_name: str | None
    enabled: bool


class UserInDB(BaseModel):
    id: UUID
    first_name: str | None
    last_name: str | None
