from sqlalchemy.orm import Mapped, mapped_column

from auth.models.base import Base
from auth.models.mixins import AuditMixin, UUIDPrimaryKeyMixin


class LoginHistory(Base, UUIDPrimaryKeyMixin, AuditMixin):
    __tablename__ = "login_histories"

    login_date: Mapped[str]
    login_device: Mapped[str]

    def __repr__(self) -> str:
        return f"<Login history {self.id}>"
