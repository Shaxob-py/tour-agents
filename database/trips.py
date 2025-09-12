import datetime
from typing import Optional

from sqlalchemy import String, Date, Boolean, ForeignKey, DateTime, func, Integer
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy.orm import selectinload

from database import Model
from database.base_model import db

# An (id, city, country_name)
# TODO country, city
class Trip(Model):
    # TODO fk to city
    away_from: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    destination :Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # TODO
    # from_country -> to_country
    {
        "where": "Spain",
        "to": "Uzbekistan",
        "from_country": "Russia",
        "to_country": "Uzbekistan",
        "options": "country",
        "when": "24.01.2025",
        "when_back": "30.01.2025"
    }

    description: Mapped[Optional[str]] = mapped_column(String(2000), nullable=True)
    start_date: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)
    end_date: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)
    is_ai_suggestion: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)

    user_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("users.id"), nullable=True)
    created_by: Mapped["User"] = relationship("User", back_populates="trips")

    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())
    # TODO view_count
    images: Mapped[list["TripImage"]] = relationship("TripImage", back_populates="trip", cascade="all, delete-orphan")
    likes: Mapped[list["TripLike"]] = relationship("TripLike", back_populates="trip", cascade="all, delete-orphan")
    likes_count: Mapped[int] = mapped_column(Integer, default=0)
    dislikes_count: Mapped[int] = mapped_column(Integer, default=0)

    @classmethod
    async def get_all(cls):
        result = await db.execute(
            select(cls).options(
                selectinload(cls.created_by),
                selectinload(cls.images),
            )
        )
        return result.scalars().all()

class TripImage(Model):
    trip_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("trips.id"), nullable=False) # TODO nullable=False default da boladi ozi
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    trip: Mapped["Trip"] = relationship("Trip", back_populates="images")


class TripLike(Model):
    trip_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("trips.id"), nullable=False)
    trip: Mapped["Trip"] = relationship("Trip", back_populates="likes")

    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    is_like: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False) # TODO base modeldan olish
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    user: Mapped["User"] = relationship("User")


