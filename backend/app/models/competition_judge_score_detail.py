from app.core.time import utcnow

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


class CompetitionJudgeScoreDetail(Base):
    __tablename__ = "competition_judge_score_details"

    __table_args__ = (
        UniqueConstraint(
            "competition_judge_score_id",
            "competition_scoring_criterion_id",
            name=(
                "uq_competition_judge_score_details_"
                "score_criterion"
            ),
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # ======================================================
    # JUDGE SCORE
    # ======================================================

    competition_judge_score_id = Column(
        Integer,
        ForeignKey("competition_judge_scores.id"),
        nullable=False,
        index=True,
    )

    # ======================================================
    # SCORING CRITERION
    # ======================================================

    competition_scoring_criterion_id = Column(
        Integer,
        ForeignKey("competition_scoring_criteria.id"),
        nullable=False,
        index=True,
    )

    # ======================================================
    # SCORE
    # ======================================================

    score = Column(
        Numeric(10, 4),
        nullable=False,
    )

    weighted_score = Column(
        Numeric(10, 4),
        nullable=True,
    )

    # ======================================================
    # SOURCE
    # ======================================================

    source = Column(
        String(30),
        nullable=False,
        default="human",
        server_default="human",
    )

    notes = Column(
        Text,
        nullable=True,
    )

    # ======================================================
    # TIMESTAMPS
    # ======================================================

    created_at = Column(
        DateTime,
        default=utcnow,
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        default=utcnow,
        onupdate=utcnow,
        nullable=False,
    )

    # ======================================================
    # RELATIONSHIPS
    # ======================================================

    competition_judge_score = relationship(
        "CompetitionJudgeScore",
        back_populates="score_details",
    )

    scoring_criterion = relationship(
        "CompetitionScoringCriterion",
        back_populates="score_details",
    )