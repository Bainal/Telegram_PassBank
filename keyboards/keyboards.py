import aiogram
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_reply_keyboard() -> aiogram.types.ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="Показать пароли")
    builder.button(text="Добавить пароль")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def get_entering_data_inline_keyboard(service_name: str, login: str, password: str) -> aiogram.types.InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=("Площадка" if service_name == None else service_name),
                callback_data="entering_service_name"
            )
        ],
        [
            InlineKeyboardButton(
                text=("Логин" if login == None else login),
                callback_data="entering_login"
            )
        ],
        [
            InlineKeyboardButton(
                text=("Пароль" if password == None else password),
                callback_data="entering_password"
            )
        ],
        [
            InlineKeyboardButton(text="Выход", callback_data="exit_cb"),
            InlineKeyboardButton(text="Сохранить", callback_data="save_cb")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)