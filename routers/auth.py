from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.responses import ORJSONResponse
from starlette import status
from database import User
from schemas.auth import RegisterSchema
from services.otp_services import OtpService
from utils.utils import generate_code

auth_router = APIRouter()


def otp_service():
    return OtpService()


@auth_router.post('/auth')
async def login_view(data: RegisterSchema, service: OtpService = Depends(otp_service)):
    phone_user = str(data.phone)
    user = await User.get_by_phone_number(phone_user)
    telegram_id = await User.get_telegram_id_by_phone_number(phone_user)

    if user is not None:
        return ORJSONResponse(
            {'message': 'Username already registered'},
            status.HTTP_400_BAD_REQUEST
        )

    code = generate_code()
    try:
        # передаём все аргументы: phone_number, code, telegram_id
        service.send_otp_by_email(phone_user, str(code), telegram_id)
        return ORJSONResponse(
            {'message': 'Check your telegram to verify your account'},
        )
    except Exception:
        return ORJSONResponse(
            {'message': 'bot ga start bosing : https://t.me/check_menssage_bot'},
        )















@auth_router.get('/verification-code')
async def login_view(code: str, service: OtpService = Depends(otp_service)):
    is_verified, user_data = service.verify_code_telegram(code)
    if is_verified:
        # await User.create(**user_data)
        return ORJSONResponse(

            {'message': 'User successfully registered'}
        )
    return ORJSONResponse(
        {'message': 'Invalid or expired code'},
        status.HTTP_400_BAD_REQUEST
    )