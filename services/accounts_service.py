from fastapi import HTTPException
from mappers.conta_mapper import conta_to_dict
from repositories.contas_repository import ContasRepository
from schemas.conta_schema import ContaCreate, ContaUpdate


class ContaService:
    def __init__(self, repo: ContasRepository):
        self.repo = repo

    def buscar_conta(self, user_id: int, conta_id: int):
        conta = self.repo.get_by_id_and_user(user_id, conta_id)

        if not conta:
            raise HTTPException(status_code=404, detail="Conta não encontrada.")

        if conta.user_id != user_id:
            raise HTTPException(status_code=403, detail="Acesso negado.")

        return conta_to_dict(conta)

    def criar_conta(self, user_id: int, account: ContaCreate):
        if account.saldo < 0:
            raise HTTPException(status_code=400, detail="Saldo inicial não pode ser negativo.")

        conta = self.repo.create(user_id, account.name, account.saldo)
        return conta_to_dict(conta)

    def atualizar_conta(self, user_id: int, conta_id: int, account: ContaUpdate):
        if account.saldo is not None and account.saldo < 0:
            raise HTTPException(status_code=400, detail="Saldo não pode ser negativo.")

        conta = self.repo.update(
            user_id=user_id,
            conta_id=conta_id,
            name=account.name,
            saldo=account.saldo,
        )

        if not conta:
            raise HTTPException(status_code=404, detail="Conta não encontrada.")

        return conta_to_dict(conta)

    def deletar_conta(self, user_id: int, conta_id: int):
        deleted = self.repo.delete(
            user_id=user_id,
            conta_id=conta_id,
        )

        if not deleted:
            raise HTTPException(status_code=404, detail="Conta não encontrada.")

        return deleted
