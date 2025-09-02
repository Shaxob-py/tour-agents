from pydantic import BaseModel, Field


class LoginSchema(BaseModel):
    phone: str = Field(..., min_length=1, examples=['991234567'])
