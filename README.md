# Finance Core

O Finance Core é uma API para gerenciamento financeiro pessoal, desenvolvida em Python com FastAPI e SQLAlchemy. O projeto permite o gerenciamento de usuários, contas e transações financeiras, além de disponibilizar um dashboard para análise e acompanhamento das movimentações.

O projeto foi desenvolvido com foco em organização de código, separação de responsabilidades, segurança, validações, testes e aplicação de conceitos de desenvolvimento de APIs.

## Funcionalidades

* Cadastro e autenticação de usuários
* Autenticação utilizando JWT
* Gerenciamento das próprias informações do usuário
* Criação, atualização, consulta e exclusão de contas
* Criação e consulta de transações
* Controle automático do saldo das contas
* Validação de saldo insuficiente
* Paginação na listagem de transações
* Filtros de transações
* Dashboard financeiro
* Resumo de entradas, saídas e resultado
* Agrupamento de movimentações por categoria
* Histórico financeiro por data
* Distribuição de despesas por categoria
* Geração de insights financeiros baseados em regras
* Persistência utilizando MySQL
* Ambiente de execução utilizando Docker
* Testes automatizados com Pytest

## Tecnologias utilizadas

* Python 3.13
* FastAPI
* SQLAlchemy
* MySQL
* PyMySQL
* Pydantic
* Pydantic Settings
* PyJWT
* pwdlib + Argon2
* Uvicorn
* Poetry
* Pytest
* pytest-cov
* Ruff
* Taskipy
* Docker
* Docker Compose

## Arquitetura

O projeto utiliza uma arquitetura baseada na separação de responsabilidades:

```text
Controller
    ↓
Service
    ↓
Repository
    ↓
SQLAlchemy
    ↓
MySQL
```

### Controller

Responsável por receber as requisições HTTP, validar os parâmetros através dos schemas e direcionar a operação para o Service.

### Service

Responsável pelas regras de negócio e pelo processamento dos dados retornados pelos repositories.

### Repository

Responsável pelo acesso aos dados e pela construção das consultas utilizando SQLAlchemy.

### Model

Representa as entidades persistidas no banco de dados.

### Schema

Define os formatos de entrada e saída da API e auxilia na validação dos dados.

Essa divisão permite que cada camada possua uma responsabilidade específica, facilitando manutenção, testes e evolução do projeto.

## Estrutura do projeto

```text
app/
├── controllers/
│   ├── accounts_controller.py
│   ├── auth_controller.py
│   ├── dashboard_controller.py
│   ├── transactions_controller.py
│   └── users_controller.py
│
├── core/
│   ├── base.py
│   ├── database.py
│   ├── security.py
│   └── settings.py
│
├── dependencies/
│   ├── accounts.py
│   ├── auth.py
│   ├── dashboard.py
│   ├── transaction.py
│   └── users.py
│
├── mappers/
│   ├── conta_mapper.py
│   └── transaction_mapper.py
│
├── models/
│   ├── contas.py
│   ├── transacoes.py
│   └── users.py
│
├── repositories/
│   ├── contas_repository.py
│   ├── dashboard_repository.py
│   ├── transacao_repository.py
│   └── users_repository.py
│
├── schemas/
│   ├── auth_schema.py
│   ├── conta_schema.py
│   ├── dashboard_schema.py
│   ├── transaction_schema.py
│   └── user_schema.py
│
├── services/
│   ├── accounts_service.py
│   ├── dashboard_service.py
│   ├── transactions_service.py
│   └── users_service.py
│
└── main.py

tests/
├── conftest.py
├── test_accounts.py
├── test_auth.py
├── test_transactions.py
└── test_users.py
```

## Autenticação

A API utiliza JWT para autenticação.

Após realizar o login, o usuário recebe um token de acesso que deve ser enviado nas requisições protegidas:

```http
Authorization: Bearer <token>
```

Os recursos financeiros são associados ao usuário autenticado. Dessa forma, operações sobre contas e transações são realizadas considerando o usuário identificado pelo token.

## Endpoints

### Autenticação

