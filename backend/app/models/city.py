from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class City(Base):
    __tablename__ = "cities"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    province_id = Column(
        Integer,
        ForeignKey("provinces.id"),
        nullable=False,
    )

    name = Column(
        String(100),
        nullable=False,
    )

    province = relationship(
        "Province",
        back_populates="cities",
    )

    users = relationship(
        "User",
        back_populates="city",
    )