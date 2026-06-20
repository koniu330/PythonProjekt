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
    """
    code = code.strip().upper()

    if len(code) != 3:
        raise NBPApiError("Kod waluty musi mieć 3 znaki, np. EUR albo USD")

    url = f"{API_BASE_URL}/rates/a/{code}/?format=json"

    try:
        response = requests.get(
            url,
            timeout=10,
            headers={"Accept": "application/json"},
        )

        if response.status_code == 404:
            raise NBPApiError(f"Nie znaleziono kursu waluty {code}")

        response.raise_for_status()
        data: dict[str, Any] = response.json()

        return float(data["rates"][0]["mid"])

    except requests.RequestException as error:
        raise NBPApiError(f"Błąd połączenia z API NBP dla waluty {code}") from error
    except (KeyError, IndexError, ValueError, TypeError) as error:
        raise NBPApiError(f"Niepoprawna odpowiedź API NBP dla waluty {code}") from error


def get_many_currency_rates(*codes: str) -> dict[str, float]:
    """Pobiera kursy wielu walut z API NBP.

    Args:
        *codes: Dowolna liczba kodów walut, np. EUR, USD, GBP.

    Returns:
        Słownik w formacie kod waluty -> kurs PLN.
    """
    rates: dict[str, float] = {}

    for code in codes:
        code = code.strip().upper()
        rates[code] = get_currency_rate(code)

    return rates


def print_api_test() -> None:
    """Pomocniczo pokazuje, że API faktycznie działa."""
    for code in ["EUR", "USD", "GBP", "CHF"]:
        rate = get_currency_rate(code)
        print(f"{code}: {rate:.4f} PLN")