| Método | Endpoint      | Descrição                         |
| ------ | ------------- | --------------------------------- |
| POST   | `/auth/login` | Realiza a autenticação do usuário |

### Usuários

| Método | Endpoint    | Descrição                                |
| ------ | ----------- | ---------------------------------------- |
| POST   | `/users`    | Cria um novo usuário                     |
| GET    | `/users/me` | Retorna os dados do usuário autenticado  |
| PATCH  | `/users/me` | Atualiza os dados do usuário autenticado |
| DELETE | `/users/me` | Remove o usuário autenticado             |

### Contas

| Método | Endpoint               | Descrição                              |
| ------ | ---------------------- | -------------------------------------- |
| POST   | `/accounts`            | Cria uma conta                         |
| GET    | `/accounts`            | Lista as contas do usuário autenticado |
| PATCH  | `/accounts/{conta_id}` | Atualiza uma conta                     |
| DELETE | `/accounts/{conta_id}` | Remove uma conta                       |

### Transações

| Método | Endpoint        | Descrição                      |
| ------ | --------------- | ------------------------------ |
| POST   | `/transactions` | Cria uma transação             |
| GET    | `/transactions` | Lista as transações do usuário |

A listagem de transações permite paginação e filtros de acordo com os parâmetros implementados na API.

Exemplo:

```text
/transactions?limit=10
```

## Dashboard

O Dashboard concentra consultas analíticas sobre as movimentações financeiras do usuário.

As consultas podem receber filtros de período através dos parâmetros `start_date` e `end_date`.

| Método | Endpoint              | Descrição                                                    |
| ------ | --------------------- | ------------------------------------------------------------ |
| GET    | `/dashboard/summary`  | Retorna saldo total, entradas, saídas e resultado do período |
| GET    | `/dashboard/category` | Agrupa as movimentações por categoria e tipo                 |
| GET    | `/dashboard/history`  | Retorna o histórico diário de entradas e saídas              |
| GET    | `/dashboard/analysis` | Retorna a distribuição das despesas e insights financeiros   |

### `/dashboard/summary`

Retorna um resumo financeiro do período informado.

Exemplo:

```text
/dashboard/summary?start_date=2026-08-01&end_date=2026-08-31
```

Resposta:

```json
{
    "saldo_total": "233000.00",
    "total_entradas": "2000.00",
    "total_saidas": "16000.00",
    "resultado": "-14000.00"
}
```

O `saldo_total` representa o saldo atual das contas do usuário, enquanto o `resultado` representa:

```text
resultado = entradas - saídas
```

### `/dashboard/category`

Agrupa as movimentações financeiras por categoria e tipo.

Exemplo:

```json
[
    {
        "category": "Aluguel da empresa",
        "type": "saida",
        "total": "16000.00"
    },
    {
        "category": "Salário",
        "type": "entrada",
        "total": "2000.00"
    }
]
```

### `/dashboard/history`

Apresenta as movimentações agrupadas por data.

Exemplo:

```json
[
    {
        "date": "2026-08-22",
        "entradas": "0.00",
        "saidas": "16000.00"
    },
    {
        "date": "2026-08-25",
        "entradas": "2000.00",
        "saidas": "0.00"
    }
]
```

### `/dashboard/analysis`

Realiza uma análise das despesas agrupadas por categoria e calcula a participação percentual de cada categoria no total de despesas.

Exemplo:

```json
{
    "expense_distribution": [
        {
            "category": "Aluguel da empresa",
            "amount": "16000.00",
            "percentage": "100.00"
        }
    ],
    "insights": [
        {
            "type": "warning",
            "title": "Alta concentração de gastos",
            "description": "A categoria Aluguel da empresa representa uma parcela significativa das despesas."
        }
    ]
}
```

Os insights atuais são gerados através de regras determinísticas baseadas na concentração das despesas. Não há utilização de Machine Learning nessa etapa.

## Regras de negócio atuais

### Controle de saldo

Ao registrar uma entrada, o saldo da conta é incrementado.

Ao registrar uma saída, o saldo é reduzido.

```text
entrada → saldo + valor
saída   → saldo - valor
```

