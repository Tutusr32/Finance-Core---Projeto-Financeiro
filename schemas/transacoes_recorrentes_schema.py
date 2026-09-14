from datetime import date, datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class TransacaoRecorrenteCreate(BaseModel):
    conta_id: int
    tipo: Literal["entrada", "saida"]
    valor: Decimal = Field(gt=0)
    categoria: str = Field(min_length=1, max_length=50)
    frequencia: Literal["semanal", "quinzenal", "mensal"]
    data_inicio: date


class TransacaoRecorrenteUpdate(BaseModel):
    valor: Decimal | None = Field(default=None, gt=0)
    categoria: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
    )
    frequencia: Literal["semanal", "quinzenal", "mensal"] | None = None
    ativo: bool | None = None


class TransacaoRecorrenteResponse(BaseModel):
    id: int
    conta_id: int
    tipo: Literal["entrada", "saida"]
    valor: Decimal
    categoria: str
    frequencia: Literal["semanal", "quinzenal", "mensal"]
    data_inicio: date
    proxima_data: date
    ativo: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
