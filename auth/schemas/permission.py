from pydantic import BaseModel
from uuid import UUID


class PermissionId(BaseModel):
    """Схема для передачи id ограничения в объект роли."""

    id: str


class PermissionCreate(BaseModel):
    """Схема для создания нового ограничения."""

    name: str
    description: str | None
    resource: str | None


class PermissionRead(PermissionCreate):
    """Схема для получения информации о существующем ограничении."""

    id: UUID


class PermissionUpdate(BaseModel):
    """Схема для обновления информации о существующем ограничении."""

    description: str | None
    resource: str | None
