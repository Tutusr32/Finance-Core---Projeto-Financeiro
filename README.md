# 💰 Finance Core

Backend desenvolvido em **Python**, **SQLAlchemy** e **MySQL**, simulando um sistema de gerenciamento financeiro.

O projeto foi criado para consolidar conceitos de desenvolvimento backend, aplicando boas práticas de arquitetura como **MVC**, **Repository Pattern**, **Service Layer** e **separação de responsabilidades**, servindo como base para futuras evoluções utilizando **FastAPI**.

---

Alteração -- 01/07/2026

# 🚀 Funcionalidades

## 👤 Usuários

* Criar usuário
* Buscar usuário por ID
* Atualizar usuário
* Deletar usuário

## 🏦 Contas Bancárias

* Criar conta
* Buscar conta
* Atualizar conta
* Deletar conta
* Gerenciamento de saldo

## 💸 Transações

* Registrar entradas
* Registrar saídas
* Atualização automática do saldo da conta
* Buscar transações
* Excluir transações com reversão automática do saldo

---

# 🏛 Arquitetura

O projeto utiliza uma arquitetura em camadas para manter o código desacoplado e de fácil manutenção.

```text
Finance-Core/
│
├── core/
│   ├── base.py
│   └── connection.py
│
├── models/
│   ├── users.py
│   ├── contas.py
│   └── transacoes.py
│
├── repositories/
│   ├── users_repository.py
│   ├── contas_repository.py
│   └── transacao_repository.py
│
├── services/
│   ├── users_service.py
│   ├── accounts_service.py
│   └── transaction_service.py
│
├── schemas/
│   └── contas.py
│
├── mappers/
│   └── conta_mapper.py
│
├── main.py
├── run.py
└── README.md
```

### Fluxo da aplicação

```text
Interface (CLI)
       │
       ▼
    Services
       │
       ▼
 Repositories
       │
       ▼
  SQLAlchemy ORM
       │
       ▼
      MySQL
```

### Responsabilidade de cada camada

| Camada           | Responsabilidade                                |
| ---------------- | ----------------------------------------------- |
| **core**         | Configuração da aplicação e conexão com o banco |
| **models**       | Entidades mapeadas pelo SQLAlchemy              |
| **repositories** | Operações de acesso ao banco de dados           |
| **services**     | Regras de negócio da aplicação                  |
| **schemas**      | DTOs utilizados para padronização dos dados     |
| **mappers**      | Conversão entre Models e Schemas                |
| **main**         | Interface de interação com o usuário            |

---

# 🛠 Tecnologias Utilizadas

* Python 3.13
* SQLAlchemy
* MySQL
* PyMySQL
* Git

---

# ▶️ Como executar

Clone o repositório

```bash
git clone https://github.com/Tutusr32/Finance-Core---Projeto-Financeiro
```

Entre na pasta

```bash
cd Finance-Core---Projeto-Financeiro
```

Instale as dependências

```bash
pip install sqlalchemy pymysql
```

Crie o banco de dados

```sql
CREATE DATABASE finance_core;
```

Configure sua conexão no arquivo

```text
core/connection.py
```

Execute a aplicação

```bash
python run.py
```

---

# 📚 Conceitos aplicados

* Programação Orientada a Objetos (POO)
* SQLAlchemy ORM
* CRUD completo
* Relacionamentos entre tabelas
* Context Manager para gerenciamento de sessões
* Arquitetura MVC
* Repository Pattern
* Service Layer Pattern
* Separação de responsabilidades
* Injeção de dependência
* Mappers
* DTOs (Schemas)

---

# 🎯 Objetivo

Este projeto foi desenvolvido para aprofundar conhecimentos em desenvolvimento backend utilizando Python, criando uma aplicação organizada, escalável e preparada para evoluir para uma API REST.

Além da implementação do CRUD, o foco foi aplicar conceitos presentes em aplicações reais, buscando uma arquitetura limpa e de fácil manutenção.

---

# 🔮 Roadmap

* ✅ CRUD completo
* ✅ Arquitetura MVC
* ✅ Repository Pattern
* ✅ Service Layer
* ✅ Mappers
* ✅ Schemas (DTOs)

### Próximas evoluções

* API REST com FastAPI
* Controllers
* DTOs completos para todas as entidades
* Pydantic
* Autenticação JWT
* Testes automatizados
* Docker
* Swagger/OpenAPI
* Logging
* Tratamento global de exceções

---

# 👨‍💻 Autor

Desenvolvido por **Arthur Rezende** como projeto de estudos para evolução em desenvolvimento backend com Python, SQLAlchemy e boas práticas de arquitetura de software.
