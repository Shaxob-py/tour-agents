# from typing import Annotated
#
# from fastapi import APIRouter, Depends, HTTPException, status
# from starlette.responses import JSONResponse
#
# from database.users import User
# from schemas.users import LoginForm
# from utils.security import create_access_token, get_current_user
#
# user_router = APIRouter()
#
#
# @user_router.post('/login')
# async def login_view(data: LoginForm):
#     user = await User.get_by_phone_number(data.phone_number)
#
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Invalid phone number"
#         )
#
#     token = create_access_token({"sub": str(user.id)})
#     return {"access_token": token}
#
#
# @user_router.get('/get-me')
# async def get_me_view(current_user: User = Depends(get_current_user)):
#     return JSONResponse(
#         {'message': f"Current user is {current_user.phone_number}"}
#     )
