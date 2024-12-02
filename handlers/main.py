from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from modules.db import mysql
from modules.config import configJson

from keyboards import kb_start
import my_states
from texts import get_text

router = Router()


@router.message(Command("start"))
async def menu(
    message: types.Message,
    state: FSMContext,
    # mysql_client: mysql.Client,
    config_client: configJson.Client,
):
    await message.answer(get_text("menu"), reply_markup=kb_start.get_menu_ik())
    await state.set_state()
    await state.update_data({})


@router.callback_query(F.data == "check")
async def menu_callback(
    callback: types.CallbackQuery,
    state: FSMContext,
    # mysql_client: mysql.Client,
    config_client: configJson.Client,
):
    await callback.answer(get_text("check"))
