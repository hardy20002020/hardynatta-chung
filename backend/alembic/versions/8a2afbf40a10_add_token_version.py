"""add token version

Revision ID: 8a2afbf40a10
Revises: 3b771539cbce
Create Date: 2026-08-02 13:21:44.368165

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a2afbf40a10'
down_revision: Union[str, Sequence[str], None] = '3b771539cbce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add token version to users."""

    op.add_column(
        "users",
        sa.Column(
            "token_version",
            sa.Integer(),
            server_default=sa.text("0"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    """Remove token version from users."""

    op.drop_column(
        "users",
        "token_version",
    )
