from app.market import copy_default_stocks
from app.portfolio import buy_currency, buy_stock, calculate_total_value, create_portfolio, sell_stock


def test_buy_stock_success():
    stocks = copy_default_stocks()
    portfolio = create_portfolio(1000)

    result = buy_stock(portfolio, stocks, "CDR", 2)

    assert "Kupiono" in result
    assert portfolio["stocks"]["CDR"] == 2
    assert portfolio["cash"] == 760.0


def test_buy_stock_not_enough_cash():
    stocks = copy_default_stocks()
    portfolio = create_portfolio(10)

    result = buy_stock(portfolio, stocks, "CDR", 1)

    assert result == "Błąd: za mało gotówki"
    assert portfolio["stocks"]["CDR"] == 0


def test_sell_stock_success():
    stocks = copy_default_stocks()
    portfolio = create_portfolio(1000)
    buy_stock(portfolio, stocks, "PKO", 5)

    result = sell_stock(portfolio, stocks, "PKO", 2)

    assert "Sprzedano" in result
    assert portfolio["stocks"]["PKO"] == 3


def test_buy_currency_success():
    portfolio = create_portfolio(1000)

    result = buy_currency(portfolio, "EUR", 100, 4.25)

    assert "Kupiono" in result
    assert portfolio["currencies"]["EUR"] == 100
    assert portfolio["cash"] == 575.0


def test_calculate_total_value_with_currency():
    stocks = copy_default_stocks()
    portfolio = create_portfolio(1000)
    buy_stock(portfolio, stocks, "PKO", 2)
    buy_currency(portfolio, "USD", 10, 4.0)

    total = calculate_total_value(portfolio, stocks, {"USD": 4.0})

    assert total == 1000.0
