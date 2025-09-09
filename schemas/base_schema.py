from datetime import datetime, date
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar('T', bound=BaseModel)


class ResponseSchema(BaseModel, Generic[T]):
    message: str
    data: T | None = None


class ChatAiSchema(BaseModel):
    message: str


class TourSchema(BaseModel):
    where: str = Field(..., examples=['Spain'])
    to: str = Field(..., examples=['Uzbekistan'])
    when: str = Field(..., examples=['24.01.2025'])
    when_back: str = Field(..., examples=['30.01.2025'])


class LoginSchema(BaseModel):
    phone: str = Field(..., min_length=1, examples=['991234567'])


class UserSchema(BaseModel):
    username: str

    class Config:
        from_attributes = True


class ImageSchema(BaseModel):
    url: str

    class Config:
        from_attributes = True


class ReadTourSchema(BaseModel):
    away_from: str
    destination: str
    description: str
    start_date: date
    end_date: date
    created_at: datetime | None = None
    update_at: datetime | None = None
    created_by: UserSchema
    images: list[ImageSchema]
    likes_count: int
    dislikes_count: int

    class Config:
        from_attributes = True
    # away_from: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    # destination :Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    # description: Mapped[Optional[str]] = mapped_column(String(2000), nullable=True)
    # start_date: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)
    # end_date: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)
    # is_ai_suggestion: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    # user_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("users.id"), nullable=True)
    # created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now())
    # update_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())
    #
    # created_by: Mapped["User"] = relationship("User", back_populates="trips")
    # images: Mapped[list["TripImage"]] = relationship("TripImage", back_populates="trip", cascade="all, delete-orphan")
    # likes: Mapped[list["TripLike"]] = relationship("TripLike", back_populates="trip", cascade="all, delete-orphan")
    # likes_count: Mapped[int] = mapped_column(Integer, default=0)
    # dislikes_count: Mapped[int] = mapped_column(Integer, default=0)
