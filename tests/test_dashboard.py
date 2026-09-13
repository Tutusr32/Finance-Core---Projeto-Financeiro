from datetime import date
from http import HTTPStatus


def test_dashboard_summary(
    client,
    account,
    create_transaction,
    token,
):
    create_transaction(
        account,
        "entrada",
        2000,
        "Salário",
        date(2026, 8, 22),
    )
    create_transaction(
        account,
        "saida",
        500,
        "Mercado",
        date(2026, 8, 23),
    )

    response = client.get(
        "/dashboard/summary?start_date=2026-08-20&end_date=2026-08-23",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data["saldo_total"] == "2500.00"
    assert data["total_entradas"] == "2000.00"
    assert data["total_saidas"] == "500.00"
    assert data["resultado"] == "1500.00"


def test_dashboard_summary_with_date_filter(
    client,
    account,
    create_transaction,
    token,
):
    create_transaction(
        account,
        "entrada",
        2000,
        "Salário",
        date(2026, 8, 20),
    )
    create_transaction(
        account,
        "saida",
        500,
        "Mercado",
        date(2026, 8, 25),
    )

    response = client.get(
        "/dashboard/summary?start_date=2026-08-21&end_date=2026-08-25",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data["total_entradas"] == "0.00"
    assert data["total_saidas"] == "500.00"
    assert data["resultado"] == "-500.00"


def test_dashboard_summary_without_transactions(
    client,
    account,
    token,
):
    response = client.get(
        "/dashboard/summary?start_date=2026-08-20&end_date=2026-08-23",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data["saldo_total"] == "1000.00"
    assert data["total_entradas"] == "0.00"
    assert data["total_saidas"] == "0.00"
    assert data["resultado"] == "0.00"


def test_dashboard_summary_isolated_by_user(
    client,
    account,
    other_account,
    create_transaction,
    token,
):
    create_transaction(
        other_account,
        "entrada",
        5000,
        "Salário",
        date(2026, 8, 22),
    )

    response = client.get(
        "/dashboard/summary?start_date=2026-08-20&end_date=2026-08-23",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data["saldo_total"] == "1000.00"
    assert data["total_entradas"] == "0.00"
    assert data["total_saidas"] == "0.00"


def test_dashboard_category(
    client,
    account,
    create_transaction,
    token,
):
    create_transaction(
        account,
        "saida",
        1000,
        "Aluguel",
        date(2026, 8, 22),
    )
    create_transaction(
        account,
        "saida",
        500,
        "Mercado",
        date(2026, 8, 23),
    )
    create_transaction(
        account,
        "entrada",
        2000,
        "Salário",
        date(2026, 8, 24),
    )

    response = client.get(
        "/dashboard/category?start_date=2026-08-20&end_date=2026-08-24",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert len(data) == 3

    assert data[0] == {
        "category": "Salário",
        "type": "entrada",
        "total": "2000.00",
    }

    assert data[1] == {
        "category": "Aluguel",
        "type": "saida",
        "total": "1000.00",
    }

    assert data[2] == {
        "category": "Mercado",
        "type": "saida",
        "total": "500.00",
    }


def test_dashboard_category_with_date_filter(
    client,
    account,
    create_transaction,
    token,
):
    create_transaction(
        account,
        "saida",
        1000,
        "Aluguel",
        date(2026, 8, 20),
    )
    create_transaction(
        account,
        "saida",
        500,
        "Mercado",
        date(2026, 8, 25),
    )

    response = client.get(
        "/dashboard/category?start_date=2026-08-21&end_date=2026-08-25",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data == [
        {
            "category": "Mercado",
            "type": "saida",
            "total": "500.00",
        }
    ]


def test_dashboard_history(
    client,
    account,
    create_transaction,
    token,
):
    create_transaction(
        account,
        "entrada",
        2000,
        "Salário",
        date(2026, 8, 22),
    )
    create_transaction(
        account,
        "saida",
        500,
        "Mercado",
        date(2026, 8, 22),
    )
    create_transaction(
        account,
        "saida",
        300,
        "Delivery",
        date(2026, 8, 23),
    )

    response = client.get(
        "/dashboard/history?start_date=2026-08-20&end_date=2026-08-23",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data["start_date"] == "2026-08-20"
    assert data["end_date"] == "2026-08-23"
    assert data["saldo_inicial"] == "1000.00"
    assert data["saldo_final"] == "2200.00"

    assert data["historico"] == [
        {
            "date": "2026-08-22",
            "entradas": "2000.00",
            "saidas": "500.00",
            "variacao": "1500.00",
            "saldo": "2500.00",
        },
        {
            "date": "2026-08-23",
            "entradas": "0.00",
            "saidas": "300.00",
            "variacao": "-300.00",
            "saldo": "2200.00",
        },
    ]


def test_dashboard_history_with_date_filter(
    client,
    account,
    create_transaction,
    token,
):
    create_transaction(
        account,
        "entrada",
        2000,
        "Salário",
        date(2026, 8, 20),
    )
    create_transaction(
        account,
        "saida",
        500,
        "Mercado",
        date(2026, 8, 25),
    )

    response = client.get(
        "/dashboard/history?start_date=2026-08-21&end_date=2026-08-25",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data["start_date"] == "2026-08-21"
    assert data["end_date"] == "2026-08-25"
    assert data["saldo_inicial"] == "3000.00"
    assert data["saldo_final"] == "2500.00"

    assert data["historico"] == [
        {
            "date": "2026-08-25",
            "entradas": "0.00",
            "saidas": "500.00",
            "variacao": "-500.00",
            "saldo": "2500.00",
        }
    ]


def test_dashboard_analysis(
    client,
    account,
    create_transaction,
    token,
):
    create_transaction(
        account,
        "saida",
        4000,
        "Aluguel",
        date(2026, 8, 22),
    )
    create_transaction(
        account,
        "saida",
        1000,
        "Mercado",
        date(2026, 8, 23),
    )

    response = client.get(
        "/dashboard/analysis?start_date=2026-08-20&end_date=2026-08-23",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data["expense_distribution"] == [
        {
            "category": "Aluguel",
            "amount": "4000.00",
            "percentage": "80.00",
        },
        {
            "category": "Mercado",
            "amount": "1000.00",
            "percentage": "20.00",
        },
    ]

    assert len(data["insights"]) == 2

    assert data["insights"][0] == {
        "rule": "NEGATIVE_RESULT",
        "type": "warning",
        "severity": "high",
        "title": "Resultado financeiro negativo",
        "description": ("Suas despesas superaram suas entradas em R$ 5000.00 no período."),
        "metric": {
            "income": "0.00",
            "expenses": "5000.00",
            "result": "-5000.00",
        },
    }

    assert data["insights"][1] == {
        "rule": "HIGH_CATEGORY_CONCENTRATION",
        "type": "warning",
        "severity": "medium",
        "title": "Alta concentração de gastos",
        "description": ("Aluguel representa 80.00% das suas despesas."),
        "metric": {
            "category": "Aluguel",
            "percentage": "80.0",
            "amount": "4000.00",
        },
    }


def test_dashboard_analysis_without_expenses(
    client,
    account,
    create_transaction,
    token,
):
    create_transaction(
        account,
        "entrada",
        2000,
        "Salário",
        date(2026, 8, 22),
    )

    response = client.get(
        "/dashboard/analysis?start_date=2026-08-20&end_date=2026-08-23",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data["expense_distribution"] == []

    assert data["insights"] == [
        {
            "rule": "POSITIVE_RESULT",
            "type": "info",
            "severity": "low",
            "title": "Resultado financeiro positivo",
            "description": ("Suas entradas superaram suas despesas em R$ 2000.00 no período."),
            "metric": {
                "income": "2000.00",
                "expenses": "0.00",
                "result": "2000.00",
            },
        }
    ]


def test_dashboard_analysis_with_zero_result(
    client,
    account,
    create_transaction,
    token,
):
    create_transaction(
        account,
        "entrada",
        1000,
        "Salário",
        date(2026, 8, 22),
    )
    create_transaction(
        account,
        "saida",
        1000,
        "Mercado",
        date(2026, 8, 23),
    )

    response = client.get(
        "/dashboard/analysis?start_date=2026-08-20&end_date=2026-08-23",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert len(data["insights"]) == 1

    assert data["insights"][0]["rule"] == "HIGH_CATEGORY_CONCENTRATION"

    assert data["insights"][0]["metric"] == {
        "category": "Mercado",
        "percentage": "100",
        "amount": "1000.00",
    }


def test_dashboard_analysis_with_category_below_25_percent(
    client,
    account,
    create_transaction,
    token,
):
    create_transaction(
        account,
        "entrada",
        10000,
        "Salário",
        date(2026, 8, 22),
    )

    create_transaction(
        account,
        "saida",
        1000,
        "Aluguel",
        date(2026, 8, 23),
    )

    create_transaction(
        account,
        "saida",
        900,
        "Mercado",
        date(2026, 8, 23),
    )

    create_transaction(
        account,
        "saida",
        8100,
        "Outros",
        date(2026, 8, 23),
    )

    response = client.get(
        "/dashboard/analysis?start_date=2026-08-20&end_date=2026-08-23",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data["expense_distribution"] == [
        {
            "category": "Outros",
            "amount": "8100.00",
            "percentage": "81.00",
        },
        {
            "category": "Aluguel",
            "amount": "1000.00",
            "percentage": "10.00",
        },
        {
            "category": "Mercado",
            "amount": "900.00",
            "percentage": "9.00",
        },
    ]

    rules = [insight["rule"] for insight in data["insights"]]

    assert "HIGH_CATEGORY_CONCENTRATION" in rules
    assert "TOP_THREE_CONCENTRATION" in rules
    assert "MAIN_EXPENSE_CATEGORY" not in rules
    assert "POSITIVE_RESULT" not in rules


def test_dashboard_analysis_with_main_expense_category(
    client,
    account,
    create_transaction,
    token,
):
    create_transaction(
        account,
        "entrada",
        10000,
        "Salário",
        date(2026, 8, 22),
    )

    create_transaction(
        account,
        "saida",
        3800,
        "Aluguel",
        date(2026, 8, 23),
    )

    create_transaction(
        account,
        "saida",
        3200,
        "Mercado",
        date(2026, 8, 23),
    )

    create_transaction(
        account,
        "saida",
        3000,
        "Outros",
        date(2026, 8, 23),
    )

    response = client.get(
        "/dashboard/analysis?start_date=2026-08-20&end_date=2026-08-23",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    rules = [insight["rule"] for insight in data["insights"]]

    assert "MAIN_EXPENSE_CATEGORY" in rules
    assert "TOP_THREE_CONCENTRATION" in rules
    assert "POSITIVE_RESULT" not in rules

    main_expense_insight = next(
        insight for insight in data["insights"] if insight["rule"] == "MAIN_EXPENSE_CATEGORY"
    )

    assert main_expense_insight["metric"] == {
        "category": "Aluguel",
        "percentage": "38.00",
        "amount": "3800.00",
    }


def test_dashboard_requires_authentication(client):
    response = client.get(
        "/dashboard/summary?start_date=2026-08-20&end_date=2026-08-23",
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_dashboard_requires_date_filters(
    client,
    token,
):
    response = client.get(
        "/dashboard/summary",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
