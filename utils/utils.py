
from random import randint

import httpx

from core.config import settings


def send_telegram_message(chat_id: int, text: str):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    response = httpx.post(url, data=payload)
    return response.json()

def generate_code() -> int:
    return randint(100000, 999999)

def verification_send_telegram(chat_id: int, code: str):
    text = f"🔑 Your verification code is: {code}"
    return send_telegram_message(chat_id, text)
