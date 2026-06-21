from configs.connection import DBConnectionHandler
from sqlalchemy.orm import joinedload
from models.contas import Contas
from sqlalchemy.exc import NoResultFound
from models.users import Users

class ContasRepository:
    def select(self):
        while True:
            with DBConnectionHandler() as db:
                try:
                    user_id = int(input("Digite o ID do usuário: "))
                    conta_id = int(input("Digite o ID da conta: "))

                    data = (
                        db.session
                        .query(Contas)
                        .options(joinedload(Contas.user))
                        .filter(Contas.user_id == user_id)
                        .filter(Contas.id == conta_id)
                        .one()
                    )

                    print(data)

                except ValueError:
                    print("Digite apenas números.")

                except NoResultFound:
                    print("Conta ou usuário não encontrado.")

            if input("Continuar? (S/N): ").upper() != "S":
                break

    def insert(self):

        while True:
            with DBConnectionHandler() as db:
                try:
                    user_id = int(input("ID do usuário: "))

                    user = db.session.query(Users).filter(Users.id == user_id).first()

                    if not user:
                        print("Usuário não existe.")
                        continue

                    nome = input("Nome da conta: ")
                    saldo = int(input("Saldo inicial: "))

                    conta = Contas(user_id=user_id, nome=nome, saldo=saldo)

                    db.session.add(conta)
                    db.session.commit()

                    print("Conta criada.")

                except ValueError:
                    print("Digite valores válidos.")

                except Exception as e:
                    db.session.rollback()
                    raise e

            if input("Continuar? (S/N): ").upper() != "S":
                break

    def update(self):
        while True:
            with DBConnectionHandler() as db:
                try:
                    id = int(input("ID da conta: "))

                    conta = db.session.query(Contas).filter(Contas.id == id).first()

                    if not conta:
                        print("Conta não existe.")
                        continue

                    print("1 - Nome\n2 - Saldo")
                    opcao = int(input("Opção: "))

                    if opcao == 1:
                        conta.nome = input("Novo nome: ")

                    elif opcao == 2:
                        conta.saldo = int(input("Novo saldo: "))

                    else:
                        print("Opção inválida.")
                        continue

                    db.session.commit()
                    print("Atualizado.")

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
                    id = int(input("ID da conta: "))

                    conta = db.session.query(Contas).filter(Contas.id == id).first()

                    if not conta:
                        print("Conta não existe.")
                        continue

                    db.session.delete(conta)
                    db.session.commit()

                    print("Conta deletada.")

                except ValueError:
                    print("Digite apenas números.")

                except Exception as e:
                    db.session.rollback()
                    raise e

            if input("Continuar? (S/N): ").upper() != "S":
                break
