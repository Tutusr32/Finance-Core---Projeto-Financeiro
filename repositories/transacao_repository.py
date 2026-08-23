from models.transacoes import Transacoes


class TransacaoRepository:
    def __init__(self, session):
        self.session = session

    def create(self, conta_id: int, tipo: str, valor, categoria: str, commit: bool = True):
        transacao = Transacoes(
            conta_id=conta_id,
            tipo=tipo,
            valor=valor,
            categoria=categoria,
        )

        self.session.add(transacao)

        if commit:
            self.session.commit()
            self.session.refresh(transacao)

        return transacao

    def get_by_conta(self, conta_id: int, limit: int, offset: int):
        return (
            self.session.query(Transacoes)
            .filter(Transacoes.conta_id == conta_id)
            .order_by(Transacoes.id.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
