from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ContaCreate(BaseModel):
    name: str = Field(..., min_length=1)
    saldo: Decimal = Field(default=0)


class ContaResponse(BaseModel):
    id: int
    user_id: int
    name: str
    saldo: Decimal
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ContaUpdate(BaseModel):
    name: str | None = None
    saldo: Decimal | None = None
