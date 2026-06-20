"""Moduł portfela inwestora dla projektu MarketSim."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from app.market import Stock, get_stock


Portfolio = dict[str, Any]


def create_operation_counter():
    """Tworzy licznik operacji jako domknięcie."""
    counter = 0

    def next_id() -> int:
        nonlocal counter
        counter += 1
        return counter

    return next_id


next_operation_id = create_operation_counter()


def create_portfolio(start_cash: float = 100_000.0) -> Portfolio:
    """Tworzy nowy portfel inwestora."""
    return {
        "cash": float(start_cash),
        "stocks": defaultdict(int),
        "currencies": defaultdict(float),
        "history": [],
    }


def buy_stock(portfolio: Portfolio, stocks: dict[str, Stock], symbol: str, quantity: int) -> str:
    """Kupuje akcje wybranej spółki."""
    symbol = symbol.strip().upper()
    stock = get_stock(stocks, symbol)

    if stock is None:
        return "Błąd: nie ma takiej spółki"

    if quantity <= 0:
        return "Błąd: liczba akcji musi być dodatnia"

    price = float(stock["price"])
    cost = round(price * quantity, 2)

    if cost > portfolio["cash"]:
        return "Błąd: za mało gotówki"

    portfolio["cash"] = round(portfolio["cash"] - cost, 2)
    portfolio["stocks"][symbol] += quantity

    portfolio["history"].append({
        "id": next_operation_id(),
        "type": "kupno_akcji",
        "asset": symbol,
        "quantity": quantity,
        "price": price,
        "value": cost,
    })

    return f"Kupiono {quantity} akcji {symbol} za {cost:.2f} zł"


def sell_stock(portfolio: Portfolio, stocks: dict[str, Stock], symbol: str, quantity: int) -> str:
    """Sprzedaje akcje wybranej spółki."""
    symbol = symbol.strip().upper()
    stock = get_stock(stocks, symbol)

    if stock is None:
        return "Błąd: nie ma takiej spółki"

    if quantity <= 0:
        return "Błąd: liczba akcji musi być dodatnia"

    if portfolio["stocks"][symbol] < quantity:
        return "Błąd: nie masz tylu akcji"

    price = float(stock["price"])
    value = round(price * quantity, 2)

    portfolio["stocks"][symbol] -= quantity
    portfolio["cash"] = round(portfolio["cash"] + value, 2)

    portfolio["history"].append({
        "id": next_operation_id(),
        "type": "sprzedaz_akcji",
        "asset": symbol,
        "quantity": quantity,
        "price": price,
        "value": value,
    })

    return f"Sprzedano {quantity} akcji {symbol} za {value:.2f} zł"


def buy_currency(portfolio: Portfolio, code: str, amount: float, rate: float) -> str:
    """Kupuje walutę po kursie pobranym z API NBP."""
    code = code.strip().upper()

    if len(code) != 3:
        return "Błąd: kod waluty musi mieć 3 znaki"

    if amount <= 0:
        return "Błąd: ilość waluty musi być dodatnia"

    if rate <= 0:
        return "Błąd: kurs musi być dodatni"

    cost = round(amount * rate, 2)

    if cost > portfolio["cash"]:
        return "Błąd: za mało gotówki"

    portfolio["cash"] = round(portfolio["cash"] - cost, 2)
    portfolio["currencies"][code] = round(portfolio["currencies"][code] + amount, 4)

    portfolio["history"].append({
        "id": next_operation_id(),
        "type": "kupno_waluty",
        "asset": code,
        "quantity": amount,
        "price": rate,
        "value": cost,
    })

    return f"Kupiono {amount:.2f} {code} po kursie {rate:.4f} PLN"


def sell_currency(portfolio: Portfolio, code: str, amount: float, rate: float) -> str:
    """Sprzedaje walutę po aktualnym kursie pobranym z API NBP."""
    code = code.strip().upper()

    if len(code) != 3:
        return "Błąd: kod waluty musi mieć 3 znaki"

    if amount <= 0:
        return "Błąd: ilość waluty musi być dodatnia"

    if rate <= 0:
        return "Błąd: kurs musi być dodatni"

    if portfolio["currencies"][code] < amount:
        return "Błąd: nie masz tyle waluty"

    value = round(amount * rate, 2)

    portfolio["currencies"][code] = round(portfolio["currencies"][code] - amount, 4)
    portfolio["cash"] = round(portfolio["cash"] + value, 2)

    portfolio["history"].append({
        "id": next_operation_id(),
        "type": "sprzedaz_waluty",
        "asset": code,
        "quantity": amount,
        "price": rate,
        "value": value,
    })

    return f"Sprzedano {amount:.2f} {code} po kursie {rate:.4f} PLN"


def calculate_total_value(
    portfolio: Portfolio,
    stocks: dict[str, Stock],
    currency_rates: dict[str, float] | None = None,
) -> float:
    """Oblicza całkowitą wartość portfela w PLN."""
    total = float(portfolio["cash"])

    for symbol, quantity in portfolio["stocks"].items():
        if quantity > 0 and symbol in stocks:
            total += float(stocks[symbol]["price"]) * quantity

    if currency_rates:
        for code, amount in portfolio["currencies"].items():
            if amount > 0:
                total += currency_rates.get(code, 0.0) * amount

    return round(total, 2)