import asyncio
from os import getenv

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from fastapi import Depends

from bot.reply_markup import phone_number
from core.config import settings
from database import User

TOKEN = settings.TELEGRAM_BOT_TOKEN

dp = Dispatcher()


# Command handler
@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer("telefon raqamingizni kriting", reply_markup=phone_number())

@dp.message(F.contact)
async def handle_contact(message: Message) -> None:
    await message.answer(f"Siz royxattan ottingiz")
    phone = {'phone':message.contact.phone_number}
    await User.create(**phone)




async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
