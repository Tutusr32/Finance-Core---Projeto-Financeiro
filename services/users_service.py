from repositories.users_repository import UsersRepository
from configs.connection import DBConnectionHandler

class UsersService:

    def __init__(self):
        self.repo = UsersRepository()

    def buscar_usuario(self, user_id):
        with DBConnectionHandler() as db:
            user = self.repo.get_by_id(db.session, user_id)

            if not user:
                print("Usuário não encontrado.")
                return

            return user
        

    def criar_usuario(self, nome: str, email: str):
        with DBConnectionHandler() as db:
            return self.repo.create(db.session, nome, email)
        

    def atualizar_usuario(self, user_id, nome=None, email=None):
        with DBConnectionHandler() as db:
            user = self.repo.update(db.session, user_id, nome, email)

            if not user:
                print("Usuário não encontrado.")
                return

            return user
        

    def deletar_usuario(self, user_id):
        with DBConnectionHandler() as db:
            user = self.repo.delete_user(db.session, user_id)

            return user