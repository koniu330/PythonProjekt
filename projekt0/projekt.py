from collections import Counter, defaultdict
from functools import lru_cache
from itertools import combinations
import random
import json


# =====================================================
# DANE STARTOWE
# =====================================================

spolki = {
    "CDR": {"nazwa": "CD Projekt", "cena": 120.00, "sektor": "gry"},
    "PKN": {"nazwa": "Orlen", "cena": 65.00, "sektor": "paliwa"},
    "PKO": {"nazwa": "PKO BP", "cena": 48.00, "sektor": "banki"},
    "ALE": {"nazwa": "Allegro", "cena": 36.00, "sektor": "e-commerce"},
    "LPP": {"nazwa": "LPP", "cena": 14500.00, "sektor": "odzież"},
    "KGH": {"nazwa": "KGHM", "cena": 135.00, "sektor": "surowce"},
}

portfel = {
    "gotowka": 100000.00,
    "akcje": defaultdict(int),
    "historia": []
}


# =====================================================
# HISTORIA OPERACJI — CLOSURE
# =====================================================

def stworz_licznik_operacji():
    licznik = 0

    def zwieksz():
        nonlocal licznik
        licznik += 1
        return licznik

    return zwieksz


licznik_operacji = stworz_licznik_operacji()


# =====================================================
# FUNKCJE GIEŁDOWE
# =====================================================

def pokaz_spolki():
    print("\n=== DOSTĘPNE SPÓŁKI ===")
    for symbol, dane in spolki.items():
        print(
            f"{symbol:4s} | {dane['nazwa']:15s} | "
            f"{dane['cena']:8.2f} zł | sektor: {dane['sektor']}"
        )


def aktualizuj_kursy():
    print("\n=== AKTUALIZACJA KURSÓW ===")

    for symbol, dane in spolki.items():
        zmiana = random.uniform(-0.08, 0.08)
        stara_cena = dane["cena"]
        nowa_cena = round(stara_cena * (1 + zmiana), 2)

        if nowa_cena < 1:
            nowa_cena = 1

        dane["cena"] = nowa_cena

        print(
            f"{symbol}: {stara_cena:.2f} zł → {nowa_cena:.2f} zł "
            f"({zmiana * 100:.2f}%)"
        )


def kup_akcje(symbol, ilosc):
    symbol = symbol.upper()

    if symbol not in spolki:
        return "Błąd: nie ma takiej spółki"

    if ilosc <= 0:
        return "Błąd: liczba akcji musi być dodatnia"

    cena = spolki[symbol]["cena"]
    koszt = cena * ilosc

    if koszt > portfel["gotowka"]:
        return "Błąd: za mało gotówki"

    portfel["gotowka"] -= koszt
    portfel["akcje"][symbol] += ilosc

    operacja_id = licznik_operacji()

    portfel["historia"].append({
        "id": operacja_id,
        "typ": "kupno",
        "symbol": symbol,
        "ilosc": ilosc,
        "cena": cena,
        "wartosc": round(koszt, 2)
    })

    return f"Kupiono {ilosc} akcji {symbol} za {koszt:.2f} zł"


def sprzedaj_akcje(symbol, ilosc):
    symbol = symbol.upper()

    if symbol not in spolki:
        return "Błąd: nie ma takiej spółki"

    if ilosc <= 0:
        return "Błąd: liczba akcji musi być dodatnia"

    if portfel["akcje"][symbol] < ilosc:
        return "Błąd: nie masz tylu akcji"

    cena = spolki[symbol]["cena"]
    wartosc = cena * ilosc

    portfel["akcje"][symbol] -= ilosc
    portfel["gotowka"] += wartosc

    operacja_id = licznik_operacji()

    portfel["historia"].append({
        "id": operacja_id,
        "typ": "sprzedaż",
        "symbol": symbol,
        "ilosc": ilosc,
        "cena": cena,
        "wartosc": round(wartosc, 2)
    })

    return f"Sprzedano {ilosc} akcji {symbol} za {wartosc:.2f} zł"


def wartosc_portfela():
    wartosc_akcji = 0

    for symbol, ilosc in portfel["akcje"].items():
        wartosc_akcji += spolki[symbol]["cena"] * ilosc

    return round(portfel["gotowka"] + wartosc_akcji, 2)


def pokaz_portfel():
    print("\n=== PORTFEL INWESTORA ===")
    print(f"Gotówka: {portfel['gotowka']:.2f} zł")

    print("\nAkcje:")
    if not portfel["akcje"]:
        print("Brak akcji w portfelu")
    else:
        for symbol, ilosc in portfel["akcje"].items():
            if ilosc > 0:
                cena = spolki[symbol]["cena"]
                wartosc = cena * ilosc
                print(f"{symbol}: {ilosc} szt. | cena: {cena:.2f} zł | wartość: {wartosc:.2f} zł")

    print(f"\nCałkowita wartość portfela: {wartosc_portfela():.2f} zł")


# =====================================================
# ANALIZA DANYCH
# =====================================================

def najczesciej_handlowane_spolki():
    symbole = []

    for operacja in portfel["historia"]:
        symbole.append(operacja["symbol"])

    licznik = Counter(symbole)
    return licznik.most_common(3)


def grupuj_transakcje_po_typie():
    grupy = defaultdict(list)

    for operacja in portfel["historia"]:
        grupy[operacja["typ"]].append(operacja)

    return dict(grupy)


