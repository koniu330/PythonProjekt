# Wyjaśnienie kodu — MarketSim

Ten plik pomaga przygotować się do obrony projektu. Nie opisuje dosłownie każdego znaku, ale tłumaczy rolę każdego pliku i najważniejszych funkcji.

---

## main.py

```python
from app.menu import run_menu
```

Importuje funkcję `run_menu` z modułu `menu.py`. To główna funkcja uruchamiająca aplikację konsolową.

```python
if __name__ == "__main__":
    run_menu()
```

Ten warunek sprawia, że menu uruchamia się tylko wtedy, gdy plik `main.py` jest uruchamiany bezpośrednio, np. przez `python main.py`.

---

## app/market.py

Ten plik odpowiada za rynek akcji.

### `DEFAULT_STOCKS`

Słownik z przykładowymi spółkami. Kluczem jest symbol spółki, np. `CDR`, a wartością jest kolejny słownik z nazwą, ceną, sektorem i poziomem ryzyka.

### `RISK_TO_VOLATILITY`

Słownik zamieniający poziom ryzyka na zmienność ceny. Im większe ryzyko, tym większy zakres losowej zmiany ceny.

### `copy_default_stocks()`

Zwraca kopię domyślnych spółek. Dzięki temu program może zmieniać ceny w trakcie działania, ale nie psuje oryginalnej stałej `DEFAULT_STOCKS`.

### `get_stock(stocks, symbol)`

Wyszukuje spółkę po symbolu. Używa `symbol.upper()`, żeby działały też małe litery, np. `cdr`.

### `update_stock_prices(stocks)`

Przechodzi po wszystkich spółkach, losuje procentową zmianę ceny i aktualizuje cenę. Funkcja zwraca listę komunikatów do wypisania w menu.

### `generate_stock_pairs(stocks)`

Używa `itertools.combinations`, aby wygenerować wszystkie możliwe pary spółek do porównania.

### `forecast_price(price, days, daily_growth=0.01)`

Prosta rekurencyjna prognoza ceny. Używa dekoratora `@lru_cache`, więc Python zapamiętuje wcześniej policzone wyniki.

---

## app/portfolio.py

Ten plik odpowiada za portfel inwestora.

### `create_operation_counter()`

Tworzy licznik operacji jako domknięcie. Zmienna `counter` jest zapamiętana wewnątrz funkcji `next_id`. Słowo `nonlocal` pozwala ją zmieniać.

### `create_portfolio(start_cash=100_000.0)`

Tworzy nowy portfel. Portfel ma gotówkę, akcje, waluty i historię transakcji.

### `buy_stock(...)`

Kupuje akcje. Funkcja sprawdza, czy spółka istnieje, czy liczba akcji jest dodatnia i czy użytkownik ma wystarczająco gotówki. Potem zmniejsza gotówkę, zwiększa liczbę akcji i zapisuje transakcję w historii.

### `sell_stock(...)`

Sprzedaje akcje. Sprawdza, czy spółka istnieje, czy ilość jest poprawna i czy użytkownik posiada wystarczającą liczbę akcji.

### `buy_currency(...)`

Kupuje walutę po podanym kursie. Kurs może pochodzić z API NBP.

### `calculate_total_value(...)`

Liczy całkowitą wartość portfela: gotówka + wartość akcji + wartość walut.

---

## app/nbp_api.py

Ten plik odpowiada za integrację z API NBP.

### `API_BASE_URL`

Adres bazowy API NBP.

### `NBPApiError`

Własny wyjątek, który informuje, że nie udało się pobrać danych z API.

### `get_currency_rate(code)`

Pobiera kurs jednej waluty, np. EUR. Funkcja używa biblioteki `requests`, wysyła zapytanie HTTP, odczytuje JSON i zwraca kurs `mid`.

### `get_many_currency_rates(*codes)`

Przyjmuje dowolną liczbę kodów walut dzięki `*codes` i zwraca słownik kursów.

---

## app/analysis.py

Ten plik analizuje historię transakcji.

### `most_traded_assets(history, limit=3)`

Używa `Counter`, aby policzyć, którymi aktywami handlowano najczęściej.

### `group_transactions_by_type(history)`

Używa `defaultdict(list)`, aby pogrupować transakcje według typu, np. `kupno_akcji`, `sprzedaz_akcji`, `kupno_waluty`.

### `total_transaction_value(history, *transaction_types)`

Liczy sumę transakcji. Dzięki `*transaction_types` można podać dowolną liczbę typów transakcji do filtrowania.

### `build_report_data(**data)`

Pokazuje użycie `**kwargs`. Funkcja przyjmuje dowolne dane nazwane i buduje z nich słownik raportowy.

---

## app/storage.py

Ten plik odpowiada za zapis i odczyt JSON.

### `save_json(path, data)`

Zapisuje dane do pliku JSON.

### `load_json(path)`

Wczytuje dane z pliku JSON.

### `serialize_portfolio(portfolio)`

Zamienia portfel na zwykły słownik, żeby można było go bez problemu zapisać do JSON.

### `restore_portfolio(data)`

Odtwarza portfel po wczytaniu z pliku. Przywraca `defaultdict`, żeby brakujące akcje lub waluty miały domyślną wartość 0.

---

## app/menu.py

Ten plik zawiera menu konsolowe.

### `print_stocks(stocks)`

Wypisuje spółki w czytelnej formie.

### `print_portfolio(portfolio, stocks)`

Wypisuje gotówkę, posiadane akcje i waluty.

### `print_history(portfolio)`

Wypisuje historię transakcji.

### `print_analysis(portfolio, stocks)`

Pokazuje analizę portfela: wartość portfela, najczęściej handlowane aktywa, sumę transakcji i grupowanie według typu.

### `run_menu()`

Najważniejsza funkcja aplikacji. Tworzy spółki i portfel, a następnie w pętli `while True` pokazuje użytkownikowi menu. Na podstawie wybranej opcji wywołuje odpowiednie funkcje z innych modułów.

---

## tests/

Katalog `tests` zawiera testy jednostkowe.

- `test_portfolio.py` sprawdza kupowanie, sprzedawanie i wartość portfela.
- `test_market.py` sprawdza funkcje rynku akcji.
- `test_analysis.py` sprawdza analizę historii transakcji.
- `test_nbp_api.py` sprawdza API z użyciem mocka, czyli bez wykonywania prawdziwego zapytania do internetu.

Testy uruchamia się komendą:

```bash
pytest
```
