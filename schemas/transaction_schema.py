from pydantic import BaseModel, Field
from decimal import Decimal


class TransactionCreate(BaseModel):
    type: str
    amount: Decimal
    category: str


class TransactionResponse(BaseModel):
    id: int
    conta_id: int
    type: str
    amount: Decimal
    category: str
    data: str | None = None

    class Config:
        from_attributes = True
