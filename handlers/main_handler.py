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
    F.data.startswith("entering_"),
    my_states.States.passed
)
async def change_service_name(
    callback: types.CallbackQuery,
    state: FSMContext,
    mysql_client: mysql.Client,
    bot: Bot
):
    data_name = callback.data.replace("entering_", "")
    await state.update_data(data_name=data_name)

    await callback.message.edit_text(text=get_text(f"{data_name}_request"), reply_markup=None)
    await state.set_state(my_states.States.entering_service_name)

@router.message(
    F.text,
    my_states.States.entering_service_name
)
async def entering_data(
    message: types.Message,
    state: FSMContext,
    mysql_client: mysql.Client,
    bot: Bot
):
    user_data = await state.get_data()

    data = {user_data["data_name"]: message.text}
    user_data[user_data["data_name"]] = message.text

    await state.update_data(data)
    await state.set_state(my_states.States.passed)

    await bot.delete_message(chat_id=message.from_user.id, message_id=user_data["bot_last_message"])
    bot_last_message = await message.answer(text=get_text("add_password_main_text"), reply_markup=keyboards.get_entering_data_inline_keyboard(user_data["service_name"],user_data["login"],user_data["password"]))
    await state.update_data(bot_last_message=bot_last_message.message_id)
    
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)

@router.callback_query(
    F.data == "exit_cb",
    my_states.States.passed
)
async def back(
    callback: types.CallbackQuery,
    state: FSMContext,
    mysql_client: mysql.Client,
    bot: Bot
):
    user_data = await state.get_data()
    await bot.delete_message(chat_id=callback.from_user.id, message_id=user_data["bot_last_message"])

    bot_last_message = await callback.message.answer(text="Воспользуйтесь функционалом ниже:", reply_markup=keyboards.get_main_reply_keyboard())
    await state.set_data({"bot_last_message": bot_last_message.message_id})

@router.callback_query(
    F.data == "save_cb",
    my_states.States.passed
)
async def save(
    callback: types.CallbackQuery,
    state: FSMContext,
    mysql_client: mysql.Client,
    bot: Bot
):
    user_data = await state.get_data()
    print(f"{user_data["service_name"]} | {user_data["login"]} | {user_data["password"]}")

    if user_data["service_name"] == None:
        await callback.answer(text=f"Ошибка!\n{get_text("service_name_request")}", show_alert=True)
        return
    if user_data["login"] == None:
        await callback.answer(text=f"Ошибка!\n{get_text("login_request")}", show_alert=True)
        return
    if user_data["password"] == None:
        await callback.answer(text=f"Ошибка!\n{get_text("password_request")}", show_alert=True)
        return
    
    await mysql_client.password_add(telegram_id=callback.from_user.id, service_name=user_data["service_name"], login=user_data["login"], password=user_data["password"])
    await callback.answer(text="Пароль успешно сохранен!", show_alert=True)
    
    await bot.delete_message(chat_id=callback.from_user.id, message_id=user_data["bot_last_message"])
    
    bot_last_message = await callback.message.answer(text="Воспользуйтесь функционалом ниже:", reply_markup=keyboards.get_main_reply_keyboard())
    await state.set_data({"bot_last_message": bot_last_message.message_id})
    