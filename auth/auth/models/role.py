from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from auth.models.base import Base
from auth.models.mixins import AuditMixin
from auth.models.permission import Permission

role_permission_association = Table(
    "role_permission_association",
    Base.metadata,
    Column("role_id", String, ForeignKey("roles.id", ondelete="CASCADE")),
    Column("permission_id", UUID(as_uuid=True), ForeignKey("permissions.id", ondelete="CASCADE")),
)

association_table = Table(
    "user_role_association",
    Base.metadata,
    Column("role_id", ForeignKey("roles.id", ondelete="CASCADE")),
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE")),
)


class Role(Base, AuditMixin):
    __tablename__ = "roles"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    permissions: Mapped[list[Permission]] = relationship(
        secondary=role_permission_association, lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<Role {self.id}>"
