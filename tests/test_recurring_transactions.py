from datetime import date, datetime, timedelta, timezone

from models.transacoes_recorrentes import TransacoesRecorrentes
from repositories.transacoes_recorrentes_repository import TransacoesRecorrentesRepository
from schemas.transacoes_recorrentes_schema import (
    TransacaoRecorrenteCreate,
    TransacaoRecorrenteUpdate,
)
from services.recurring_transaction_service import TransacoesRecorrentesService


def test_create_recurring_transaction(db_session, user, account):
    repository = TransacoesRecorrentesRepository(db_session)

    service = TransacoesRecorrentesService(repository=repository)

    data = TransacaoRecorrenteCreate(
        conta_id=account.id,
        tipo="saida",
        valor=500,
        categoria="Aluguel",
        frequencia="mensal",
        data_inicio=date(2026, 9, 13),
    )

    result = service.create(user_id=user.id, data=data)

    assert result.id is not None
    assert result.conta_id == account.id
    assert result.tipo == "saida"
    assert result.valor == 500
    assert result.categoria == "Aluguel"
    assert result.frequencia == "mensal"
    assert result.data_inicio == date(2026, 9, 13)
    assert result.ativo is True


def test_get_recurring_transactions(db_session, user, account):
    recurring_transaction = TransacoesRecorrentes(
        conta_id=account.id,
        tipo="saida",
        valor=500,
        categoria="Aluguel",
        frequencia="mensal",
        data_inicio=date(2026, 9, 13),
        proxima_data=date(2026, 10, 13),
    )

    db_session.add(recurring_transaction)
    db_session.commit()

    repository = TransacoesRecorrentesRepository(db_session)

    service = TransacoesRecorrentesService(repository=repository)

    result = service.get_all(user_id=user.id)

    assert len(result) == 1
    assert result[0].id == recurring_transaction.id


def test_update_recurring_transaction(db_session, user, account):
    recurring_transaction = TransacoesRecorrentes(
        conta_id=account.id,
        tipo="saida",
        valor=500,
        categoria="Aluguel",
        frequencia="mensal",
        data_inicio=date(2026, 9, 13),
        proxima_data=date(2026, 10, 13),
    )

    db_session.add(recurring_transaction)
    db_session.commit()
    db_session.refresh(recurring_transaction)

    repository = TransacoesRecorrentesRepository(db_session)

    service = TransacoesRecorrentesService(repository=repository)

    data = TransacaoRecorrenteUpdate(
        valor=700,
        categoria="Aluguel + condomínio",
        ativo=False,
    )

    result = service.update(
        user_id=user.id,
        recurring_transaction_id=recurring_transaction.id,
        data=data,
    )

    assert result.valor == 700
    assert result.categoria == "Aluguel + condomínio"
    assert result.ativo is False


def test_update_recurring_transaction_frequency_with_future_date(db_session, user, account):
    future_date = datetime.now(timezone.utc).date() + timedelta(days=30)

    recurring_transaction = TransacoesRecorrentes(
        conta_id=account.id,
        tipo="saida",
        valor=500,
        categoria="Aluguel",
        frequencia="mensal",
        data_inicio=date(2026, 9, 13),
        proxima_data=future_date,
    )

    db_session.add(recurring_transaction)
    db_session.commit()
    db_session.refresh(recurring_transaction)

    repository = TransacoesRecorrentesRepository(db_session)
    service = TransacoesRecorrentesService(repository=repository)

    data = TransacaoRecorrenteUpdate(frequencia="semanal")

    result = service.update(
        user_id=user.id,
        recurring_transaction_id=recurring_transaction.id,
        data=data,
    )

    assert result.frequencia == "semanal"
    assert result.proxima_data == future_date


def test_update_recurring_transaction_frequency_with_today_date(db_session, user, account):
    today = datetime.now(timezone.utc).date()

    recurring_transaction = TransacoesRecorrentes(
        conta_id=account.id,
        tipo="saida",
        valor=500,
        categoria="Aluguel",
        frequencia="mensal",
        data_inicio=date(2026, 9, 13),
        proxima_data=today,
    )

    db_session.add(recurring_transaction)
    db_session.commit()
    db_session.refresh(recurring_transaction)

    repository = TransacoesRecorrentesRepository(db_session)
    service = TransacoesRecorrentesService(repository=repository)

    data = TransacaoRecorrenteUpdate(frequencia="semanal")

    result = service.update(
        user_id=user.id,
        recurring_transaction_id=recurring_transaction.id,
        data=data,
    )

    assert result.frequencia == "semanal"
    assert result.proxima_data == today


def test_update_recurring_transaction_frequency_with_past_date(db_session, user, account):
    today = datetime.now(timezone.utc).date()
    past_date = today - timedelta(days=365)

    recurring_transaction = TransacoesRecorrentes(
        conta_id=account.id,
        tipo="saida",
        valor=500,
        categoria="Aluguel",
        frequencia="mensal",
        data_inicio=date(2026, 9, 13),
        proxima_data=past_date,
    )

    db_session.add(recurring_transaction)
    db_session.commit()
    db_session.refresh(recurring_transaction)

    repository = TransacoesRecorrentesRepository(db_session)
    service = TransacoesRecorrentesService(repository=repository)

    data = TransacaoRecorrenteUpdate(frequencia="semanal")

    result = service.update(
        user_id=user.id,
        recurring_transaction_id=recurring_transaction.id,
        data=data,
    )

    assert result.frequencia == "semanal"
    assert result.proxima_data >= today
    