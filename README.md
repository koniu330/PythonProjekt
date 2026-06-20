# 📈 MarketSim – Symulator Inwestowania i Analizy Portfela

## Autorzy

Projekt wykonany w ramach przedmiotu **Programowanie w języku Python**.

## Opis projektu

MarketSim jest aplikacją konsolową napisaną w języku Python, której celem jest symulacja działania rynku inwestycyjnego. Użytkownik otrzymuje wirtualny kapitał początkowy i może inwestować go w akcje wybranych spółek oraz waluty zagraniczne.

Projekt został stworzony w celu praktycznego wykorzystania zagadnień omawianych podczas zajęć, takich jak:

* funkcje i wartości zwracane,
* moduły i importy,
* struktury danych (listy, słowniki, krotki),
* obsługa wyjątków,
* type hints i docstringi,
* moduły `collections`, `itertools` i `functools`,
* testowanie aplikacji przy użyciu `pytest`,
* komunikacja z zewnętrznym API.

Dodatkowo aplikacja wykorzystuje publiczne API Narodowego Banku Polskiego do pobierania aktualnych kursów walut.

---

## Funkcjonalności

### Obsługa akcji

* przegląd dostępnych spółek,
* kupowanie akcji,
* sprzedawanie akcji,
* aktualizacja kursów akcji,
* prognozowanie przyszłych cen.

### Obsługa walut

* pobieranie aktualnych kursów walut z API NBP,
* zakup walut po aktualnym kursie,
* sprzedaż walut po aktualnym kursie,
* przechowywanie walut w portfelu.

### Portfel inwestora

* przechowywanie gotówki,
* przechowywanie akcji,
* przechowywanie walut,
* historia wszystkich operacji,
* obliczanie całkowitej wartości portfela.

### Analiza danych

* analiza najczęściej handlowanych aktywów (`Counter`),
* grupowanie transakcji według typu (`defaultdict`),
* generowanie wszystkich par spółek (`itertools.combinations`),
* prognozowanie cen z wykorzystaniem pamięci podręcznej (`lru_cache`).

### Zapis danych

* zapis portfela do pliku JSON,
* odczyt portfela z pliku JSON.

### Testy

Projekt zawiera zestaw testów jednostkowych sprawdzających:

* kupno akcji,
* sprzedaż akcji,
* kupno walut,
* sprzedaż walut,
* obliczanie wartości portfela,
* działanie modułów analitycznych,
* obsługę API NBP.

---

## Wykorzystane biblioteki

### Biblioteki standardowe

* json
* random
* pathlib
* collections
* itertools
* functools

### Biblioteki zewnętrzne

* requests
* pytest

Instalacja zależności:

```bash
pip install -r requirements.txt
```

---

## Struktura projektu

```text
marketsim/
│
├── main.py
├── requirements.txt
├── README.md
│
├── app/
│   ├── market.py
│   ├── portfolio.py
│   ├── nbp_api.py
│   ├── analysis.py
│   ├── storage.py
│   └── menu.py
│
└── tests/
    ├── test_market.py
    ├── test_portfolio.py
    ├── test_analysis.py
    └── test_nbp_api.py
```

---

## Uruchomienie projektu

Utworzenie środowiska:

```bash
python -m venv .venv
```

Instalacja bibliotek:

```bash
pip install -r requirements.txt
```

Uruchomienie programu:

```bash
python main.py
```

Uruchomienie testów:

```bash
pytest
```

---

## Integracja z API NBP

Projekt korzysta z publicznego API Narodowego Banku Polskiego:

https://api.nbp.pl

Przykładowe pobieranie kursu waluty:

```text
https://api.nbp.pl/api/exchangerates/rates/a/usd/?format=json
```

Na podstawie otrzymanych danych aplikacja umożliwia zakup oraz sprzedaż walut po aktualnych kursach.

---

## Przykładowe zagadnienia wykorzystane z zajęć

| Zagadnienie | Zastosowanie            |
| ----------- | ----------------------- |
| Funkcje     | logika programu         |
| Importy     | podział na moduły       |
| Type Hints  | dokumentacja kodu       |
| Docstringi  | opis funkcji            |
| Counter     | analiza transakcji      |
| defaultdict | grupowanie danych       |
| itertools   | generowanie par spółek  |
| lru_cache   | prognozowanie cen       |
| JSON        | zapis i odczyt portfela |
| API         | kursy walut NBP         |
| pytest      | testy jednostkowe       |

---

## Możliwe kierunki rozwoju

* logowanie wielu użytkowników,
* prowizje maklerskie,
* wykresy zmian kursów,
* baza danych SQLite,
* interfejs graficzny (Tkinter lub PyQt),
* integracja z rzeczywistymi notowaniami giełdowymi.

---

## Cel projektu

Głównym celem projektu było stworzenie modularnej aplikacji konsolowej wykorzystującej najważniejsze elementy języka Python poznane podczas zajęć oraz zaprezentowanie praktycznego wykorzystania zewnętrznych API, testów jednostkowych i analizy danych.
