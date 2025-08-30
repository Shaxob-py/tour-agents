from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.responses import ORJSONResponse
from starlette import status

from core.config import settings
from database import User
from schemas.auth import RegisterSchema
from services.otp_services import OtpService
from utils.utils import generate_code

auth_router = APIRouter()


def otp_service():
    return OtpService(settings.TELEGRAM_BOT_TOKEN)


@auth_router.post('/auth')
async def login_view(data: RegisterSchema, service: OtpService = Depends(otp_service)):
    phone_user = str(data.phone)
    telegram_id = await User.get_telegram_id_by_phone_number(phone_user)
    code = generate_code()  # int or str

    # ensure code is str
    code_str = str(code)

    if telegram_id is None:
        return ORJSONResponse({'message': 'Telegram ID not found for this phone'}, status_code=400)

    # IMPORTANT: call with (code, telegram_id) - same order as service method
    success = await service.send_otp_by_telegram(code_str, telegram_id)

    if success:
        return ORJSONResponse({'message': 'Check your telegram to verify your account'})
    else:
        return ORJSONResponse(
            {'message': 'Failed to send OTP. Check that user pressed /start and bot token is correct.'},
            status_code=400
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