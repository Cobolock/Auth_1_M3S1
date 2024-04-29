from datetime import datetime

from pydantic import BaseModel, Field

from auth.schemas.permission import PermissionId, PermissionRead


class RoseBase(BaseModel):
    """Базовая схема роли."""

    id: str = Field(max_length=16)
    name: str = Field(max_length=16)


class RoleCreate(RoseBase):
    """Схема для создания новой роли."""

    permissions: list[PermissionId] = []


class RoleRead(RoseBase):
    """Схема для получения информации о существующей роли."""

    updated_at: datetime
    created_at: datetime
    permissions: list[PermissionRead] = []


class RoleUpdate(BaseModel):
    """Схема для обновления информации о существующей роли."""

    name: str | None = Field(max_length=16)
    permissions: list[PermissionId] | None = None
