# Finance Core

Finance Core é uma API REST para gerenciamento financeiro pessoal, desenvolvida em Python com FastAPI, SQLAlchemy e MySQL.

O projeto foi construído com foco em separação de responsabilidades, segurança, organização de código e evolução gradual da arquitetura.

---

## Funcionalidades

* Cadastro, consulta, atualização e remoção de usuários
* Autenticação com JWT
* Hash de senhas com Argon2
* Cadastro, consulta, atualização e remoção de contas
* Registro de transações de entrada e saída
* Atualização automática do saldo da conta conforme a transação
* Validação de saldo insuficiente
* Controle de acesso por usuário autenticado
* Estrutura organizada em camadas

---

## Tecnologias utilizadas

### Backend

* Python 3.13
* FastAPI
* SQLAlchemy
* Pydantic

### Banco de dados

* MySQL
* PyMySQL

### Segurança

* JWT
* pwdlib com Argon2

### Configuração e execução

* Uvicorn
* python-dotenv
* pydantic-settings

### Desenvolvimento

* Poetry
* Ruff
* Pytest

---

## Arquitetura

A aplicação segue uma organização em camadas:

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

### Responsabilidade de cada camada

* **Controllers**: recebem a requisição e devolvem a resposta
* **Services**: concentram as regras de negócio
* **Repositories**: lidam com persistência e consultas
* **Models**: representam as tabelas do banco
* **Schemas**: validam entrada e saída de dados
* **Mappers**: transformam objetos ORM em respostas mais simples
* **Dependencies**: centralizam injeção de dependência

---

## Estrutura do projeto

```text
Finance-Core/
├── app/
│   └── main.py
├── controllers/
├── core/
├── dependencies/
├── mappers/
├── models/
├── repositories/
├── schemas/
├── services/
├── db.sql
├── pyproject.toml
└── README.md
```

---

## Autenticação

O sistema utiliza autenticação via JWT.

Rotas protegidas exigem envio do token no cabeçalho:

```text
Authorization: Bearer <token>
```

---

## Endpoints

### Autenticação

| Método | Endpoint      | Descrição                       |
| ------ | ------------- | ------------------------------- |
| POST   | `/auth/login` | Realiza login e retorna o token |

### Usuários

| Método | Endpoint           | Descrição                     |
| ------ | ------------------ | ----------------------------- |
| POST   | `/users`           | Cria um usuário               |
| GET    | `/users/me`        | Retorna o usuário autenticado |
| GET    | `/users/{user_id}` | Retorna um usuário específico |
| PATCH  | `/users/{user_id}` | Atualiza os dados do usuário  |
| DELETE | `/users/{user_id}` | Remove o usuário              |

### Contas

| Método | Endpoint                 | Descrição                                       |
| ------ | ------------------------ | ----------------------------------------------- |
| POST   | `/accounts`              | Cria uma conta vinculada ao usuário autenticado |
| GET    | `/accounts/{conta_id}`   | Consulta uma conta do usuário autenticado       |
| PATCH  | `/accounts/{account_id}` | Atualiza uma conta do usuário autenticado       |
| DELETE | `/accounts/{account_id}` | Remove uma conta do usuário autenticado         |

### Transações

| Método | Endpoint                   | Descrição                         |
| ------ | -------------------------- | --------------------------------- |
| POST   | `/transactions/{conta_id}` | Cria uma transação para uma conta |
| GET    | `/transactions/{conta_id}` | Lista transações de uma conta     |

---

## Regras de negócio atuais

* Usuário só pode acessar os próprios dados
* Conta só pode ser acessada pelo dono
* Transações de saída não podem gerar saldo negativo
* Saldo inicial da conta não pode ser negativo
* Tipos válidos de transação: `entrada` e `saida`

---

## Como executar o projeto

### 1. Instalar dependências

```bash
poetry install
```

### 2. Configurar as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com as variáveis necessárias:

```env
SECRET_KEY=sua_chave_secreta
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=mysql+pymysql://usuario:senha@localhost:3306/finance_core
ENVIRONMENT=development
LOG_LEVEL=info
```

### 3. Criar o banco de dados

```sql
CREATE DATABASE finance_core;
```

### 4. Executar a aplicação

```bash
poetry run uvicorn app.main:app --reload
```

### 5. Abrir a documentação automática

```text
http://localhost:8000/docs
```

---

## Comandos úteis

```bash
poetry run task run
poetry run task lint
poetry run task format
poetry run task test
```

---

## Conceitos aplicados

* API REST
* Autenticação JWT
* Injeção de dependência
* ORM com SQLAlchemy
* Repository Pattern
* Service Layer
* Separação de responsabilidades
* Validação com Pydantic
* Mapeamento entre camadas
* Controle de acesso por usuário

---

## Roadmap

* Implementar testes automatizados
* Adicionar paginação e filtros
* Melhorar relatórios e extratos
* Criar transferências entre contas
* Adicionar categorias mais completas
* Implementar auditoria e histórico de alterações
* Containerizar com Docker
* Adicionar CI/CD com GitHub Actions

---

## Autor

Desenvolvido por Arthur Rezende.
