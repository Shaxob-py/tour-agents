from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column

from database import Model


class Country(Model):
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String(255), unique=True, nullable=True)
    region = mapped_column(String(255), nullable=True)
    description = mapped_column(String(255), nullable=True)

