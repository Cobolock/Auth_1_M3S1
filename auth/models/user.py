from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import check_password_hash, generate_password_hash

from auth.models.base import Base
from auth.models.mixins import AuditMixin, UUIDPrimaryKeyMixin


class User(Base, UUIDPrimaryKeyMixin, AuditMixin):
    __tablename__ = "users"

    login: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]

    def __init__(
        self, login: str, password: str, first_name: str | None = None, last_name: str | None = None
    ) -> None:
        self.login = login
        self.password = generate_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def __repr__(self) -> str:
        return f"<User {self.login}>"
