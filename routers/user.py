from fastapi import APIRouter, Depends

from database import User
from database.order import Order
from schemas.base_schema import ResponseSchema, UserSchema, LoginSchema, UserDetailsSchema
from utils.security import get_current_user

user_router = APIRouter(prefix='/users', tags=["User"])


@user_router.get("/get-me", response_model=ResponseSchema[UserSchema])
async def get_me(current_user: User = Depends(get_current_user)):
    user = await User.get(current_user.id)

    return ResponseSchema[UserSchema](
        message='User detail',
        data=user
    )


@user_router.post("/order", response_model=ResponseSchema)
async def create_order(date: LoginSchema):
    await Order.create(phone_number=date.phone_number)
    return ResponseSchema(
        message='Order Successfully',
        data=None)


@user_router.get("", response_model=ResponseSchema)
async def user_detailed(id: str):
    user = await User.get_user_trips(id)
    return ResponseSchema[UserDetailsSchema](
        message='User detail',
        data=user)


@user_router.patch("", response_model=ResponseSchema)
async def update_user(username: str, current_user: User = Depends(get_current_user)):
    await User.update(current_user.id, username=username)
    return ResponseSchema(
        message='User Updated',
        data=None
    )



