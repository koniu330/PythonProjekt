"""Moduł portfela inwestora dla projektu MarketSim."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from app.market import Stock, get_stock


def create_operation_counter():
    """Tworzy licznik operacji jako domknięcie.

    Returns:
        Funkcja, która przy każdym wywołaniu zwiększa licznik o 1.
    """
    counter = 0

    def next_id() -> int:
        nonlocal counter
        counter += 1
        return counter

    return next_id


next_operation_id = create_operation_counter()


Portfolio = dict[str, Any]


def create_portfolio(start_cash: float = 100_000.0) -> Portfolio:
    """Tworzy nowy portfel inwestora.

    Args:
        start_cash: Początkowa kwota gotówki.

    Returns:
        Słownik reprezentujący portfel.
    """
    return {
        "cash": float(start_cash),
        "stocks": defaultdict(int),
        "currencies": defaultdict(float),
        "history": [],
    }


def buy_stock(portfolio: Portfolio, stocks: dict[str, Stock], symbol: str, quantity: int) -> str:
    """Kupuje akcje wybranej spółki.

    Args:
        portfolio: Portfel inwestora.
        stocks: Słownik dostępnych spółek.
        symbol: Symbol spółki.
        quantity: Liczba kupowanych akcji.

    Returns:
        Komunikat z wynikiem operacji.
    """
    symbol = symbol.upper()
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
    """Sprzedaje akcje wybranej spółki.

    Args:
        portfolio: Portfel inwestora.
        stocks: Słownik dostępnych spółek.
        symbol: Symbol spółki.
        quantity: Liczba sprzedawanych akcji.

    Returns:
        Komunikat z wynikiem operacji.
    """
    symbol = symbol.upper()
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
    """Kupuje walutę po kursie NBP.

    Args:
        portfolio: Portfel inwestora.
        code: Kod waluty, np. EUR.
        amount: Ilość kupowanej waluty.
        rate: Kurs jednej jednostki waluty w PLN.

    Returns:
        Komunikat z wynikiem operacji.
    """
    code = code.upper()

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
    return f"Kupiono {amount:.2f} {code} za {cost:.2f} zł"


def calculate_total_value(portfolio: Portfolio, stocks: dict[str, Stock], currency_rates: dict[str, float] | None = None) -> float:
    """Oblicza całkowitą wartość portfela.

    Args:
        portfolio: Portfel inwestora.
        stocks: Słownik dostępnych spółek.
        currency_rates: Opcjonalny słownik kursów walut.

    Returns:
        Całkowita wartość portfela w PLN.
    """
    total = float(portfolio["cash"])

    for symbol, quantity in portfolio["stocks"].items():
        if quantity > 0 and symbol in stocks:
            total += float(stocks[symbol]["price"]) * quantity

    if currency_rates:
        for code, amount in portfolio["currencies"].items():
            total += currency_rates.get(code, 0.0) * amount

    return round(total, 2)
