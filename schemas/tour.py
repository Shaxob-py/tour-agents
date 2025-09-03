from pydantic import BaseModel, Field


class TourSchema(BaseModel):
    where: str = Field(..., examples=['Spain'])
    to: str = Field(..., examples=['Uzbekistan'])
    when: str = Field(..., examples=['24.01.2025'])
    when_back: str = Field(..., examples=['30.01.2025'])
