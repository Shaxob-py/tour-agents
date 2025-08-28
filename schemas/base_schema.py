from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

class ResponseSchema(BaseModel, Generic[T]):
    message: str
    data: T | None = None
