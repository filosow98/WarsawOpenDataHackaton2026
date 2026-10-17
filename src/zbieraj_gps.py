"""Zbieracz pozycji GPS — buduje historię przed hackatonem.

Dane GPS to migawka "tu i teraz". Jeśli projekt ma pokazywać wzorce w czasie
(punktualność, korki, zagęszczenie o różnych porach), historii nie da się
odtworzyć wstecz — trzeba ją zbierać zawczasu.

Uruchomienie (działa w tle, Ctrl+C kończy):
    .venv/Scripts/python.exe src/zbieraj_gps.py --interval 20

Dane lądują w data/cache/ jako JSON, jeden plik na próbkę.
"""

from __future__ import annotations

import argparse
import time
from datetime import datetime

from waw_api import WawApi, WawApiError, snapshot


def main() -> None:
    parser = argparse.ArgumentParser(description="Zbiera pozycje GPS ZTM do data/cache/")
    parser.add_argument(
        "--interval",
        type=int,
        default=20,
        help="odstęp w sekundach (domyślnie 20; nie schodź poniżej 10)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="ile próbek pobrać; 0 = bez końca",
    )
    parser.add_argument(
        "--tramwaje",
        action="store_true",
        help="zbieraj też tramwaje (domyślnie tylko autobusy)",
    )
    args = parser.parse_args()

    interval = max(args.interval, 10)  # ochrona przed zbyt częstym odpytywaniem

    try:
        api = WawApi()
    except RuntimeError as exc:
        print(f"[BŁĄD] {exc}")
        return

    print(f"Zbieram co {interval}s. Ctrl+C kończy.")
    pobrane = 0
    bledy = 0

    try:
        while args.limit == 0 or pobrane < args.limit:
            stamp = datetime.now().strftime("%H:%M:%S")
            zadania = [("buses", api.buses)]
            if args.tramwaje:
                zadania.append(("trams", api.trams))

            for nazwa, metoda in zadania:
                try:
                    dane = metoda()
                    snapshot(dane, nazwa)
                    print(f"  {stamp}  {nazwa}: {len(dane)} pojazdów")
                    bledy = 0
                except WawApiError as exc:
                    bledy += 1
                    print(f"  {stamp}  [błąd API] {exc}")
                    # Nie przerywamy od razu — API bywa chwilowo niedostępne.
                    if bledy >= 10:
                        print("10 błędów z rzędu — przerywam. Sprawdź klucz.")
                        return
                except Exception as exc:  # sieć padła, DNS, timeout
                    bledy += 1
                    print(f"  {stamp}  [błąd sieci] {exc}")

            pobrane += 1
            time.sleep(interval)
    except KeyboardInterrupt:
        print(f"\nZatrzymano. Zebrano {pobrane} próbek w data/cache/.")


if __name__ == "__main__":
    main()
