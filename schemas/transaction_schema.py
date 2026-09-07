from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field


class TransactionCreate(BaseModel):
    type: Literal["entrada", "saida"]
    amount: Decimal = Field(gt=0)
    category: str = Field(min_length=2, max_length=30)


class TransactionFilter(BaseModel):
    type: Literal["entrada", "saida"] | None = None
    category: str | None = Field(default=None, min_length=2, max_length=30)
    start_date: date | None = None
    end_date: date | None = None


class TransactionResponse(BaseModel):
    id: int
    conta_id: int
    type: Literal["entrada", "saida"]
    amount: Decimal = Field(gt=0)
    category: str = Field(min_length=2, max_length=30)
    data: str | None = None

    class Config:
        from_attributes = True
