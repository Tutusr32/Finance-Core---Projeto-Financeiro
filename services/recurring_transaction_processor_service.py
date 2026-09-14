from datetime import date, datetime, timezone

from fastapi import HTTPException

from core.recurring import calculate_next_date
from models.ocorrencias_recorrentes import OcorrenciasRecorrentes
from models.transacoes_recorrentes import TransacoesRecorrentes
from repositories.ocorrencias_recorrentes_repository import OcorrenciasRecorrentesRepository
from repositories.transacoes_recorrentes_repository import TransacoesRecorrentesRepository
from schemas.transaction_schema import TransactionCreate
from services.transactions_service import TransacoesService


class RecurringTransactionProcessorService:
    def __init__(
        self,
        recurring_repository: TransacoesRecorrentesRepository,
        occurrence_repository: OcorrenciasRecorrentesRepository,
        transaction_service: TransacoesService,
    ):
        self.recurring_repository = recurring_repository
        self.occurrence_repository = occurrence_repository
        self.transaction_service = transaction_service

    def process(self, current_date: date | None = None):
        if current_date is None:
            current_date = datetime.now(timezone.utc).date()

        recurring_transactions = self.recurring_repository.get_due_transactions(
            current_date=current_date
        )

        processed_occurrences = []

        for recurring_transaction in recurring_transactions:
            processed_occurrences.append(
                self._process_recurring_transaction(
                    recurring_transaction=recurring_transaction,
                    current_date=current_date,
                )
            )

        return processed_occurrences

    def _process_recurring_transaction(
        self, recurring_transaction: TransacoesRecorrentes, current_date: date
    ):
        occurrence = OcorrenciasRecorrentes(
            transacao_recorrente_id=recurring_transaction.id,
            data_prevista=recurring_transaction.proxima_data,
            status="pendente",
        )

        self.occurrence_repository.create(occurrence)

        try:
            transaction = self.transaction_service.criar_transacao(
                user_id=recurring_transaction.conta.user_id,
                conta_id=recurring_transaction.conta_id,
                transaction=TransactionCreate(
                    type=recurring_transaction.tipo,
                    amount=recurring_transaction.valor,
                    category=recurring_transaction.categoria,
                ),
                commit=False,
            )

            occurrence.transacao = transaction
            occurrence.status = "realizada"
            occurrence.data_processamento = datetime.now(timezone.utc)

        except HTTPException as error:
            occurrence.status = "falhou"
            occurrence.motivo_falha = str(error.detail)
            occurrence.data_processamento = datetime.now(timezone.utc)

        recurring_transaction.proxima_data = calculate_next_date(
            current_date=recurring_transaction.proxima_data,
            frequency=recurring_transaction.frequencia,
        )

        self.recurring_repository.update(recurring_transaction)
        self.occurrence_repository.update(occurrence)

        try:
            self.recurring_repository.session.commit()
        except Exception:
            self.recurring_repository.session.rollback()
            raise

        return occurrence
