from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


class UUIDPrimaryKeyMixin:
    """Миксин для ORM моделей, которые используют UUID в качестве первичного ключа."""

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)


class AuditMixin:
    """Миксин для ORM моделей, которые сохраняют даты создания и обновления."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
