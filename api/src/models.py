from pydantic import BaseModel, validator


class TopUpRequest(BaseModel):
    amount: float

    @validator("amount")
    def amount_must_be_greater_0(cls, v):
        if v <= 0:
            raise ValueError("amount must be greater than 0")
        return v


class TransferRequest(BaseModel):
    receiver_id: int
    amount: float

    @validator("amount")
    def amount_must_be_greater_0(cls, v):
        if v <= 0:
            raise ValueError("amount must be greater than 0")
        return v


class ClientData(BaseModel):
    id: int
    balance: float
