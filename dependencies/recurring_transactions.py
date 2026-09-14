from fastapi import Depends
from sqlalchemy.orm import Session

from core.database import get_db
from repositories.transacoes_recorrentes_repository import TransacoesRecorrentesRepository
from services.recurring_transaction_service import TransacoesRecorrentesService


def get_transacoes_recorrentes_service(
    db: Session = Depends(get_db),
) -> TransacoesRecorrentesService:

    repository = TransacoesRecorrentesRepository(db)
    return TransacoesRecorrentesService(repository)
