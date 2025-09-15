from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from database import Model


class Country(Model): # TODO fix
    name: Mapped[Optional[str]] = mapped_column(String(255), unique=True, nullable=True)
    region: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
