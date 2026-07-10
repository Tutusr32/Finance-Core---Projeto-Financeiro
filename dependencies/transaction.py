from fastapi import Depends
from sqlalchemy.orm import Session

from core.database import get_db
from repositories.contas_repository import ContasRepository
from repositories.transacao_repository import TransacaoRepository
from services.transactions_service import TransacoesService


def get_transactions_service(db: Session = Depends(get_db)):
    trans_repo = TransacaoRepository(db)
    contas_repo = ContasRepository(db)
    return TransacoesService(trans_repo, contas_repo)
