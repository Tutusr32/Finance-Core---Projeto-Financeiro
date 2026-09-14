from datetime import date

from models.ocorrencias_recorrentes import OcorrenciasRecorrentes
from models.transacoes_recorrentes import TransacoesRecorrentes
from repositories.contas_repository import ContasRepository
from repositories.ocorrencias_recorrentes_repository import OcorrenciasRecorrentesRepository
from repositories.transacao_repository import TransacaoRepository
from repositories.transacoes_recorrentes_repository import TransacoesRecorrentesRepository
from services.recurring_transaction_processor_service import RecurringTransactionProcessorService
from services.transactions_service import TransacoesService


def test_process_recurring_transaction(db_session, user, account):
    transaction_repository = TransacaoRepository(db_session)
    account_repository = ContasRepository(db_session)
    recurring_repository = TransacoesRecorrentesRepository(db_session)
    occurrence_repository = OcorrenciasRecorrentesRepository(db_session)

    account.saldo = 5000
    db_session.commit()
    db_session.refresh(account)

    recurring_transaction = TransacoesRecorrentes(
        conta_id=account.id,
        tipo="saida",
        valor=1000,
        categoria="Aluguel",
        frequencia="mensal",
        data_inicio=date(2026, 8, 13),
        proxima_data=date(2026, 9, 13),
    )

    recurring_repository.create(recurring_transaction)
    db_session.commit()
    db_session.refresh(recurring_transaction)

    transaction_service = TransacoesService(
        repo=transaction_repository,
        contas_repo=account_repository,
    )

    processor = RecurringTransactionProcessorService(
        recurring_repository=recurring_repository,
        occurrence_repository=occurrence_repository,
        transaction_service=transaction_service,
    )

    result = processor.process(current_date=date(2026, 9, 13))

    db_session.refresh(account)
    db_session.refresh(recurring_transaction)

    assert len(result) == 1

    occurrence = result[0]

    assert occurrence.status == "realizada"
    assert occurrence.data_prevista == date(2026, 9, 13)
    assert occurrence.transacao_id is not None

    assert account.saldo == 4000
    assert recurring_transaction.proxima_data == date(2026, 10, 13)

    saved_occurrence = (
        db_session.query(OcorrenciasRecorrentes)
        .filter(OcorrenciasRecorrentes.id == occurrence.id)
        .first()
    )

    assert saved_occurrence is not None
    assert saved_occurrence.status == "realizada"


def test_process_recurring_transaction_with_insufficient_balance(db_session, user, account):
    transaction_repository = TransacaoRepository(db_session)
    account_repository = ContasRepository(db_session)
    recurring_repository = TransacoesRecorrentesRepository(db_session)
    occurrence_repository = OcorrenciasRecorrentesRepository(db_session)

    account.saldo = 100
    db_session.commit()

    recurring_transaction = TransacoesRecorrentes(
        conta_id=account.id,
        tipo="saida",
        valor=500,
        categoria="Aluguel",
        frequencia="mensal",
        data_inicio=date(2026, 8, 13),
        proxima_data=date(2026, 9, 13),
    )

    recurring_repository.create(recurring_transaction)
    db_session.commit()
    db_session.refresh(recurring_transaction)

    transaction_service = TransacoesService(
        repo=transaction_repository,
        contas_repo=account_repository,
    )

    processor = RecurringTransactionProcessorService(
        recurring_repository=recurring_repository,
        occurrence_repository=occurrence_repository,
        transaction_service=transaction_service,
    )

    result = processor.process(current_date=date(2026, 9, 13))

    db_session.refresh(account)
    db_session.refresh(recurring_transaction)

    assert len(result) == 1
    assert result[0].status == "falhou"
    assert result[0].transacao_id is None

    assert account.saldo == 100
    assert recurring_transaction.proxima_data == date(2026, 10, 13)
    assert recurring_transaction.ativo is True
