from typing import Optional

from sqlalchemy import String, select
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Model
from database.base_model import db
from database.trips import TripLike


class User(Model):
    username: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(25), nullable=True, unique=True)
    telegram_id : Mapped[Optional[int]] = mapped_column(BIGINT, unique=True)
    trips: Mapped[list["Trip"]] = relationship("Trip", back_populates="created_by")
    trips_like: Mapped[list["TripLike"]]= relationship("TripLike", back_populates="user")
    # TODO login uchun unique key topish

    @classmethod
    async def get_by_phone_number(cls, phone_number: str):
        query = select(cls).where(cls.phone_number == phone_number)
        return (await db.execute(query)).scalar()

    @classmethod
    async def get_telegram_id_by_phone_number(cls, phone_number: str):
        query = select(cls.telegram_id).where(cls.phone_number == phone_number)
        result = await db.execute(query)
        return result.scalar_one_or_none()