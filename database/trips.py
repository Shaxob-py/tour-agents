from sqlalchemy import String, Date, Float, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column

from database import Model


class Trip(Model):
    name = mapped_column(String(255),nullable=True)
    description = mapped_column(String(255), nullable=True)
    country = mapped_column(String(255), nullable=True)
    city = mapped_column(String(255), nullable=True)
    start_date = mapped_column(Date, nullable=True)
    end_date = mapped_column(Date, nullable=True)
    price = mapped_column(Float, nullable=True)
    is_ai_suggestion = mapped_column(Boolean, nullable=True)
    user_id = mapped_column(ForeignKey('users.id'), nullable=True)
