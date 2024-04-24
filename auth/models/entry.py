from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, func
from auth.models.mixins import UUIDPrimaryKeyMixin
from auth.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class Entry(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "entries"

    created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default=func.now()
    )
    ip_address: Mapped[str]
    location: Mapped[str]
    user_agent: Mapped[str]
    user_id: Mapped[UUID | None]

    def __repr__(self) -> str:
        return f"<Entry {self.user_id} {self.created} {self.location}>"
