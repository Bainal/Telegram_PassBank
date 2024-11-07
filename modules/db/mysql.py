from datetime import datetime
from typing import Any, Callable, TypeVar, cast
from aiomysql import create_pool, Cursor
from .settings import setting_insert_query, setting_insert_args
from modules.common.my_class import Users


# Определяем универсальный тип, который будет представлять функцию
F = TypeVar("F", bound=Callable[..., Any])


def with_connection_and_cursor(func: F) -> F:
    async def wrapper(self, *args, **kwargs):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Вызов оригинальной функции с передачей соединения и курсора
                return await func(self, cur, *args, **kwargs)

    return cast(F, wrapper)


class Client(object):
    def __init__(self):
        self.pool = None

    async def init_async(self, host: str, user: str, password: str, database: str):
        self.pool = await create_pool(
            host=host,
            user=user,
            password=password,
            db=database,
            minsize=1,
            maxsize=5,
            autocommit=True,
        )
        await self.create_setting()

    @with_connection_and_cursor
    async def create_setting(self, cur: Cursor):
        await cur.executemany(setting_insert_query, setting_insert_args)
        await cur.connection.commit()

    @with_connection_and_cursor
    async def setting_get(self, cur: Cursor, name: str) -> str:
        await cur.execute("""SELECT value FROM settings WHERE name = %s""", (name,))
        data = (await cur.fetchone())[0]
        return data

    @with_connection_and_cursor
    async def user_add(
        self, cur: Cursor, telegram_id: int, masterkey_lifetime: datetime = datetime.now()
    ) -> str:
        await cur.execute(
            """
                INSERT INTO Users
                    (telegram_id, masterkey_lifetime)
                    VALUES (%s, %s)
            """,
            (telegram_id, masterkey_lifetime),
        )

    @with_connection_and_cursor
    async def user_get(self, cur: Cursor, telegram_id: int) -> str:
        await cur.execute(
            """
                SELECT id, telegram_id, masterkey_lifetime
                    FROM Users
                    WHERE telegram_id = %s
            """,
            (telegram_id,),
        )
        data = await cur.fetchone()
        user = Users(*data)
        return user

    @with_connection_and_cursor
    async def user_update_masterkey_lifetime(self, cur: Cursor, telegram_id: int):
        await cur.execute(
            """
                UPDATE Users
                    SET
                        masterkey_lifetime=NOW()
                    WHERE 
                        telegram_id = %s
            """,
            (telegram_id,),
        )
