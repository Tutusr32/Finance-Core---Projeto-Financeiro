from configs.connection import DBConnectionHandler
from models.users import Users
from sqlalchemy.exc import NoResultFound

class UsersRepository:

    def get_by_id(self, session, user_id):
        return session.query(Users).filter(Users.id == user_id).first()
    
    def create(self, session, nome: str, email: str):
        user = Users(nome=nome, email=email)

        session.add(user)
        session.commit()
        session.refresh(user)

        return user
    
    def update(self, session, user_id: int, nome: str = None, email: str = None):
        user = session.query(Users).filter(Users.id == user_id).first()

        if not user:
            return None

        if nome:
            user.nome = nome

        if email:
            user.email = email

        session.commit()
        session.refresh(user)

        return user
    
    def delete_user(self, session, user_id: int):
        user = session.query(Users).filter(Users.id == user_id).first()

        if not user:
            return None
        
        session.delete(user)
        session.commit()
