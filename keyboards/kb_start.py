from typing import List
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from texts import get_text


def get_menu_ik():
    builder = InlineKeyboardBuilder()
    builder.button(text=get_text("ik_check"), callback_data="check")
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
