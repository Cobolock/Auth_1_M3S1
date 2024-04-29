from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from auth.models.base import Base
from auth.models.mixins import UUIDPrimaryKeyMixin
from auth.models.user import User


class Entry(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "entries"

    created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default=func.now()
    )
    ip_address: Mapped[str]
    location: Mapped[str]
    user_agent: Mapped[str]
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped[User] = relationship()

    def __repr__(self) -> str:
        return f"<Entry {self.user_id} {self.created} {self.location}>"
