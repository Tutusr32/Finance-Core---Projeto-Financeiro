from fastapi import APIRouter, Depends, status

from dependencies.users import get_users_service

from schemas.user_schema import (
    UserCreate, 
    UserResponse,
    UserUpdate,
    )

from services.users_service import UsersService

router = APIRouter()


@router.post("/users", response_model=UserResponse)
def create_user(
    user: UserCreate,
    service: UsersService = Depends(get_users_service)
):
    return service.criar_usuario(user)


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    service: UsersService = Depends(get_users_service)
):
    return service.buscar_usuario(user_id)


@router.patch("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user: UserUpdate,
    service: UsersService = Depends(get_users_service)
):
    
    return service.atualizar_usuario(
        user_id=user_id,
        name=user.name,
        email=user.email
    )


@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_user(
    user_id: int,
    service: UsersService = Depends(get_users_service)
):
    
    service.deletar_usuario(user_id)
