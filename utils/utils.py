import requests
from random import randint
from core.config import settings


def send_telegram_message(chat_id: int, text: str):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    response = requests.post(url, data=payload)
    result = response.json()
    print("Telegram response:", result)
    return result



def generate_code() -> int:
    return randint(100000, 999999)

def verification_send_telegram(telegram_id: int, code: str):
    text = f"🔑 Your verification code is: {code}"
    return send_telegram_message(telegram_id, text)
