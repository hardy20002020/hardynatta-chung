from app.core.time import utcnow

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class CompetitionResult(Base):

    __tablename__ = "competition_results"

    __table_args__ = (
        UniqueConstraint(
            "competition_round_entry_id",
            name=(
                "uq_competition_results_"
                "round_entry"
            ),
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # ======================================================
    # ROUND ENTRY
    # ======================================================

    competition_round_entry_id = Column(
        Integer,
        ForeignKey(
            "competition_round_entries.id"
        ),
        nullable=False,
        index=True,
    )

    # ======================================================
    # OFFICIAL RESULT SNAPSHOT
    # ======================================================

    final_score = Column(
        Numeric(10, 4),
        nullable=False,
    )

    rank = Column(
        Integer,
        nullable=False,
    )

    status = Column(
        String(30),
        nullable=False,
        default="finalized",
        server_default="finalized",
    )

    # ======================================================
    # FINALIZATION
    # ======================================================

    finalized_by_user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    finalized_at = Column(
        DateTime,
        nullable=False,
        default=utcnow,
    )

    # ======================================================
    # TIMESTAMPS
    # ======================================================

    created_at = Column(
        DateTime,
        nullable=False,
        default=utcnow,
    )

    updated_at = Column(
        DateTime,
        nullable=False,
        default=utcnow,
        onupdate=utcnow,
    )

    # ======================================================
    # RELATIONSHIPS
    # ======================================================

    competition_round_entry = relationship(
        "CompetitionRoundEntry",
        back_populates="result",
    )

    finalized_by_user = relationship(
        "User",
        back_populates="competition_results_finalized",
    )
