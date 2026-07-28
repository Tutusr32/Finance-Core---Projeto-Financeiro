from http import HTTPStatus

from core.security import verify_password


def test_create_user(client):
    response = client.post(
        "/users",
        json={
            "name": "alice",
            "email": "alice@example.com",
            "password": "secret32",
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "name": "alice",
        "email": "alice@example.com",
    }


def test_create_user_missing_name(client):
    response = client.post(
        "/users",
        json={
            "email": "teste@email.com",
            "password": "secret32",
        },
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_user_without_email(client):
    response = client.post(
        "/users",
        json={
            "name": "Arthur",
            "password": "secret32",
        },
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_user_without_password(client):
    response = client.post(
        "/users",
        json={
            "name": "Arthur",
            "email": "arthur@email.com",
        },
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_user_invalid_email(client):
    response = client.post(
        "/users",
        json={
            "name": "teste",
            "email": "email_invalido",
            "password": "secret32",
        },
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_user_short_password(client):
    response = client.post(
        "/users",
        json={
            "name": "Arthur",
            "email": "arthur@email.com",
            "password": "123",
        },
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_user_email_already_exists(client, user):
    response = client.post(
        "/users",
        json={
            "name": "OutroNome",
            "email": "teste@teste.com",
            "password": "testtest",
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Email já cadastrado."}


def test_read_user_me(client, user, token):
    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data["id"] == user.id
    assert data["email"] == user.email
    assert data["name"] == user.name


def test_read_user_me_without_token(client):
    response = client.get("/users/me")

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_update_name(client, user, token):
    response = client.patch(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "novo_nome"},
    )

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {
        "id": user.id,
        "name": "novo_nome",
        "email": user.email,
    }


def test_update_email(client, user, token):
    response = client.patch(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
        json={"email": "novo_email@example.com"},
    )

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {
        "id": user.id,
        "name": user.name,
        "email": "novo_email@example.com",
    }


def test_update_multiple_fields(client, user, token):
    response = client.patch(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Arthur",
            "email": "arthur@email.com",
        },
    )

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {
        "id": user.id,
        "name": "Arthur",
        "email": "arthur@email.com",
    }


def test_update_password(client, user, token):
    response = client.patch(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
        json={"password": "newpassword"},
    )

    assert response.status_code == HTTPStatus.OK

    assert verify_password("newpassword", user.password)


def test_update_invalid_email(client, token):
    response = client.patch(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
        json={"email": "email_invalido"},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_update_short_password(client, token):
    response = client.patch(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
        json={"password": "123"},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_update_user_email_already_exists(client, user, other_user, token):
    response = client.patch(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
        json={"email": other_user.email},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Email já cadastrado."}


def test_update_empty_body(client, user, token):
    response = client.patch(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
        json={},
    )

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {
        "id": user.id,
        "name": user.name,
        "email": user.email,
    }


def test_update_user_without_token(client):
    response = client.patch(
        "/users/me",
        json={"name": "novo_nome"},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_delete_user(client, user, token):
    response = client.delete(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.NO_CONTENT

    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_delete_user_without_token(client):
    response = client.delete("/users/me")

    assert response.status_code == HTTPStatus.UNAUTHORIZED
