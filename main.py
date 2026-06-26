from repositories.transacao_repository import TransacaoRepository
from repositories.contas_repository import ContasRepository
from repositories.users_repository import UsersRepository

from services.users_service import UsersService
from services.accounts_service import ContaService

from decimal import Decimal

from core.connection import DBConnectionHandler

trans_repo = TransacaoRepository()

users_repo = UsersRepository()
contas_repo = ContasRepository()

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
            user_id = int(input("ID do usuário: "))

            with DBConnectionHandler() as db:
                user = users_service.buscar_usuario(
                    db.session,
                    user_id)

            if not user:
                print("Usuário não encontrado.")
            else:
                print(user)


        elif opcao == "2":
            nome = str(input("Nome: "))
            email = str(input("Email: "))

            with DBConnectionHandler() as db:
                user = users_service.criar_usuario(
                    db.session,
                    nome,
                    email)

            print(user)

        elif opcao == "3":
            user_id = int(input("ID do usuário: "))

            nome = str(input("Novo nome (Enter para ignorar): "))
            email = str(input("Novo Email (Enter para ignorar): "))

            with DBConnectionHandler() as db:
                user = users_service.atualizar_usuario(
                    db.session,
                    user_id,
                    nome,
                    email)

            if not user:
                print("Usuário não encontrado.")
            else:
                print(user)

        elif opcao == "4":
            user_id = int(input("ID do usuário: "))
            
            with DBConnectionHandler() as db:
                ok = users_service.deletar_usuario(
                    db.session,
                    user_id)

            if ok:
                print("Usuário deletado.")
            else:
                print("Usuário não encontrado.")


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

            user_id = int(input("ID do usuário: "))
            conta_id = int(input("ID da conta: "))

            with DBConnectionHandler() as db:
                conta = contas_service.buscar_conta(
                    db.session,
                    user_id,
                    conta_id)

            if not conta:
                print("Conta não encontrada.")
            else:
                print(conta)


        elif opcao == "2":

            user_id = int(input("ID do usuário: "))
            nome = input("Nome da Conta: ")
            saldo = Decimal(input("Saldo Inicial: "))
            
            with DBConnectionHandler() as db:
                conta = contas_service.criar_conta(
                    db.session,
                    user_id,
                    nome,
                    saldo)

            print(conta)

        elif opcao == "3":
            conta_id = int(input("ID da conta: "))

            nome = input("Novo nome (enter manter): ")
            nome = nome if nome.strip() != "" else None

            saldo_input = input("Novo saldo (enter para manter): ")
            saldo = None

            if saldo_input.strip() != "":
                saldo = Decimal(saldo_input)

            try:

                with DBConnectionHandler() as db:
                    conta = contas_service.atualizar_conta(
                        db.session,
                        conta_id,
                        nome,
                        saldo)

                if not conta:
                    print("Conta não encontrada.")
                else:
                    print(conta)

            except ValueError as e:
                print(e)

        elif opcao == "4":
            conta_id = int(input("ID da conta para deletar: "))

            with DBConnectionHandler() as db:
                conta = contas_service.deletar_conta(
                    db.session,
                    conta_id)

            if not conta:
                print("Conta não encontrada.")
            else:
                print("Conta deletada:")
                print(conta)

        elif opcao == "0":
            break


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
            trans_repo.select()

        elif opcao == "2":
            trans_repo.insert()

        elif opcao == "3":
            trans_repo.delete()

        elif opcao == "0":
            break

        else:
            print("Opção inválida.")
