"""
В этой таблице необходимо хранить как минимум id пользователя в социальном
сервисе social_id и название поставщика услуг social_name.
social_id можно запрашивать у Поставщика услуг наравне с username или email, а
в social_name достаточно записать название Поставщика услуг.
Пара этих значений должна быть уникальной в базе, чтобы хранить только
уникальные аккаунты из всех социальных сервисов вместе.
Перед тем как создавать новый аккаунт в базе при OAuth-аутентификации, лучше
поискать по social_id и social_name существующий. Если он есть, то user в
вашей базе уже создан и его можно найти по user_id.
"""

from auth.models.base import Base
from auth.models.mixins import AuditMixin, UUIDPrimaryKeyMixin
from auth.models.user import User
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref


class SocialAccount(Base, UUIDPrimaryKeyMixin, AuditMixin):
    __tablename__ = "social_account"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped[User] = relationship(backref=backref("social_accounts", lazy=True))

    social_id = Mapped[str]
    social_name = Mapped[str]
    __table_args__ = (UniqueConstraint("social_id", "social_name", name="social_pk"),)

    def __repr__(self):
        return f"<SocialAccount {self.social_name}:{self.user_id}>"
