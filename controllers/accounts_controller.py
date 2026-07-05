from fastapi import APIRouter, Depends, status

from dependencies.accounts import get_accounts_service
from schemas.conta_schema import ContaCreate, ContaResponse, ContaUpdate
from services.accounts_service import ContaService

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.post("", response_model=ContaResponse, status_code=status.HTTP_201_CREATED)
def create_account(
    account: ContaCreate,
    service: ContaService = Depends(get_accounts_service),
):
    return service.criar_conta(
        user_id=account.user_id,
        name=account.name,
        saldo=account.saldo,
    )


@router.get("/{user_id}/{conta_id}", response_model=ContaResponse)
def get_account(
    user_id: int,
    conta_id: int,
    service: ContaService = Depends(get_accounts_service),
):
    return service.buscar_conta(user_id=user_id, conta_id=conta_id)


@router.patch(
    "/{user_id}/{account_id}",
    response_model=ContaResponse,
    status_code=status.HTTP_200_OK,
)
def update_account(
    user_id: int,
    account_id: int,
    account: ContaUpdate,
    service: ContaService = Depends(get_accounts_service),
):
    return service.atualizar_conta(
        user_id=user_id,
        conta_id=account_id,
        name=account.name,
        saldo=account.saldo,
    )


@router.delete(
    "/{user_id}/{account_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_account(
    user_id: int,
    account_id: int,
    service: ContaService = Depends(get_accounts_service),
):
    service.deletar_conta(
        user_id=user_id,
        conta_id=account_id,
    )
