from models.users import Users


class UsersRepository:

    def get_by_id(self, session, user_id: int):
        return session.query(Users).filter(Users.id == user_id).first()

    def create(self, session, nome: str, email: str):
        user = Users(nome=nome, email=email)

        session.add(user)
        session.commit()
        session.refresh(user)

        return user

    def update(self, session, user_id: int, nome=None, email=None):
        user = self.get_by_id(session, user_id)

        if not user:
            return None

        if nome is not None:
            user.nome = nome

        if email is not None:
            user.email = email

        session.commit()
        session.refresh(user)

        return user

    def delete(self, session, user_id: int):
        user = self.get_by_id(session, user_id)

        if not user:
            return False

        session.delete(user)
        session.commit()

        return True
    