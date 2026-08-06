from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class CompetitionJudgeScore(Base):
    __tablename__ = "competition_judge_scores"

    __table_args__ = (
        UniqueConstraint(
            "competition_round_entry_id",
            "competition_round_judge_id",
            name=(
                "uq_competition_judge_scores_"
                "entry_judge"
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
        ForeignKey("competition_round_entries.id"),
        nullable=False,
        index=True,
    )

    # ======================================================
    # ROUND JUDGE
    # ======================================================

    competition_round_judge_id = Column(
        Integer,
        ForeignKey("competition_round_judges.id"),
        nullable=False,
        index=True,
    )

    # ======================================================
    # SCORE
    # ======================================================

    total_score = Column(
        Numeric(10, 4),
        nullable=True,
    )

    status = Column(
        String(30),
        nullable=False,
        default="draft",
        server_default="draft",
    )

    notes = Column(
        Text,
        nullable=True,
    )

    submitted_at = Column(
        DateTime,
        nullable=True,
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

    competition_round_entry = relationship(
        "CompetitionRoundEntry",
        back_populates="judge_scores",
    )

    competition_round_judge = relationship(
        "CompetitionRoundJudge",
        back_populates="judge_scores",
    )

    score_details = relationship(
        "CompetitionJudgeScoreDetail",
        back_populates="competition_judge_score",
        cascade="all, delete-orphan",
    )