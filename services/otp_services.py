# services/otp_service.py
from typing import Tuple
import httpx
from redis.asyncio import Redis
from core.config import settings  # sensoring joying

class OtpService:
    def __init__(self, redis_url: str = settings.REDIS_URL, bot_token: str = settings.TELEGRAM_BOT_TOKEN):
        self.redis = Redis.from_url(redis_url)
        self.api_url = f"https://api.telegram.org/bot{bot_token}"

    def _get_otp_telegram_key(self, telegram_id: int) -> str:
        return f"otp:telegram:{telegram_id}"

    async def send_otp_by_telegram(self, code: str, telegram_id, expire_time: int = 60) -> bool:
        # safety: ensure telegram_id present and int
        if telegram_id is None:
            print("No telegram_id provided")
            return False
        try:
            chat_id = int(telegram_id)
        except (TypeError, ValueError):
            print("Invalid telegram_id:", telegram_id)
            return False

        key = self._get_otp_telegram_key(chat_id)

        # check TTL - if code already sent, avoid spamming
        try:
            ttl = await self.redis.ttl(key)
        except Exception as e:
            print("Redis TTL error:", e)
            ttl = None

        if ttl and ttl > 0:
            print("OTP already exists, ttl:", ttl)
            return False

        # store code
        try:
            await self.redis.set(key, str(code), ex=expire_time)
        except Exception as e:
            print("Redis set error:", e)
            return False

        # send to Telegram
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(
                f"{self.api_url}/sendMessage",
                json={"chat_id": chat_id, "text": f"🔑 Your verification code: {code}"}
            )

        # debug/inspect
        try:
            data = resp.json()
        except Exception:
            print("Telegram response not JSON:", resp.text)
            # cleanup key (optional)
            await self.redis.delete(key)
            return False

        if not data.get("ok", False):
            print("Telegram API error:", data)
            await self.redis.delete(key)  # remove stored code on failure
            return False

        return True

    async def verify_code_telegram(self, telegram_id, code: str) -> bool:
        try:
            chat_id = int(telegram_id)
        except (TypeError, ValueError):
            return False
        key = self._get_otp_telegram_key(chat_id)
        saved = await self.redis.get(key)
        if not saved:
            return False
        saved = saved.decode() if isinstance(saved, (bytes, bytearray)) else str(saved)
        return saved == str(code)
