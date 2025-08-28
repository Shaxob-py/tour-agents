from sqlalchemy import Integer, String, Date, Float, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column

from database import Model


class Trip(Model):
    id  = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String(255),nullable=True)
    description = mapped_column(String(255), nullable=True)
    country = mapped_column(String(255), nullable=True)
    city = mapped_column(String(255), nullable=True)
    start_date = mapped_column(Date, nullable=True)
    end_date = mapped_column(Date, nullable=True)
    price = mapped_column(Float, nullable=True)
    image_url = mapped_column(String(255), nullable=True)
    is_ai_suggestion = mapped_column(Boolean, nullable=True)

