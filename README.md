# MarketSim — symulator giełdy i inwestowania

MarketSim to konsolowa aplikacja napisana w języku Python. Program symuluje inwestowanie w akcje oraz waluty. Użytkownik otrzymuje wirtualny portfel z gotówką, może kupować i sprzedawać akcje, kupować waluty po kursie pobieranym z API NBP, analizować historię transakcji oraz zapisywać stan portfela do pliku JSON.

Projekt został przygotowany jako zaliczeniowy projekt zespołowy z przedmiotu **Programowanie w języku Python**.

---

## Funkcjonalności

- wyświetlanie listy spółek,
- losowa aktualizacja kursów akcji,
- kupowanie akcji,
- sprzedawanie akcji,
- kupowanie walut po kursie pobranym z API NBP,
- obliczanie wartości portfela,
- historia transakcji,
- analiza najczęściej handlowanych aktywów,
- grupowanie transakcji według typu,
- generowanie par spółek do porównania,
- prosta prognoza ceny z użyciem `lru_cache`,
- zapis portfela do pliku JSON,
- odczyt portfela z pliku JSON,
- testy jednostkowe.

---

## Integracja z API

Projekt korzysta z publicznego API Narodowego Banku Polskiego:

```text
https://api.nbp.pl/api/exchangerates/rates/A/EUR/?format=json
```

API służy do pobierania aktualnych średnich kursów walut, np. EUR, USD, GBP.

W projekcie odpowiada za to plik:

```text
app/nbp_api.py
```

---

## Struktura projektu

```text
marketsim/
│
├── main.py
├── README.md
├── requirements.txt
│
├── app/
│   ├── __init__.py
│   ├── analysis.py
│   ├── market.py
│   ├── menu.py
│   ├── nbp_api.py
│   ├── portfolio.py
│   └── storage.py
│
└── tests/
    ├── test_analysis.py
    ├── test_market.py
    ├── test_nbp_api.py
    └── test_portfolio.py
```

---

## Uruchomienie projektu

### 1. Pobranie repozytorium

```bash
git clone ADRES_REPOZYTORIUM
cd marketsim
```

### 2. Utworzenie środowiska wirtualnego

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalacja zależności

```bash
pip install -r requirements.txt
```

### 4. Uruchomienie programu

```bash
python main.py
```

---

## Uruchomienie testów

```bash
pytest
```

Testy znajdują się w katalogu `tests/`.

---

## Wykorzystane elementy języka Python

W projekcie wykorzystano zagadnienia omawiane na zajęciach:

- funkcje i wartości zwracane,
- parametry domyślne,
- `*args`,
- `**kwargs`,
- słowniki i listy,
- `Counter`,
- `defaultdict`,
- `itertools.combinations`,
- `functools.lru_cache`,
- domknięcie i `nonlocal`,
- type hints,
- docstringi,
- obsługę wyjątków,
- importy modułów,
- zapis i odczyt JSON,
- testy jednostkowe z `pytest`,
- mockowanie API w testach.

---

## Podział pracy dla 4 osób

### Osoba 1 — Rynek akcji

Plik: `app/market.py`

Zakres:

- lista spółek,
- pobieranie danych spółki,
- aktualizacja cen akcji,
- generowanie par spółek,
- prognoza ceny z cache.

### Osoba 2 — Portfel inwestora

Plik: `app/portfolio.py`

Zakres:

- tworzenie portfela,
- kupowanie akcji,
- sprzedawanie akcji,
- kupowanie walut,
- liczenie wartości portfela,
- historia operacji.

### Osoba 3 — API i zapis danych

Pliki: `app/nbp_api.py`, `app/storage.py`

Zakres:

- pobieranie kursów walut z API NBP,
- obsługa błędów API,
- zapis portfela do JSON,
- odczyt portfela z JSON.

### Osoba 4 — Analiza, menu i testy

Pliki: `app/analysis.py`, `app/menu.py`, `tests/`

Zakres:

- analiza historii transakcji,
- najczęściej handlowane aktywa,
- grupowanie transakcji,
- menu konsolowe,
- testy jednostkowe.

---

## Przykładowy scenariusz użycia

1. Użytkownik uruchamia program.
2. Wybiera opcję pokazania dostępnych spółek.
3. Kupuje akcje wybranej spółki, np. CDR.
4. Aktualizuje kursy akcji.
5. Kupuje walutę EUR po kursie z API NBP.
6. Sprawdza wartość portfela.
7. Ogląda historię transakcji.
8. Zapisuje portfel do pliku JSON.

---

## Autorzy

Projekt wykonany przez zespół 4-osobowy w ramach zajęć z programowania w języku Python.
