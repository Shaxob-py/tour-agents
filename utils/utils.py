from datetime import datetime
from random import randint

import httpx

from core.config import settings


async def send_telegram_message(chat_id: int, text: str):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=payload)
    return response.json()


def generate_code() -> int:
    return randint(100000, 999999)


async def verification_send_telegram(chat_id: int, code: int):
    text = f"🔑 Your verification code is: {code}"
    return await send_telegram_message(chat_id, text)


def get_travel_days(start: str, end: str) -> int:
    start_date = datetime.strptime(start, '%d.%m.%Y')
    end_date = datetime.strptime(end, '%d.%m.%Y')
    return (end_date - start_date).days + 1


async def check_user(phone_number: str, username: str, telegram_id: int):
    from database import User
    user = await User.get_telegram_id_by_phone_number(phone_number)
    if user:
        return await User.update_by_username(phone_number, username)
    return await User.create(
        phone_number=phone_number,
        username=username,
        telegram_id=telegram_id,
    )


def normalize_phone(raw: str) -> str:
    return ''.join(c for c in raw if c.isdigit())
