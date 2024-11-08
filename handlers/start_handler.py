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
    Command("start"),
    StateFilter(None)
)
async def main_menu(
    message: types.Message,
    state: FSMContext,
    config_client: configJson.Client,
    mysql_client: mysql.Client,
    bot: Bot
):
    user_data = await state.get_data()
    try:
        user: Users = await mysql_client.user_get(telegram_id=message.from_user.id)
    except TypeError: # Пользователя нет в базе данных
        try:
            await bot.edit_message_text(text=get_text("welcome_message"), chat_id=message.from_user.id, message_id=user_data["bot_last_message"])
        except (TelegramBadRequest, KeyError) as e:
            bot_last_message = await message.answer(text=get_text("welcome_message"))
            await state.update_data(bot_last_message=bot_last_message.message_id)

        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)

        await state.set_state(my_states.States.first_entering_master_key)
    else: # Пользователь есть в базе данных
        time_diff = datetime.now() - user.masterkey_lifetime
        if time_diff.seconds > 600: # Если время жизни пароля вышло
            try:
                await bot.edit_message_text(text=get_text("Введите мастер-пароль"), chat_id=message.from_user.id, message_id=user_data["bot_last_message"])
            except (TelegramBadRequest, KeyError) as e:
                bot_last_message = await message.answer(text="Введите мастер-пароль")
                await state.update_data(bot_last_message=bot_last_message.message_id)

            await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)

            await state.set_state(my_states.States.entering_master_key)
        else:
            if "bot_last_message" in user_data:
                bot.delete_message(chat_id=message.from_user.id, message_id=user_data["bot_last_message"])
            bot_last_message = await message.answer(text="Воспользуйтесь функционалом ниже:", reply_markup=keyboards.get_main_reply_keyboard())
            await state.update_data(bot_last_message=bot_last_message.message_id)
        
            await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)

            await state.set_state(my_states.States.passed)

@router.message(
    F.text,
    my_states.States.first_entering_master_key
)
async def registration_entering_master_key(
    message: types.Message,
    state: FSMContext,
    bot: Bot
):
    user_data = await state.get_data()
    if True: # Если пароль соответствует стандартам
        await bot.edit_message_text(text="Повторите введенный пароль", chat_id=message.from_user.id, message_id=user_data["bot_last_message"])
        
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)

        await state.update_data(master_key=message.text)
        await state.set_state(my_states.States.confirm_master_key)
    else: # Если пароль не соответствует стандарту
        await message.answer("Пароль не был добавлен. Попробуйте другой!")

@router.message(
    F.text,
    my_states.States.confirm_master_key
)
async def registration_confirm_master_key(
    message: types.Message,
    state: FSMContext,
    mysql_client: mysql.Client,
    bot: Bot
):
    user_data = await state.get_data()
    if message.text == user_data["master_key"]: # Если пароль подтвержден

        bot_last_message = await message.answer(text="Пароль сессии установлен!\nВоспользуйтесь функционалом ниже:", reply_markup=keyboards.get_main_reply_keyboard())
        await state.update_data(bot_last_message=bot_last_message.message_id)

        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
        await bot.delete_message(chat_id=message.from_user.id, message_id=user_data["bot_last_message"])

        await state.set_state(my_states.States.passed)

        await mysql_client.user_add(telegram_id=message.from_user.id)
        
    else: # Если пароль не подтвержден
        await bot.edit_message_text(text="Пароли не совпадают!\nВведите новый пароль!", chat_id=message.from_user.id, message_id=user_data["bot_last_message"])
        
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)

        _ = user_data.pop("master_key")
        await state.set_data(user_data)
        await state.set_state(my_states.States.first_entering_master_key)
        
@router.message(
    F.text,
    my_states.States.entering_master_key
)
async def registration_confirm_master_key(
    message: types.Message,
    state: FSMContext,
    mysql_client: mysql.Client,
    bot: Bot
):
    user_data = await state.get_data()

    bot_last_message = await message.answer(text="Пароль сессии установлен!\nВоспользуйтесь функционалом ниже:", reply_markup=keyboards.get_main_reply_keyboard())
    await state.update_data(bot_last_message=bot_last_message.message_id)

    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    await bot.delete_message(chat_id=message.from_user.id, message_id=user_data["bot_last_message"])

    await state.update_data(master_key=message.text)
    await state.set_state(my_states.States.passed)
    await mysql_client.user_update_masterkey_lifetime(telegram_id=message.from_user.id)