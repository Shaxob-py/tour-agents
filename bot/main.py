import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ContentType
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.reply_markup import phone_number
from core.config import settings
from database import User

TOKEN = settings.TELEGRAM_BOT_TOKEN

dp = Dispatcher()


# TODO aiogram i18n qoshish

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("telefon raqamingizni kiriting", reply_markup=phone_number())


@dp.message(F.content_type.in_({ContentType.CONTACT}))
async def handle_contact(message: Message, state: FSMContext) -> None:
    contact = message.contact
    data = await state.get_data()
    register = data.get('register')
    if register is None:
        if contact.user_id != message.from_user.id:
            await message.answer("❌ Faqat o'zingizning telefon raqamingizni yuboring!")
            return
        data = {
            'username': contact.username,  # TODO first_name, last_name qoshish kk
            'phone_number': contact.phone_number,
            'telegram_id': message.from_user.id,
        }
        # TODO create dan oldin check qilish kk phone, tlg id boyicha
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
