import asyncio
import logging
from modules.logging import logging_tuner
from start import start_bot
from functions.common import set_terminal_title


async def main():
    logging.info("Либы загружены")
    set_terminal_title("Bainal_Telegram_PassBank")
    logging.info("Поменяли название")
    logging.info("Запускаем бота")
    await start_bot()


if __name__ == "__main__":
    logging_tuner.set()
    asyncio.run(main())
