from uuid import UUID

from pydantic import BaseModel, Field


class PermissionId(BaseModel):
    """Схема для передачи id ограничения в объект роли."""

    id: str = Field(max_length=16)


class PermissionUpdate(BaseModel):
    """Схема для обновления информации о существующем ограничении."""

    description: str | None = Field(default=None, max_length=512)
    resource: str | None = Field(default=None, max_length=16)


class PermissionCreate(PermissionUpdate):
    """Схема для создания нового ограничения."""

    name: str = Field(max_length=16)


class PermissionRead(PermissionCreate):
    """Схема для получения информации о существующем ограничении."""

    id: UUID
