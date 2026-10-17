"""Test dymny: sprawdza oba portale i kluczowe zasoby.

Uruchom po wklejeniu tokenu/klucza do .env:
    .venv/Scripts/python.exe src/sprawdz_setup.py
"""

from waw_api import WawApi, WawApiError, WawApiNew

# resource_id starego portalu bywają zmieniane przez UM — jeśli zawiodą,
# aktualny ID jest na karcie zasobu w api.um.warszawa.pl.
ZASOBY_STARE = {
    "Przystanki ZTM (dbstore)": "ab75c33d-3a26-4342-b36a-6e5fef0a3ac3",
}


def sprawdz_nowy() -> None:
    print("=== NOWY portal: dane.um.warszawa.pl (POST + token) ===")
    try:
        api = WawApiNew()
    except RuntimeError as exc:
        print(f"  [POMINIĘTO] {exc}")
        return

    testy = [
        ("Lokalizacja pojazdów (autobusy)", lambda: api.lokalizacja_pojazdow(1)),
        ("Lokalizacja pojazdów (tramwaje)", lambda: api.lokalizacja_pojazdow(2)),
        ("Linie na przystanku 5070/03", lambda: api.linie_na_przystanku("5070", "03")),
        (
            "Ceny nieruchomości (Bemowo 2022)",
            lambda: api.ceny_nieruchomosci(
                "Bemowo", "nieruchomoscLokalowa", "rynekPierwotny", 2022
            ),
        ),
    ]
    for nazwa, fn in testy:
        try:
            dane = fn()
            licznik = len(dane) if hasattr(dane, "__len__") else "?"
            print(f"  OK   {nazwa}: {licznik} rekordów")
            if isinstance(dane, list) and dane:
                print(f"       przykład: {str(dane[0])[:110]}")
        except WawApiError as exc:
            print(f"  FAIL {nazwa}: {exc}")
        except Exception as exc:
            print(f"  FAIL {nazwa}: [{type(exc).__name__}] {exc}")


def sprawdz_stary() -> None:
    print("\n=== STARY portal: api.um.warszawa.pl (GET + apikey) ===")
    try:
        api = WawApi()
    except RuntimeError as exc:
        print(f"  [POMINIĘTO] {exc}")
        return

    for nazwa, metoda in (("autobusy", api.buses), ("tramwaje", api.trams)):
        try:
            dane = metoda()
            print(f"  OK   {nazwa}: {len(dane)} pojazdów")
        except WawApiError as exc:
            print(f"  FAIL {nazwa}: {exc}")

    for nazwa, rid in ZASOBY_STARE.items():
        try:
            dane = api.dbstore(rid)
            print(f"  OK   {nazwa}: {len(dane)} rekordów")
        except WawApiError as exc:
            print(f"  FAIL {nazwa}: {exc}  (sprawdź resource_id na portalu)")


def main() -> None:
    sprawdz_nowy()
    sprawdz_stary()
    print(
        "\nUwaga: HTTP 500 'Service unavailable' na nowym portalu zwykle NIE oznacza "
        "awarii, tylko zły typ parametru (np. rok jako tekst zamiast liczby)."
    )


if __name__ == "__main__":
    main()
