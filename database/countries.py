import uuid
from typing import Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Model


class Country(Model):
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)
    cities: Mapped[list["City"]] = relationship("City", back_populates="country")



class City(Model):
    name: Mapped[str] = mapped_column(String(255), nullable=True)
    region: Mapped[str] = mapped_column(String(255), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    country_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("countries.id"), nullable=False)
    country: Mapped["Country"] = relationship("Country", back_populates="cities")