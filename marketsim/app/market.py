"""Moduł rynku akcji dla projektu MarketSim."""

from __future__ import annotations

import random
from functools import lru_cache
from itertools import combinations
from typing import Any


Stock = dict[str, Any]


DEFAULT_STOCKS: dict[str, Stock] = {
    "CDR": {"name": "CD Projekt", "price": 120.00, "sector": "gry", "risk": "wysokie"},
    "PKN": {"name": "Orlen", "price": 65.00, "sector": "paliwa", "risk": "srednie"},
    "PKO": {"name": "PKO BP", "price": 48.00, "sector": "banki", "risk": "niskie"},
    "ALE": {"name": "Allegro", "price": 36.00, "sector": "e-commerce", "risk": "srednie"},
    "LPP": {"name": "LPP", "price": 14500.00, "sector": "odziez", "risk": "wysokie"},
    "KGH": {"name": "KGHM", "price": 135.00, "sector": "surowce", "risk": "srednie"},
}


RISK_TO_VOLATILITY: dict[str, float] = {
    "niskie": 0.03,
    "srednie": 0.06,
    "wysokie": 0.10,
}


def copy_default_stocks() -> dict[str, Stock]:
    """Tworzy kopię domyślnej listy spółek.

    Returns:
        Nowy słownik ze spółkami, aby nie modyfikować stałej DEFAULT_STOCKS.
    """
    return {symbol: data.copy() for symbol, data in DEFAULT_STOCKS.items()}


def get_stock(stocks: dict[str, Stock], symbol: str) -> Stock | None:
    """Zwraca dane spółki po symbolu.

    Args:
        stocks: Słownik dostępnych spółek.
        symbol: Symbol spółki, np. CDR.

    Returns:
        Słownik z danymi spółki albo None, jeżeli spółka nie istnieje.
    """
    return stocks.get(symbol.upper())


def update_stock_prices(stocks: dict[str, Stock]) -> list[str]:
    """Aktualizuje ceny spółek na podstawie losowej zmienności.

    Args:
        stocks: Słownik spółek do aktualizacji.

    Returns:
        Lista tekstowych komunikatów opisujących zmianę ceny.
    """
    messages: list[str] = []

    for symbol, data in stocks.items():
        old_price = float(data["price"])
        risk = str(data.get("risk", "srednie"))
        volatility = RISK_TO_VOLATILITY.get(risk, 0.06)
        change = random.uniform(-volatility, volatility)
        new_price = round(max(1.0, old_price * (1 + change)), 2)
        data["price"] = new_price
        messages.append(f"{symbol}: {old_price:.2f} zł -> {new_price:.2f} zł ({change * 100:.2f}%)")

    return messages


def generate_stock_pairs(stocks: dict[str, Stock]) -> list[tuple[str, str]]:
    """Generuje wszystkie pary spółek do porównania.

    Args:
        stocks: Słownik spółek.

    Returns:
        Lista unikalnych par symboli spółek.
    """
    return list(combinations(stocks.keys(), 2))


@lru_cache(maxsize=256)
def forecast_price(price: float, days: int, daily_growth: float = 0.01) -> float:
    """Prognozuje cenę instrumentu finansowego z użyciem rekurencji i cache.

    Args:
        price: Cena początkowa.
        days: Liczba dni prognozy.
        daily_growth: Stały dzienny wzrost używany w prostej prognozie.

    Returns:
        Prognozowana cena po podanej liczbie dni.
    """
    if days <= 0:
        return round(price, 2)
    return forecast_price(round(price * (1 + daily_growth), 4), days - 1, daily_growth)
