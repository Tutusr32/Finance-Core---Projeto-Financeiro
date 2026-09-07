from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, field_serializer


class DashboardFilter(BaseModel):
    start_date: date | None = None
    end_date: date | None = None


class DashboardSummary(BaseModel):
    saldo_total: Decimal
    total_entradas: Decimal
    total_saidas: Decimal
    resultado: Decimal


class DashboardCategory(BaseModel):
    category: str
    type: Literal["entrada", "saida"]
    total: Decimal


class DashboardHistory(BaseModel):
    date: date
    entradas: Decimal
    saidas: Decimal


class ExpenseDistribution(BaseModel):
    category: str
    amount: Decimal
    percentage: Decimal

    @field_serializer("percentage")
    def serialize_percentage(self, value: Decimal) -> str:
        return f"{value:.2f}"


class DashboardInsight(BaseModel):
    type: Literal["info", "warning", "recommendation"]
    title: str
    description: str


class DashboardAnalysis(BaseModel):
    expense_distribution: list[ExpenseDistribution]
    insights: list[DashboardInsight]
