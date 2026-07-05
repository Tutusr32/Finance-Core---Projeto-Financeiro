from fastapi import Depends
from sqlalchemy.orm import Session

from core.database import get_db
from dependencies.accounts import get_accounts_repository
from repositories.contas_repository import ContasRepository
from repositories.transacao_repository import TransacaoRepository
from services.transactions_service import TransacoesService


def get_transactions_repository(db: Session = Depends(get_db)):
    return TransacaoRepository(db)


def get_transactions_service(
    trans_repo: TransacaoRepository = Depends(get_transactions_repository),
    contas_repo: ContasRepository = Depends(get_accounts_repository),
):
    return TransacoesService(trans_repo, contas_repo)
