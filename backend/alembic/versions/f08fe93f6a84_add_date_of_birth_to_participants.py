"""add date of birth to participants

Revision ID: f08fe93f6a84
Revises: 95846b6534a7
Create Date: 2026-08-05 09:06:10.648219

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# ==========================================================
# ALEMBIC REVISION
# ==========================================================

revision: str = "f08fe93f6a84"

down_revision: Union[
    str,
    Sequence[str],
    None,
] = "95846b6534a7"

branch_labels: Union[
    str,
    Sequence[str],
    None,
] = None

depends_on: Union[
    str,
    Sequence[str],
    None,
] = None


# ==========================================================
# UPGRADE
# ==========================================================

def upgrade() -> None:
    """
    Add date of birth to participant profiles.

    The database column is initially nullable
    to preserve compatibility with participant
    records created before date of birth became
    part of the MAJE participant profile.

    New participant profiles require date of
    birth through the application schema.
    """

    op.add_column(
        "participants",
        sa.Column(
            "date_of_birth",
            sa.Date(),
            nullable=True,
        ),
    )


# ==========================================================
# DOWNGRADE
# ==========================================================

def downgrade() -> None:
    """
    Remove date of birth from participant
    profiles.
    """

    op.drop_column(
        "participants",
        "date_of_birth",
    )