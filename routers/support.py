from fastapi import APIRouter, Depends

from database import User, SupportMessage
from schemas.base_schema import CreateSupportSchema, ReadSupportSchema, ResponseSchema
from services.support_service import create_support_message
from utils.security import get_current_user

support_router = APIRouter(tags=["Support"]    )


@support_router.post("/send_message_support/", response_model=ReadSupportSchema)
async def send_message(data: CreateSupportSchema, current_user: User = Depends(get_current_user)):
    return await create_support_message(data, current_user)


@support_router.get("/message_list/", response_model=ResponseSchema)
async def get_message_list():
    messages = await SupportMessage.get_all()
    if messages:
        return ResponseSchema[list[ReadSupportSchema]](
            message='List of messages',
            data=messages,
        )
