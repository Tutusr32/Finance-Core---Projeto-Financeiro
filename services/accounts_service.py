from mappers.conta_mapper import conta_to_dict
from repositories.contas_repository import ContasRepository


class ContaService:
    def __init__(self, repo: ContasRepository):
        self.repo = repo

    def buscar_conta(self, session, user_id: int, conta_id: int):
        conta = self.repo.get_by_id_and_user(session, user_id, conta_id)

        if not conta:
            return None

        return conta_to_dict(conta)

    def criar_conta(self, session, user_id: int, name: str, saldo):
        conta = self.repo.create(session, user_id, name, saldo)
        return conta_to_dict(conta)

    def atualizar_conta(self, session, conta_id: int, name=None, saldo=None):
        if saldo is not None and saldo < 0:
            raise ValueError("Saldo não pode ser negativo.")

        conta = self.repo.update(session, conta_id, name, saldo)

        if not conta:
            return None

        return conta_to_dict(conta)

    def deletar_conta(self, session, conta_id: int):
        return self.repo.delete(session, conta_id)
    