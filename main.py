from repositories.transacao_repository import TransacaoRepository
from repositories.contas_repository import ContasRepository
from repositories.users_repository import UsersRepository

from services.users_service import UsersService
from services.accounts_service import ContaService
from services.transaction_service import TransactionService

from decimal import Decimal

from core.connection import DBConnectionHandler

trans_repo = TransacaoRepository()
users_repo = UsersRepository()
contas_repo = ContasRepository()

trans_service = TransactionService(trans_repo)
users_service = UsersService(users_repo)
contas_service = ContaService(contas_repo)


def menu_principal():
    while True:
        print("""
========= FINANCE CORE =========

1 - Usuários
2 - Contas
3 - Transações
0 - Sair

===============================
""")

        opcao = input("Selecione uma opção: ").strip()

        if opcao == "1":
            menu_users()

        elif opcao == "2":
            menu_contas()

        elif opcao == "3":
            menu_transacoes()

        elif opcao == "0":
            print("Encerrando sistema...")
            break

        else:
            print("Opção inválida.")

def menu_users():
    while True:
        print("""
----- USUÁRIOS -----

1 - Buscar usuário
2 - Criar usuário
3 - Atualizar usuário
4 - Deletar usuário
0 - Voltar
""")

        opcao = input("Opção: ").strip()

        if opcao == "1":

            try:
                user_id = int(input("ID do usuário: "))

                with DBConnectionHandler() as db:
                    user = users_service.buscar_usuario(
                        db.session,
                        user_id
                    )

                if user:
                    print(user)
                else:
                    print("Usuário não encontrado.")

            except ValueError:
                print("ID inválido.")

        elif opcao == "2":

            try:
                nome = input("Nome: ")
                email = input("Email: ")

                with DBConnectionHandler() as db:
                    user = users_service.criar_usuario(
                        db.session,
                        nome,
                        email
                    )

                print(user)

            except ValueError as e:
                print(e)

        elif opcao == "3":

            try:
                user_id = int(input("ID do usuário: "))

                nome = input("Novo nome (Enter para manter): ")
                nome = nome if nome.strip() else None

                email = input("Novo email (Enter para manter): ")
                email = email if email.strip() else None

                with DBConnectionHandler() as db:
                    user = users_service.atualizar_usuario(
                        db.session,
                        user_id,
                        nome,
                        email
                    )

                if user:
                    print(user)
                else:
                    print("Usuário não encontrado.")

            except ValueError as e:
                print(e)

        elif opcao == "4":

            try:
                user_id = int(input("ID do usuário: "))

                with DBConnectionHandler() as db:
                    ok = users_service.deletar_usuario(
                        db.session,
                        user_id
                    )

                if ok:
                    print("Usuário deletado.")
                else:
                    print("Usuário não encontrado.")

            except ValueError:
                print("ID inválido.")

        elif opcao == "0":
            break

        else:
            print("Opção inválida.")


def menu_contas():
    while True:
        print("""
----- CONTAS -----

1 - Buscar conta
2 - Criar conta
3 - Atualizar conta
4 - Deletar conta
0 - Voltar
""")

        opcao = input("Opção: ").strip()

        if opcao == "1":

            try:
                user_id = int(input("ID do usuário: "))
                conta_id = int(input("ID da conta: "))

                with DBConnectionHandler() as db:
                    conta = contas_service.buscar_conta(
                        db.session,
                        user_id,
                        conta_id
                    )

                if conta:
                    print(conta)
                else:
                    print("Conta não encontrada.")

            except ValueError:
                print("IDs inválidos.")

        elif opcao == "2":

            try:
                user_id = int(input("ID do usuário: "))
                nome = input("Nome da conta: ")
                saldo = Decimal(input("Saldo inicial: "))

                with DBConnectionHandler() as db:
                    conta = contas_service.criar_conta(
                        db.session,
                        user_id,
                        nome,
                        saldo
                    )

                print(conta)

            except ValueError as e:
                print(e)

        elif opcao == "3":

            try:
                conta_id = int(input("ID da conta: "))

                nome = input("Novo nome (Enter para manter): ")
                nome = nome if nome.strip() else None

                saldo_input = input("Novo saldo (Enter para manter): ")
                saldo = Decimal(saldo_input) if saldo_input.strip() else None

                with DBConnectionHandler() as db:
                    conta = contas_service.atualizar_conta(
                        db.session,
                        conta_id,
                        nome,
                        saldo
                    )

                if conta:
                    print(conta)
                else:
                    print("Conta não encontrada.")

            except ValueError as e:
                print(e)

        elif opcao == "4":

            try:
                conta_id = int(input("ID da conta: "))

                with DBConnectionHandler() as db:
                    conta = contas_service.deletar_conta(
                        db.session,
                        conta_id
                    )

                if conta:
                    print("Conta deletada.")
                    print(conta)
                else:
                    print("Conta não encontrada.")

            except ValueError:
                print("ID inválido.")

        elif opcao == "0":
            break

        else:
            print("Opção inválida.")


def menu_transacoes():
    while True:
        print("""
----- TRANSAÇÕES -----

1 - Buscar transação
2 - Criar transação
3 - Deletar transação
0 - Voltar
""")

        opcao = input("Opção: ").strip()

        if opcao == "1":

            try:
                transacao_id = int(input("ID da transação: "))

                with DBConnectionHandler() as db:
                    transacao = trans_service.get_transaction(
                        db.session,
                        transacao_id
                    )

                if transacao:
                    print(transacao)
                else:
                    print("Transação não encontrada.")

            except ValueError:
                print("ID inválido.")

        elif opcao == "2":

            try:
                conta_id = int(input("ID da conta: "))
                valor = Decimal(input("Valor: "))
                tipo = input("Tipo (E/S): ").strip().upper()
                categoria = input("Categoria: ")

                with DBConnectionHandler() as db:
                    transacao, mensagem = trans_service.create_transaction(
                        db.session,
                        conta_id,
                        valor,
                        tipo,
                        categoria
                    )

                print(mensagem)

                if transacao:
                    print(transacao)

            except ValueError as e:
                print(e)

        elif opcao == "3":

            try:
                transacao_id = int(input("ID da transação: "))

                with DBConnectionHandler() as db:
                    ok, mensagem = trans_service.delete_transaction(
                        db.session,
                        transacao_id
                    )

                print(mensagem)

            except ValueError:
                print("ID inválido.")

        elif opcao == "0":
            break

        else:
            print("Opção inválida.")
            