from enum import Enum
from typing import Optional

from passlib.context import CryptContext
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import String, select, update
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base_model import db, CreatedModel
from database.trips import TripLike

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class User(CreatedModel):
    class Role(Enum):
        ADMIN = 'ADMIN'
        USER = 'USER'

    username: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(25), unique=True)
    telegram_id: Mapped[int] = mapped_column(BIGINT, unique=True)
    trips: Mapped[list["Trip"]] = relationship("Trip", back_populates="created_by")  # noqa
    trips_like: Mapped[list["TripLike"]] = relationship("TripLike", back_populates="user")
    password: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    role: Mapped[Role] = mapped_column(
        SQLEnum(Role, name="role"),
        default=Role.USER,

    )

    @classmethod
    async def get_by_phone_number(cls, phone_number: str):
        query = select(cls).where(cls.phone_number == phone_number)
        return (await db.execute(query)).scalar()

    @classmethod
    async def get_telegram_id_by_phone_number(cls, phone_number: str):
        query = select(cls.telegram_id).where(cls.phone_number == phone_number)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def update_by_username(cls, phone_number: str, username: str):
        query = (update(cls).where(cls.phone_number == phone_number).values(username=username))
        await db.execute(query)
        await db.commit()

    def check_password(self, plain_password: str) -> bool:
        if not self.password:
            return False
        return pwd_context.verify(plain_password, self.password)

    def set_password(self, password: str):
        self.password = pwd_context.hash(password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)