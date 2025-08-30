from pydantic import BaseModel

class ChatAiSchema(BaseModel):
    message: str
