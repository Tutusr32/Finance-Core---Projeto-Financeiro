from repositories.users_repository import UsersRepository


class UsersService:

    def __init__(self, repo: UsersRepository):
        self.repo = repo

    def buscar_usuario(self, session, user_id: int):
        return self.repo.get_by_id(session, user_id)

    def criar_usuario(self, session, nome: str, email: str):
        return self.repo.create(session, nome, email)

    def atualizar_usuario(self, session, user_id: int, nome=None, email=None):
        return self.repo.update(session, user_id, nome, email)

    def deletar_usuario(self, session, user_id: int):
        return self.repo.delete(session, user_id)