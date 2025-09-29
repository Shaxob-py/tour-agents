from fastapi import APIRouter, Depends

from database import User
from schemas.base_schema import ResponseSchema, UserSchema
from utils.security import get_current_user

user_router=APIRouter(tags=["user"])


@user_router.get("get-me",response_model=ResponseSchema[UserSchema])
async def get_me(current_user:User=Depends(get_current_user)):
    user = await User.get(current_user.id)

    return ResponseSchema[UserSchema](
        message='User detail',
        data=user
    )
