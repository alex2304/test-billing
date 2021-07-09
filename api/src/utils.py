import contextlib

import asyncpg

import settings


@contextlib.asynccontextmanager
async def get_asyncpg_connection() -> asyncpg.connection.Connection:
    conn = await asyncpg.connect(
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        database=settings.POSTGRES_DB,
        host=settings.POSTGRES_HOST,
    )
    try:
        yield conn
    finally:
        await conn.close()
