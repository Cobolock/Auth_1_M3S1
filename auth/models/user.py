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

    def __init__(
        self,
        username: str,
        password: str,
        first_name: str | None = None,
        last_name: str | None = None,
    ) -> None:
        self.username = username
        self.password = generate_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    async def create_user(self) -> bool:
        session = [s async for s in get_session()][0]
        session.add(self)
        try:
            await session.commit()
            return True
        except:
            raise
            return False

    def __repr__(self) -> str:
        return f"<User {self.username}>"
