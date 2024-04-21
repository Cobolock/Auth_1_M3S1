from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, ForeignKey, Table, String

from auth.models.base import Base
from auth.models.mixins import AuditMixin
from auth.models.permission import Permission


role_permission_association = Table(
    "role_permission_association",
    Base.metadata,
    Column("role_id", String, ForeignKey("roles.id")),
    Column("permission_id", String, ForeignKey("permissions.id")),
)


class Role(Base, AuditMixin):
    __tablename__ = "roles"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    # add new field - FK
    permissions: Mapped[List[Permission]] = relationship(secondary=role_permission_association)

    def __repr__(self) -> str:
        return f"<Role {self.id}>"
