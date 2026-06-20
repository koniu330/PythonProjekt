"""Zapis i odczyt stanu aplikacji z pliku JSON."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any


def save_json(path: str | Path, data: dict[str, Any]) -> None:
    """Zapisuje dane do pliku JSON.

    Args:
        path: Ścieżka do pliku.
        data: Dane do zapisania.
    """
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def load_json(path: str | Path) -> dict[str, Any]:
    """Wczytuje dane z pliku JSON.

    Args:
        path: Ścieżka do pliku.

    Returns:
        Dane wczytane z pliku.
    """
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def serialize_portfolio(portfolio: dict[str, Any]) -> dict[str, Any]:
    """Przygotowuje portfel do zapisu w JSON.

    Args:
        portfolio: Portfel używany przez aplikację.

    Returns:
        Portfel bez typów defaultdict, które trudniej zapisywać.
    """
    return {
        "cash": portfolio["cash"],
        "stocks": dict(portfolio["stocks"]),
        "currencies": dict(portfolio["currencies"]),
        "history": portfolio["history"],
    }


def restore_portfolio(data: dict[str, Any]) -> dict[str, Any]:
    """Odtwarza portfel po wczytaniu z JSON.

    Args:
        data: Dane portfela z pliku JSON.

    Returns:
        Portfel z przywróconymi defaultdict.
    """
    return {
        "cash": float(data.get("cash", 0.0)),
        "stocks": defaultdict(int, data.get("stocks", {})),
        "currencies": defaultdict(float, data.get("currencies", {})),
        "history": data.get("history", []),
    }
