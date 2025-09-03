from sqlalchemy import String, Date, Float, Boolean
from sqlalchemy.orm import mapped_column

from database import Model
from database.base_model import CreatedModel


class Trip(Model,CreatedModel):
    name = mapped_column(String(255),nullable=True)
    description = mapped_column(String(255), nullable=True)
    country = mapped_column(String(255), nullable=True)
    city = mapped_column(String(255), nullable=True)
    start_date = mapped_column(Date, nullable=True)
    end_date = mapped_column(Date, nullable=True)
    price = mapped_column(Float, nullable=True)
    image_url = mapped_column(String(255), nullable=True)
    is_ai_suggestion = mapped_column(Boolean, nullable=True)

