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


class CompetitionRoundJudge(Base):
    __tablename__ = "competition_round_judges"

    __table_args__ = (
        UniqueConstraint(
            "competition_round_id",
            "user_id",
            name=(
                "uq_competition_round_judges_"
                "round_user"
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
    # JUDGE USER
    # ======================================================

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    # ======================================================
    # JUDGE PANEL
    # ======================================================

    judge_order = Column(
        Integer,
        nullable=True,
    )

    status = Column(
        String(30),
        nullable=False,
        default="assigned",
        server_default="assigned",
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
        back_populates="judges",
    )

    user = relationship(
        "User",
        back_populates="competition_round_judges",
    )