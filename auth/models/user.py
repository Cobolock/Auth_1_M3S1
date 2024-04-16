from datetime import UTC, datetime
from functools import lru_cache

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import check_password_hash, generate_password_hash

from auth.db.postgres import UUIDBase, get_session


class User(UUIDBase):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(UTC))
    enabled: Mapped[bool]

    def __init__(
        self,
        username: str,
        password: str,
        first_name: str | None = None,
        last_name: str | None = None,
        enabled: bool | None = True,
    ) -> None:
        self.username = username
        self.password = generate_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name
        self.enabled = enabled

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def __repr__(self) -> str:
        return f"<User {self.username}>"
