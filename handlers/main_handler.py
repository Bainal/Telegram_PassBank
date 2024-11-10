from datetime import datetime

from aiogram import Router, F, types, Bot
from aiogram.enums import ParseMode
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from modules.db import mysql
from modules.config import configJson
from modules.common.my_class import Users
from modules.common import encryption, my_class

from keyboards import keyboards
import my_states
from texts import get_text

router = Router()


@router.message(F.text == "Показать пароли", my_states.States.passed)
async def show_passwords(
    message: types.Message,
    state: FSMContext,
    mysql_client: mysql.Client,
    bot: Bot,
):
    await state.update_data(current_page=1)
    passwords_count = await mysql_client.passwords_get_count(message.from_user.id)

    user_data = await state.get_data()

    passwords: list = await mysql_client.passwords_get(
        telegram_id=message.from_user.id, limit=10, offset=0
    )
    buttons_texts = [
        f"{passwords[i].service_name} - {passwords[i].login}" for i in range(0, len(passwords))
    ]
    buttons_callbacks = [f"password_{passwords[i].id}" for i in range(0, len(passwords))]

    await bot.delete_message(
        chat_id=message.from_user.id, message_id=user_data["bot_last_message"]
    )

    bot_last_message = await message.answer(
        text="Выберите сохраненную площадку или иное действие",
        reply_markup=keyboards.get_show_password_inline_keyboard(
            buttons_texts,
            buttons_callbacks,
            user_data["current_page"],
            int(passwords_count / 10) + 1,
        ),
    )
    await state.update_data(bot_last_message=bot_last_message.message_id)

    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)


@router.callback_query(F.data.startswith("password_"), my_states.States.passed)
async def show_password(
    callback: types.CallbackQuery,
    state: FSMContext,
    mysql_client: mysql.Client,
    bot: Bot,
):
    await state.update_data(choising_password_id=callback.data.replace("password_", ""))

    user_data = await state.get_data()

    password: my_class.Passwords = await mysql_client.password_get_by_id(
        user_data["choising_password_id"]
    )
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=user_data["bot_last_message"],
        text=f"Текст доступен для копирования\nПлощадка: `{password.service_name}`\nЛогин: `{password.login}`\nПароль: `{encryption.decrypt_password(password.password, user_data["master_key"])}`",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=keyboards.get_password_inline_keyboard(),
    )


@router.callback_query(F.data == "back_cb", my_states.States.passed)
async def back_to_show_passwords(
    callback: types.CallbackQuery,
    state: FSMContext,
    mysql_client: mysql.Client,
    bot: Bot,
):
    user_data = await state.get_data()
    passwords_count = await mysql_client.passwords_get_count(callback.from_user.id)
    passwords: list = await mysql_client.passwords_get(
        telegram_id=callback.from_user.id, limit=10, offset=0
    )

    buttons_texts = [
        f"{passwords[i].service_name} - {passwords[i].login}" for i in range(0, len(passwords))
    ]
    buttons_callbacks = [f"password_{passwords[i].id}" for i in range(0, len(passwords))]
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=user_data["bot_last_message"],
        text="Выберите сохраненную площадку или иное действие",
        reply_markup=keyboards.get_show_password_inline_keyboard(
            buttons_texts,
            buttons_callbacks,
            user_data["current_page"],
            int(passwords_count / 10) + 1,
        ),
    )


@router.callback_query(F.data == "delete_cb", my_states.States.passed)
async def delete_passwords(
    callback: types.CallbackQuery,
    state: FSMContext,
    mysql_client: mysql.Client,
    bot: Bot,
):
    user_data = await state.get_data()
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=user_data["bot_last_message"],
        text=callback.message.text + "\n\nПодтвердите удаление данных",
        reply_markup=keyboards.get_confirmation_inline_keyboard(),
    )


@router.callback_query(F.data == "answer_yes_cb", my_states.States.passed)
async def yes_delete_passwords(
    callback: types.CallbackQuery,
    state: FSMContext,
    mysql_client: mysql.Client,
    bot: Bot,
):
    user_data = await state.get_data()

    await mysql_client.password_delete(
        telegram_id=callback.from_user.id, id=int(user_data["choising_password_id"])
    )
    await callback.answer("Пароль был успешно удален!", show_alert=True)

    passwords_count = await mysql_client.passwords_get_count(callback.from_user.id)
    passwords: list = await mysql_client.passwords_get(
        telegram_id=callback.from_user.id, limit=10, offset=0
    )
    buttons_texts = [
        f"{passwords[i].service_name} - {passwords[i].login}" for i in range(0, len(passwords))
    ]
    buttons_callbacks = [f"password_{passwords[i].id}" for i in range(0, len(passwords))]
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=user_data["bot_last_message"],
        text="Выберите сохраненную площадку или иное действие",
        reply_markup=keyboards.get_show_password_inline_keyboard(
            buttons_texts,
            buttons_callbacks,
            user_data["current_page"],
            int(passwords_count / 10) + 1,
        ),
    )


@router.callback_query(F.data == "answer_no_cb", my_states.States.passed)
async def no_delete_passwords(
    callback: types.CallbackQuery,
    state: FSMContext,
    mysql_client: mysql.Client,
    bot: Bot,
):
    user_data = await state.get_data()
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=user_data["bot_last_message"],
        text=callback.message.text.replace("\n\nПодтвердите удаление данных", ""),
        reply_markup=keyboards.get_password_inline_keyboard(),
    )


