from sqlalchemy import String, Date, Float, Boolean, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import mapped_column, relationship

from database import Model, Base


class Trip(Model):
    name = mapped_column(String(255),nullable=True)
    description = mapped_column(String(500), nullable=True)
    country = mapped_column(String(255), nullable=True)
    city = mapped_column(String(255), nullable=True)
    start_date = mapped_column(Date, nullable=True)
    end_date = mapped_column(Date, nullable=True)
    price = mapped_column(Float, nullable=True)
    is_ai_suggestion = mapped_column(Boolean, nullable=True)
    user_id = mapped_column(ForeignKey('users.id'), nullable=True)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    update_at = mapped_column(DateTime(timezone=True), onupdate=func.now())
    created_by = relationship("User", back_populates="trips")
    images = relationship("TripImage", back_populates="trip", cascade="all, delete-orphan")
    likes = relationship("TripLike", back_populates="trip", cascade="all, delete-orphan")


class TripImage(Model):
    trip_id = mapped_column(UUID(as_uuid=True), ForeignKey("Trip.id"), nullable=False)
    url = mapped_column(String(255), nullable=False)
    description = mapped_column(String(255), nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    trip = relationship("Trip", back_populates="images")


class TripLike(Model):
    trip_id = mapped_column(UUID(as_uuid=True), ForeignKey("trips.id"), nullable=False)
    user_id = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    is_like = mapped_column(Boolean, nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    trip = relationship("Trip", back_populates="likes")
    user = relationship("User")


# TODO created_at updated_at qoshish kk

    # TODO created_by qoshish kk

    # TODO nta rasmli bolishi kk

    # TODO like va dislike qoshish kk faqat login qilgan user uchun