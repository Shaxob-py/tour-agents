from redis import Redis

from core.config import settings
from utils.utils import verification_send_telegram


class OtpService:
    def __init__(self):
        self.redis_client = Redis.from_url(settings.REDIS_URL)

    async def send_otp_by_telegram(self, user, code: int, expire_time=60) -> tuple[bool, int]:
        _key = user.phone_number
        _ttl = self.redis_client.ttl(_key)
        if _ttl > 0:
            return False, _ttl
        self.redis_client.set(_key, code, ex=expire_time)  # noqa
        print(f"🔑 OTP code: {code} , phone: {_key}")
        await verification_send_telegram(user.telegram_id, code)  # noqa
        return True, 0

    async def verify_code_telegram(self, phone: str, code: str) -> tuple[bool, dict | None]:
        saved_code = self.redis_client.get(phone)

        if saved_code:
            saved_code = saved_code.decode()  # noqa
        else:
            return False, None

        user_data = None

        return saved_code == code, user_data
