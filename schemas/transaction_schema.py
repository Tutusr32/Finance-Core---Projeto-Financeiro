from pydantic import BaseModel, Field
from decimal import Decimal


class TransactionCreate(BaseModel):
    user_id: int = Field(..., description="ID do usuário dono da conta")
    conta_id: int = Field(..., description="ID da conta relacionada à transação")
    type: str = Field(..., description="Tipo da transação: entrada ou saída")
    amount: Decimal = Field(..., description="Valor da transação")
    category: str = Field(default="geral", description="Categoria da transação")


class TransactionResponse(BaseModel):
    id: int
    conta_id: int
    type: str
    amount: Decimal
    category: str
    data: str | None = None

    class Config:
        from_attributes = True
