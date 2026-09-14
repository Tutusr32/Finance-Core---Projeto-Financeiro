from calendar import monthrange
from datetime import date, timedelta


def calculate_next_date(current_date: date, frequency: str) -> date:
    if frequency == "semanal":
        return current_date + timedelta(days=7)

    if frequency == "quinzenal":
        return current_date + timedelta(days=15)

    if frequency == "mensal":
        if current_date.month == 12:
            next_year = current_date.year + 1
            next_month = 1
        else:
            next_year = current_date.year
            next_month = current_date.month + 1

        last_day = monthrange(next_year, next_month)[1]

        return date(
            next_year,
            next_month,
            min(current_date.day, last_day),
        )

    raise ValueError(f"Frequência inválida: {frequency}")
