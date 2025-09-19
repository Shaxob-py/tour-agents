from typing import Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from database import Model


class Country(Model): #
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)

class City(Model):
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)
    country_id : Mapped[str] = mapped_column(ForeignKey(Country.id), nullable=True)