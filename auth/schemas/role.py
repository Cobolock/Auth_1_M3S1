from datetime import datetime

from pydantic import BaseModel

from auth.schemas.permission import PermissionId, PermissionRead


class RoleCreate(BaseModel):
    """Схема для создания новой роли."""

    id: str
    name: str
    permissions: list[PermissionId]


class RoleRead(BaseModel):
    """Схема для получения информации о существующей роли."""

    id: str
    name: str
    updated_at: datetime
    created_at: datetime
    permissions: list[PermissionRead]


class RoleUpdate(BaseModel):
    """Схема для обновления информации о существующей роли."""

    name: str
