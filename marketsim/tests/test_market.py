from app.market import (
    copy_default_stocks,
    forecast_price,
    generate_stock_pairs,
    get_stock,
    update_stock_prices,
)


def test_get_stock_existing_symbol():
    """Sprawdza, czy funkcja poprawnie zwraca dane istniejącej spółki."""
    stocks = copy_default_stocks()

    stock = get_stock(stocks, "cdr")

    assert stock is not None
    assert stock["name"] == "CD Projekt"


def test_get_stock_missing_symbol():
    """Sprawdza, czy dla nieistniejącego symbolu zwracane jest None."""
    stocks = copy_default_stocks()

    stock = get_stock(stocks, "XYZ")

    assert stock is None


def test_generate_stock_pairs():
    """Sprawdza, czy generowane są wszystkie unikalne pary spółek."""
    stocks = {"A": {}, "B": {}, "C": {}}

    pairs = generate_stock_pairs(stocks)

    assert pairs == [("A", "B"), ("A", "C"), ("B", "C")]


def test_forecast_price():
    """Sprawdza poprawność prognozowania ceny akcji."""
    assert forecast_price(100.0, 2) == 102.01


def test_update_stock_prices_keeps_prices_positive():
    """Sprawdza, czy po aktualizacji wszystkie ceny akcji pozostają dodatnie."""
    stocks = copy_default_stocks()

    update_stock_prices(stocks)

    for data in stocks.values():
        assert data["price"] >= 1.0