from repositories.contas_repository import ContasRepository
from repositories.transacao_repository import TransacaoRepository
from services.users_service import UsersService

users_service = UsersService()
contas_repo = ContasRepository()
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
            contas_repo.select()

        elif opcao == "2":
            contas_repo.insert()

        elif opcao == "3":
            contas_repo.update()

        elif opcao == "4":
            contas_repo.delete()

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
