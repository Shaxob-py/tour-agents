from datetime import datetime, date
from typing import Generic, TypeVar, Optional, Any
from uuid import UUID

from pydantic import BaseModel, Field

T = TypeVar('T', bound=BaseModel)


class ResponseSchema(BaseModel, Generic[T]):
    message: str
    data: T | None = None


class ChatAiSchema(BaseModel):
    message: str


class TripSchema(BaseModel):
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


class ReadTripSchema(BaseModel):
    id : UUID = Field(...)
    away_from: str
    destination: str
    description: str
    start_date: date
    end_date: date
    view_count: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    created_by: UserSchema
    images: list[ImageSchema]
    likes_count: int
    dislikes_count: int

    class Config:
        from_attributes = True


class LoginSuccessSchema(BaseModel):
    access_token: str
    refresh_token: str


class APIResponse(BaseModel):
    message: str
    data: Optional[Any] = None


class SearchTripSchema(BaseModel):
    days: Optional[int] = None
    destination: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class TripLikeRequest(BaseModel):
    trip_id: UUID
    is_like: bool


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class TokenSchema(BaseModel):
    phone: str = Field(..., min_length=1, examples=['991234567'])
    code : str


