from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from core.security import create_access_token
from dependencies.users import get_users_service
from schemas.auth_schema import TokenResponse
from services.users_service import UsersService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: UsersService = Depends(get_users_service),
):
    user = service.autenticar_usuario(email=form_data.username, password=form_data.password)
    access_token = create_access_token(sub=user.email, user_id=user.id)
    return TokenResponse(access_token=access_token)
