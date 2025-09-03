from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.responses import ORJSONResponse
from starlette import status

from database import User
from schemas.auth import LoginSchema
from services.otp_services import OtpService
from utils.security import create_access_token
from utils.utils import generate_code

auth_router = APIRouter()


def otp_service():
    return OtpService()


@auth_router.post('/auth')
async def login_view(data: LoginSchema, service: OtpService = Depends(otp_service)):
    code = generate_code()
    telegram_id = await User.get_telegram_id_by_phone_number(data.phone)
    service.send_otp_by_telegram(data.phone, telegram_id, code)
    try:
        return ORJSONResponse(
            {'message': 'Check your email to verify your account'},
        )
    except Exception as e:
        return ORJSONResponse(
            {'message': 'you should register your number with bot'})


@auth_router.get('/verification-code')
async def login_view(phone: str, code: str, service: OtpService = Depends(otp_service)):
    is_verified, user_data = service.verify_code_telegram(phone, code)
    print(is_verified, user_data)
    if is_verified:
        user = await User.get_by_phone_number(phone)

        # await User.create(**user_data)
        token = create_access_token({"sub": str(user.id)})
        return {"access_token": token}
    return ORJSONResponse(
        {'message': 'Invalid or expired code'},
        status.HTTP_400_BAD_REQUEST
    )

    # TODO refresh token qoshish kerak
