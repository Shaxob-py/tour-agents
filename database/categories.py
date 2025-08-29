from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Model


class Category(Model):
    name: Mapped[str] = mapped_column(String(255), nullable=True)
    description = mapped_column(String, nullable=True)
