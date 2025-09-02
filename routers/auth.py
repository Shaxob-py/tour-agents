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
    code = generate_code()
    telegram_id = await User.get_telegram_id_by_phone_number(data.phone)
    service.send_otp_by_email(data.phone,   telegram_id,code)
    try:
        return ORJSONResponse(
            {'message': 'Check your email to verify your account'},
        )
    except Exception as e:
        return ORJSONResponse(
            {'message': 'you should register your number with bot'})


# @auth_router.post('/register')
# async def login_view(service: OtpService = Depends(otp_service)):
#     code = generate_code()
#     print(code)
#     service.send_otp_by_email(str(1910644443), str(code))
#     return ORJSONResponse(
#         {'message': 'Check your email to verify your account'},
#     )


@auth_router.get('/verification-code')
async def login_view(phone : str,code: str, service: OtpService = Depends(otp_service)):
    # telegram_id = await User.get_telegram_id_by_phone_number(code)
    # is_verified = service.verify_code_telegram(telegram_id, code)
    # print(code, telegram_id, is_verified)
    # if is_verified:
    #     # await User.create(**user_data)
    #     return ORJSONResponse(
    #         {'message': 'User successfully registered'}
    #     )
    # return ORJSONResponse(
    #     {'message': 'Invalid or expired code'},
    #     status.HTTP_400_BAD_REQUEST
    # )
    is_verified, user_data = service.verify_code_telegram(phone, code)
    print(is_verified,user_data)
    if is_verified:
        # await User.create(**user_data)
        return ORJSONResponse(
            {'message': 'User successfully registered'}
        )
    return ORJSONResponse(
        {'message': 'Invalid or expired code'},
        status.HTTP_400_BAD_REQUEST
    )
