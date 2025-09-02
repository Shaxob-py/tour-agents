

from sqlalchemy import Integer, String , select
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from database import Model
from database.base_model import db


class User(Model):
    phone_number: Mapped[str] = mapped_column(String(25), nullable=True, unique=True)
    telegram_id : Mapped[int] = mapped_column(BIGINT, unique=True)

    @classmethod
    async def get_by_phone_number(cls, phone_number: str):
        query = select(cls).where(cls.phone_number == phone_number)
        return (await db.execute(query)).scalar()

    @classmethod
    async def get_telegram_id_by_phone_number(cls, phone_number: str):
        query = select(cls.telegram_id).where(cls.phone_number == phone_number)
        result = await db.execute(query)
        return result.scalar_one_or_none()