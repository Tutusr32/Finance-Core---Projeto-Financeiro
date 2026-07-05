from fastapi import APIRouter, Depends, status

from dependencies.transaction import get_transactions_service
from schemas.transaction_schema import TransactionCreate, TransactionResponse
from services.transactions_service import TransacoesService

router = APIRouter(prefix="/transactions", tags=["Transactions"])
 

@router.post("", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction: TransactionCreate,
    service: TransacoesService = Depends(get_transactions_service),
):
    return service.criar_transacao(
        user_id=transaction.user_id,
        conta_id=transaction.conta_id,
        tipo=transaction.type,
        valor=transaction.amount,
        categoria=transaction.category,
    )


@router.get("/{conta_id}", response_model=list[TransactionResponse])
def list_transactions(
    conta_id: int = ...,
    service: TransacoesService = Depends(get_transactions_service),
):
    return service.listar_transacoes(conta_id=conta_id)
