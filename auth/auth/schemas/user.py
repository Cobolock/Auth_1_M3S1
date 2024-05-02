from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str = Field(max_length=32)
    first_name: str | None = Field(default=None, max_length=32)
    last_name: str | None = Field(default=None, max_length=32)


class UserCreate(UserBase):
    password: str = Field(max_length=128)


class UserInDB(UserBase):
    id: UUID


class EntrySchema(BaseModel):
    created: datetime
    ip_address: str = Field(max_length=16)
    location: str = Field(max_length=32)
    user_agent: str = Field(max_length=64)
    user_id: UUID | None
