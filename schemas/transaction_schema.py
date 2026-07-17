from pydantic import BaseModel, Field
from typing import Literal
from decimal import Decimal


class TransactionCreate(BaseModel):
    type: Literal["entrada", "saida"]
    amount: Decimal = Field(gt=0)
    category: str = Field(min_length=2, max_length=30)


class TransactionResponse(BaseModel):
    id: int
    conta_id: int
    type: Literal["entrada", "saida"]
    amount: Decimal = Field(gt=0)
    category: str = Field(min_length=2, max_length=30)
    data: str | None = None

    class Config:
        from_attributes = True
