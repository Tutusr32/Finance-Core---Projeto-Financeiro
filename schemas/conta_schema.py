from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ContaCreate(BaseModel):
    name: str
    saldo: Decimal
    user_id: int


class ContaResponse(BaseModel):
    id: int
    user_id: int
    name: str
    saldo: Decimal

    model_config = ConfigDict(from_attributes=True)


class ContaUpdate(BaseModel):
    name: str | None = None
    saldo: Decimal | None = None
