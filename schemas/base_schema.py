from typing import Generic, TypeVar

from pydantic import BaseModel,Field

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
