from fastapi import HTTPException

from repositories.users_repository import UsersRepository


class UsersService:
    def __init__(self, repo: UsersRepository):
        self.repo = repo

    def criar_usuario(self, user):
        return self.repo.create(name=user.name, email=user.email)

    def buscar_usuario(self, user_id):
        user = self.repo.get_by_id(user_id)

        if user is None:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")

        return user

    def atualizar_usuario(self, user_id: int, name=None, email=None):

        user = self.repo.update(user_id, name, email)

        if user is None:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")

        return user

    def deletar_usuario(self, user_id: int):

        deleted = self.repo.delete(user_id)

        if not deleted:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")
