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


@auth_router.post('/register')
async def login_view(data : RegisterSchema ,service: OtpService = Depends(otp_service)):
    user = await User.get_by_username(data.username)
    user_id = await User.get_id_by_username(data.username)
    if user is not None:
        return ORJSONResponse(
            {'message': 'Username already registered'},
            status.HTTP_400_BAD_REQUEST)
    code = generate_code()
    try:
        service.send_otp_by_email(user_id,str(code))
        return ORJSONResponse(
            {'message': 'Check your telegram to verify your account'},
        )
    except Exception as e:
        return ORJSONResponse(
            {'message': 'bot ga start bosing :https://t.me/check_menssage_bot'},
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