from sqlalchemy.orm import joinedload
from models.contas import Contas


class ContasRepository:
    def __init__(self, session):
        self.session = session

    def get_by_id_and_user(self, user_id: int, conta_id: int):
        return (
            self.session.query(Contas)
            .options(joinedload(Contas.user))
            .filter(Contas.user_id == user_id, Contas.id == conta_id)
            .first()
        )

    def get_by_id(self, conta_id: int):
        return (
            self.session.query(Contas)
            .options(joinedload(Contas.user))
            .filter(Contas.id == conta_id)
            .first()
        )

    def create(self, user_id: int, name: str, saldo):
        conta = Contas(user_id=user_id, name=name, saldo=saldo)
        self.session.add(conta)
        self.session.commit()
        self.session.refresh(conta)
        return conta

    def update(
        self,
        user_id: int,
        conta_id: int,
        name=None,
        saldo=None,
    ):
        conta = (
            self.session.query(Contas)
            .filter(
                Contas.id == conta_id,
                Contas.user_id == user_id,
            )
            .first()
        )

        if not conta:
            return None

        if name is not None:
            conta.name = name

        if saldo is not None:
            conta.saldo = saldo

        self.session.commit()
        self.session.refresh(conta)

        return conta

    def delete(self, user_id: int, conta_id: int,):
        conta = (
            self.session.query(Contas)
            .filter(
                Contas.id == conta_id,
                Contas.user_id == user_id,
            )
            .first()
        )

        if not conta:
            return None

        self.session.delete(conta)
        self.session.commit()

        return True
