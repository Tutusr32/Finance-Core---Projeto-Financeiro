from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from core.base import Base
from core.database import get_db
from core.security import hash_password
from models import Contas, Transacoes, Users

TEST_DATABASE_URL = "sqlite+pysqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.rollback()
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def user(db_session):
    user = Users(
        name="Teste",
        email="teste@teste.com",
        password=hash_password("testtest"),
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    user.clean_password = "testtest"
    return user


@pytest.fixture
def other_user(db_session):
    user = Users(
        name="Outro Teste",
        email="outro@teste.com",
        password=hash_password("testtest"),
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    user.clean_password = "testtest"
    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        "/auth/login",
        data={"username": user.email, "password": user.clean_password},
    )

    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def account(db_session, user):
    conta = Contas(
        user_id=user.id,
        name="Carteira principal",
        saldo=Decimal("1000.00"),
    )
    db_session.add(conta)
    db_session.commit()
    db_session.refresh(conta)
    return conta


@pytest.fixture
def other_account(db_session, other_user):
    account = Contas(
        user_id=other_user.id,
        name="Conta do outro usuário",
        saldo=1000,
    )

    db_session.add(account)
    db_session.commit()
    db_session.refresh(account)

    return account


@pytest.fixture
def transaction(db_session, account):
    transacao = Transacoes(
        conta_id=account.id,
        tipo="entrada",
        valor=Decimal("150.00"),
        categoria="Salário",
    )
    db_session.add(transacao)
    db_session.commit()
    db_session.refresh(transacao)
    return transacao


@pytest.fixture
def create_transaction(db_session):
    def _create_transaction(
        account,
        transaction_type,
        amount,
        category,
        transaction_date,
    ):
        transaction = Transacoes(
            conta_id=account.id,
            tipo=transaction_type,
            valor=Decimal(str(amount)),
            categoria=category,
            data=transaction_date,
        )

        db_session.add(transaction)
        db_session.commit()
        db_session.refresh(transaction)

        return transaction

    return _create_transaction
