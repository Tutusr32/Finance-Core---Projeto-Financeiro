from sqlalchemy.orm import joinedload

from models.contas import Contas


class ContasRepository:

    def get_by_id_and_user(self, session, user_id: int, conta_id: int):
        return (
            session.query(Contas)
            .options(joinedload(Contas.user))
            .filter(
                Contas.user_id == user_id,
                Contas.id == conta_id
            )
            .first()
        )

    def get_by_id(self, session, conta_id: int):
        return (
            session.query(Contas)
            .options(joinedload(Contas.user))
            .filter(Contas.id == conta_id)
            .first()
        )

    def create(self, session, user_id: int, nome: str, saldo):
        conta = Contas(
            user_id=user_id,
            nome=nome,
            saldo=saldo
        )

        session.add(conta)
        session.commit()
        session.refresh(conta)

        return conta

    def update(self, session, conta_id: int, nome=None, saldo=None):
        conta = self.get_by_id(session, conta_id)

        if not conta:
            return None

        if nome is not None:
            conta.nome = nome

        if saldo is not None:
            conta.saldo = saldo

        session.commit()
        session.refresh(conta)

        return conta

    def delete(self, session, conta_id: int):
        conta = self.get_by_id(session, conta_id)

        if not conta:
            return None

        data = {
            "id": conta.id,
            "user_id": conta.user_id,
            "nome_usuario": conta.user.nome,
            "nome": conta.nome,
            "saldo": conta.saldo
        }

        session.delete(conta)
        session.commit()

        return data
    