from fastapi import HTTPException

from mappers.transaction_mapper import transacao_to_dict


class TransacoesService:
    def __init__(self, repo, contas_repo):
        self.repo = repo
        self.contas_repo = contas_repo

    def criar_transacao(self, user_id: int, conta_id: int, tipo: str, valor, categoria: str = "geral"):
        conta = self.contas_repo.get_by_id(conta_id)

        if not conta:
            raise HTTPException(status_code=404, detail="Conta não encontrada.")

        if conta.user_id != user_id:
            raise HTTPException(status_code=404, detail="Conta não encontrada para este usuário.")

        if valor <= 0:
            raise HTTPException(status_code=400, detail="Valor inválido.")

        if tipo == "saida":
            if conta.saldo < valor:
                raise HTTPException(status_code=400, detail="Saldo insuficiente.")
            conta.saldo -= valor

        elif tipo == "entrada":
            conta.saldo += valor

        else:
            raise HTTPException(status_code=400, detail="Tipo inválido (use entrada ou saída).")

        self.contas_repo.update(user_id=conta.user_id, conta_id=conta.id, saldo=conta.saldo)

        transacao = self.repo.create(conta_id, tipo, valor, categoria)

        return transacao_to_dict(transacao)

    def listar_transacoes(self, conta_id: int):
        transacoes = self.repo.get_by_conta(conta_id)

        return [transacao_to_dict(t) for t in transacoes]
