from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from auth.models.base import Base
from auth.models.user import User
from auth.models.mixins import AuditMixin, UUIDPrimaryKeyMixin


class LoginHistory(Base, UUIDPrimaryKeyMixin, AuditMixin):
    __tablename__ = "login_histories"
    # правильнее будет сделать связь с Логином у Юзера, так как у Юзера может
    # быть много логинов, а у одного логина будет только один юзер - и
    # здесь по факту связь 1:1
    user: Mapped[User] = mapped_column(ForeignKey("user.id"))
    login_date: Mapped[str]
    login_device: Mapped[str]

    def __repr__(self) -> str:
        return f"<Login history {self.id}>"
