from pydantic import BaseModel


class RegisterSchema(BaseModel):
    phone: str
