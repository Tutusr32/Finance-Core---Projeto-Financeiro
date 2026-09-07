from datetime import date, datetime, timedelta

from models.transacoes import Transacoes


class TransacaoRepository:
    def __init__(self, session):
        self.session = session

    def create(
        self,
        conta_id: int,
        tipo: str,
        valor,
        categoria: str,
        commit: bool = True,
    ):
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

    def get_by_conta(
        self,
        conta_id: int,
        limit: int,
        offset: int,
        tipo: str | None = None,
        categoria: str | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ):
        query = self.session.query(Transacoes).filter(Transacoes.conta_id == conta_id)

        if tipo:
            query = query.filter(Transacoes.tipo == tipo)

        if categoria:
            query = query.filter(Transacoes.categoria == categoria)

        if start_date:
            query = query.filter(
                Transacoes.data >= datetime.combine(start_date, datetime.min.time())
            )

        if end_date:
            next_day = end_date + timedelta(days=1)

            query = query.filter(
                Transacoes.data
                < datetime.combine(
                    next_day,
                    datetime.min.time(),
                )
            )

        return query.order_by(Transacoes.id.desc()).offset(offset).limit(limit).all()
