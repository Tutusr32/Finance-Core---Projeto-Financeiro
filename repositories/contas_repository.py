from configs.connection import DBConnectionHandler
from sqlalchemy.orm import joinedload
from models.contas import Contas
from sqlalchemy.exc import NoResultFound
from models.users import Users

class ContasRepository:
    def get_by_id_and_user(self, session, user_id, conta_id):
        return (session
                .query(Contas)
                .options(joinedload(Contas.user))
                .filter(
                    Contas.user_id == user_id,
                    Contas.id == conta_id
                    )
                .first())
    

    def create_account(self, session, user_id, nome, saldo):
        session.query(Contas).options(joinedload(Contas.user))
        
        conta = Contas(user_id=user_id, nome=nome, saldo=saldo)

        session.add(conta)
        session.commit()
        session.refresh(conta)

        return conta

    def update_account(self, session, conta_id, nome=None, saldo=None):
        conta = session.query(Contas).filter(Contas.id == conta_id).first()

        if not conta:
            return None

        if nome:
            conta.nome = nome

        if saldo is not None:
            conta.saldo = saldo

        session.commit()
        session.refresh(conta)

        return conta

    
    def delete_account(self, session, conta_id):
        conta = session.query(Contas).filter(Contas.id == conta_id).first()

        data = {
        "id": conta.id,
        "user_id": conta.user_id,
        "nome_usuario": conta.user.nome,
        "nome": conta.nome,
        "saldo": conta.saldo
            }

        if not conta:
            return None

        session.delete(conta)
        session.commit()

        return data
    