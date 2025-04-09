from typing import Any, Callable, Dict, Awaitable
from datetime import datetime

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from aiogram.dispatcher.flags import get_flag

from modules.common.my_class import Users
import my_states


class CheckMasterKeyLifeTime(BaseMiddleware):
    # def __init__(self, mysql_client):
    #     self.mysql_client = mysql_client

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        lifetime_flag = get_flag(data, "lifetime_check")

        user_data = await data["state"].get_data()
        if lifetime_flag:
            telegram_user = data["event_from_user"]
            if "masterkey_lifetime" in user_data:
                time_diff = datetime.now() - user_data["masterkey_lifetime"]
            else:
                try:
                    user: Users = await data["mysql_client"].user_get(telegram_id=telegram_user.id)
                except TypeError:
                    return await handler(event, data)
                time_diff = datetime.now() - user.masterkey_lifetime
            if (
                "master_key" in user_data and time_diff.seconds <= 600
            ):  # Если пароль существует и он "живой"
                return await handler(event, data)  # Запускаем хендлер
            else:  # Иначе просим мастер кей
                if isinstance(event, Message):
                    try:
                        await data["bot"].delete_message(
                            chat_id=telegram_user.id, message_id=user_data["bot_last_message"]
                        )
                    except:
                        pass
                    bot_last_message = await event.answer(
                        "Время жизни пароля вышло!\nВведите мастер-пароль:"
                    )
                    await data["state"].update_data(bot_last_message=bot_last_message.message_id)

                    await data["bot"].delete_message(
                        chat_id=telegram_user.id, message_id=event.message_id
                    )
                elif isinstance(event, CallbackQuery):
                    await data["bot"].edit_message_text(
                        chat_id=telegram_user.id,
                        message_id=event.message.message_id,
                        text="Время жизни пароля вышло!\nВведите мастер-пароль:",
                        reply_markup=None,
                    )

                await data["state"].set_state(my_states.States.entering_master_key)
                return
        else:
            await data["state"].update_data(masterkey_lifetime=datetime.now())
            return await handler(event, data)
