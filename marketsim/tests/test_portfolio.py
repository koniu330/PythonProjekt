from app.market import copy_default_stocks
from app.portfolio import (
    buy_currency,
    buy_stock,
    calculate_total_value,
    create_portfolio,
    sell_currency,
    sell_stock,
)


def test_buy_stock_success():
    """Sprawdza poprawne kupowanie akcji i aktualizację portfela."""
    stocks = copy_default_stocks()
    portfolio = create_portfolio(1000)

    result = buy_stock(portfolio, stocks, "PKO", 2)

    assert result.startswith("Kupiono")
    assert portfolio["stocks"]["PKO"] == 2
    assert portfolio["cash"] < 1000
    assert portfolio["history"][-1]["type"] == "kupno_akcji"


def test_buy_stock_not_enough_cash():
    """Sprawdza reakcję programu przy zbyt małej ilości gotówki."""
    stocks = copy_default_stocks()
    portfolio = create_portfolio(10)

    result = buy_stock(portfolio, stocks, "PKO", 100)

    assert result == "Błąd: za mało gotówki"


def test_sell_stock_success():
    """Sprawdza poprawną sprzedaż posiadanych akcji."""
    stocks = copy_default_stocks()
    portfolio = create_portfolio(1000)

    buy_stock(portfolio, stocks, "PKO", 2)
    result = sell_stock(portfolio, stocks, "PKO", 1)

    assert result.startswith("Sprzedano")
    assert portfolio["stocks"]["PKO"] == 1
    assert portfolio["history"][-1]["type"] == "sprzedaz_akcji"


def test_sell_stock_without_stock():
    """Sprawdza próbę sprzedaży akcji, których użytkownik nie posiada."""
    stocks = copy_default_stocks()
    portfolio = create_portfolio(1000)

    result = sell_stock(portfolio, stocks, "PKO", 1)

    assert result == "Błąd: nie masz tylu akcji"


def test_calculate_total_value_with_stocks():
    """Sprawdza obliczanie wartości portfela zawierającego akcje."""
    stocks = copy_default_stocks()
    portfolio = create_portfolio(1000)

    buy_stock(portfolio, stocks, "PKO", 2)

    expected = portfolio["cash"] + stocks["PKO"]["price"] * 2

    assert calculate_total_value(portfolio, stocks) == round(expected, 2)


def test_buy_currency_success():
    """Sprawdza poprawny zakup waluty i aktualizację portfela."""
    portfolio = create_portfolio(start_cash=1000)

    result = buy_currency(portfolio, "EUR", 100, 4.5)

    assert result.startswith("Kupiono")
    assert portfolio["cash"] == 550
    assert portfolio["currencies"]["EUR"] == 100
    assert portfolio["history"][-1]["type"] == "kupno_waluty"


def test_sell_currency_success():
    """Sprawdza poprawną sprzedaż posiadanej waluty."""
    portfolio = create_portfolio(start_cash=1000)

    buy_currency(portfolio, "EUR", 100, 4.5)
    result = sell_currency(portfolio, "EUR", 40, 4.6)

    assert result.startswith("Sprzedano")
    assert portfolio["currencies"]["EUR"] == 60
    assert portfolio["cash"] == 734
    assert portfolio["history"][-1]["type"] == "sprzedaz_waluty"


def test_sell_currency_not_enough_currency():
    """Sprawdza próbę sprzedaży większej ilości waluty niż użytkownik posiada."""
    portfolio = create_portfolio(start_cash=1000)

    result = sell_currency(portfolio, "EUR", 10, 4.5)

    assert result == "Błąd: nie masz tyle waluty"


def test_calculate_total_value_with_currency():
    """Sprawdza obliczanie wartości portfela zawierającego akcje i waluty."""
    stocks = copy_default_stocks()
    portfolio = create_portfolio(1000)

    buy_stock(portfolio, stocks, "PKO", 2)
    buy_currency(portfolio, "USD", 10, 4.0)

    rates = {"USD": 4.0}
    expected = (
        portfolio["cash"]
        + stocks["PKO"]["price"] * 2
        + portfolio["currencies"]["USD"] * rates["USD"]
    )

    assert calculate_total_value(portfolio, stocks, rates) == round(expected, 2)