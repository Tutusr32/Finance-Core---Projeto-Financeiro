from http import HTTPStatus


def test_create_account(client, token):
    response = client.post(
        "/accounts",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Carteira",
            "saldo": 100,
        },
    )

    assert response.status_code == HTTPStatus.CREATED

    data = response.json()

    assert data["name"] == "Carteira"
    assert data["saldo"] == "100.00"
    assert data["created_at"] is not None
    assert data["updated_at"] is not None


def test_create_account_negative_balance(client, token):
    response = client.post(
        "/accounts",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Carteira",
            "saldo": -10,
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Saldo inicial não pode ser negativo."}


def test_create_account_without_token(client):
    response = client.post(
        "/accounts",
        json={
            "name": "Carteira",
            "saldo": 100,
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_get_account(client, account, token):
    response = client.get(
        f"/accounts/{account.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data["id"] == account.id
    assert data["created_at"] is not None
    assert data["updated_at"] is not None


def test_get_account_not_found(client, token):
    response = client.get(
        "/accounts/999",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Conta não encontrada."}


def test_get_account_other_user(
    client,
    other_user,
    other_account,
    token,
):
    response = client.get(
        f"/accounts/{other_account.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Acesso negado."}


def test_get_account_without_token(client, account):
    response = client.get(
        f"/accounts/{account.id}",
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_update_account_name(client, account, token):
    response = client.patch(
        f"/accounts/{account.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Banco Inter",
        },
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data["name"] == "Banco Inter"
    assert data["created_at"] is not None
    assert data["updated_at"] is not None


def test_update_account_updates_updated_at(client, account, token):
    response = client.get(
        f"/accounts/{account.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK

    before = response.json()

    response = client.patch(
        f"/accounts/{account.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Conta Atualizada",
        },
    )

    assert response.status_code == HTTPStatus.OK

    after = response.json()

    assert after["created_at"] == before["created_at"]
    assert after["updated_at"] != before["updated_at"]


def test_update_account_not_found(client, token):
    response = client.patch(
        "/accounts/999",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Teste",
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_account_other_user(client, other_account, token):
    response = client.patch(
        f"/accounts/{other_account.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Teste",
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN


def test_update_account_empty_body(client, account, token):
    response = client.patch(
        f"/accounts/{account.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={},
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data["created_at"] is not None
    assert data["updated_at"] is not None


def test_update_account_without_token(client, account):
    response = client.patch(
        f"/accounts/{account.id}",
        json={
            "name": "Novo Nome",
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_delete_account(client, account, token):
    response = client.delete(
        f"/accounts/{account.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_account_not_found(client, token):
    response = client.delete(
        "/accounts/999",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_account_other_user(
    client,
    other_account,
    token,
):
    response = client.delete(
        f"/accounts/{other_account.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN


def test_delete_account_without_token(client, account):
    response = client.delete(
        f"/accounts/{account.id}",
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
