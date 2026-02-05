from configs.connection import DBConnectionHandler
from models.users import Users
from sqlalchemy.exc import NoResultFound

class UsersRepository:
    def select(self):
        while True:
            with DBConnectionHandler() as db:
                try:
                    user_id = int(input("ID do usuário: "))

                    data = (
                        db.session
                        .query(Users)
                        .filter(Users.id == user_id)
                        .one()
                    )

                    print(data)

                except ValueError:
                    print("Digite apenas números.")

                except NoResultFound:
                    print("Usuário não encontrado.")

            if input("Continuar? (S/N): ").upper() != "S":
                break

    def insert(self):
        while True:
            with DBConnectionHandler() as db:
                try:
                    nome = input("Nome: ").capitalize()
                    email = input("Email: ")

                    user = Users(nome=nome, email=email)

                    db.session.add(user)
                    db.session.commit()

                    print("Usuário criado.")

                except Exception as e:
                    db.session.rollback()
                    raise e

            if input("Continuar? (S/N): ").upper() != "S":
                break

    def update(self):
        while True:
            with DBConnectionHandler() as db:
                try:
                    user_id = int(input("ID do usuário: "))

                    user = db.session.query(Users).filter(Users.id == user_id).first()

                    if not user:
                        print("Usuário não encontrado.")
                        continue

                    print("1 - Nome\n2 - Email")
                    opcao = int(input("Opção: "))

                    if opcao == 1:
                        user.nome = input("Novo nome: ")

                    elif opcao == 2:
                        user.email = input("Novo email: ")

                    else:
                        print("Opção inválida.")
                        continue

                    db.session.commit()
                    print("Atualizado com sucesso.")

                except ValueError:
                    print("Digite valores válidos.")

                except Exception as e:
                    db.session.rollback()
                    raise e

            if input("Continuar? (S/N): ").upper() != "S":
                break

    def delete(self):
        while True:
            with DBConnectionHandler() as db:
                try:
                    user_id = int(input("ID do usuário: "))

                    user = db.session.query(Users).filter(Users.id == user_id).first()

                    if not user:
                        print("Usuário não encontrado.")
                        continue

                    db.session.delete(user)
                    db.session.commit()

                    print("Usuário deletado.")

                except ValueError:
                    print("Digite apenas números.")

                except Exception as e:
                    db.session.rollback()
                    raise e

            if input("Continuar? (S/N): ").upper() != "S":
                break
