from typing import Optional

from sqlalchemy import String, Date, Boolean, ForeignKey, Integer, update, func
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy.orm import selectinload

from database import Model
from database.base_model import db, CreatedModel


class Trip(CreatedModel):
    away_from: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    destination: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    days: Mapped[int] = mapped_column(Integer, default=0)
    description: Mapped[Optional[str]] = mapped_column(String(2000), nullable=True)
    start_date: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)
    end_date: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)
    is_ai_suggestion: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    view_count: Mapped[int] = mapped_column(Integer, default=0)

    user_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("users.id"))
    created_by: Mapped["User"] = relationship("User", back_populates="trips") # noqa

    images: Mapped[list["TripImage"]] = relationship("TripImage", back_populates="trip", cascade="all, delete-orphan")
    likes: Mapped[list["TripLike"]] = relationship("TripLike", back_populates="trip", cascade="all, delete-orphan")

    likes_count: Mapped[int] = mapped_column(Integer, server_default="0", default=0)
    dislikes_count: Mapped[int] = mapped_column(Integer, server_default="0", default=0)

    @classmethod
    async def get_all(cls, search=None, destination=None, start_date=None, end_date=None, skip=0, limit=10):
        query = select(cls).options(
            selectinload(cls.created_by),
            selectinload(cls.images)
        )

        if search: # noqa
            query = query.filter(
                (cls.destination.ilike(f"%{search}%")) |
                (cls.description.ilike(f"%{search}%"))
            )
        if destination:
            query = query.filter(cls.destination.ilike(f"%{destination}%"))
        if start_date:
            query = query.filter(cls.start_date >= start_date)
        if end_date:
            query = query.filter(cls.end_date <= end_date)

        query = query.offset(skip).limit(limit)

        result = await db.execute(query)
        return result.scalars().all()

    @classmethod
    async def get(cls, id_):
        query = (
            select(cls)
            .where(cls.id == id_)
            .options(
                selectinload(cls.created_by),
                selectinload(cls.images)
            )
        )
        return (await db.execute(query)).scalar_one_or_none()

    @classmethod
    async def update_view_count(cls, id_: UUID):
        query = (
            update(cls)
            .where(cls.id == id_)
            .values(view_count=cls.view_count + 1)
        )
        await db.execute(query)
        await db.commit()

    @classmethod
    async def like_update(cls, id_: UUID, is_like: bool):
        if is_like:
            query = update(cls).where(cls.id == id_).values(likes_count=cls.likes_count + 1)
        else:
            query = update(cls).where(cls.id == id_).values(dislikes_count=cls.dislikes_count + 1)
        await db.execute(query)
        await db.commit()


class TripImage(Model):
    trip_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("trips.id"))
    url: Mapped[str] = mapped_column(String(255))

    trip: Mapped["Trip"] = relationship("Trip", back_populates="images")


class TripLike(Model):
    trip_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("trips.id"))
    trip: Mapped["Trip"] = relationship("Trip", back_populates="likes")

    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    is_like: Mapped[bool] = mapped_column(Boolean, nullable=True)

    user: Mapped["User"] = relationship("User") # noqa

    @classmethod
    async def update_like(cls, trip_id: UUID, user_id: UUID, is_like: bool):
        query = (
            update(cls)
            .where(cls.trip_id == trip_id, cls.user_id == user_id)
            .values(is_like=is_like)
        )
        await db.execute(query)
        await db.commit()

    @classmethod
    async def create_or_update(cls, trip_id, user_id, is_like: bool):
        result = await db.execute(
            select(cls).where(cls.trip_id == trip_id, cls.user_id == user_id)
        )
        trip_like = result.scalars().first()

        if trip_like:
            return await cls.update_like(trip_id, user_id, is_like)
        return await cls.create(
            user_id=user_id,
            trip_id=trip_id,
            is_like=is_like,
        )