### Saldo insuficiente

Uma saída não pode ser realizada caso a conta não possua saldo suficiente.

### Atomicidade

A criação de transações e a atualização do saldo são tratadas de forma que a operação mantenha consistência entre os dados financeiros.

### Isolamento por usuário

As contas e transações são associadas ao usuário autenticado, evitando que um usuário consulte ou altere dados financeiros pertencentes a outro usuário.

### Valores monetários

Valores financeiros utilizam `Decimal` para evitar problemas de precisão comuns ao utilizar números de ponto flutuante.

## Consultas analíticas

O Dashboard utiliza recursos de agregação do SQL para processar os dados diretamente no banco.

Entre os recursos utilizados estão:

* `SUM` para cálculo de totais
* `CASE` para separar entradas e saídas
* `GROUP BY` para agrupamento por categoria e data
* `ORDER BY` para ordenação dos resultados
* `COALESCE` para tratamento de resultados nulos
* `JOIN` para relacionar transações, contas e usuários

Exemplo conceitual:

```sql
SELECT
    categoria,
    SUM(valor)
FROM transacoes
GROUP BY categoria;
```

Essa abordagem evita carregar todas as transações para a aplicação quando uma agregação pode ser realizada diretamente pelo banco de dados.

## Testes

O projeto utiliza Pytest para testes automatizados.

Os testes cobrem funcionalidades relacionadas a:

* Usuários
* Autenticação
* Contas
* Transações

Para executar os testes:

```bash
poetry run pytest
```

Para executar os testes com cobertura:

```bash
poetry run pytest --cov=. -vv
```

## Qualidade de código

O projeto utiliza Ruff para análise e formatação do código.

Verificar problemas:

```bash
poetry run task lint
```

Corrigir problemas automaticamente:

```bash
poetry run task fix
```

Formatar o projeto:

```bash
poetry run task format
```

## Como executar o projeto

### Com Poetry

Instale as dependências:

```bash
poetry install
```

Execute a API:

```bash
poetry run task run
```

A API estará disponível em:

```text
http://localhost:8000
```

A documentação interativa do FastAPI pode ser acessada em:

```text
http://localhost:8000/docs
```

### Com Docker

Para construir e iniciar os containers:

```bash
docker compose up --build
```

Para executar em segundo plano:

```bash
docker compose up --build -d
```

Para visualizar os logs:

```bash
docker compose logs -f
```

## Comandos úteis

```bash
# Instalar dependências
poetry install

# Executar aplicação
poetry run task run

# Executar testes
poetry run pytest

# Executar testes com cobertura
poetry run pytest --cov=. -vv

# Verificar lint
poetry run task lint

# Corrigir problemas do Ruff
poetry run task fix

# Formatar código
poetry run task format

# Construir containers
docker compose build

# Iniciar containers
docker compose up

# Iniciar reconstruindo a imagem
docker compose up --build
```

## Conceitos aplicados

O projeto busca aplicar conceitos utilizados no desenvolvimento de aplicações backend, incluindo:

* Arquitetura em camadas
* Separação de responsabilidades
* Injeção de dependências
* REST API
* Autenticação e autorização com JWT
* Hash seguro de senhas
* ORM com SQLAlchemy
* Consultas SQL e agregações
* Validação de dados
* Tratamento de regras de negócio
* Controle de transações e atomicidade
* Paginação
* Filtros
* Testes automatizados
* Cobertura de testes
* Linting e formatação
* Containerização
* Variáveis de ambiente
* Processamento analítico de dados

## Roadmap

Próximos passos planejados para evolução do projeto:

* Implementação de Alembic para gerenciamento de migrations
* Expansão da cobertura de testes do Dashboard
* Melhorias nas análises financeiras
* Histórico de saldo e movimentações
* Melhorias nas validações e mapeamentos
* Implementação de frontend
* Evolução da camada de análise financeira
* Exploração futura de Machine Learning para geração de análises e recomendações

## Autor

Arthur Rezende

Projeto desenvolvido como estudo prático de desenvolvimento backend, arquitetura de software, bancos de dados e análise de dados.
