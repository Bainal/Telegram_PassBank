import asyncio
import logging
from pathlib import Path
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from modules.config import configJson
from modules.db import mysql
from functions.regular import start_regular_wrap
from routers import routers as routs
from middlewares.my_middlewares import CheckMasterKeyLifeTime


async def on_start(
    bot: Bot,
    mysql_client: mysql.Client,
    config_client: configJson.Client,
):
    # await start_regular_wrap(bot, mysql_client, config_client)
    # logging.info("Циклы запущены")
    pass


async def start_bot():
    config_client = configJson.Client(Path("config.ini"))

    # База данных
    mysql_client = mysql.Client()
    host = config_client.get_setting("mysql", "host")
    user = config_client.get_setting("mysql", "user")
    password = config_client.get_setting("mysql", "password")
    database = config_client.get_setting("mysql", "database")
    await mysql_client.init_async(host=host, user=user, password=password, database=database)

    bot = Bot(token=config_client.get_setting("settings", "token"))
    dp = Dispatcher()

    dp.update.outer_middleware.register(CheckMasterKeyLifeTime())

    dp.include_routers(*routs)

    dp.startup.register(on_start)

    # Убираем сообщения, которые пришли до запуска
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, mysql_client=mysql_client, config_client=config_client)
    # await dp.start_polling(bot, config_client=config_client)
