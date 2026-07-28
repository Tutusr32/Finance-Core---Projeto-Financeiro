from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from core.security import hash_password, verify_password
from repositories.users_repository import UsersRepository
from schemas.user_schema import UserCreate, UserUpdate


class UsersService:
    def __init__(self, repo: UsersRepository):
        self.repo = repo

    def criar_usuario(self, user: UserCreate):
        try:
            return self.repo.create(
                name=user.name,
                email=user.email,
                password=hash_password(user.password),
            )
        except IntegrityError:
            self.repo.session.rollback()
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Email já cadastrado.",
            )

    def autenticar_usuario(self, email: str, password: str):
        user = self.repo.get_by_email(email)

        if user is None:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Credenciais inválidas.",
            )

        if not verify_password(password, user.password):
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Credenciais inválidas.",
            )

        return user

    def atualizar_usuario(self, user_id: int, user_update: UserUpdate):
        password = None
        if user_update.password is not None:
            password = hash_password(user_update.password)

        try:
            user = self.repo.update(
                user_id,
                name=user_update.name,
                email=user_update.email,
                password=password,
            )
        except IntegrityError:
            self.repo.session.rollback()
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Email já cadastrado.",
            )

        if user is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado.")

        return user

    def deletar_usuario(self, user_id: int):

        deleted = self.repo.delete(user_id)

        if not deleted:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado.")
