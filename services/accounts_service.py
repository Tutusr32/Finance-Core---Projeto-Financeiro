from repositories.contas_repository import ContasRepository
from configs.connection import DBConnectionHandler
from mappers.conta_mapper import conta_to_dict

class ContaService:

    def __init__(self):
        self.repo = ContasRepository()


    def buscar_conta(self, user_id, conta_id):
        with DBConnectionHandler() as db:
            conta = self.repo.get_by_id_and_user(db.session, user_id, conta_id)

            if not conta:
                print("Conta não encontrada.")
                return

            return conta

    def criar_conta(self, user_id, nome, saldo):
        with DBConnectionHandler() as db:
            conta = self.repo.create_account(db.session, user_id, nome, saldo)

            return conta_to_dict(conta)
        

    def atualizar_conta(self, conta_id, nome=None, saldo=None):
        with DBConnectionHandler() as db:

            if saldo is not None and saldo < 0:
                raise Exception("Saldo não pode ser negativo")
            
            conta = self.repo.update_account(
                db.session, conta_id, nome, saldo
            )

            if not conta:
                raise Exception("Conta não existe")
            
            return conta_to_dict(conta)
        
        
    def deletar_conta(self, conta_id):
        with DBConnectionHandler() as db:
            conta = self.repo.delete_account(db.session, conta_id)

            if not conta:
                raise Exception("Conta não existe")

            return conta
    