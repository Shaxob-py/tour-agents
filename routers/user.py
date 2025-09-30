from fastapi import APIRouter, Depends
from database import User
from database.order import Order
from schemas.base_schema import ResponseSchema, UserSchema, LoginSchema
from utils.security import get_current_user

user_router = APIRouter(prefix='/users', tags=["User"])


@user_router.get("/get-me", response_model=ResponseSchema[UserSchema])
async def get_me(current_user: User = Depends(get_current_user)):
    user = await User.get(current_user.id)

    return ResponseSchema[UserSchema](
        message='User detail',
        data=user
    )


@user_router.post("/create", response_model=LoginSchema)
async def create_order(date: LoginSchema):
    await Order.create(phone_number=date)
