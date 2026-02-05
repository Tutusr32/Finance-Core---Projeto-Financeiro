from configs.connection import DBConnectionHandler
from models.contas import Contas
from models.transacoes import Transacoes
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import NoResultFound

class TransacaoRepository():
    def select(self):
        while True:
            with DBConnectionHandler() as db:
                try:
                    trans_id = int(input("Digite o ID da transação: "))

                    data = (
                        db.session
                        .query(Transacoes)
                        .options(joinedload(Transacoes.conta))
                        .filter(Transacoes.id == trans_id)
                        .one()
                    )

                    print(data)

                except ValueError:
                    print("Digite apenas números.")

                except NoResultFound:
                    print("Transação não encontrada.")

            if input("Continuar? (S/N): ").upper() != "S":
                break

    def insert(self):
        while True:
            with DBConnectionHandler() as db:
                try:
                    conta_id = int(input("ID da conta: "))

                    conta = db.session.query(Contas).filter(Contas.id == conta_id).first()

                    if not conta:
                        print("Conta não existe.")
                        continue

                    valor = int(input("Valor da transação: "))

                    if valor <= 0:
                        print("Valor inválido.")
                        continue

                    tipo = input("Entrada(E) ou Saída(S): ").upper()[0]
                    categoria = input("Categoria: ")

                    if tipo == "E":
                        conta.saldo += valor
                        tipo = "entrada"

                    elif tipo == "S":
                        if valor > conta.saldo:
                            print("Saldo insuficiente.")
                            continue
                        conta.saldo -= valor
                        tipo = "saida"

                    else:
                        print("Tipo inválido.")
                        continue

                    transacao = Transacoes(
                        conta_id=conta_id,
                        valor=valor,
                        tipo=tipo,
                        categoria=categoria
                    )

                    db.session.add(transacao)
                    db.session.commit()

                    print("Transação registrada com sucesso.")

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
                    trans_id = int(input("ID da transação: "))

                    trans = (
                        db.session
                        .query(Transacoes)
                        .filter(Transacoes.id == trans_id)
                        .one()
                    )

                    conta = db.session.query(Contas).filter(Contas.id == trans.conta_id).first()

                    # rollback financeiro
                    if trans.tipo == "entrada":
                        conta.saldo -= trans.valor

                    elif trans.tipo == "saida":
                        conta.saldo += trans.valor

                    db.session.delete(trans)
                    db.session.commit()

                    print("Transação excluída e saldo ajustado.")

                except ValueError:
                    print("Digite apenas números.")

                except NoResultFound:
                    print("Transação não encontrada.")

                except Exception as e:
                    db.session.rollback()
                    raise e

            if input("Continuar? (S/N): ").upper() != "S":
                break
