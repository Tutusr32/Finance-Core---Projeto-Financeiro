from fastapi import Depends
from sqlalchemy.orm import Session

from core.database import get_db
from repositories.contas_repository import ContasRepository
from services.accounts_service import ContaService


def get_accounts_repository(db: Session = Depends(get_db)):
    return ContasRepository(db)


def get_accounts_service(repo: ContasRepository = Depends(get_accounts_repository)):
    return ContaService(repo)
