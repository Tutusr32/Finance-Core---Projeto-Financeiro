from sqlalchemy.orm import joinedload

from models.contas import Contas
from models.transacoes import Transacoes


class TransacaoRepository:
    def __init__(self, session):
        self.session = session

    def create(self, conta_id: int, tipo: str, valor, categoria: str):
        transacao = Transacoes(
            conta_id=conta_id,
            tipo=tipo,
            valor=valor,
            categoria=categoria,
        )
        self.session.add(transacao)
        self.session.commit()
        self.session.refresh(transacao)
        return transacao

    def get_by_conta(self, conta_id: int):
        return (
            self.session.query(Transacoes)
            .filter(Transacoes.conta_id == conta_id)
            .order_by(Transacoes.id.desc())
            .all()
        )

    def create_transaction(self, transacao):
        self.session.add(transacao)
        self.session.commit()
        self.session.refresh(transacao)
        return transacao

    def get_transaction_by_id(self, transacao_id):
        return (
            self.session.query(Transacoes)
            .options(joinedload(Transacoes.conta))
            .filter(Transacoes.id == transacao_id)
            .first()
        )

    def get_account_by_id(self, conta_id):
        return self.session.query(Contas).filter(Contas.id == conta_id).first()

    def delete_transaction(self, transacao):
        self.session.delete(transacao)
        self.session.commit()
