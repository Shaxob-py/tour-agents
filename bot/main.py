import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ContentType, ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile
from aiogram.utils.i18n import I18n, FSMI18nMiddleware
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from bot.reply_markup import phone_number, reply_button
from core.config import settings
from utils.utils import check_user, normalize_phone

TOKEN = settings.TELEGRAM_BOT_TOKEN

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(_("telefon raqamingizni kiriting"), reply_markup=phone_number())


@dp.message(F.content_type.in_({ContentType.CONTACT}))
async def handle_contact(message: Message) -> None:
    contact = message.contact

    if contact.user_id != message.from_user.id:
        await message.answer(_("❌ Faqat o'zingizning telefon raqamingizni yuboring!"))
        return
    await check_user(
        phone_number=normalize_phone(contact.phone_number),
        username=message.from_user.first_name,
        telegram_id=message.from_user.id,
    )
    await message.answer(_("✅ Royxattan muvaffaqiyatli o'tdingiz!"))


@dp.message(F.text == __('til 🇺🇸🇺🇿'))
async def handle_language(message: Message) -> None:
    buttons = ['English 🇺🇸', 'Uzbek 🇺🇿']
    await message.answer('Til tanlang', reply_markup=reply_button(buttons))


@dp.message(F.text.in_(["English 🇺🇸", "Uzbek 🇺🇿"]))
async def handler_language(message: Message, state: FSMContext) -> None:
    map_lang = {
        "English 🇺🇸": "en",
        "Uzbek 🇺🇿": "uz",
    }
    lang = map_lang.get(message.text)
    if lang:
        await state.update_data(locale=lang)
        await message.answer(
            _("telefon raqamingizni kiriting"),
            reply_markup=phone_number()
        )


async def send_trip_to_telegram(
        group_id: int,
        data,
        current_user,
        return_text: str,
        image_url: str,
        days: int,
        trip_id: int
):
    site_url = f"http://0.0.0.0:3000/trip/{trip_id}"
    print(image_url)
    msg = (
        f"✈️ *Yangi AI tavsiya safari!*\n\n"
        f"📍 Yo'nalish: {data.to}\n"
        f"🚩 Qayerdan: {data.where}\n"
        f"📅 Kunlar soni: {days}\n"
        f"👤 Foydalanuvchi: {current_user}\n\n"
        f"🧠 Tavsif:\n{return_text[:500]}...\n\n"
        f"🌍 [Saytga o'tish]({site_url})"
    )
    full_image_url = os.path.join(image_url.lstrip('/'))
    print(full_image_url)

    await bot.send_photo(
        chat_id=group_id,
        photo=FSInputFile(full_image_url),
        caption=msg,
        parse_mode="Markdown"
    )


i18n = I18n(path="locales", default_locale="uz")
dp.update.middleware(FSMI18nMiddleware(i18n=i18n))

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
