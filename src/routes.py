from fastapi import APIRouter

import logic
from models import ClientData, TopUpRequest, TransferRequest

router = APIRouter()


@router.post("/client/", response_model=ClientData)
async def create_client():
    return await logic.create_client()


@router.get("/client/{client_id}", response_model=ClientData)
async def get_client(client_id: int):
    return await logic.get_client_by_id(client_id)


@router.post("/client/{client_id}/topup", response_model=ClientData)
async def top_up_client_balance(client_id: int, body: TopUpRequest):
    return await logic.top_up_client_balance(client_id, amount=body.amount)


@router.post("/client/{sender_id}/transfer", response_model=ClientData)
async def transfer_money(sender_id: int, body: TransferRequest):
    return await logic.transfer_money(sender_id, receiver_id=body.receiver_id, amount=body.amount)
