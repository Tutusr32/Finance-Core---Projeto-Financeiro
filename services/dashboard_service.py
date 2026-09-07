from decimal import Decimal

from repositories.dashboard_repository import DashboardRepository
from schemas.dashboard_schema import (
    DashboardAnalysis,
    DashboardCategory,
    DashboardHistory,
    DashboardHistoryItem,
    DashboardInsight,
    DashboardSummary,
    ExpenseDistribution,
)


class DashboardService:
    def __init__(self, repository: DashboardRepository):
        self.repository = repository

    def get_summary(
        self,
        user_id: int,
        start_date,
        end_date,
    ) -> DashboardSummary:
        saldo_total = self.repository.get_total_balance(user_id)

        summary = self.repository.get_summary(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
        )

        total_entradas = summary.total_income
        total_saidas = summary.total_expense
        resultado = total_entradas - total_saidas

        return DashboardSummary(
            saldo_total=saldo_total,
            total_entradas=total_entradas,
            total_saidas=total_saidas,
            resultado=resultado,
        )

    def get_category_summary(
        self,
        user_id: int,
        start_date,
        end_date,
    ) -> list[DashboardCategory]:
        categories = self.repository.get_category_summary(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
        )

        return [
            DashboardCategory(
                category=category,
                type=transaction_type,
                total=total,
            )
            for category, transaction_type, total in categories
        ]

    def get_history(
        self,
        user_id: int,
        start_date,
        end_date,
    ) -> DashboardHistory:
        initial_balance = self.repository.get_initial_balance(
            user_id=user_id,
            start_date=start_date,
        )

        history = self.repository.get_history(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
        )

        current_balance = initial_balance
        history_items = []

        for date, entradas, saidas in history:
            variacao = entradas - saidas
            current_balance += variacao

            history_items.append(
                DashboardHistoryItem(
                    date=date,
                    entradas=entradas,
                    saidas=saidas,
                    variacao=variacao,
                    saldo=current_balance,
                )
            )

        return DashboardHistory(
            start_date=start_date,
            end_date=end_date,
            saldo_inicial=initial_balance,
            saldo_final=current_balance,
            historico=history_items,
        )

    def get_analysis(
        self,
        user_id: int,
        start_date,
        end_date,
    ) -> DashboardAnalysis:
        analysis = self.repository.get_analysis(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
        )

        total_expenses = sum(
            (amount for _, amount in analysis),
            Decimal("0"),
        )

        expense_distribution = []

        for category, amount in analysis:
            percentage = (
                (amount / total_expenses) * Decimal("100") if total_expenses > 0 else Decimal("0")
            )

            expense_distribution.append(
                ExpenseDistribution(
                    category=category,
                    amount=amount,
                    percentage=percentage,
                )
            )

        insights = self._generate_insights(expense_distribution)

        return DashboardAnalysis(
            expense_distribution=expense_distribution,
            insights=insights,
        )

    def _generate_insights(
        self,
        distribution: list[ExpenseDistribution],
    ) -> list[DashboardInsight]:

        insights = []

        if not distribution:
            return insights

        biggest_category = distribution[0]

        if biggest_category.percentage >= Decimal("40"):
            insights.append(
                DashboardInsight(
                    type="warning",
                    title="Alta concentração de gastos",
                    description=(
                        f"{biggest_category.percentage:.2f}% "
                        f"das suas despesas estão em "
                        f"{biggest_category.category}."
                    ),
                )
            )

        elif biggest_category.percentage >= Decimal("25"):
            insights.append(
                DashboardInsight(
                    type="info",
                    title="Principal categoria de gasto",
                    description=(
                        f"{biggest_category.category} representa "
                        f"{biggest_category.percentage:.2f}% "
                        f"das suas despesas."
                    ),
                )
            )

        if len(distribution) >= 3:
            top_three_percentage = sum(
                (item.percentage for item in distribution[:3]),
                Decimal("0"),
            )

            if top_three_percentage >= Decimal("70"):
                insights.append(
                    DashboardInsight(
                        type="recommendation",
                        title="Despesas concentradas",
                        description=(
                            f"As três maiores categorias representam "
                            f"{top_three_percentage:.2f}% "
                            f"das suas despesas."
                        ),
                    )
                )

        return insights
