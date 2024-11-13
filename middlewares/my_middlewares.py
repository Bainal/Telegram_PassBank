from typing import Any, Callable, Dict, Awaitable
from datetime import datetime

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.dispatcher.flags import get_flag
import aiogram.dispatcher.flags as BIBA

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
        # authorization = get_flag(data, "authorization")
        user_data = await data["state"].get_data()

        if await data["state"].get_state() == my_states.States.passed:
            telegram_user = data["event_from_user"]
            user: Users = await data["mysql_client"].user_get(telegram_id=telegram_user.id)
            time_diff = datetime.now() - user.masterkey_lifetime
            if time_diff.seconds <= 600:  # Если мастер-кей живой
                return await handler(event, data)
            else:
                if event.message is not None:
                    try:
                        await data["bot"].delete_message(
                            chat_id=telegram_user.id, message_id=user_data["bot_last_message"]
                        )
                    except:
                        pass
                    bot_last_message = await event.message.answer(
                        "Время жизни пароля вышло!\nВведите мастер-пароль:"
                    )
                    await data["state"].update_data(bot_last_message=bot_last_message.message_id)

                    await data["bot"].delete_message(
                        chat_id=telegram_user.id, message_id=event.message.message_id
                    )
                elif event.callback_query is not None:
                    # bot_last_message = await event.callback_query.answer(
                    #     "Время жизни пароля вышло!\nВведите мастер-пароль:", show_alert=False
                    # )
                    await data["bot"].edit_message_text(
                        chat_id=telegram_user.id,
                        message_id=user_data["bot_last_message"],
                        text="Время жизни пароля вышло!\nВведите мастер-пароль:",
                        reply_markup=None,
                    )

                await data["state"].set_state(my_states.States.entering_master_key)
                return
        else:
            return await handler(event, data)

        # user = data["event_from_user"]
        # user: Users = await data["mysql_client"].user_get(telegram_id=user.id)
        # time_diff = datetime.now() - user.masterkey_lifetime
        # if time_diff.seconds <= 600:  # Если мастер-кей живой
        #     return await handler(event, data)
        # else:
        #     user_data = await data["state"].get_data()

        #     await data["bot"].delete_message(
        #         chat_id=user.id, message_id=user_data["bot_last_message"]
        #     )
        #     bot_last_message = await event.message.answer(text="Введите мастер-пароль")
        #     await data["state"].update_data(bot_last_message=bot_last_message.message_id)

        #     await data["bot"].delete_message(chat_id=user.id, message_id=event.message.message_id)

        #     await data["state"].set_state(my_states.States.entering_master_key)

        #     await event.answer("Время жизни пароля вышло!\nВведите мастер-пароль:")

        #     return
