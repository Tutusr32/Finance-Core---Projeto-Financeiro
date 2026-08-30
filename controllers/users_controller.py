from http import HTTPStatus

from fastapi import APIRouter, Depends

from dependencies.auth import get_current_user
from dependencies.users import get_users_service
from schemas.user_schema import (
    UserCreate,
    UserResponse,
    UserUpdate,
)
from services.users_service import UsersService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=UserResponse, status_code=HTTPStatus.CREATED)
def create_user(user: UserCreate, service: UsersService = Depends(get_users_service)):
    return service.criar_usuario(user)


@router.get("/me", response_model=UserResponse, status_code=HTTPStatus.OK)
def get_me(current_user=Depends(get_current_user)):
    return current_user


@router.patch("/me", response_model=UserResponse, status_code=HTTPStatus.OK)
def update_user(
    user: UserUpdate,
    service: UsersService = Depends(get_users_service),
    current_user=Depends(get_current_user),
):
    return service.atualizar_usuario(
        user_id=current_user.id,
        user_update=user,
    )


@router.delete("/me", status_code=HTTPStatus.NO_CONTENT)
def delete_user(
    service: UsersService = Depends(get_users_service),
    current_user=Depends(get_current_user),
):
    service.deletar_usuario(current_user.id)
