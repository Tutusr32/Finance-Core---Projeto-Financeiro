from fastapi import APIRouter, Depends, status, Query

from dependencies.auth import get_current_user
from dependencies.transaction import get_transactions_service
from schemas.transaction_schema import TransactionCreate, TransactionResponse
from services.transactions_service import TransacoesService

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/{conta_id}", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(
    conta_id: int,
    transaction: TransactionCreate,
    service: TransacoesService = Depends(get_transactions_service),
    current_user=Depends(get_current_user),
):
    return service.criar_transacao(
        user_id=current_user.id,
        conta_id=conta_id,
        transaction=transaction,
    )


@router.get("/{conta_id}", response_model=list[TransactionResponse])
def list_transactions(
    conta_id: int,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: TransacoesService = Depends(get_transactions_service),
    current_user=Depends(get_current_user),
):
    return service.listar_transacoes(
        user_id=current_user.id,
        conta_id=conta_id,
        limit=limit,
        offset=offset,
    )
