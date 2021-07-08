from pydantic import BaseModel


class TopUpRequest(BaseModel):
    amount: float


class TransferRequest(BaseModel):
    receiver_id: int
    amount: float


class ClientData(BaseModel):
    id: int
    balance: float
