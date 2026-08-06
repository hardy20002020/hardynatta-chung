from datetime import datetime

from sqlalchemy import (
    Boolean,
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


class CompetitionScoringCriterion(Base):
    __tablename__ = "competition_scoring_criteria"

    __table_args__ = (
        UniqueConstraint(
            "competition_round_id",
            "code",
            name=(
                "uq_competition_scoring_criteria_"
                "round_code"
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
    # CRITERION
    # ======================================================

    code = Column(
        String(50),
        nullable=False,
    )

    name = Column(
        String(150),
        nullable=False,
    )

    description = Column(
        String(500),
        nullable=True,
    )

    # ======================================================
    # SCORING
    # ======================================================

    weight = Column(
        Numeric(7, 4),
        nullable=False,
    )

    min_score = Column(
        Numeric(10, 4),
        nullable=False,
        default=0,
        server_default="0",
    )

    max_score = Column(
        Numeric(10, 4),
        nullable=False,
        default=100,
        server_default="100",
    )

    # ======================================================
    # DISPLAY ORDER
    # ======================================================

    sort_order = Column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )

    # ======================================================
    # STATUS
    # ======================================================

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
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
        back_populates="scoring_criteria",
    )

    score_details = relationship(
        "CompetitionJudgeScoreDetail",
        back_populates="scoring_criterion",
        cascade="all, delete-orphan",
    )