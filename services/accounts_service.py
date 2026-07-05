from fastapi import HTTPException
from mappers.conta_mapper import conta_to_dict
from repositories.contas_repository import ContasRepository


class ContaService:
    def __init__(self, repo: ContasRepository):
        self.repo = repo

    def buscar_conta(self, user_id: int, conta_id: int):
        conta = self.repo.get_by_id_and_user(user_id, conta_id)

        if not conta:
            raise HTTPException(status_code=404, detail="Conta não encontrada.")

        return conta_to_dict(conta)

    def criar_conta(self, user_id: int, name: str, saldo):
        conta = self.repo.create(user_id, name, saldo)
        return conta_to_dict(conta)

    def atualizar_conta(
        self,
        user_id: int,
        conta_id: int,
        name=None,
        saldo=None,
    ):
        if saldo is not None and saldo < 0:
            raise HTTPException(status_code=400, detail="Saldo não pode ser negativo.")

        conta = self.repo.update(
            user_id=user_id,
            conta_id=conta_id,
            name=name,
            saldo=saldo,
        )

        if not conta:
            raise HTTPException(status_code=404, detail="Conta não encontrada.")

        return conta_to_dict(conta)

    def deletar_conta(
        self,
        user_id: int,
        conta_id: int,
    ):
        deleted = self.repo.delete(
            user_id=user_id,
            conta_id=conta_id,
        )

        if not deleted:
            raise HTTPException(status_code=404, detail="Conta não encontrada.")

        return deleted
