import datetime
from typing import Optional

from sqlalchemy import String, Date, Float, Boolean, ForeignKey, DateTime, func, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship, Mapped

from database import Model


class Trip(Model):
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    start_date: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)
    end_date: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)
    price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    is_ai_suggestion: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    user_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("users.id"), nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now())
    update_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    created_by: Mapped["User"] = relationship("User", back_populates="trips")
    images: Mapped[list["TripImage"]] = relationship("TripImage", back_populates="trip", cascade="all, delete-orphan")
    likes: Mapped[list["TripLike"]] = relationship("TripLike", back_populates="trip", cascade="all, delete-orphan")
    likes_count: Mapped[int] = mapped_column(Integer, default=0)
    dislikes_count: Mapped[int] = mapped_column(Integer, default=0)


class TripImage(Model):
    trip_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("trips.id"), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    trip: Mapped["Trip"] = relationship("Trip", back_populates="images")


class TripLike(Model):
    trip_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("trips.id"), nullable=False)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    is_like: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    trip: Mapped["Trip"] = relationship("Trip", back_populates="likes")
    user: Mapped["User"] = relationship("User")


