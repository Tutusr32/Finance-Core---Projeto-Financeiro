# Finance Core

API REST de gerenciamento financeiro pessoal, desenvolvida para consolidar fundamentos de backend em Python e evoluir uma aplicação de CRUD para um sistema com regras de negócio, autenticação, análises financeiras e automação.

O projeto foi construído com foco em **separação de responsabilidades, persistência relacional, segurança, testes e evolução incremental da arquitetura**.

> **Status:** projeto de portfólio / estudo avançado de backend. O núcleo funcional está implementado; os próximos passos mais relevantes são hardening de infraestrutura e, depois, integração com Machine Learning.

---

## Funcionalidades

* Cadastro, atualização e remoção de usuários
* Autenticação com JWT e proteção de endpoints
* Hash de senhas utilizando Argon2 via `pwdlib`
* Criação, consulta, atualização e remoção de contas
* Registro de transações de entrada e saída
* Atualização automática do saldo das contas
* Validação de saldo insuficiente
* Isolamento de dados por usuário autenticado
* Filtros por tipo, categoria e período
* Paginação de transações com `limit` e `offset`
* Dashboard financeiro com resumo, categorias e histórico
* Análise de concentração de despesas e geração de insights baseados em regras
* Transações recorrentes com processamento automático
* Registro das ocorrências de transações recorrentes, incluindo falhas
* Agendamento do processamento recorrente com APScheduler
* Testes automatizados da API e das regras de negócio
* Configuração para Docker
* Estrutura de migrations com Alembic

---

## Stack

### Backend

* Python 3.13
* FastAPI
* Pydantic
* SQLAlchemy 2

### Banco de dados

* MySQL
* PyMySQL

### Segurança

* JWT
* `pwdlib` + Argon2

### Automação e infraestrutura

* APScheduler
* Docker
* Uvicorn
* Alembic

### Qualidade e desenvolvimento

* Poetry
* Pytest
* Pytest-Cov
* Ruff

---

## Arquitetura

A aplicação utiliza uma arquitetura em camadas, com responsabilidades separadas entre HTTP, regras de negócio, persistência e infraestrutura.

```text
                     HTTP Request
                          │
                          ▼
                   ┌─────────────┐
                   │ Controllers │
                   └──────┬──────┘
                          │
                          ▼
                   ┌─────────────┐
                   │  Services   │
                   │ Business    │
                   │   Rules     │
                   └──────┬──────┘
                          │
                          ▼
                   ┌─────────────┐
                   │ Repositories│
                   │ Persistence │
                   └──────┬──────┘
                          │
                          ▼
                   ┌─────────────┐
                   │ SQLAlchemy  │
                   └──────┬──────┘
                          │
                          ▼
                       MySQL
```

### Camadas

**Controllers**

Responsáveis pela interface HTTP, validação via schemas e composição das dependências. A maior parte da lógica de negócio fica fora dessa camada.

**Services**

Concentram regras como atualização de saldo, autorização por usuário, processamento de recorrências e geração de análises do dashboard.

**Repositories**

Abstraem o acesso ao banco e concentram queries e operações de persistência.

**Models**

Representam as entidades persistidas no banco através do SQLAlchemy ORM.

**Schemas**

Definem contratos de entrada e saída da API usando Pydantic.

**Mappers**

Fazem a transformação entre entidades ORM e o formato exposto pela API quando os nomes internos e externos são diferentes.

**Dependencies**

Compondo repositories e services através da injeção de dependências do FastAPI.

**Core**

Reúne infraestrutura transversal, como configuração, segurança, banco de dados, cálculo de recorrências e scheduler.

---

## Estrutura

```text
Finance-Core/
├── app/
│   └── main.py
├── controllers/
├── core/
├── dependencies/
├── mappers/
├── migrations/
│   └── versions/
├── models/
├── repositories/
├── schemas/
├── services/
├── tests/
├── alembic.ini
├── db.sql
├── dockerfile
├── poetry.lock
├── pyproject.toml
└── README.md
```

---

## Domínio

O fluxo principal de transações é baseado na relação:

```text
User
 │
 └── Contas
      │
      ├── Transacoes
      │
      └── TransacoesRecorrentes
             │
             └── OcorrenciasRecorrentes
```

Uma transação altera o saldo da conta dentro da mesma unidade de trabalho do banco:

```text
Entrada  → saldo += valor
Saída    → saldo -= valor
```

Saídas que ultrapassariam o saldo disponível são rejeitadas.

Transações recorrentes possuem uma `proxima_data`. O scheduler procura recorrências vencidas, cria a ocorrência correspondente, tenta gerar a transação e registra o resultado como realizada ou falhou.

---

## Autenticação

O login utiliza OAuth2 Password Flow do FastAPI e gera um JWT contendo o usuário autenticado.

As rotas protegidas utilizam:

```text
Authorization: Bearer <token>
```

As senhas não são armazenadas em texto puro. O projeto utiliza Argon2 através do `pwdlib`.

---

## Endpoints

### Auth

| Método | Endpoint      | Descrição                            |
| ------ | ------------- | ------------------------------------ |
| POST   | `/auth/login` | Autentica o usuário e retorna um JWT |

### Users

| Método | Endpoint    | Descrição                             |
| ------ | ----------- | ------------------------------------- |
| POST   | `/users`    | Cria um usuário                       |
| GET    | `/users/me` | Retorna o usuário autenticado         |
| PATCH  | `/users/me` | Atualiza dados do usuário autenticado |
| DELETE | `/users/me` | Remove o usuário autenticado          |

### Accounts

