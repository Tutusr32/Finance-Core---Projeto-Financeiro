from datetime import date, timedelta
from decimal import Decimal

from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from models.contas import Contas
from models.transacoes import Transacoes


class DashboardRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_total_balance(self, user_id: int) -> Decimal:
        statement = select(func.coalesce(func.sum(Contas.saldo), 0)).where(
            Contas.user_id == user_id
        )

        result = self.session.execute(statement)

        return result.scalar_one()

    def get_summary(
        self,
        user_id: int,
        start_date: date | None,
        end_date: date | None,
    ):
        income = func.coalesce(
            func.sum(
                case(
                    (Transacoes.tipo == "entrada", Transacoes.valor),
                    else_=0,
                )
            ),
            0,
        )

        expense = func.coalesce(
            func.sum(
                case(
                    (Transacoes.tipo == "saida", Transacoes.valor),
                    else_=0,
                )
            ),
            0,
        )

        statement = (
            select(
                income.label("total_income"),
                expense.label("total_expense"),
            )
            .join(Contas, Transacoes.conta_id == Contas.id)
            .where(Contas.user_id == user_id)
        )

        if start_date:
            statement = statement.where(Transacoes.data >= start_date)

        if end_date:
            statement = statement.where(Transacoes.data < end_date + timedelta(days=1))

        result = self.session.execute(statement)

        return result.one()

    def get_category_summary(
        self,
        user_id: int,
        start_date: date | None,
        end_date: date | None,
    ):
        statement = (
            select(
                Transacoes.categoria,
                Transacoes.tipo,
                func.sum(Transacoes.valor).label("total"),
            )
            .join(Contas, Transacoes.conta_id == Contas.id)
            .where(Contas.user_id == user_id)
            .group_by(
                Transacoes.categoria,
                Transacoes.tipo,
            )
            .order_by(func.sum(Transacoes.valor).desc())
        )

        if start_date:
            statement = statement.where(Transacoes.data >= start_date)

        if end_date:
            statement = statement.where(Transacoes.data < end_date + timedelta(days=1))

        result = self.session.execute(statement)

        return result.all()

    def get_history(
        self,
        user_id: int,
        start_date: date | None,
        end_date: date | None,
    ):
        statement = (
            select(
                func.date(Transacoes.data).label("date"),
                func.coalesce(
                    func.sum(
                        case(
                            (
                                Transacoes.tipo == "entrada",
                                Transacoes.valor,
                            ),
                            else_=0,
                        )
                    ),
                    0,
                ).label("income"),
                func.coalesce(
                    func.sum(
                        case(
                            (
                                Transacoes.tipo == "saida",
                                Transacoes.valor,
                            ),
                            else_=0,
                        )
                    ),
                    0,
                ).label("expense"),
            )
            .join(Contas, Transacoes.conta_id == Contas.id)
            .where(Contas.user_id == user_id)
            .group_by(func.date(Transacoes.data))
            .order_by(func.date(Transacoes.data))
        )

        if start_date:
            statement = statement.where(Transacoes.data >= start_date)

        if end_date:
            statement = statement.where(Transacoes.data < end_date + timedelta(days=1))

        result = self.session.execute(statement)

        return result.all()

    def get_initial_balance(
        self,
        user_id: int,
        start_date: date,
    ) -> Decimal:
        net_movement = func.coalesce(
            func.sum(
                case(
                    (Transacoes.tipo == "entrada", Transacoes.valor),
                    (Transacoes.tipo == "saida", -Transacoes.valor),
                    else_=0,
                )
            ),
            0,
        )

        statement = (
            select(net_movement)
            .join(Contas, Transacoes.conta_id == Contas.id)
            .where(
                Contas.user_id == user_id,
                Transacoes.data >= start_date,
            )
        )

        result = self.session.execute(statement)

        current_balance = self.get_total_balance(user_id)
        movement = result.scalar_one()

        return current_balance - movement

    def get_analysis(
        self,
        user_id: int,
        start_date: date | None,
        end_date: date | None,
    ):
        expense = func.sum(Transacoes.valor).label("total")

        statement = (
            select(
                Transacoes.categoria,
                expense,
            )
            .join(Contas, Transacoes.conta_id == Contas.id)
            .where(
                Contas.user_id == user_id,
                Transacoes.tipo == "saida",
            )
            .group_by(Transacoes.categoria)
            .order_by(expense.desc())
        )

        if start_date:
            statement = statement.where(Transacoes.data >= start_date)

        if end_date:
            statement = statement.where(Transacoes.data < end_date + timedelta(days=1))

        result = self.session.execute(statement)

        return result.all()
