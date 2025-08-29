import asyncio
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from bot.reply_markup import phone_number
from core.config import settings

TOKEN = settings.TELEGRAM_BOT_TOKEN

dp = Dispatcher()


# Command handler
@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer("telefon raqamingizni kriting", reply_markup=phone_number())


async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
