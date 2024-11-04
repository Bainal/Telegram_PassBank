import asyncio
from datetime import datetime, time, timedelta
import io
import logging
from pathlib import Path
from random import randint

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramNetworkError
from aiogram.types import (
    BufferedInputFile,
    FSInputFile,
    ChatMemberMember,
    ChatMemberAdministrator,
    ChatMemberOwner,
    ChatMemberRestricted,
)
from aiogram.utils.media_group import MediaGroupBuilder

from modules.db import mysql
from modules.config import configJson


async def start_regular_wrap(
    bot: Bot, mysql_client: mysql.Client, config_client: configJson.Client
):
    asyncio.create_task(start_check_timer(bot, mysql_client))


async def start_check_timer(
    bot: Bot,
    mysql_client: mysql.Client,
):
    while True:
        pass
