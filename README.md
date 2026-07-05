# Finance Core

Finance Core é uma API REST desenvolvida em Python utilizando FastAPI, SQLAlchemy e MySQL para gerenciamento financeiro.

O projeto tem como objetivo aplicar boas práticas de desenvolvimento backend, utilizando arquitetura em camadas, separação de responsabilidades e padrões amplamente utilizados no desenvolvimento de APIs.

---

## Funcionalidades

- CRUD de usuários
- CRUD de contas bancárias
- Registro de transações de entrada e saída
- Atualização automática do saldo das contas
- Validação de saldo insuficiente para operações de débito
- Hash seguro de senhas utilizando Argon2
- Injeção de dependências com FastAPI
- Mapeamento entre entidades e objetos de resposta

---

## Arquitetura

A aplicação foi desenvolvida utilizando uma arquitetura em camadas, onde cada componente possui uma responsabilidade específica.

```text
HTTP Request
      │
      ▼
Controllers
      │
      ▼
Services
(Regras de negócio)
      │
      ▼
Repositories
(Acesso ao banco)
      │
      ▼
MySQL
```

### Estrutura do projeto

```text
Finance-Core/
├── controllers/
├── core/
├── dependencies/
├── mappers/
├── models/
├── repositories/
├── schemas/
├── services/
├── main.py
├── pyproject.toml
└── README.md
```

---

## Tecnologias

### Backend

- Python 3.13
- FastAPI
- SQLAlchemy

### Banco de dados

- MySQL
- PyMySQL

### Validação

- Pydantic

### Segurança

- pwdlib (Argon2)

### Servidor

- Uvicorn

---

## Endpoints

### Usuários

| Método | Endpoint |
|---------|----------|
| POST | /users |
| GET | /users/{user_id} |
| PATCH | /users/{user_id} |
| DELETE | /users/{user_id} |

### Contas

| Método | Endpoint |
|---------|----------|
| POST | /accounts |
| GET | /accounts/{user_id}/{account_id} |
| PATCH | /accounts/{user_id}/{account_id} |
| DELETE | /accounts/{user_id}/{account_id} |

### Transações

| Método | Endpoint |
|---------|----------|
| POST | /transactions |
| GET | /transactions/{account_id} |

---

## Como executar

Clone o repositório:

```bash
git clone https://github.com/Tutusr32/Finance-Core---Projeto-Financeiro
```

Entre na pasta:

```bash
cd Finance-Core---Projeto-Financeiro
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Crie o banco de dados:

```sql
CREATE DATABASE finance_core;
```

Configure a conexão em:

```text
core/database.py
```

Inicie a aplicação:

```bash
uvicorn main:app --reload
```

A documentação estará disponível em:

```text
http://localhost:8000/docs
```

---

## Conceitos aplicados

- Programação Orientada a Objetos
- SQLAlchemy ORM
- Repository Pattern
- Service Layer Pattern
- Arquitetura em Camadas
- Injeção de Dependências
- Separação de Responsabilidades
- Mappers
- Schemas
- Relacionamentos entre tabelas
- Hash de senhas com Argon2

---

## Roadmap

- Implementar autenticação JWT
- Implementar autorização baseada no usuário autenticado
- Adicionar testes automatizados
- Containerizar a aplicação com Docker
- Configurar CI/CD com GitHub Actions
- Implementar logs estruturados
- Adicionar paginação e filtros de consulta

---

## Autor

Desenvolvido por Arthur Rezende como projeto para demonstrar conhecimentos em desenvolvimento backend com Python, FastAPI, SQLAlchemy e arquitetura em camadas.