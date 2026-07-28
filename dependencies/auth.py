import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import decode_access_token
from repositories.users_repository import UsersRepository
from services.users_service import UsersService

security = HTTPBearer(auto_error=False)


def get_auth_service(db: Session = Depends(get_db)):
    repo = UsersRepository(db)
    return UsersService(repo)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    service: UsersService = Depends(get_auth_service),
):
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token ausente.",
        )

    token = credentials.credentials

    try:
        payload = decode_access_token(token)

    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado.",
        ) from exc

    except jwt.InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido.",
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Erro ao validar token.",
        ) from exc

    user_id = payload.get("user_id")
    sub = payload.get("sub")

    if user_id is None or sub is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido.",
        )

    user = service.repo.get_by_id(user_id)

    if user is None or user.email != sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado.",
        )

    return user
