from http import HTTPStatus

from fastapi import APIRouter, Depends

from dependencies.accounts import get_accounts_service
from dependencies.auth import get_current_user
from schemas.conta_schema import ContaCreate, ContaResponse, ContaUpdate
from services.accounts_service import ContaService

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.post("", response_model=ContaResponse, status_code=HTTPStatus.CREATED)
def create_account(
    account: ContaCreate,
    service: ContaService = Depends(get_accounts_service),
    current_user=Depends(get_current_user),
):
    return service.criar_conta(user_id=current_user.id, account=account)


@router.get("/{conta_id}", response_model=ContaResponse)
def get_account(
    conta_id: int,
    service: ContaService = Depends(get_accounts_service),
    current_user=Depends(get_current_user),
):
    return service.buscar_conta(user_id=current_user.id, conta_id=conta_id)


@router.patch(
    "/{conta_id}",
    response_model=ContaResponse,
    status_code=HTTPStatus.OK,
)
def update_account(
    conta_id: int,
    account: ContaUpdate,
    service: ContaService = Depends(get_accounts_service),
    current_user=Depends(get_current_user),
):
    return service.atualizar_conta(
        user_id=current_user.id,
        conta_id=conta_id,
        account=account,
    )


@router.delete(
    "/{conta_id}",
    status_code=HTTPStatus.NO_CONTENT,
)
def delete_account(
    conta_id: int,
    service: ContaService = Depends(get_accounts_service),
    current_user=Depends(get_current_user),
):
    service.deletar_conta(
        user_id=current_user.id,
        conta_id=conta_id,
    )
