from datetime import datetime
from http import HTTPStatus


def test_create_transaction_income(client, account, token):
    response = client.post(
        f"/accounts/{account.id}/transactions",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "type": "entrada",
            "amount": 500,
            "category": "Salário",
        },
    )

    assert response.status_code == HTTPStatus.CREATED

    data = response.json()

    assert data["type"] == "entrada"
    assert data["amount"] == "500.00"
    assert data["category"] == "Salário"


def test_create_income_updates_balance(client, account, token):
    response = client.post(
        f"/accounts/{account.id}/transactions",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "type": "entrada",
            "amount": 500,
            "category": "Salário",
        },
    )

    assert response.status_code == HTTPStatus.CREATED

    account_response = client.get(
        f"/accounts/{account.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert account_response.status_code == HTTPStatus.OK
    assert account_response.json()["saldo"] == "1500.00"


def test_create_transaction_expense(client, account, token):
    response = client.post(
        f"/accounts/{account.id}/transactions",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "type": "saida",
            "amount": 200,
            "category": "Mercado",
        },
    )

    assert response.status_code == HTTPStatus.CREATED

    data = response.json()

    assert data["type"] == "saida"
    assert data["amount"] == "200.00"
    assert data["category"] == "Mercado"


def test_create_expense_updates_balance(client, account, token):
    response = client.post(
        f"/accounts/{account.id}/transactions",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "type": "saida",
            "amount": 200,
            "category": "Mercado",
        },
    )

    assert response.status_code == HTTPStatus.CREATED

    account_response = client.get(
        f"/accounts/{account.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert account_response.status_code == HTTPStatus.OK
    assert account_response.json()["saldo"] == "800.00"


def test_create_expense_without_balance(client, account, token):
    response = client.post(
        f"/accounts/{account.id}/transactions",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "type": "saida",
            "amount": 999999,
            "category": "Compra",
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Saldo insuficiente."}


def test_create_transaction_account_not_found(client, token):
    response = client.post(
        "/accounts/999/transactions",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "type": "entrada",
            "amount": 100,
            "category": "Teste",
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Conta não encontrada."}


def test_create_transaction_other_user_account(client, other_account, token):
    response = client.post(
        f"/accounts/{other_account.id}/transactions",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "type": "entrada",
            "amount": 100,
            "category": "Teste",
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Acesso negado."}


def test_create_transaction_without_token(client, account):
    response = client.post(
        f"/accounts/{account.id}/transactions",
        json={
            "type": "entrada",
            "amount": 100,
            "category": "Teste",
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_list_transactions(client, account, token, transaction):
    response = client.get(
        f"/accounts/{account.id}/transactions",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert len(data) == 1
    assert data[0]["type"] == "entrada"
    assert data[0]["amount"] == "150.00"
    assert data[0]["category"] == "Salário"


def test_list_transactions_with_limit(
    client,
    account,
    token,
    create_transaction,
):
    create_transaction(
        account,
        "entrada",
        100,
        "Salário",
        datetime(2026, 9, 1),
    )
    create_transaction(
        account,
        "saida",
        50,
        "Mercado",
        datetime(2026, 9, 2),
    )
    create_transaction(
        account,
        "saida",
        30,
        "Transporte",
        datetime(2026, 9, 3),
    )

    response = client.get(
        f"/accounts/{account.id}/transactions?limit=2",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 2


def test_list_transactions_with_offset(
    client,
    account,
    token,
    create_transaction,
):
    create_transaction(
        account,
        "entrada",
        100,
        "Salário",
        datetime(2026, 9, 1),
    )
    create_transaction(
        account,
        "saida",
        50,
        "Mercado",
        datetime(2026, 9, 2),
    )
    create_transaction(
        account,
        "saida",
        30,
        "Transporte",
        datetime(2026, 9, 3),
    )

    response = client.get(
        f"/accounts/{account.id}/transactions?offset=1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 2
