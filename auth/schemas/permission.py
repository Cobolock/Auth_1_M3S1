from typing import List

from pydantic import BaseModel


class PermissionCreate(BaseModel):
    """Схема для создания новой роли."""

    name: str
    description: str | None
    resource: List[str] | None


class PermissionRead(PermissionCreate):
    """Схема для получения информации о существующей роли."""


class PermissionUpdate(BaseModel):
    """Схема для обновления информации о существующей роли."""

    description: str | None
    resource: List[str] | None
