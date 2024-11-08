from datetime import datetime

from aiogram import Router, F, types, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from modules.db import mysql
from modules.config import configJson
from modules.common.my_class import Users

from keyboards import keyboards
import my_states
from texts import get_text

router = Router()

@router.message(
    F.text == "Показать пароли",
    my_states.States.passed
)
async def show_passwords(
    message: types.Message,
    state: FSMContext,
    mysql_client: mysql.Client,
    bot: Bot
):
    pass

@router.message(
    F.text == "Добавить пароль",
    my_states.States.passed
)
async def add_password(
    message: types.Message,
    state: FSMContext,
    mysql_client: mysql.Client,
    bot: Bot
):
    await state.update_data(service_name=None)
    await state.update_data(login=None)
    await state.update_data(password=None)

    user_data = await state.get_data()
    await bot.delete_message(chat_id=message.from_user.id, message_id=user_data["bot_last_message"])
    bot_last_message = await message.answer(text=get_text("add_password_main_text"), reply_markup=keyboards.get_entering_data_inline_keyboard(user_data["service_name"],user_data["login"],user_data["password"]))
    await state.update_data(bot_last_message=bot_last_message.message_id)

    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)



@router.callback_query(
    F.data == "service_name_cb",
    my_states.States.passed
)
async def change_service_name(
    callback: types.CallbackQuery,
    state: FSMContext,
    mysql_client: mysql.Client,
    bot: Bot
):
    await callback.message.edit_text(text="Введите название площадки", reply_markup=None)
    await state.set_state(my_states.States.entering_service_name)

@router.message(
    F.text,
    my_states.States.entering_service_name
)
async def entering_service_name(
    message: types.Message,
    state: FSMContext,
    mysql_client: mysql.Client,
    bot: Bot
):
    await state.update_data(service_name=message.text)
    await state.set_state(my_states.States.passed)

    user_data = await state.get_data()
    await bot.delete_message(chat_id=message.from_user.id, message_id=user_data["bot_last_message"])
    bot_last_message = await message.answer(text=get_text("add_password_main_text"), reply_markup=keyboards.get_entering_data_inline_keyboard(user_data["service_name"],user_data["login"],user_data["password"]))
    await state.update_data(bot_last_message=bot_last_message.message_id)

    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)