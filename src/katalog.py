"""Przeglądarka katalogu zbiorów dane.um.warszawa.pl.

Katalog da się czytać programowo i **bez tokenu** — przydatne przy wybieraniu
tematu projektu, zanim cokolwiek zaczniesz pobierać.

    .venv/Scripts/python.exe src/katalog.py                  # wszystkie zbiory
    .venv/Scripts/python.exe src/katalog.py --kategoria Transport
    .venv/Scripts/python.exe src/katalog.py --szukaj powietrze
    .venv/Scripts/python.exe src/katalog.py --szczegoly <id>  # parametry API zbioru
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request

# Ustawienie kodowania konsoli — Windows bywa w cp1251 i wywala polskie znaki.
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

KATALOG_URL = "https://dane.um.warszawa.pl/api/datasets"
PLIK_URL = "https://dane.um.warszawa.pl/files/{}.json"


def _pasuje(zbior: dict, fraza: str) -> bool:
    """Dopasowanie odporne na polską odmianę.

    "powietrze" ma trafić w "Monitoring jakości powietrza", dlatego porównujemy
    też rdzeń słowa — bez dwóch ostatnich liter (końcówki fleksyjnej).
    """
    tekst = f"{zbior.get('title', '')} {zbior.get('notes') or ''}".lower()
    fraza = fraza.lower().strip()
    if fraza in tekst:
        return True
    # Rdzeń dopasowujemy tylko na początku słowa, inaczej krótkie rdzenie
    # trafiają w środek niezwiązanych wyrazów ("row" w "Rejestr"... ).
    if len(fraza) > 4:
        rdzen = fraza[:-2]
        return any(slowo.startswith(rdzen) for slowo in re.findall(r"\w+", tekst))
    return False


def pobierz_katalog() -> list[dict]:
    """Zbiera wszystkie strony katalogu. Bez tokenu."""
    wszystkie: list[dict] = []
    seen: set[str] = set()
    for page in range(1, 11):  # zabezpieczenie przed pętlą bez końca
        with urllib.request.urlopen(f"{KATALOG_URL}?page={page}", timeout=30) as r:
            wynik = json.load(r)["result"]
        for x in wynik["results"]:
            if x["id"] not in seen:
                seen.add(x["id"])
                wszystkie.append(x)
        if len(wszystkie) >= wynik.get("count", 0):
            break
    return wszystkie


def _url_specyfikacji(zbior_id: str, pole: str) -> str | None:
    """Czyta z karty zbioru URL pliku `parameters` albo `call_examples`."""
    strona = f"https://dane.um.warszawa.pl/pl/catalogue/{zbior_id}"
    try:
        with urllib.request.urlopen(strona, timeout=25) as r:
            html = r.read().decode("utf-8", errors="replace")
    except Exception:
        return None
    m = re.search(rf'"{pole}\\?":\\?"(https://[^"\\]+)', html)
    return m.group(1) if m else None


def pokaz_szczegoly(zbior: dict) -> None:
    """Parametry API i przykłady wywołań leżą w plikach <nazwa>_pa/_pw.json."""
    print(f"\n{zbior['title']}")
    print(f"  id:        {zbior['id']}")
    print(f"  kategoria: {zbior.get('category', '?')}")
    print(f"  odświeża:  {zbior.get('refresh_info', '?')}")
    print(f"  opis:      {(zbior.get('notes') or '')[:200]}")
    print(f"  strona:    https://dane.um.warszawa.pl/pl/catalogue/{zbior['id']}")

    # URL-e plików ze specyfikacją mają prefiks instytucji (np. "bopipk_"),
    # którego nie da się wyprowadzić z pola `name` — trzeba je odczytać
    # ze strony zbioru, gdzie siedzą w polach parameters/call_examples.
    for pole, etykieta in (("parameters", "PARAMETRY"), ("call_examples", "PRZYKŁADY WYWOŁAŃ")):
        url = _url_specyfikacji(zbior["id"], pole)
        if not url:
            continue
        try:
            with urllib.request.urlopen(url, timeout=20) as r:
                dane = json.load(r)
        except Exception:
            continue  # nie każdy zbiór publikuje te pliki
        print(f"\n  --- {etykieta} ---")
        for sekcja in dane if isinstance(dane, list) else []:
            print(f"  {sekcja.get('section_name', '')}")
            for el in sekcja.get("section_elements", []):
                if "name" in el:
                    print(f"    {el['name']:28} {(el.get('description') or '')[:70]}")
                elif "content" in el:
                    print(f"    {el.get('title', '')}")
                    print(f"      {el['content'][:300]}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Przegląda katalog otwartych danych Warszawy")
    ap.add_argument("--kategoria", help="filtruj po kategorii, np. Transport")
    ap.add_argument("--szukaj", help="szukaj w tytule i opisie")
    ap.add_argument("--szczegoly", help="pokaż parametry API dla zbioru o tym id lub nazwie")
    args = ap.parse_args()

    print("Pobieram katalog (bez tokenu) ...")
    try:
        zbiory = pobierz_katalog()
    except Exception as exc:
        print(f"[BŁĄD] Nie udało się pobrać katalogu: {exc}")
        return
    print(f"Zbiorów w katalogu: {len(zbiory)}\n")

    if args.szczegoly:
        szukane = args.szczegoly.lower()
        trafione = [
            z for z in zbiory
            if szukane in z["id"].lower() or szukane in z.get("name", "").lower()
        ]
        if not trafione:
            print(f"Nie znaleziono zbioru: {args.szczegoly}")
            return
        for z in trafione:
            pokaz_szczegoly(z)
        return

    wybrane = zbiory
    if args.kategoria:
        k = args.kategoria.lower()
        wybrane = [z for z in wybrane if k in (z.get("category") or "").lower()]
    if args.szukaj:
        wybrane = [z for z in wybrane if _pasuje(z, args.szukaj)]

    if not wybrane:
        print("Brak zbiorów spełniających kryteria.")
        return

    biezaca = None
    for z in sorted(wybrane, key=lambda x: ((x.get("category") or ""), x["title"])):
        kat = z.get("category") or "?"
        if kat != biezaca:
            biezaca = kat
            print(f"\n=== {kat} ===")
        print(f"  {z['title']:46} {z.get('refresh_info') or '?':12} {z['id']}")

    print(f"\nRazem: {len(wybrane)} zbiorów")
    print("Szczegóły: src/katalog.py --szczegoly <id>")


if __name__ == "__main__":
    main()
