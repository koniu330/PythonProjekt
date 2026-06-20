"""Menu konsolowe aplikacji MarketSim."""

from __future__ import annotations

from pathlib import Path

from app.analysis import group_transactions_by_type, most_traded_assets, total_transaction_value
from app.market import copy_default_stocks, forecast_price, generate_stock_pairs, update_stock_prices
from app.nbp_api import NBPApiError, get_currency_rate, get_many_currency_rates, print_api_test
from app.portfolio import (
    buy_currency,
    buy_stock,
    calculate_total_value,
    create_portfolio,
    sell_currency,
    sell_stock,
)
from app.storage import load_json, restore_portfolio, save_json, serialize_portfolio


SAVE_FILE = Path("portfolio.json")


def print_stocks(stocks: dict) -> None:
    """Wypisuje dostępne spółki."""
    print("\n=== DOSTĘPNE SPÓŁKI ===")

    for symbol, data in stocks.items():
        print(
            f"{symbol:4s} | {data['name']:12s} | "
            f"{data['price']:9.2f} zł | sektor: {data['sector']} | ryzyko: {data['risk']}"
        )


def print_portfolio(portfolio: dict, stocks: dict) -> None:
    """Wypisuje zawartość portfela."""
    print("\n=== PORTFEL ===")
    print(f"Gotówka: {portfolio['cash']:.2f} zł")

    print("\nAkcje:")
    has_stocks = False

    for symbol, quantity in portfolio["stocks"].items():
        if quantity > 0:
            has_stocks = True
            price = stocks[symbol]["price"]
            value = price * quantity
            print(f"{symbol}: {quantity} szt. | cena: {price:.2f} zł | wartość: {value:.2f} zł")

    if not has_stocks:
        print("Brak akcji")

    print("\nWaluty:")
    has_currencies = False

    for code, amount in portfolio["currencies"].items():
        if amount > 0:
            has_currencies = True
            try:
                rate = get_currency_rate(code)
                value = amount * rate
                print(f"{code}: {amount:.2f} | kurs NBP: {rate:.4f} zł | wartość: {value:.2f} zł")
            except NBPApiError:
                print(f"{code}: {amount:.2f} | nie udało się pobrać kursu")

    if not has_currencies:
        print("Brak walut")


def print_history(portfolio: dict) -> None:
    """Wypisuje historię transakcji."""
    print("\n=== HISTORIA TRANSAKCJI ===")

    if not portfolio["history"]:
        print("Brak transakcji")
        return

    for operation in portfolio["history"]:
        print(
            f"ID {operation['id']}: {operation['type']} | {operation['asset']} | "
            f"ilość: {operation['quantity']} | cena: {operation['price']:.4f} | "
            f"wartość: {operation['value']:.2f} zł"
        )


def print_currency_rates() -> None:
    """Pobiera i pokazuje aktualne kursy popularnych walut z API NBP."""
    print("\n=== KURSY WALUT Z API NBP ===")

    try:
        rates = get_many_currency_rates("EUR", "USD", "GBP", "CHF")
    except NBPApiError as error:
        print(error)
        return

    for code, rate in rates.items():
        print(f"{code}: {rate:.4f} PLN")


def print_analysis(portfolio: dict, stocks: dict) -> None:
    """Wypisuje analizę portfela i transakcji."""
    print("\n=== ANALIZA ===")

    try:
        currency_codes = [
            code for code, amount in portfolio["currencies"].items()
            if amount > 0
        ]
        rates = get_many_currency_rates(*currency_codes) if currency_codes else {}
    except NBPApiError:
        rates = {}
        print("Nie udało się pobrać kursów walut. Liczę wartość bez walut.")

    print(f"Wartość portfela: {calculate_total_value(portfolio, stocks, rates):.2f} zł")
    print(f"Najczęściej handlowane aktywa: {most_traded_assets(portfolio['history'])}")
    print(f"Suma wszystkich transakcji: {total_transaction_value(portfolio['history']):.2f} zł")

    grouped = group_transactions_by_type(portfolio["history"])

    for transaction_type, operations in grouped.items():
        print(f"{transaction_type}: {len(operations)}")


def run_menu() -> None:
    """Uruchamia główną pętlę programu."""
    stocks = copy_default_stocks()
    portfolio = create_portfolio()

    while True:
        print("\n========== MarketSim ==========")
        print("1. Pokaż spółki")
        print("2. Aktualizuj kursy akcji")
        print("3. Kup akcje")
        print("4. Sprzedaj akcje")
        print("5. Pokaż kursy walut z API NBP")
        print("6. Kup walutę po kursie NBP")
        print("7. Sprzedaj walutę po kursie NBP")
        print("8. Pokaż portfel")
        print("9. Historia transakcji")
        print("10. Analiza portfela")
        print("11. Pary spółek do porównania")
        print("12. Prognoza ceny akcji")
        print("13. Test połączenia z API NBP")
        print("14. Zapisz portfel")
        print("15. Wczytaj portfel")
        print("0. Zakończ")

        choice = input("Wybierz opcję: ").strip()

        if choice == "1":
            print_stocks(stocks)

        elif choice == "2":
            for message in update_stock_prices(stocks):
                print(message)

        elif choice == "3":
            symbol = input("Symbol spółki: ")
            quantity = int(input("Liczba akcji: "))
            print(buy_stock(portfolio, stocks, symbol, quantity))

        elif choice == "4":
            symbol = input("Symbol spółki: ")
            quantity = int(input("Liczba akcji: "))
            print(sell_stock(portfolio, stocks, symbol, quantity))

        elif choice == "5":
            print_currency_rates()

        elif choice == "6":
            code = input("Kod waluty, np. EUR: ")
            amount = float(input("Ilość waluty: "))

            try:
                rate = get_currency_rate(code)
                print(f"Aktualny kurs NBP {code.upper()}: {rate:.4f} PLN")
                print(buy_currency(portfolio, code, amount, rate))
            except NBPApiError as error:
                print(error)

        elif choice == "7":
            code = input("Kod waluty, np. EUR: ")
            amount = float(input("Ilość waluty: "))

            try:
                rate = get_currency_rate(code)
                print(f"Aktualny kurs NBP {code.upper()}: {rate:.4f} PLN")
                print(sell_currency(portfolio, code, amount, rate))
            except NBPApiError as error:
                print(error)

        elif choice == "8":
            print_portfolio(portfolio, stocks)

        elif choice == "9":
            print_history(portfolio)

        elif choice == "10":
            print_analysis(portfolio, stocks)

        elif choice == "11":
            print(generate_stock_pairs(stocks))

        elif choice == "12":
            symbol = input("Symbol spółki: ").upper()
            days = int(input("Liczba dni: "))

            if symbol in stocks:
                price = stocks[symbol]["price"]
                print(f"Prognoza: {forecast_price(price, days):.2f} zł")
                print(f"Cache: {forecast_price.cache_info()}")
            else:
                print("Błąd: nie ma takiej spółki")

        elif choice == "13":
            try:
                print_api_test()
            except NBPApiError as error:
                print(error)

        elif choice == "14":
            save_json(SAVE_FILE, serialize_portfolio(portfolio))
            print("Zapisano portfel")

        elif choice == "15":
            try:
                portfolio = restore_portfolio(load_json(SAVE_FILE))
                print("Wczytano portfel")
            except FileNotFoundError:
                print("Błąd: plik portfolio.json nie istnieje")

        elif choice == "0":
            print("Zakończono program")
            break

        else:
            print("Nieznana opcja")