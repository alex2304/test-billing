from fastapi import APIRouter, HTTPException

import logic
from errors import ReceiverNotFound, InsufficientBalance
from models import ClientData, TopUpRequest, TransferRequest

router = APIRouter()


@router.post("/client/", response_model=ClientData)
async def create_client():
    return await logic.create_client()


@router.get("/client/{client_id}", response_model=ClientData)
async def get_client(client_id: int):
    client_data: ClientData = await logic.get_client_by_id(client_id)
    if client_data is None:
        raise HTTPException(status_code=404, detail="No client with such id")
    return client_data


@router.post("/client/{client_id}/topup", response_model=ClientData)
async def top_up_client_balance(client_id: int, body: TopUpRequest):
    client_data: ClientData = await logic.top_up_client_balance(client_id, amount=body.amount)
    if client_data is None:
        raise HTTPException(status_code=404, detail="No client with such id")
    return client_data


@router.post("/client/{sender_id}/transfer", response_model=ClientData)
async def transfer_money(sender_id: int, body: TransferRequest):
    if sender_id == body.receiver_id:
        raise HTTPException(status_code=422, detail="Sender and receiver must be different")

    try:
        client_data: ClientData = await logic.transfer_money(
            sender_id, receiver_id=body.receiver_id, amount=body.amount
        )
    except ReceiverNotFound:
        raise HTTPException(status_code=422, detail="No receiver with such id")
    except InsufficientBalance:
        raise HTTPException(status_code=422, detail="Sender doesn't have enough balance")

    if client_data is None:
        raise HTTPException(status_code=404, detail="No sender with such id")

    return client_data
