from models.transacoes import Transacoes
from models.contas import Contas
from sqlalchemy.orm import joinedload


class TransacaoRepository:

    def get_transaction_by_id(self, session, transacao_id):
        return (
            session.query(Transacoes)
            .options(joinedload(Transacoes.conta))
            .filter(Transacoes.id == transacao_id)
            .first()
        )
    

    def get_account_by_id(self, session, conta_id):
        return (
            session.query(Contas)
            .filter(Contas.id == conta_id)
            .first()
        )
    

    def create_transaction(self, session, transacao):
        session.add(transacao)
        session.commit()
        session.refresh(transacao)
        return transacao
    

    def delete_transaction(self, session, transacao):
        session.delete(transacao)
        session.commit()
