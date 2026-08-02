"""add is_active to users

Revision ID: 695b63e8f6cc
Revises: fabb84cac028
Create Date: 2026-08-02 12:58:49.618678

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '695b63e8f6cc'
down_revision: Union[str, Sequence[str], None] = 'fabb84cac028'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add account activation status to users."""

    op.add_column(
        "users",
        sa.Column(
            "is_active",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    """Remove account activation status from users."""

    op.drop_column(
        "users",
        "is_active",
    )
