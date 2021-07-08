import contextlib

import asyncpg


@contextlib.asynccontextmanager
async def get_asyncpg_connection() -> asyncpg.connection.Connection:
    conn = await asyncpg.connect(user="postgres", password="postgres", database="postgres", host="127.0.0.1")
    try:
        yield conn
    finally:
        await conn.close()
