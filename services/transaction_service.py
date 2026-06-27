from models.transacoes import Transacoes


class TransactionService:

    def __init__(self, repository):
        self.repository = repository
        

    def create_transaction(self, session, conta_id, valor, tipo, categoria):

        conta = self.repository.get_account_by_id(session, conta_id)

        if not conta:
            return None, "Conta não encontrada."

        if valor <= 0:
            return None, "Valor inválido."

        if tipo == "E":
            conta.saldo += valor
            tipo = "entrada"

        elif tipo == "S":

            if conta.saldo < valor:
                return None, "Saldo insuficiente."

            conta.saldo -= valor
            tipo = "saida"

        else:
            return None, "Tipo inválido."

        transacao = Transacoes(
            conta_id=conta_id,
            valor=valor,
            tipo=tipo,
            categoria=categoria
        )

        transacao = self.repository.create_transaction(session, transacao)

        return transacao, "Transação registrada com sucesso."
    

    def get_transaction(self, session, transacao_id):
        return self.repository.get_transaction_by_id(session, transacao_id)
    

    def delete_transaction(self, session, transacao_id):

        transacao = self.repository.get_transaction_by_id(session, transacao_id)

        if not transacao:
            return False, "Transação não encontrada."

        conta = self.repository.get_account_by_id(session, transacao.conta_id)

        if transacao.tipo == "entrada":
            conta.saldo -= transacao.valor

        elif transacao.tipo == "saida":
            conta.saldo += transacao.valor

        self.repository.delete_transaction(session, transacao)

        return True, "Transação excluída e saldo ajustado."
    