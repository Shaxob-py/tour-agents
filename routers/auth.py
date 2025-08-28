from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.responses import ORJSONResponse
from starlette import status

from services.otp_services import OtpService
from utils.utils import generate_code

auth_router = APIRouter()


def otp_service():
    return OtpService()


@auth_router.post('/register')
async def login_view(service: OtpService = Depends(otp_service)):

    code = generate_code()
    print(code)
    service.send_otp_by_email(str(5121755384), str(code))
    return ORJSONResponse(
        {'message': 'Check your email to verify your account'},
    )

@auth_router.get('/verification-code')
async def login_view(code: str, service: OtpService = Depends(otp_service)):
    is_verified, user_data = service.verify_code_telegram   (code)
    if is_verified:
        # await User.create(**user_data)
        return ORJSONResponse(

            {'message': 'User successfully registered'}
        )
    return ORJSONResponse(
        {'message': 'Invalid or expired code'},
        status.HTTP_400_BAD_REQUEST
    )