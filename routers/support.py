from fastapi import APIRouter, Depends

from database import User
from schemas.base_schema import CreateSupportSchema, ReadSupportSchema
from services.support_service import create_support_message, get_support_messages
from utils.security import get_current_user

support_router = APIRouter(tags=["Support"], dependencies=[Depends(get_current_user)]    )


@support_router.post("/send_message_support/", response_model=ReadSupportSchema)
async def send_message(data: CreateSupportSchema, current_user: User = Depends(get_current_user)):
    return await create_support_message(data, current_user)


@support_router.get("/message_list/", response_model=list[ReadSupportSchema])
async def get_message_list():
    return await get_support_messages()
