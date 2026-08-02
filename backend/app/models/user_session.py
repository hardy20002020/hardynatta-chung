from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from app.db.base import Base


class UserSession(Base):

    __tablename__ = "user_sessions"


    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )


    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )


    # SHA-256 hash of the refresh token.
    # The raw refresh token is never stored.
    refresh_token_hash = Column(
        String(64),
        unique=True,
        nullable=False,
        index=True,
    )


    expires_at = Column(
        DateTime,
        nullable=False,
    )


    created_at = Column(
        DateTime,
        nullable=False,
    )


    last_used_at = Column(
        DateTime,
        nullable=True,
    )


    revoked_at = Column(
        DateTime,
        nullable=True,
    )


    user_agent = Column(
        String(512),
        nullable=True,
    )


    ip_address = Column(
        String(45),
        nullable=True,
    )


    user = relationship(
        "User",
        back_populates="sessions",
    )
