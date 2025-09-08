import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.reply_markup import phone_number
from core.config import settings
from database import User

TOKEN = settings.TELEGRAM_BOT_TOKEN

dp = Dispatcher()


@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer("telefon raqamingizni kriting", reply_markup=phone_number())


@dp.message(F.contact)
async def handle_contact(message: Message, state: FSMContext) -> None:
    contact = message.contact
    data = await state.get_data()
    register = data.get('register')
    if register is None:
        if contact.user_id != message.from_user.id:
            await message.answer("❌ Faqat o'zingizning telefon raqamingizni yuboring!")
            return
        data = {
            'phone_number': contact.phone_number,
            'telegram_id': message.from_user.id,
        }
        await User.create(**data)
        await state.update_data(register=True)
        await message.answer("✅ Royxattan muvaffaqiyatli o'tdingiz!")

    else:
        await message.answer('Siz allaqachon registerdan otgansiz')


async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
