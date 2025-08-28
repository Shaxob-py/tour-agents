from pydantic import BaseModel


class ChatAiSchema(BaseModel):
    chat: str