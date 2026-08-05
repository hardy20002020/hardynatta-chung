"""add competition registrations table

Revision ID: fa767e531dc3
Revises: f08fe93f6a84
Create Date: 2026-08-05 09:19:12.328922

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# ==========================================================
# ALEMBIC REVISION
# ==========================================================

revision: str = "fa767e531dc3"

down_revision: Union[
    str,
    Sequence[str],
    None,
] = "f08fe93f6a84"

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
    Create competition registrations.

    A competition registration connects:
    - competition
    - competition group
    - participant
    - registration number

    One participant can register only once
    in the same competition.

    Registration numbers must also be unique
    within the same competition.
    """

    op.create_table(
        "competition_registrations",

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),

        # ==================================================
        # COMPETITION
        # ==================================================

        sa.Column(
            "competition_id",
            sa.Integer(),
            nullable=False,
        ),

        # ==================================================
        # COMPETITION GROUP
        # ==================================================

        sa.Column(
            "competition_group_id",
            sa.Integer(),
            nullable=False,
        ),

        # ==================================================
        # PARTICIPANT
        # ==================================================

        sa.Column(
            "participant_id",
            sa.Integer(),
            nullable=False,
        ),

        # ==================================================
        # REGISTRATION
        # ==================================================

        sa.Column(
            "registration_number",
            sa.String(length=50),
            nullable=False,
        ),

        sa.Column(
            "status",
            sa.String(length=30),
            server_default="registered",
            nullable=False,
        ),

        # ==================================================
        # TIMESTAMPS
        # ==================================================

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
        ),

        # ==================================================
        # FOREIGN KEYS
        # ==================================================

        sa.ForeignKeyConstraint(
            ["competition_id"],
            ["competitions.id"],
        ),

        sa.ForeignKeyConstraint(
            ["competition_group_id"],
            ["competition_groups.id"],
        ),

        sa.ForeignKeyConstraint(
            ["participant_id"],
            ["participants.id"],
        ),

        # ==================================================
        # PRIMARY KEY
        # ==================================================

        sa.PrimaryKeyConstraint(
            "id",
        ),

        # ==================================================
        # UNIQUE CONSTRAINTS
        # ==================================================

        sa.UniqueConstraint(
            "competition_id",
            "participant_id",
            name=(
                "uq_competition_registrations_"
                "competition_participant"
            ),
        ),

        sa.UniqueConstraint(
            "competition_id",
            "registration_number",
            name=(
                "uq_competition_registrations_"
                "competition_registration_number"
            ),
        ),
    )

    # ======================================================
    # INDEXES
    # ======================================================

    op.create_index(
        op.f(
            "ix_competition_registrations_"
            "competition_id"
        ),
        "competition_registrations",
        ["competition_id"],
        unique=False,
    )

    op.create_index(
        op.f(
            "ix_competition_registrations_"
            "competition_group_id"
        ),
        "competition_registrations",
        ["competition_group_id"],
        unique=False,
    )

    op.create_index(
        op.f(
            "ix_competition_registrations_"
            "participant_id"
        ),
        "competition_registrations",
        ["participant_id"],
        unique=False,
    )

    op.create_index(
        op.f(
            "ix_competition_registrations_id"
        ),
        "competition_registrations",
        ["id"],
        unique=False,
    )


# ==========================================================
# DOWNGRADE
# ==========================================================

def downgrade() -> None:
    """
    Remove competition registrations.
    """

    op.drop_index(
        op.f(
            "ix_competition_registrations_id"
        ),
        table_name="competition_registrations",
    )

    op.drop_index(
        op.f(
            "ix_competition_registrations_"
            "participant_id"
        ),
        table_name="competition_registrations",
    )

    op.drop_index(
        op.f(
            "ix_competition_registrations_"
            "competition_group_id"
        ),
        table_name="competition_registrations",
    )

    op.drop_index(
        op.f(
            "ix_competition_registrations_"
            "competition_id"
        ),
        table_name="competition_registrations",
    )

    op.drop_table(
        "competition_registrations",
    )