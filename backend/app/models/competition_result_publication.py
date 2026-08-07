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


class CompetitionResultPublication(Base):

    __tablename__ = "competition_result_publications"

    __table_args__ = (
        UniqueConstraint(
            "competition_round_id",
            name=(
                "uq_competition_result_publications_"
                "round"
            ),
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # ======================================================
    # ROUND
    # ======================================================

    competition_round_id = Column(
        Integer,
        ForeignKey(
            "competition_rounds.id"
        ),
        nullable=False,
        index=True,
    )

    # ======================================================
    # PUBLICATION STATE
    # ======================================================

    status = Column(
        String(30),
        nullable=False,
        default="approved",
        server_default="approved",
    )

    # ======================================================
    # APPROVAL
    # ======================================================

    approved_by_user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    approved_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    # ======================================================
    # PUBLICATION
    # ======================================================

    published_by_user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )

    published_at = Column(
        DateTime,
        nullable=True,
    )

    # ======================================================
    # TIMESTAMPS
    # ======================================================

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    # ======================================================
    # RELATIONSHIPS
    # ======================================================

    competition_round = relationship(
        "CompetitionRound",
        back_populates="result_publication",
    )

    approved_by_user = relationship(
        "User",
        foreign_keys=[
            approved_by_user_id
        ],
        back_populates=(
            "competition_result_publications_approved"
        ),
    )

    published_by_user = relationship(
        "User",
        foreign_keys=[
            published_by_user_id
        ],
        back_populates=(
            "competition_result_publications_published"
        ),
    )
