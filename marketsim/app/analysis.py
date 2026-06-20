"""Moduł analizy transakcji i portfela."""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any

History = list[dict[str, Any]]


def most_traded_assets(history: History, limit: int = 3) -> list[tuple[str, int]]:
    """Zwraca najczęściej handlowane aktywa.

    Args:
        history: Historia transakcji.
        limit: Maksymalna liczba wyników.

    Returns:
        Lista krotek w formacie aktywo, liczba transakcji.
    """
    assets = [operation["asset"] for operation in history]
    return Counter(assets).most_common(limit)


def group_transactions_by_type(history: History) -> dict[str, list[dict[str, Any]]]:
    """Grupuje transakcje według typu.

    Args:
        history: Historia transakcji.

    Returns:
        Zwykły słownik, którego kluczem jest typ transakcji.
    """
    grouped: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    for operation in history:
        grouped[operation["type"]].append(operation)
    return dict(grouped)


def total_transaction_value(history: History, *transaction_types: str) -> float:
    """Liczy sumę wartości transakcji.

    Args:
        history: Historia transakcji.
        *transaction_types: Opcjonalne typy transakcji do uwzględnienia.

    Returns:
        Suma wartości transakcji.
    """
    allowed_types = set(transaction_types)
    total = 0.0

    for operation in history:
        if not allowed_types or operation["type"] in allowed_types:
            total += float(operation["value"])

    return round(total, 2)


def build_report_data(**data: Any) -> dict[str, Any]:
    """Buduje słownik danych raportu z argumentów nazwanych.

    Args:
        **data: Dowolne dane raportowe przekazane jako argumenty nazwane.

    Returns:
        Słownik z danymi raportowymi.
    """
    return data
