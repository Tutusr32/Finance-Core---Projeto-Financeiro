from sqlalchemy.orm import joinedload

from models.contas import Contas


class ContasRepository:
    def get_by_id_and_user(self, session, user_id: int, conta_id: int):
        return (
            session.query(Contas)
            .options(joinedload(Contas.user))
            .filter(Contas.user_id == user_id, Contas.id == conta_id)
            .first()
        )

    def get_by_id(self, session, conta_id: int):
        return (
            session.query(Contas)
            .options(joinedload(Contas.user))
            .filter(Contas.id == conta_id)
            .first()
        )

    def create(self, session, user_id: int, name: str, saldo):
        conta = Contas(user_id=user_id, name=name, saldo=saldo)

        session.add(conta)
        session.commit()
        session.refresh(conta)

        return conta

    def update(self, session, conta_id: int, name=None, saldo=None):
        conta = self.get_by_id(session, conta_id)

        if not conta:
            return None

        if name is not None:
            conta.name = name

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
            "user_name": conta.user.name,
            "name": conta.name,
            "saldo": conta.saldo,
        }

        session.delete(conta)
        session.commit()

        return data
    