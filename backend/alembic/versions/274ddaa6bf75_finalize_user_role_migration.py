"""finalize user role migration

Revision ID: 274ddaa6bf75
Revises: 8a2afbf40a10
Create Date: 2026-08-02 13:31:42.638644

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '274ddaa6bf75'
down_revision: Union[str, Sequence[str], None] = '8a2afbf40a10'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Finalize users RBAC migration."""

    op.alter_column(
        "users",
        "role_id",
        existing_type=sa.Integer(),
        nullable=False,
    )

    op.drop_column(
        "users",
        "role",
    )


def downgrade() -> None:
    """Restore legacy users role column."""

    op.add_column(
        "users",
        sa.Column(
            "role",
            sa.String(length=50),
            server_default=sa.text("'user'"),
            nullable=False,
        ),
    )

    op.execute(
        """
        UPDATE users
        SET role = roles.name
        FROM roles
        WHERE users.role_id = roles.id
        """
    )

    op.alter_column(
        "users",
        "role_id",
        existing_type=sa.Integer(),
        nullable=True,
    )
