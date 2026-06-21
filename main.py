from repositories.transacao_repository import TransacaoRepository
from services.users_service import UsersService
from services.accounts_service import ContaService
from decimal import Decimal

users_service = UsersService()
contas_service = ContaService()
trans_repo = TransacaoRepository()


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
            
            user = users_service.buscar_usuario(user_id)
            print(user)

        elif opcao == "2":

            nome = input("Nome: ")
            email = input("Email: ")

            user = users_service.criar_usuario(nome, email)

            print("Usuário criado:", user)

        elif opcao == "3":
            user_id = int(input("ID do usuário: "))

            print("1 - Nome\n2 - Email")
            opcao = int(input("Opção: "))

            nome = None
            email = None

            if opcao == 1:
                nome = input("Novo nome: ")

            elif opcao == 2:
                email = input("Novo email: ")

            user = users_service.atualizar_usuario(user_id, nome, email)

            print("Atualizado:", user)

        elif opcao == "4":
            user_id = int(input("ID do usuário: "))
            print(user)
            user = users_service.deletar_usuario(user_id)


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

            conta = contas_service.buscar_conta(user_id, conta_id)
            print(conta)

        elif opcao == "2":

            user_id = int(input("ID do usuário: "))
            nome = input("Nome da Conta: ")
            saldo = Decimal(input("Saldo Inicial: "))
            
            conta = contas_service.criar_conta(user_id, nome, saldo)
            
            print(conta)

        elif opcao == "3":
            conta_id = int(input("ID da conta: "))

            nome = input("Novo nome (enter manter): ")
            nome = nome if nome.strip() != "" else None

            saldo_input = input("Novo saldo (enter para manter): ")
            saldo = None

            if saldo_input.strip() != "":
                saldo = Decimal(saldo_input)

            conta = contas_service.atualizar_conta(conta_id, nome, saldo)
            
            print(conta)

        elif opcao == "4":
            conta_id = int(input("ID da conta para deletar: "))

            resultado = contas_service.deletar_conta(conta_id)

            print("Conta deletada:")
            print(resultado)

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
            trans_repo.select()

        elif opcao == "2":
            trans_repo.insert()

        elif opcao == "3":
            trans_repo.delete()

        elif opcao == "0":
            break

        else:
            print("Opção inválida.")
