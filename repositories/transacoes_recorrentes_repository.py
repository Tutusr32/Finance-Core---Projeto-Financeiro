from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.contas import Contas
from models.transacoes_recorrentes import TransacoesRecorrentes


class TransacoesRecorrentesRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, recurring_transaction: TransacoesRecorrentes) -> TransacoesRecorrentes:
        self.session.add(recurring_transaction)

        return recurring_transaction

    def get_account(self, user_id: int, account_id: int) -> Contas | None:
        statement = select(Contas).where(
            Contas.id == account_id,
            Contas.user_id == user_id,
        )

        result = self.session.execute(statement)

        return result.scalar_one_or_none()

    def get_by_id(
        self, user_id: int, recurring_transaction_id: int
    ) -> TransacoesRecorrentes | None:
        statement = (
            select(TransacoesRecorrentes)
            .join(Contas, TransacoesRecorrentes.conta_id == Contas.id)
            .where(
                TransacoesRecorrentes.id == recurring_transaction_id,
                Contas.user_id == user_id,
            )
        )

        result = self.session.execute(statement)

        return result.scalar_one_or_none()

    def get_all_by_user(
        self, user_id: int, ativo: bool | None = None
    ) -> list[TransacoesRecorrentes]:
        statement = (
            select(TransacoesRecorrentes)
            .join(Contas, TransacoesRecorrentes.conta_id == Contas.id)
            .where(Contas.user_id == user_id)
            .order_by(TransacoesRecorrentes.proxima_data)
        )

        if ativo is not None:
            statement = statement.where(TransacoesRecorrentes.ativo == ativo)

        result = self.session.execute(statement)

        return list(result.scalars().all())

    def get_due_transactions(self, current_date: date) -> list[TransacoesRecorrentes]:
        statement = select(TransacoesRecorrentes).where(
            TransacoesRecorrentes.ativo,
            TransacoesRecorrentes.proxima_data <= current_date,
        )
        result = self.session.execute(statement)
        return list(result.scalars().all())

    def update(self, recurring_transaction: TransacoesRecorrentes) -> TransacoesRecorrentes:
        self.session.add(recurring_transaction)

        return recurring_transaction
