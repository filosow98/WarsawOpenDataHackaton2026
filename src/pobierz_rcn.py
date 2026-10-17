"""Rejestr Cen Nieruchomości — pierwsze pobranie krok po kroku.

Uruchomienie (z katalogu projektu):
    .venv/Scripts/python.exe src/pobierz_rcn.py

Domyślnie pobiera lokale z rynku pierwotnego na Bemowie za 2022 — to przykład
z oficjalnej dokumentacji, więc dobry punkt startowy do sprawdzenia, czy
połączenie w ogóle działa.

Własne zapytanie:
    .venv/Scripts/python.exe src/pobierz_rcn.py --dzielnica Mokotow --rok 2026
"""

from __future__ import annotations

import argparse
import json

from waw_api import WawApiError, WawApiNew, snapshot


def _rekordy(dane):
    """Wyciąga listę rekordów. Zbiór zwraca GeoJSON, ale bywa też goła lista."""
    if isinstance(dane, dict) and "features" in dane:
        return dane["features"]
    if isinstance(dane, list):
        return dane
    return []


def _ile_rekordow(dane) -> int:
    return len(_rekordy(dane))


def main() -> None:
    parser = argparse.ArgumentParser(description="Pobiera dane z Rejestru Cen Nieruchomości")
    parser.add_argument(
        "--dzielnica",
        default="Mokotow",
        help="bez polskich znaków i łącznie, np. pragapolnoc (domyślnie: Mokotow)",
    )
    parser.add_argument("--rodzaj", default="nieruchomoscLokalowa", help="rodzaj nieruchomości")
    parser.add_argument("--rynek", default="rynekPierwotny", help="rodzaj rynku")
    parser.add_argument("--rok", default="2026", help="rok sporządzenia dokumentu")
    parser.add_argument(
        "--fallback",
        action="store_true",
        help="jeśli dla podanego roku nie ma danych, cofaj się rok po roku (do 5 lat wstecz)",
    )
    args = parser.parse_args()

    print("Krok 1/3: wczytuję token z pliku .env ...")
    try:
        api = WawApiNew()
    except RuntimeError as exc:
        print(f"  [STOP] {exc}")
        print("  Zobacz docs/06-rcn-krok-po-kroku.md, sekcja 'Krok 1'.")
        return
    print("  OK — token wczytany.")

    # Rejestr opiera się na aktach notarialnych, które trafiają do bazy
    # z opóźnieniem — bieżący rok bywa pusty lub niekompletny.
    lata = [str(args.rok)]
    if args.fallback:
        lata += [str(int(args.rok) - i) for i in range(1, 6)]

    dane = None
    uzyty_rok = None
    for rok in lata:
        print(
            f"Krok 2/3: pytam API o {args.rodzaj} / {args.rynek} / "
            f"{args.dzielnica} / {rok} ..."
        )
        try:
            odp = api.ceny_nieruchomosci(args.dzielnica, args.rodzaj, args.rynek, rok)
        except WawApiError as exc:
            print(f"  [STOP] {exc}")
            if "500" in str(exc):
                print(
                    "  To awaria po stronie miasta, nie Twój błąd — token tego nie naprawi.\n"
                    "  Spróbuj ponownie później. Szczegóły: docs/04-troubleshooting.md"
                )
            return
        except Exception as exc:
            print(f"  [STOP] [{type(exc).__name__}] {exc}")
            return

        if _ile_rekordow(odp) > 0:
            dane, uzyty_rok = odp, rok
            print("  OK — odpowiedź z danymi.")
            break

        print(f"  Pusto dla roku {rok}.")
        dane, uzyty_rok = odp, rok

    if uzyty_rok != str(args.rok):
        print(f"  (użyto roku {uzyty_rok} zamiast {args.rok})")

    print("Krok 3/3: zapisuję i podsumowuję ...")
    sciezka = snapshot(dane, "rcn")

    # Dane opisowe siedzą w features[i]["properties"].
    rekordy = _rekordy(dane)
    if not rekordy and not isinstance(dane, (list, dict)):
        print(f"  Nieoczekiwany kształt odpowiedzi: {type(dane).__name__}")

    print(f"  Zapisano: {sciezka}")
    print(f"  Liczba rekordów: {len(rekordy)}  (rok {uzyty_rok})")

    if rekordy:
        pierwszy = rekordy[0]
        props = pierwszy.get("properties", pierwszy) if isinstance(pierwszy, dict) else {}
        print("\n  Pola w pierwszym rekordzie:")
        for klucz, wartosc in list(props.items())[:15]:
            print(f"    {klucz}: {str(wartosc)[:60]}")
        print("\n  Pełny pierwszy rekord (fragment):")
        print("   ", json.dumps(pierwszy, ensure_ascii=False)[:400])
    else:
        print(
            f"  Brak rekordów dla roku {uzyty_rok}.\n"
            "  Rejestr opiera się na aktach notarialnych wprowadzanych z opóźnieniem,\n"
            "  więc bieżący rok bywa pusty. Spróbuj starszego rocznika:\n"
            f"    .venv/Scripts/python.exe src/pobierz_rcn.py "
            f"--dzielnica {args.dzielnica} --fallback"
        )


if __name__ == "__main__":
    main()
