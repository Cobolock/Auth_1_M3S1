import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from auth.models.base import Base
from auth.models.mixins import UUIDPrimaryKeyMixin


class Permission(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "permissions"

    name: Mapped[str]
    description = Mapped[str]
    resource = Mapped[str]

    def __repr__(self) -> str:
        return f"<Permission {self.name}>"
