import uuid

from pydantic import EmailStr
from sqlalchemy import Integer, String, Float, Enum, select
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import Mapped, mapped_column

from database import Model
from database.base_model import db


class User(Model):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True, )
    first_name: Mapped[str] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str] = mapped_column(String(255), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(25), nullable=True, unique=True)
    email: Mapped[EmailStr] = mapped_column(String(150), nullable=True, unique=True)
    username: Mapped[str] = mapped_column(String(255), nullable=True, unique=True)

    @classmethod
    async def get_by_username(cls, username: str):
        query = select(cls).where(cls.username == username)
        return (await db.execute(query)).scalar()

    @classmethod
    async def get_id_by_username(cls, username: str):
        query = select(cls.id).where(cls.username == username)
        result = await db.execute(query)
        return result.scalar_one_or_none()