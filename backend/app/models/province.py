from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Province(Base):
    __tablename__ = "provinces"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    name = Column(
        String,
        nullable=False,
        unique=True,
    )

    cities = relationship(
        "City",
        back_populates="province",
        cascade="all, delete-orphan",
    )

    users = relationship(
        "User",
        back_populates="province",
    )