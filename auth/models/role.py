from sqlalchemy.orm import Mapped, mapped_column

from auth.models.base import Base
from auth.models.mixins import AuditMixin


class Role(Base, AuditMixin):
    __tablename__ = "roles"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]

    def __repr__(self) -> str:
        return f"<Role {self.id}>"
