"""Integracja z publicznym API Narodowego Banku Polskiego."""

from __future__ import annotations

from functools import lru_cache
from typing import Any

import requests


API_BASE_URL = "https://api.nbp.pl/api/exchangerates"


class NBPApiError(Exception):
    """Wyjątek zgłaszany przy problemach z API NBP."""


@lru_cache(maxsize=64)
def get_currency_rate(code: str) -> float:
    """Pobiera aktualny średni kurs waluty z tabeli A API NBP.

    Args:
        code: Kod waluty, np. EUR, USD, GBP.

    Returns:
        Aktualny kurs średni waluty w PLN.

    Raises:
        NBPApiError: Gdy API nie odpowiada albo zwraca niepoprawne dane.
    """
    code = code.upper()
    url = f"{API_BASE_URL}/rates/A/{code}/?format=json"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data: dict[str, Any] = response.json()
        return float(data["rates"][0]["mid"])
    except (requests.RequestException, KeyError, IndexError, ValueError) as error:
        raise NBPApiError(f"Nie udało się pobrać kursu waluty {code}") from error


def get_many_currency_rates(*codes: str) -> dict[str, float]:
    """Pobiera kursy wielu walut.

    Args:
        *codes: Dowolna liczba kodów walut.

    Returns:
        Słownik w formacie kod waluty -> kurs w PLN.
    """
    rates: dict[str, float] = {}
    for code in codes:
        rates[code.upper()] = get_currency_rate(code)
    return rates
