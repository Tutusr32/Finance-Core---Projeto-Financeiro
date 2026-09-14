from apscheduler.schedulers.background import BackgroundScheduler

from core.database import SessionLocal
from repositories.contas_repository import ContasRepository
from repositories.ocorrencias_recorrentes_repository import OcorrenciasRecorrentesRepository
from repositories.transacao_repository import TransacaoRepository
from repositories.transacoes_recorrentes_repository import TransacoesRecorrentesRepository
from services.recurring_transaction_processor_service import RecurringTransactionProcessorService
from services.transactions_service import TransacoesService

scheduler = BackgroundScheduler()


def process_recurring_transactions():
    db = SessionLocal()

    try:
        transaction_repository = TransacaoRepository(db)
        account_repository = ContasRepository(db)

        transaction_service = TransacoesService(
            repo=transaction_repository,
            contas_repo=account_repository,
        )

        recurring_repository = TransacoesRecorrentesRepository(db)
        occurrence_repository = OcorrenciasRecorrentesRepository(db)

        processor = RecurringTransactionProcessorService(
            recurring_repository=recurring_repository,
            occurrence_repository=occurrence_repository,
            transaction_service=transaction_service,
        )

        processor.process()

    finally:
        db.close()


def start_scheduler():
    scheduler.add_job(
        process_recurring_transactions,
        "interval",
        hours=1,
        id="process_recurring_transactions",
        replace_existing=True,
    )

    scheduler.start()


def stop_scheduler():
    scheduler.shutdown()