@router.message(F.text == "Добавить пароль", my_states.States.passed)
async def add_password(
    message: types.Message, state: FSMContext, mysql_client: mysql.Client, bot: Bot
):
    await state.update_data(service_name=None)
    await state.update_data(login=None)
    await state.update_data(password=None)

    user_data = await state.get_data()
    await bot.delete_message(
        chat_id=message.from_user.id, message_id=user_data["bot_last_message"]
    )
    bot_last_message = await message.answer(
        text=get_text("add_password_main_text"),
        reply_markup=keyboards.get_entering_data_inline_keyboard(
            user_data["service_name"], user_data["login"], user_data["password"]
        ),
    )
    await state.update_data(bot_last_message=bot_last_message.message_id)
    await state.set_state(my_states.States.entering_all_data)

    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)


@router.message(F.text.split("\n").len() == 3, my_states.States.entering_all_data)
async def text_all_data(
    message: types.Message, state: FSMContext, mysql_client: mysql.Client, bot: Bot
):
    data = message.text.split("\n")
    await state.update_data(service_name=data[0], login=data[1], password=data[2])

    user_data = await state.get_data()
    await bot.delete_message(
        chat_id=message.from_user.id, message_id=user_data["bot_last_message"]
    )
    bot_last_message = await message.answer(
        text=get_text("add_password_main_text"),
        reply_markup=keyboards.get_entering_data_inline_keyboard(
            user_data["service_name"], user_data["login"], user_data["password"]
        ),
    )
    await state.update_data(bot_last_message=bot_last_message.message_id)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)


@router.callback_query(F.data.startswith("entering_"), my_states.States.entering_all_data)
async def change_service_name(
    callback: types.CallbackQuery,
    state: FSMContext,
    mysql_client: mysql.Client,
    bot: Bot,
):
    data_name = callback.data.replace("entering_", "")
    await state.update_data(data_name=data_name)

    await callback.message.edit_text(text=get_text(f"{data_name}_request"), reply_markup=None)
    await state.set_state(my_states.States.entering_data)


@router.message(F.text, my_states.States.entering_data)
async def entering_data(
    message: types.Message, state: FSMContext, mysql_client: mysql.Client, bot: Bot
):
    user_data = await state.get_data()

    data = {user_data["data_name"]: message.text}
    user_data[user_data["data_name"]] = message.text

    await state.update_data(data)
    await state.set_state(my_states.States.entering_all_data)

    await bot.delete_message(
        chat_id=message.from_user.id, message_id=user_data["bot_last_message"]
    )
    bot_last_message = await message.answer(
        text=get_text("add_password_main_text"),
        reply_markup=keyboards.get_entering_data_inline_keyboard(
            user_data["service_name"], user_data["login"], user_data["password"]
        ),
    )
    await state.update_data(bot_last_message=bot_last_message.message_id)

    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)


@router.callback_query(F.data == "exit_cb", my_states.States.passed)
@router.callback_query(F.data == "exit_cb", my_states.States.entering_all_data)
async def entering_password_exit(
    callback: types.CallbackQuery,
    state: FSMContext,
    mysql_client: mysql.Client,
    bot: Bot,
):
    user_data = await state.get_data()
    await bot.delete_message(
        chat_id=callback.from_user.id, message_id=user_data["bot_last_message"]
    )

    bot_last_message = await callback.message.answer(
        text="Воспользуйтесь функционалом ниже:",
        reply_markup=keyboards.get_main_reply_keyboard(),
    )
    await state.set_data(
        {
            "bot_last_message": bot_last_message.message_id,
            "master_key": user_data["master_key"],
        }
    )
    await state.set_state(my_states.States.passed)


@router.callback_query(F.data == "save_cb", my_states.States.entering_all_data)
async def save(
    callback: types.CallbackQuery,
    state: FSMContext,
    mysql_client: mysql.Client,
    bot: Bot,
):
    user_data = await state.get_data()

    data_names = ("service_name", "login", "password")
    error_message = ""
    for i in data_names:
        if user_data[i] is None:
            error_message += f"\n{get_text(f"{i}_request")}"

    if len(error_message) > 0:
        await callback.answer(text="Ошибка!" + error_message, show_alert=True)
        return

    await mysql_client.password_add(
        telegram_id=callback.from_user.id,
        service_name=user_data["service_name"],
        login=user_data["login"],
        password=encryption.encrypt_password(
            password=user_data["password"], user_password=user_data["master_key"]
        ),
    )
    await callback.answer(text="Пароль зашифрован и успешно сохранен!", show_alert=True)

    await bot.delete_message(
        chat_id=callback.from_user.id, message_id=user_data["bot_last_message"]
    )

    bot_last_message = await callback.message.answer(
        text="Воспользуйтесь функционалом ниже:",
        reply_markup=keyboards.get_main_reply_keyboard(),
    )
    await state.set_data(
        {
            "bot_last_message": bot_last_message.message_id,
            "master_key": user_data["master_key"],
        }
    )
    await state.set_state(my_states.States.passed)
