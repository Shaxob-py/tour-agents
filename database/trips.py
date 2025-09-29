from typing import Optional

from sqlalchemy import String, Date, Boolean, ForeignKey, Integer, update, delete
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy.orm import selectinload
from database.base_model import db, CreatedModel, Model


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
    created_by: Mapped["User"] = relationship("User", back_populates="trips")

    images: Mapped[list["TripImage"]] = relationship("TripImage", back_populates="trip", cascade="all, delete-orphan")
    likes: Mapped[list["TripLike"]] = relationship("TripLike", back_populates="trip", cascade="all, delete-orphan")
    likes_count: Mapped[int] = mapped_column(Integer, server_default='0')
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

    @classmethod
    async def get(cls, id_):
        query = (
            select(cls)
            .where(cls.id == id_)
            .options(
                selectinload(cls.created_by),
                selectinload(cls.images),
            )
        )
        return (await db.execute(query)).scalar_one_or_none()

    @classmethod
    async def update_view_count(cls, id_: int):
        query = (
            update(cls)
            .where(cls.id == id_)
            .values(view_count=cls.view_count + 1)
        )
        await db.execute(query)
        await db.commit()


class TripImage(Model):
    trip_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("trips.id"))
    url: Mapped[str] = mapped_column(String(255))  # TODO kerak emas

    trip: Mapped["Trip"] = relationship("Trip", back_populates="images")


class TripLike(Model):
    trip_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("trips.id"))
    trip: Mapped["Trip"] = relationship("Trip", back_populates="likes")

    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User")

    is_like: Mapped[bool] = mapped_column(Boolean, nullable=True)

    @classmethod
    async def update_like(cls, trip_id: UUID, user_id: UUID, is_like: bool):
        query = await db.execute(select(cls).where(cls.trip_id == trip_id, cls.user_id == user_id))

        existing_record = query.scalar_one_or_none()

        key = 'dis' * (not is_like) + 'likes_count'

        kwargs = {
            key: getattr(Trip, key) + bool(existing_record) * (-2) + 1
        }

        if existing_record:
            await db.execute(delete(cls).where(cls.trip_id == trip_id, cls.user_id == user_id))
        else:
            await cls.create(user_id=user_id, trip_id=trip_id, is_like=is_like)

        await db.execute(update(Trip).where(Trip.id == trip_id).values(**kwargs))

        # if is_like:
        #     if existing_record:
        #         await db.execute(update(Trip).where(Trip.id == trip_id).values(likes_count=Trip.likes_count - 1)),
        #         await db.execute(delete(cls).where(cls.trip_id == trip_id, cls.user_id == user_id))
        #     else:
        #         await db.execute(update(Trip).where(Trip.id == trip_id).values(likes_count=Trip.likes_count + 1))
        #         await cls.create(user_id=user_id, trip_id=trip_id, is_like=is_like)
        #
        # else:
        #     if existing_record:
        #         await db.execute(update(Trip).where(Trip.id == trip_id).values(dislikes_count=Trip.dislikes_count - 1))
        #         await db.execute(delete(cls).where(cls.trip_id == trip_id, cls.user_id == user_id))
        #     else:
        #         await db.execute(update(Trip).where(Trip.id == trip_id).values(dislikes_count=Trip.dislikes_count + 1))
        #         await cls.create(user_id=user_id, trip_id=trip_id, is_like=is_like)

        await db.commit()

