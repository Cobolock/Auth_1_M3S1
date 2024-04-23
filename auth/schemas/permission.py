from pydantic import BaseModel
from uuid import UUID


class PermissionCreate(BaseModel):
    """Схема для создания новой роли."""

    name: str
    description: str | None
    resource: str | None


class PermissionRead(PermissionCreate):
    """Схема для получения информации о существующей роли."""

    id: UUID


class PermissionUpdate(BaseModel):
    """Схема для обновления информации о существующей роли."""

    description: str | None
    resource: str | None
