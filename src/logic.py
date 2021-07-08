import asyncpg

from models import ClientData
from utils import get_asyncpg_connection


async def create_client() -> ClientData:
    async with get_asyncpg_connection() as conn:
        record: asyncpg.Record = await conn.fetchrow(
            "INSERT INTO client_wallet(balance) VALUES (DEFAULT) RETURNING id, balance;"
        )
    return ClientData(id=record["id"], balance=record["balance"])


async def get_client_by_id(client_id: int):
    async with get_asyncpg_connection() as conn:
        record: asyncpg.Record = await conn.fetchrow("SELECT id, balance FROM client_wallet WHERE id = $1", client_id)
    return record


async def top_up_client_balance(client_id: int, *, amount: float):
    async with get_asyncpg_connection() as conn:
        async with conn.transaction():
            record: asyncpg.Record = await conn.fetchrow(
                "UPDATE client_wallet SET balance = balance + $1 WHERE id = $2 RETURNING id, balance",
                amount,
                client_id,
            )
            await conn.execute(
                "INSERT INTO refill_history(client_id, amount) VALUES ($1, $2)", client_id, amount,
            )
    return ClientData(id=record["id"], balance=record["balance"])


async def transfer_money(sender_id: int, *, receiver_id: int, amount: float):
    async with get_asyncpg_connection() as conn:
        async with conn.transaction():
            record: asyncpg.Record = await conn.fetchrow(
                "UPDATE client_wallet SET balance = balance - $1 WHERE id = $2 RETURNING id, balance",
                amount,
                sender_id,
            )
            await conn.execute("UPDATE client_wallet SET balance = balance + $1 WHERE id = $2", amount, receiver_id)
            await conn.execute(
                "INSERT INTO transaction_history(receiver_id, sender_id, amount) VALUES ($1, $2, $3)",
                receiver_id,
                sender_id,
                amount,
            )
    return ClientData(id=record["id"], balance=record["balance"])
