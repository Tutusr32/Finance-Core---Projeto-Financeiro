from datetime import datetime, timezone

from core.recurring import calculate_next_date
from models.transacoes_recorrentes import TransacoesRecorrentes
from repositories.transacoes_recorrentes_repository import TransacoesRecorrentesRepository
from schemas.transacoes_recorrentes_schema import (
    TransacaoRecorrenteCreate,
    TransacaoRecorrenteUpdate,
)


class TransacoesRecorrentesService:
    def __init__(self, repository: TransacoesRecorrentesRepository):
        self.repository = repository

    def create(self, user_id: int, data: TransacaoRecorrenteCreate) -> TransacoesRecorrentes:
        account = self.repository.get_account(
            user_id=user_id,
            account_id=data.conta_id,
        )

        if account is None:
            raise ValueError("Conta não encontrada.")

        next_date = calculate_next_date(
            current_date=data.data_inicio,
            frequency=data.frequencia,
        )

        recurring_transaction = TransacoesRecorrentes(
            conta_id=data.conta_id,
            tipo=data.tipo,
            valor=data.valor,
            categoria=data.categoria,
            frequencia=data.frequencia,
            data_inicio=data.data_inicio,
            proxima_data=next_date,
        )

        self.repository.create(recurring_transaction)
        self.repository.session.commit()
        self.repository.session.refresh(recurring_transaction)

        return recurring_transaction

    def get_by_id(
        self, user_id: int, recurring_transaction_id: int
    ) -> TransacoesRecorrentes | None:
        return self.repository.get_by_id(
            user_id=user_id,
            recurring_transaction_id=recurring_transaction_id,
        )

    def get_all(self, user_id: int, ativo: bool | None = None) -> list[TransacoesRecorrentes]:
        return self.repository.get_all_by_user(
            user_id=user_id,
            ativo=ativo,
        )

    def update(
        self, user_id: int, recurring_transaction_id: int, data: TransacaoRecorrenteUpdate
    ) -> TransacoesRecorrentes | None:
        recurring_transaction = self.repository.get_by_id(
            user_id=user_id,
            recurring_transaction_id=recurring_transaction_id,
        )

        if recurring_transaction is None:
            return None

        update_data = data.model_dump(exclude_unset=True)

        if "frequencia" in update_data:
            next_date = recurring_transaction.proxima_data
            frequency = update_data["frequencia"]

            today = datetime.now(timezone.utc).date()

            while next_date < today:
                next_date = calculate_next_date(
                    current_date=next_date,
                    frequency=frequency,
                )

            recurring_transaction.proxima_data = next_date

        for field, value in update_data.items():
            setattr(recurring_transaction, field, value)

        self.repository.update(recurring_transaction)
        self.repository.session.commit()
        self.repository.session.refresh(recurring_transaction)

        return recurring_transaction
