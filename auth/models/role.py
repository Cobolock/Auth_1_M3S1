from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column

from auth.models.base import Base
from auth.models.mixins import AuditMixin

association_table = Table(
    "user_role_association",
    Base.metadata,
    Column("role_id", ForeignKey("roles.id")),
    Column("user_id", ForeignKey("users.id")),
)


class Role(Base, AuditMixin):
    __tablename__ = "roles"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]

    def __repr__(self) -> str:
        return f"<Role {self.id}>"
