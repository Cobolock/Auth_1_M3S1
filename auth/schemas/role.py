from datetime import datetime

from pydantic import BaseModel


class RoleCreate(BaseModel):
    """Схема для создания новой роли."""

    id: str
    name: str


class RoleRead(RoleCreate):
    """Схема для получения информации о существующей роли."""

    id: str
    name: str
    updated_at: datetime
    created_at: datetime


class RoleUpdate(BaseModel):
    """Схема для обновления информации о существующей роли."""

    name: str
