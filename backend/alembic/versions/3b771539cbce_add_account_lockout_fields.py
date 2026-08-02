"""add account lockout fields

Revision ID: 3b771539cbce
Revises: 695b63e8f6cc
Create Date: 2026-08-02 13:11:33.464415

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3b771539cbce'
down_revision: Union[str, Sequence[str], None] = '695b63e8f6cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add account lockout fields to users."""

    op.add_column(
        "users",
        sa.Column(
            "failed_login_attempts",
            sa.Integer(),
            server_default=sa.text("0"),
            nullable=False,
        ),
    )

    op.add_column(
        "users",
        sa.Column(
            "locked_until",
            sa.DateTime(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Remove account lockout fields from users."""

    op.drop_column(
        "users",
        "locked_until",
    )

    op.drop_column(
        "users",
        "failed_login_attempts",
    )
