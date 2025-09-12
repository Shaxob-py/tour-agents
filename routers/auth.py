from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.responses import ORJSONResponse
from starlette import status

from database import User
from schemas.base_schema import LoginSchema
from services.otp_services import OtpService
from utils.security import create_access_token, create_refresh_token, verify_refresh_token
from utils.utils import generate_code

auth_router = APIRouter()


def otp_service():
    return OtpService()


@auth_router.post('/auth')
async def login_view(data: LoginSchema, service: OtpService = Depends(otp_service)):
    user = await User.get_by_phone_number(data.phone)

    if not user:
        return ORJSONResponse(
            {"message": "Siz bot orqali ro'yxatdan o'tmagansiz. Iltimos, botdan ro'yxatdan o'ting."},
            status_code=400
        )

    code = generate_code()
    telegram_id = user.telegram_id

    service.send_otp_by_telegram(data.phone, telegram_id, code)

    return ORJSONResponse(
        {"message": "Tasdiqlash kodi telegram orqali yuborildi"}
    )


@auth_router.get('/verification-code')
async def login_view(phone: str, code: str, service: OtpService = Depends(otp_service)):
    is_verified, user_data = service.verify_code_telegram(phone, code)

    if is_verified:
        user = await User.get_by_phone_number(phone)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})

        return {
            "access_token": token,
            "refresh_token": refresh_token,
        }

    return ORJSONResponse(
        {"message": "Invalid or expired code"},
        status.HTTP_400_BAD_REQUEST
    )


@auth_router.get('/refresh-token')
async def refresh_token(refresh_token: str):
    user_uuid = verify_refresh_token(refresh_token)
    new_access_token = create_access_token({'sub': str(user_uuid)})
    return {
        "access_token": new_access_token,
        "refresh_token": refresh_token,
    }
