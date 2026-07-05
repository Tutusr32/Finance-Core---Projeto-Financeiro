from fastapi import HTTPException, status

from repositories.users_repository import UsersRepository

from core.security import hash_password


class UsersService:
    def __init__(self, repo: UsersRepository):
        self.repo = repo

    def criar_usuario(self, user):

        return self.repo.create(
            name=user.name, email=user.email, password=hash_password(user.password)
        )

    def buscar_usuario(self, user_id):
        user = self.repo.get_by_id(user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado."
            )

        return user

    def atualizar_usuario(self, user_id: int, name=None, email=None):

        user = self.repo.update(user_id, name, email)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado."
            )

        return user

    def deletar_usuario(self, user_id: int):

        deleted = self.repo.delete(user_id)

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado."
            )
