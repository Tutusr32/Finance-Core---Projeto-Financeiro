from fastapi import HTTPException

from mappers.transaction_mapper import transacao_to_dict
from schemas.transaction_schema import TransactionCreate


class TransacoesService:
    def __init__(self, repo, contas_repo):
        self.repo = repo
        self.contas_repo = contas_repo

    def criar_transacao(self, user_id: int, conta_id: int, transaction: TransactionCreate):
        conta = self.contas_repo.get_by_id(conta_id)

        if not conta:
            raise HTTPException(status_code=404, detail="Conta não encontrada.")

        if conta.user_id != user_id:
            raise HTTPException(status_code=403, detail="Acesso negado.")

        if transaction.type == "saida":
            if conta.saldo < transaction.amount:
                raise HTTPException(status_code=400, detail="Saldo insuficiente.")

            conta.saldo -= transaction.amount

        if transaction.type == "entrada":
            conta.saldo += transaction.amount

        self.contas_repo.update(
            user_id=conta.user_id, conta_id=conta.id, saldo=conta.saldo, commit=False
        )

        transacao = self.repo.create(
            conta_id, transaction.type, transaction.amount, transaction.category, commit=False
        )

        try:
            self.repo.session.commit()

        except Exception:
            self.repo.session.rollback()
            raise

        self.repo.session.refresh(transacao)

        return transacao_to_dict(transacao)

    def listar_transacoes(self, user_id: int, conta_id: int):
        conta = self.contas_repo.get_by_id(conta_id)

        conta = self.contas_repo.get_by_id(conta_id)

        if not conta:
            raise HTTPException(
                status_code=404,
                detail="Conta não encontrada.",
            )

        if conta.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="Acesso negado.",
            )

        transacoes = self.repo.get_by_conta(conta_id)

        return [transacao_to_dict(t) for t in transacoes]
