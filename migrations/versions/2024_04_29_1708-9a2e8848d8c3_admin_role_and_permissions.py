"""Admin role and permissions

Revision ID: 9a2e8848d8c3
Revises: 5d19968d0c84
Create Date: 2024-04-29 17:08:56.523020

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy import orm, delete

from auth.models import Permission, Role

# revision identifiers, used by Alembic.
revision: str = "9a2e8848d8c3"
down_revision: Union[str, None] = "5d19968d0c84"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    manage_roles_permission = Permission(name="manage_roles", description="Управление ролями", resource="all")
    manage_users_permission = Permission(
        name="manage_users", description="Управление пользователями", resource="all"
    )
    role = Role(id="admin", name="Администратор", permissions=[manage_roles_permission, manage_users_permission])

    session.add(role)
    session.commit()


def downgrade() -> None:
    op.execute(delete(Role).where(Role.id == "admin"))
    op.execute(delete(Permission).where(Permission.name == "manage_roles"))
    op.execute(delete(Permission).where(Permission.name == "manage_users"))
