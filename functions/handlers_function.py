from math import ceil
from aiogram import Router, F, types, Bot, flags
from aiogram.fsm.context import FSMContext

from keyboards import keyboards
from modules.db import mysql

sorts = {0: "id ASC", 1: "service_name ASC", 2: "id DESC", 3: "service_name DESC"}


async def func_show_passwords(
    state: FSMContext,
    mysql_client: mysql.Client,
    message: types.Message = None,
    callback: types.CallbackQuery = None,
):
    user_data = await state.get_data()
    if message:
        user_id = message.from_user.id
    elif callback:
        user_id = callback.from_user.id
    else:
        raise TypeError
    passwords_count = await mysql_client.passwords_get_count(user_id)

    if passwords_count != 0:
        passwords: list = await mysql_client.passwords_get(
            telegram_id=user_id,
            limit=6,
            offset=int(user_data["current_page"] - 1),
            order_by=sorts[user_data["current_sort"]].split(" ")[0],
            sort_by=sorts[user_data["current_sort"]].split(" ")[1],
        )
        buttons_texts = [
            f"{passwords[i].service_name} - {passwords[i].login}" for i in range(0, len(passwords))
        ]
        buttons_callbacks = [f"password_{passwords[i].id}" for i in range(0, len(passwords))]

        if message:
            bot_last_message = await message.answer(
                text="Выберите сохраненную площадку или иное действие",
                reply_markup=keyboards.get_show_password_inline_keyboard(
                    buttons_texts,
                    buttons_callbacks,
                    user_data["current_page"],
                    ceil(passwords_count / 6),
                    sorts[user_data["current_sort"]],
                ),
            )
        elif callback:
            await callback.message.edit_text(
                text="Выберите сохраненную площадку или иное действие",
                reply_markup=keyboards.get_show_password_inline_keyboard(
                    buttons_texts,
                    buttons_callbacks,
                    user_data["current_page"],
                    ceil(passwords_count / 6),
                    sorts[user_data["current_sort"]],
                ),
            )
    else:
        if message:
            bot_last_message = await message.answer(
                text="У вас не сохранено ни одного пароля!\nВоспользуйтесь функционалом ниже:",
                reply_markup=keyboards.get_main_reply_keyboard(),
            )
        elif callback:
            await callback.message.answer(
                text="У вас не сохранено ни одного пароля!\nВоспользуйтесь функционалом ниже:",
                reply_markup=keyboards.get_main_reply_keyboard(),
            )
            await callback.message.delete()
        else:
            raise TypeError
    if message:
        await state.update_data(bot_last_message=bot_last_message.message_id)
