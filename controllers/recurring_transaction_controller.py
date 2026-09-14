from fastapi import APIRouter, Depends, HTTPException, Query, status

from dependencies.auth import get_current_user
from dependencies.recurring_transactions import get_transacoes_recorrentes_service
from models.users import Users
from schemas.transacoes_recorrentes_schema import (
    TransacaoRecorrenteCreate,
    TransacaoRecorrenteResponse,
    TransacaoRecorrenteUpdate,
)
from services.recurring_transaction_service import TransacoesRecorrentesService

router = APIRouter(prefix="/transactions/recurring", tags=["Transações Recorrentes"])


@router.post("", response_model=TransacaoRecorrenteResponse, status_code=status.HTTP_201_CREATED)
def create_recurring_transaction(
    data: TransacaoRecorrenteCreate,
    current_user: Users = Depends(get_current_user),
    service: TransacoesRecorrentesService = Depends(get_transacoes_recorrentes_service),
):
    try:
        return service.create(
            user_id=current_user.id,
            data=data,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )


@router.get("", response_model=list[TransacaoRecorrenteResponse])
def get_recurring_transactions(
    ativo: bool | None = Query(default=None),
    current_user: Users = Depends(get_current_user),
    service: TransacoesRecorrentesService = Depends(get_transacoes_recorrentes_service),
):
    return service.get_all(
        user_id=current_user.id,
        ativo=ativo,
    )


@router.get("/{recurring_transaction_id}", response_model=TransacaoRecorrenteResponse)
def get_recurring_transaction(
    recurring_transaction_id: int,
    current_user: Users = Depends(get_current_user),
    service: TransacoesRecorrentesService = Depends(get_transacoes_recorrentes_service),
):
    recurring_transaction = service.get_by_id(
        user_id=current_user.id,
        recurring_transaction_id=recurring_transaction_id,
    )

    if recurring_transaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transação recorrente não encontrada.",
        )

    return recurring_transaction


@router.patch("/{recurring_transaction_id}", response_model=TransacaoRecorrenteResponse)
def update_recurring_transaction(
    recurring_transaction_id: int,
    data: TransacaoRecorrenteUpdate,
    current_user: Users = Depends(get_current_user),
    service: TransacoesRecorrentesService = Depends(get_transacoes_recorrentes_service),
):
    recurring_transaction = service.update(
        user_id=current_user.id,
        recurring_transaction_id=recurring_transaction_id,
        data=data,
    )

    if recurring_transaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transação recorrente não encontrada.",
        )

    return recurring_transaction
