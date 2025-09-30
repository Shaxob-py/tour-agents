from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base_model import CreatedModel


class Order(CreatedModel):
    phone_number: Mapped[str] = mapped_column(String(25), unique=True)

