from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from auth.core.config import extra_config
from auth.models.base import Base
from auth.models.mixins import AuditMixin, UUIDPrimaryKeyMixin
from auth.models.role import Role


class User(Base, UUIDPrimaryKeyMixin, AuditMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    roles: Mapped[set[Role]] = relationship(secondary="user_role_association")
    enabled: Mapped[bool | None]

    def __init__(
        self,
        username: str,
        password: str,
        first_name: str | None = None,
        last_name: str | None = None,
    ) -> None:
        self.username = username
        self.password = self.make_password(password)
        self.first_name = first_name
        self.last_name = last_name
        self.enabled = True

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password + extra_config.salt)

    def make_password(self, password) -> str:
        return generate_password_hash(password + extra_config.salt)

    def __repr__(self) -> str:
        return f"<User {self.username}>"
