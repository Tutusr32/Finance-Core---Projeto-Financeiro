#  Finance Core - Sistema Financeiro com Python + SQLAlchemy

Projeto backend desenvolvido em Python utilizando SQLAlchemy e MySQL para gerenciar:

- Usuários
- Contas bancárias
- Transações financeiras

Tudo organizado em estrutura de serviços + repositórios, com menu interativo no terminal.

---

##  Funcionalidades

###  Usuários
- Criar usuário
- Buscar usuário
- Atualizar usuário
- Deletar usuário

###  Contas
- Criar conta bancária
- Listar contas de um usuário
- Atualizar conta
- Deletar conta
- Gerenciar saldo

###  Transações
- Registrar transações (entrada e saída)
- Listar transações
- Deletar transações
- Resetar tabela de transações

---

##  Tecnologias Utilizadas

- Python 3.13
- SQLAlchemy (ORM)
- MySQL
- PyMySQL
- Git

---

##  Estrutura do Projeto

```text
Projeto Financeiro - Alchemy/
│
├── run.py                # Arquivo principal para executar o sistema
├── main.py               # Menus do sistema
│
├── database/
│   └── connection.py    # Gerenciador de conexão com o banco
│
├── models/
│   ├── users.py         # Model de usuários
│   ├── accounts.py     # Model de contas
│   └── transactions.py # Model de transações
│
├── services/
│   ├── users_repository.py
│   ├── accounts_repository.py
│   └── transactions_repository.py
│
└── README.md
```

## Como Rodar
- git clone https://github.com/Tutusr32/Finance-Core---Projeto-Financeiro
  
  # Instale as dependências
- pip install sqlalchemy pymysql
  
  # Crie o banco de dados
- CREATE DATABASE finance_core;
- Crie e coloque sua engine no arquivo connecrion.py
  
  # Execute o run.py

## Objetivo do projeto

- Projeto criado para:

-- Praticar SQLAlchemy na prática

-- Trabalhar com CRUD completo

-- Entender relacionamento entre tabelas

-- Simular um sistema financeiro real

## Próximos passos

- Validações mais robustas

- Tratamento de erros melhorado

- Logs

- Interface futura (API ou web)
