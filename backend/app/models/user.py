from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from app.db.base import Base


class User(Base):

    __tablename__ = "users"


    # ==========================================================
    # BASIC
    # ==========================================================

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )


    name = Column(
        String,
        nullable=False,
    )


    email = Column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )


    password = Column(
        String,
        nullable=False,
    )


    # ==========================================================
    # ACCOUNT STATUS
    # ==========================================================

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
    )


    # ==========================================================
    # ACCOUNT LOCKOUT
    # ==========================================================

    failed_login_attempts = Column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )


    locked_until = Column(
        DateTime,
        nullable=True,
    )


    # ==========================================================
    # TOKEN REVOCATION
    # ==========================================================

    token_version = Column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )


    # ==========================================================
    # RBAC ROLE
    # ==========================================================

    role_id = Column(
        Integer,
        ForeignKey("roles.id"),
        nullable=False,
        default=2,
    )


    # ==========================================================
    # LOCATION
    # ==========================================================

    province_id = Column(
        Integer,
        ForeignKey("provinces.id"),
        nullable=True,
    )


    city_id = Column(
        Integer,
        ForeignKey("cities.id"),
        nullable=True,
    )


    # ==========================================================
    # RELATIONSHIPS
    # ==========================================================

    role_ref = relationship(
        "Role",
        back_populates="users",
    )


    province = relationship(
        "Province",
        back_populates="users",
    )


    city = relationship(
        "City",
        back_populates="users",
    )


    audit_logs = relationship(
        "AuditLog",
        back_populates="user",
    )


    sessions = relationship(
        "UserSession",
        back_populates="user",
        cascade="all, delete-orphan",
    )


    participant = relationship(
        "Participant",
        back_populates="user",
        uselist=False,
    )


    competition_round_judges = relationship(
        "CompetitionRoundJudge",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    competition_results_finalized = relationship(
        "CompetitionResult",
        back_populates="finalized_by_user",
    )

    competition_result_publications_approved = relationship(
        "CompetitionResultPublication",
        foreign_keys=(
            "CompetitionResultPublication."
            "approved_by_user_id"
        ),
        back_populates="approved_by_user",
    )

    competition_result_publications_published = relationship(
        "CompetitionResultPublication",
        foreign_keys=(
            "CompetitionResultPublication."
            "published_by_user_id"
        ),
        back_populates="published_by_user",
    )


    # ==========================================================
    # COMPATIBILITY FOR RESPONSE SCHEMA
    # ==========================================================

    @property
    def role(self):
        """
        Return role name from RBAC relation.
        Used by UserResponse schema.
        """

        if self.role_ref:
            return self.role_ref.name

        return None