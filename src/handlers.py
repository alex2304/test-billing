import asyncpg
from fastapi import APIRouter

from models import ClientResponse, TopUpRequest, TransferRequest

router = APIRouter()


@router.post("/client/", response_model=ClientResponse)
async def create_client() -> ClientResponse:
    conn = await asyncpg.connect(user="postgres", password="postgres", database="postgres", host="127.0.0.1")
    record: asyncpg.Record = await conn.fetchrow(
        "INSERT INTO client_wallet(balance) VALUES (DEFAULT) RETURNING id, balance;"
    )
    await conn.close()
    return ClientResponse(id=record["id"], balance=record["balance"])


@router.get("/client/{client_id}", response_model=ClientResponse)
async def get_client(client_id: int):
    conn = await asyncpg.connect(user="postgres", password="postgres", database="postgres", host="127.0.0.1")
    record: asyncpg.Record = await conn.fetchrow("SELECT id, balance FROM client_wallet WHERE id = $1", client_id)
    await conn.close()
    return ClientResponse(id=record["id"], balance=record["balance"])


@router.post("/client/{client_id}/topup", response_model=ClientResponse)
async def top_up_client_balance(client_id: int, body: TopUpRequest):
    conn = await asyncpg.connect(user="postgres", password="postgres", database="postgres", host="127.0.0.1")
    async with conn.transaction():
        record: asyncpg.Record = await conn.fetchrow(
            "UPDATE client_wallet SET balance = balance + $1 WHERE id = $2 RETURNING id, balance",
            body.amount,
            client_id,
        )
        await conn.execute(
            "INSERT INTO refill_history(client_id, amount) VALUES ($1, $2)", client_id, body.amount,
        )
    await conn.close()
    return ClientResponse(id=record["id"], balance=record["balance"])


@router.post("/client/{sender_id}/transfer", response_model=ClientResponse)
async def transfer_money(sender_id: int, body: TransferRequest):
    conn = await asyncpg.connect(user="postgres", password="postgres", database="postgres", host="127.0.0.1")
    async with conn.transaction():
        record = await conn.fetchrow(
            "UPDATE client_wallet SET balance = balance - $1 WHERE id = $2 RETURNING id, balance",
            body.amount,
            sender_id,
        )
        await conn.execute(
            "UPDATE client_wallet SET balance = balance + $1 WHERE id = $2", body.amount, body.receiver_id
        )
        await conn.execute(
            "INSERT INTO transaction_history(receiver_id, sender_id, amount) VALUES ($1, $2, $3)",
            body.receiver_id,
            sender_id,
            body.amount,
        )
    await conn.close()
    return ClientResponse(id=record["id"], balance=record["balance"])