def pokaz_historie():
    print("\n=== HISTORIA TRANSAKCJI ===")

    if not portfel["historia"]:
        print("Brak transakcji")
        return

    for op in portfel["historia"]:
        print(
            f"ID {op['id']}: {op['typ']} | {op['symbol']} | "
            f"{op['ilosc']} szt. | cena {op['cena']:.2f} zł | "
            f"wartość {op['wartosc']:.2f} zł"
        )


def pokaz_analize():
    print("\n=== ANALIZA PORTFELA ===")

    print(f"Wartość portfela: {wartosc_portfela():.2f} zł")

    print("\nNajczęściej handlowane spółki:")
    top = najczesciej_handlowane_spolki()

    if not top:
        print("Brak danych")
    else:
        for symbol, liczba in top:
            print(f"{symbol}: {liczba} transakcji")

    print("\nTransakcje według typu:")
    grupy = grupuj_transakcje_po_typie()
    for typ, lista in grupy.items():
        print(f"{typ}: {len(lista)}")


# =====================================================
# ITERTOOLS — PORÓWNYWANIE SPÓŁEK
# =====================================================

def pokaz_pary_spolek():
    print("\n=== MOŻLIWE PARY SPÓŁEK DO PORÓWNANIA ===")

    pary = list(combinations(spolki.keys(), 2))

    for para in pary:
        print(f"{para[0]} + {para[1]}")


# =====================================================
# LRU CACHE — PRZYKŁADOWA PROGNOZA
# =====================================================

@lru_cache
def prognozuj_wartosc(cena, dni):
    if dni == 0:
        return cena

    return round(prognozuj_wartosc(cena * 1.01, dni - 1), 2)


def pokaz_prognoze():
    symbol = input("Podaj symbol spółki: ").upper()

    if symbol not in spolki:
        print("Błąd: nie ma takiej spółki")
        return

    dni = int(input("Podaj liczbę dni prognozy: "))
    cena = spolki[symbol]["cena"]

    wynik = prognozuj_wartosc(cena, dni)

    print(f"Prognozowana cena {symbol} za {dni} dni: {wynik:.2f} zł")
    print(f"Cache info: {prognozuj_wartosc.cache_info()}")


# =====================================================
# ZAPIS I ODCZYT JSON
# =====================================================

def zapisz_portfel(nazwa_pliku="portfel.json"):
    dane = {
        "gotowka": portfel["gotowka"],
        "akcje": dict(portfel["akcje"]),
        "historia": portfel["historia"]
    }

    with open(nazwa_pliku, "w", encoding="utf-8") as plik:
        json.dump(dane, plik, indent=4, ensure_ascii=False)

    print("Zapisano portfel do pliku")


def wczytaj_portfel(nazwa_pliku="portfel.json"):
    try:
        with open(nazwa_pliku, "r", encoding="utf-8") as plik:
            dane = json.load(plik)

        portfel["gotowka"] = dane["gotowka"]
        portfel["akcje"] = defaultdict(int, dane["akcje"])
        portfel["historia"] = dane["historia"]

        print("Wczytano portfel z pliku")

    except FileNotFoundError:
        print("Błąd: plik nie istnieje")


# =====================================================
# RAPORT
# =====================================================

def generuj_raport():
    print("\n=== RAPORT INWESTORA ===")
    print(f"Gotówka: {portfel['gotowka']:.2f} zł")
    print(f"Wartość całego portfela: {wartosc_portfela():.2f} zł")
    print(f"Liczba transakcji: {len(portfel['historia'])}")

    top = najczesciej_handlowane_spolki()
    print(f"Najczęściej handlowane spółki: {top}")


# =====================================================
# MENU
# =====================================================

def menu():
    while True:
        print("\n========== SYMULATOR GIEŁDY ==========")
        print("1. Pokaż spółki")
        print("2. Aktualizuj kursy")
        print("3. Kup akcje")
        print("4. Sprzedaj akcje")
        print("5. Pokaż portfel")
        print("6. Historia transakcji")
        print("7. Analiza portfela")
        print("8. Pokaż pary spółek")
        print("9. Prognoza ceny")
        print("10. Zapisz portfel")
        print("11. Wczytaj portfel")
        print("12. Generuj raport")
        print("0. Zakończ")

        wybor = input("Wybierz opcję: ")

        if wybor == "1":
            pokaz_spolki()

        elif wybor == "2":
            aktualizuj_kursy()

        elif wybor == "3":
            symbol = input("Podaj symbol spółki: ")
            ilosc = int(input("Podaj liczbę akcji: "))
            print(kup_akcje(symbol, ilosc))

        elif wybor == "4":
            symbol = input("Podaj symbol spółki: ")
            ilosc = int(input("Podaj liczbę akcji: "))
            print(sprzedaj_akcje(symbol, ilosc))

        elif wybor == "5":
            pokaz_portfel()

        elif wybor == "6":
            pokaz_historie()

        elif wybor == "7":
            pokaz_analize()

        elif wybor == "8":
            pokaz_pary_spolek()

        elif wybor == "9":
            pokaz_prognoze()

        elif wybor == "10":
            zapisz_portfel()

        elif wybor == "11":
            wczytaj_portfel()

        elif wybor == "12":
            generuj_raport()

        elif wybor == "0":
            print("Zakończono program")
            break

        else:
            print("Nieznana opcja")


menu()