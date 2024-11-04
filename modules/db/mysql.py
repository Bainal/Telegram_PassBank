from typing import Any, Callable, TypeVar, cast
from aiomysql import create_pool, Cursor
from .settings import setting_insert_query, setting_insert_args


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