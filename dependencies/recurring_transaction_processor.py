from fastapi import Depends
from sqlalchemy.orm import Session

from core.database import get_db
from repositories.contas_repository import ContasRepository
from repositories.ocorrencias_recorrentes_repository import OcorrenciasRecorrentesRepository
from repositories.transacao_repository import TransacaoRepository
from repositories.transacoes_recorrentes_repository import TransacoesRecorrentesRepository
from services.recurring_transaction_processor_service import RecurringTransactionProcessorService
from services.transactions_service import TransacoesService


def get_recurring_transaction_processor_service(
    db: Session = Depends(get_db),
) -> RecurringTransactionProcessorService:
    transaction_repository = TransacaoRepository(db)
    account_repository = ContasRepository(db)

    transaction_service = TransacoesService(
        repo=transaction_repository,
        contas_repo=account_repository,
    )

    recurring_repository = TransacoesRecorrentesRepository(db)
    occurrence_repository = OcorrenciasRecorrentesRepository(db)

    return RecurringTransactionProcessorService(
        recurring_repository=recurring_repository,
        occurrence_repository=occurrence_repository,
        transaction_service=transaction_service,
    )
