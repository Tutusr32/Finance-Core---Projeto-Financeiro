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
        expense_analysis = self.repository.get_analysis(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
        )

        summary = self.repository.get_summary(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
        )

        total_expenses = sum(
            (amount for _, amount in expense_analysis),
            Decimal("0"),
        )

        expense_distribution = [
            ExpenseDistribution(
                category=category,
                amount=amount,
                percentage=(
                    (amount / total_expenses) * Decimal("100")
                    if total_expenses > 0
                    else Decimal("0")
                ),
            )
            for category, amount in expense_analysis
        ]

        insights = self._generate_insights(
            total_income=summary.total_income,
            total_expenses=summary.total_expense,
            expense_distribution=expense_distribution,
        )

        return DashboardAnalysis(
            expense_distribution=expense_distribution,
            insights=insights,
        )

    def _generate_insights(
        self,
        total_income: Decimal,
        total_expenses: Decimal,
        expense_distribution: list[ExpenseDistribution],
    ) -> list[DashboardInsight]:
        insights = []

        result = total_income - total_expenses

        insights.extend(
            self._generate_result_insights(
                total_income=total_income,
                total_expenses=total_expenses,
                result=result,
            )
        )

        insights.extend(
            self._generate_category_insights(
                expense_distribution=expense_distribution,
            )
        )

        return insights

    def _generate_result_insights(
        self,
        total_income: Decimal,
        total_expenses: Decimal,
        result: Decimal,
    ) -> list[DashboardInsight]:
        insights = []

        if result < 0:
            insights.append(
                DashboardInsight(
                    rule="NEGATIVE_RESULT",
                    type="warning",
                    severity="high",
                    title="Resultado financeiro negativo",
                    description=(
                        f"Suas despesas superaram suas entradas em R$ {abs(result):.2f} no período."
                    ),
                    metric={
                        "income": total_income,
                        "expenses": total_expenses,
                        "result": result,
                    },
                )
            )

        elif result > 0:
            insights.append(
                DashboardInsight(
                    rule="POSITIVE_RESULT",
                    type="info",
                    severity="low",
                    title="Resultado financeiro positivo",
                    description=(
                        f"Suas entradas superaram suas despesas em R$ {result:.2f} no período."
                    ),
                    metric={
                        "income": total_income,
                        "expenses": total_expenses,
                        "result": result,
                    },
                )
            )

        return insights

    def _generate_category_insights(
        self,
        expense_distribution: list[ExpenseDistribution],
    ) -> list[DashboardInsight]:
        insights = []

        if not expense_distribution:
            return insights

        biggest_category = expense_distribution[0]

        if biggest_category.percentage >= Decimal("40"):
            insights.append(
                DashboardInsight(
                    rule="HIGH_CATEGORY_CONCENTRATION",
                    type="warning",
                    severity="medium",
                    title="Alta concentração de gastos",
                    description=(
                        f"{biggest_category.category} representa "
                        f"{biggest_category.percentage:.2f}% "
                        f"das suas despesas."
                    ),
                    metric={
                        "category": biggest_category.category,
                        "percentage": f"{biggest_category.percentage:.2f}",
                        "amount": biggest_category.amount,
                    },
                )
            )

        elif biggest_category.percentage >= Decimal("25"):
            insights.append(
                DashboardInsight(
                    rule="MAIN_EXPENSE_CATEGORY",
                    type="info",
                    severity="low",
                    title="Principal categoria de gasto",
                    description=(
                        f"{biggest_category.category} representa "
                        f"{biggest_category.percentage:.2f}% "
                        f"das suas despesas."
                    ),
                    metric={
                        "category": biggest_category.category,
                        "percentage": f"{biggest_category.percentage:.2f}",
                        "amount": biggest_category.amount,
                    },
                )
            )

        if len(expense_distribution) >= 3:
            top_three_percentage = sum(
                (item.percentage for item in expense_distribution[:3]),
                Decimal("0"),
            )

            if top_three_percentage >= Decimal("70"):
                insights.append(
                    DashboardInsight(
                        rule="TOP_THREE_CONCENTRATION",
                        type="recommendation",
                        severity="medium",
                        title="Despesas concentradas",
                        description=(
                            f"As três maiores categorias representam "
                            f"{top_three_percentage:.2f}% "
                            f"das suas despesas."
                        ),
                        metric={
                            "percentage": f"{top_three_percentage:.2f}",
                        },
                    )
                )

        return insights
