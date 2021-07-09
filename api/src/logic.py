from typing import Optional

import asyncpg

from errors import ReceiverNotFound, InsufficientBalance, ClientNotFound
from models import ClientData
from utils import get_asyncpg_connection


async def create_client() -> ClientData:
    async with get_asyncpg_connection() as conn:
        record: asyncpg.Record = await conn.fetchrow(
            "INSERT INTO client_wallet(balance) VALUES (DEFAULT) RETURNING id, balance;"
        )
    return ClientData(id=record["id"], balance=record["balance"])


async def get_client_by_id(client_id: int) -> Optional[ClientData]:
    async with get_asyncpg_connection() as conn:
        record: asyncpg.Record = await conn.fetchrow("SELECT id, balance FROM client_wallet WHERE id = $1", client_id)
    return ClientData(id=record["id"], balance=record["balance"]) if record is not None else None


async def top_up_client_balance(client_id: int, *, amount: float) -> Optional[ClientData]:
    async with get_asyncpg_connection() as conn:
        try:
            async with conn.transaction():
                record = await conn.fetchrow(
                    "UPDATE client_wallet SET balance = balance + $1 WHERE id = $2 RETURNING id, balance",
                    amount,
                    client_id,
                )
                # need to rollback transaction, even if it doesn't contain any active changes
                if record is None:
                    raise ClientNotFound
                await conn.execute(
                    "INSERT INTO refill_history(client_id, amount) VALUES ($1, $2)", client_id, amount,
                )
        except ClientNotFound:
            # at this point, transaction will be rollbacked due to exception
            return None

    return ClientData(id=record["id"], balance=record["balance"])


async def transfer_money(sender_id: int, *, receiver_id: int, amount: float) -> Optional[ClientData]:
    async with get_asyncpg_connection() as conn:
        try:
            async with conn.transaction():
                record: asyncpg.Record = await conn.fetchrow(
                    "UPDATE client_wallet SET balance = balance - $1 WHERE id = $2 RETURNING id, balance",
                    amount,
                    sender_id,
                )
                if record is None:
                    raise ClientNotFound
                if record["balance"] < 0:
                    raise InsufficientBalance
                receiver_record = await conn.execute(
                    "UPDATE client_wallet SET balance = balance + $1 WHERE id = $2 RETURNING id", amount, receiver_id
                )
                if receiver_record is None:
                    raise ReceiverNotFound
                await conn.execute(
                    "INSERT INTO transaction_history(receiver_id, sender_id, amount) VALUES ($1, $2, $3)",
                    receiver_id,
                    sender_id,
                    amount,
                )
        except ClientNotFound:
            return None

    return ClientData(id=record["id"], balance=record["balance"])