| Método | Endpoint               | Descrição                |
| ------ | ---------------------- | ------------------------ |
| POST   | `/accounts`            | Cria uma conta           |
| GET    | `/accounts/{conta_id}` | Consulta uma conta       |
| PATCH  | `/accounts/{conta_id}` | Atualiza o nome da conta |
| DELETE | `/accounts/{conta_id}` | Remove uma conta         |

### Transactions

| Método | Endpoint                            | Descrição                                |
| ------ | ----------------------------------- | ---------------------------------------- |
| POST   | `/accounts/{conta_id}/transactions` | Cria uma transação                       |
| GET    | `/accounts/{conta_id}/transactions` | Lista transações com filtros e paginação |

Filtros disponíveis na listagem:

```text
?type=entrada
?category=Mercado
?start_date=2026-09-01
?end_date=2026-09-30
?limit=20
?offset=0
```

### Dashboard

| Método | Endpoint              | Descrição                                              |
| ------ | --------------------- | ------------------------------------------------------ |
| GET    | `/dashboard/summary`  | Totais de entradas, saídas, resultado e saldo          |
| GET    | `/dashboard/category` | Agrupamento por categoria e tipo                       |
| GET    | `/dashboard/history`  | Evolução diária do saldo no período                    |
| GET    | `/dashboard/analysis` | Distribuição de despesas e insights baseados em regras |

Os endpoints de dashboard utilizam `start_date` e `end_date` como filtros de período.

### Transações recorrentes

| Método | Endpoint                                             | Descrição                               |
| ------ | ---------------------------------------------------- | --------------------------------------- |
| POST   | `/transactions/recurring`                            | Cria uma recorrência                    |
| GET    | `/transactions/recurring`                            | Lista recorrências, com filtro de ativo |
| GET    | `/transactions/recurring/{recurring_transaction_id}` | Consulta uma recorrência                |
| PATCH  | `/transactions/recurring/{recurring_transaction_id}` | Atualiza uma recorrência                |

Frequências disponíveis:

```text
semanal
quinzenal
mensal
```

---

## Dashboard e análise

O dashboard não é apenas uma camada de apresentação. Parte da análise é calculada no backend a partir das transações do período.

Entre os dados produzidos estão:

* total de entradas e saídas
* resultado financeiro do período
* distribuição de despesas por categoria
* histórico diário de movimentação e saldo
* concentração de despesas
* insights derivados de regras de negócio

Exemplos de regras implementadas:

```text
NEGATIVE_RESULT
POSITIVE_RESULT
HIGH_CATEGORY_CONCENTRATION
MAIN_EXPENSE_CATEGORY
TOP_THREE_CONCENTRATION
```

Essa camada foi estruturada de forma determinística, deixando espaço para uma futura evolução para análises estatísticas e modelos de Machine Learning.

---

## Testes

A suíte possui testes cobrindo:

* autenticação
* criação e atualização de usuários
* autorização por usuário
* contas
* transações
* validações de saldo
* filtros e paginação
* dashboard
* transações recorrentes
* processamento de recorrências
* falha de recorrência por saldo insuficiente

O projeto atual possui **72 funções de teste** distribuídas em sete arquivos de teste.

Comandos principais:

```bash
poetry run task test
poetry run task coverage
```

ou diretamente:

```bash
poetry run pytest
poetry run pytest --cov=.
```

> A suíte do repositório utiliza SQLite em memória durante os testes para manter o isolamento e reduzir a dependência de infraestrutura externa.

---

## Migrations

O projeto utiliza Alembic para versionamento da estrutura do banco:

```text
migrations/
└── versions/
    ├── 666a1395a481_define_schema_inicial.py
    └── a92c76962d7f_adiciona_transacoes_recorrentes.py
```

As migrations registram a evolução do schema junto com o código.

**Nota de manutenção:** a migration inicial atual foi gerada sobre um schema que já existia e, portanto, não representa um bootstrap completo de banco vazio. Antes de utilizar Alembic como única fonte de verdade para provisionamento em novos ambientes, o baseline deve ser normalizado e o `db.sql` deve ser alinhado com o schema atual.

---

## Configuração local

Crie um `.env` na raiz:

```env
SECRET_KEY=sua_chave_secreta
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=mysql+pymysql://usuario:senha@localhost:3306/finance_core
ENVIRONMENT=development
LOG_LEVEL=info
```

Depois:

```bash
poetry install
poetry run task run
```

A documentação interativa fica disponível em:

```text
http://localhost:8000/docs
```

O projeto também contém configuração Docker para desenvolvimento. Credenciais e segredos devem permanecer fora do controle de versão.

---

## Comandos úteis

```bash
poetry run task run
poetry run task lint
poetry run task fix
poetry run task format
poetry run task test
poetry run task coverage
```

---

## O que este projeto consolidou

O Finance Core foi construído para praticar conceitos que vão além de endpoints CRUD:

* arquitetura em camadas
* injeção de dependência
* Repository Pattern
* Service Layer
* ORM com SQLAlchemy
* validação com Pydantic
* autenticação e autorização
* hashing de senhas
* tratamento de erros HTTP
* precisão monetária com `Decimal`
* transações e atomicidade
* filtros e paginação
* agregações SQL
* regras de negócio determinísticas
* processamento assíncrono por scheduler
* versionamento de schema com Alembic
* testes automatizados

---

## Próximos passos

O projeto já atingiu um ponto em que adicionar funcionalidades indefinidamente tem retorno menor do que consolidar o que existe.

As próximas evoluções mais relevantes são:

1. tornar Alembic a fonte oficial do schema
2. separar o scheduler da aplicação web em um worker/processo próprio
3. adicionar controles de concorrência para atualização de saldo
4. evoluir a análise financeira para estatística e Machine Learning

---

## Autor

Arthur Rezende

Desenvolvido como projeto de estudo e portfólio em backend com Python.
