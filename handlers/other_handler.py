from datetime import datetime

from aiogram import Router, F, types, Bot, flags
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


@router.message()
@flags.lifetime_check
async def another_message(message: types.Message, state: FSMContext, bot: Bot):
    # user_data = await state.get_data()

    # try:
    #     await bot.edit_message_text(text="Я такого не знаю!", chat_id=message.from_user.id, message_id=user_data["bot_last_message"])
    # except TelegramBadRequest:
    #     if "bot_last_message" in user_data:
    #         await bot.delete_message(chat_id=message.from_user.id, message_id=user_data["bot_last_message"])
    #     bot_last_message = await message.answer("Я такого не знаю!")
    #     await state.update_data(bot_last_message=bot_last_message.message_id)
    # except KeyError:
    #     if "bot_last_message" in user_data:
    #         await bot.delete_message(chat_id=message.from_user.id, message_id=user_data["bot_last_message"])
    #     bot_last_message = await message.answer("Я такого не знаю!")
    #     await state.update_data(bot_last_message=bot_last_message.message_id)

    # await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
