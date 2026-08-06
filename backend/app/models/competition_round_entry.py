from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class CompetitionRoundEntry(Base):
    __tablename__ = "competition_round_entries"

    __table_args__ = (
        UniqueConstraint(
            "competition_round_id",
            "competition_registration_id",
            name=(
                "uq_competition_round_entries_"
                "round_registration"
            ),
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # ======================================================
    # COMPETITION ROUND
    # ======================================================

    competition_round_id = Column(
        Integer,
        ForeignKey("competition_rounds.id"),
        nullable=False,
        index=True,
    )

    # ======================================================
    # COMPETITION REGISTRATION
    # ======================================================

    competition_registration_id = Column(
        Integer,
        ForeignKey("competition_registrations.id"),
        nullable=False,
        index=True,
    )

    # ======================================================
    # PERFORMANCE
    # ======================================================

    performance_order = Column(
        Integer,
        nullable=True,
    )

    status = Column(
        String(30),
        nullable=False,
        default="scheduled",
        server_default="scheduled",
    )

    # ======================================================
    # TIMESTAMPS
    # ======================================================

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # ======================================================
    # RELATIONSHIPS
    # ======================================================

    competition_round = relationship(
        "CompetitionRound",
        back_populates="entries",
    )

    competition_registration = relationship(
        "CompetitionRegistration",
        back_populates="round_entries",
    )

    judge_scores = relationship(
        "CompetitionJudgeScore",
        back_populates="competition_round_entry",
        cascade="all, delete-orphan",
    )