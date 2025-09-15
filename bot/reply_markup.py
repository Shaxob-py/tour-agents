from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.i18n import gettext as _


def phone_number():
    rkb = ReplyKeyboardBuilder()
    rkb.add(KeyboardButton(text=_('Telefon raqam yuborish'), request_contact=True),
            KeyboardButton(text='til 🇺🇸🇺🇿')
            )
    size = [1]
    rkb.adjust(*size)
    return rkb.as_markup(resize_keyboard=True)


def reply_button(buttons):
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[KeyboardButton(text=btn) for btn in buttons])
    rkb.adjust(2)
    return rkb.as_markup(resize_keyboard=True)