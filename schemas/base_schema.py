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
    view_count: int
    created_at: datetime | None = None
    update_at: datetime | None = None
    created_by: UserSchema
    images: list[ImageSchema]
    likes_count: int
    dislikes_count: int

    class Config:
        from_attributes = True
