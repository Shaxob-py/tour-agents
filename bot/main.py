import asyncio
from os import getenv

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from fastapi import Depends

from bot.reply_markup import phone_number
from core.config import settings
from routers.auth import otp_service
from services.otp_services import OtpService
from utils.utils import generate_code

TOKEN = settings.TELEGRAM_BOT_TOKEN

dp = Dispatcher()


# Command handler
@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer("telefon raqamingizni kriting", reply_markup=phone_number())

@dp.message(F.contact)
async def handle_contact(message: Message) -> None:
    code = generate_code()
    phone_number = message.contact.phone_number
    telegram_id = message.from_user.id

    await message.answer(f"Sizning maxfiy kodingiz: {code}")

    # сохраняем код в Redis и отправляем в бот
    otp_service.send_otp_by_email(phone_number, str(code), str(telegram_id))


async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
