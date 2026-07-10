from fastapi import APIRouter, Depends, HTTPException, status

from dependencies.auth import get_current_user
from dependencies.users import get_users_service
from schemas.user_schema import (
    UserCreate,
    UserResponse,
    UserUpdate,
)
from services.users_service import UsersService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, service: UsersService = Depends(get_users_service)):
    return service.criar_usuario(user)


@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_me(current_user=Depends(get_current_user)):
    return current_user


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(
    user_id: int,
    service: UsersService = Depends(get_users_service),
    current_user=Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você só pode acessar seu próprio usuário.",
        )

    return service.buscar_usuario(user_id)


@router.patch("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(
    user_id: int,
    user: UserUpdate,
    service: UsersService = Depends(get_users_service),
    current_user=Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você só pode atualizar seu próprio usuário.",
        )

    return service.atualizar_usuario(user_id=user_id, user_update=user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    service: UsersService = Depends(get_users_service),
    current_user=Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você só pode deletar seu próprio usuário.",
        )

    service.deletar_usuario(user_id)
