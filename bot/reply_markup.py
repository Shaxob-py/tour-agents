from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def phone_number():
    rkb = ReplyKeyboardBuilder()
    rkb.add(KeyboardButton(text='Telefon raqam yuborish', request_contact=True),
            KeyboardButton(text='🔚 Orqaga'))
    size = [1]
    rkb.adjust(*size)
    return rkb.as_markup(resize_keyboard=True)