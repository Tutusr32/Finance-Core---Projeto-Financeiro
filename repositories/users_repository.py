from models.users import Users


class UsersRepository:
    def __init__(self, session):
        self.session = session

    def create(self, name: str, email: str):
        user = Users(name=name, email=email)

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return user

    def get_by_id(self, user_id: int):
        return (
            self.session
            .query(Users)
            .filter(Users.id == user_id)
            .first()
        )

    def update(self, user_id: int, name=None, email=None):
        user = self.get_by_id(user_id)

        if not user:
            return None

        if name is not None:
            user.name = name

        if email is not None:
            user.email = email

        self.session.commit()
        self.session.refresh(user)

        return user

    def delete(self, user_id):

        user = self.get_by_id(user_id)

        if not user:
            return False

        self.session.delete(user)
        self.session.commit()

        return True
        