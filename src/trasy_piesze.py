"""Trasy piesze przystanek → toaleta z OSRM (docs/14, krok 8 — próba).

Uruchomienie (z katalogu projektu), potem src/ulotki_dane.py dołącza trasy:
    .venv/Scripts/python.exe src/trasy_piesze.py --dzielnica Ochota
    .venv/Scripts/python.exe src/trasy_piesze.py --wszystkie --serwer http://localhost:5000

Dla każdego słupka bierze KANDYDACI najbliższych toalet w linii prostej,
pyta OSRM (profil pieszy) o odległości do wszystkich naraz (/table), wybiera
najbliższą pieszo i pobiera jej trasę (/route). Dwa zapytania na słupek.

Serwer publiczny FOSSGIS ma limit zapytań (HTTP 429): ok. 12 s na słupek,
więc całe miasto tylko z lokalnym serwerem OSRM w Dockerze (docs/14, krok 8).
Wyniki trafiają do data/cache/trasy_piesze.json; ponowne uruchomienie liczy
tylko brakujące.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

import requests

import waw_api  # noqa: F401 — UTF-8 na konsoli (Windows, cp1251)
from luka_toaletowa import odleglosc_m
from ulotki_dane import wczytaj_dzielnice, wczytaj_przystanki, wczytaj_toalety

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "cache" / "trasy_piesze.json"
OSRM_PUBLICZNY = "https://routing.openstreetmap.de/routed-foot"
KANDYDACI = 10
ODSTEP_PUBLICZNY_S = 1.0  # między zapytaniami do serwera publicznego
UPROSZCZENIE_M = 2.0  # tolerancja upraszczania kształtu trasy

sesja = requests.Session()
sesja.headers["User-Agent"] = "hackaton-warszawa-2026 ulotki-toalety (trasy piesze, jednorazowo)"
ostatnie_zapytanie = 0.0
serwer, odstep_s = OSRM_PUBLICZNY, ODSTEP_PUBLICZNY_S


def osrm(usluga: str, punkty: list[tuple[float, float]], **parametry) -> dict:
    """Zapytanie do OSRM z odstępem odstep_s i 3 próbami. Punkty jako (lat, lon)."""
    global ostatnie_zapytanie
    wsp = ";".join(f"{lon:.6f},{lat:.6f}" for lat, lon in punkty)
    url = f"{serwer}/{usluga}/v1/driving/{wsp}"
    for proba in range(3):
        czekaj = ostatnie_zapytanie + odstep_s - time.monotonic()
        if czekaj > 0:
            time.sleep(czekaj)
        ostatnie_zapytanie = time.monotonic()
        try:
            odp = sesja.get(url, params=parametry, timeout=30)
            dane = odp.json()
            if dane.get("code") == "Ok":
                return dane
            blad = f"{odp.status_code} {dane.get('code')}: {dane.get('message')}"
        except (requests.RequestException, ValueError) as e:
            blad = str(e)
        time.sleep(2 ** proba * 2)
    raise RuntimeError(f"OSRM {usluga}: {blad}")


def uprosc(punkty: list[tuple[float, float]], tolerancja_m: float) -> list[tuple[float, float]]:
    """Douglas–Peucker w metrach (rzut lokalny, wystarczy na kilka km)."""
    if len(punkty) < 3:
        return punkty
    kx = 111_320 * math.cos(math.radians(punkty[0][0]))
    xy = [(lon * kx, lat * 110_540) for lat, lon in punkty]
    zostaw = [False] * len(punkty)
    zostaw[0] = zostaw[-1] = True
    stos = [(0, len(punkty) - 1)]
    while stos:
        a, b = stos.pop()
        (x1, y1), (x2, y2) = xy[a], xy[b]
        dl = math.hypot(x2 - x1, y2 - y1) or 1e-9
        najdalej, idx = 0.0, None
        for i in range(a + 1, b):
            x, y = xy[i]
            d = abs((x2 - x1) * (y1 - y) - (x1 - x) * (y2 - y1)) / dl
            if d > najdalej:
                najdalej, idx = d, i
        if idx is not None and najdalej > tolerancja_m:
            zostaw[idx] = True
            stos += [(a, idx), (idx, b)]
    return [p for p, z in zip(punkty, zostaw) if z]


def policz_slupek(s: dict, toalety: list[dict]) -> dict:
    tu = (s["lat"], s["lon"])
    kandydaci = sorted(toalety, key=lambda t: odleglosc_m(*tu, t["lat"], t["lon"]))[:KANDYDACI]
    cele = [(t["lat"], t["lon"]) for t in kandydaci]

    tabela = osrm("table", [tu, *cele], sources="0", annotations="distance")
    # OSRM liczy od punktu na najbliższej ścieżce — dojście do niej doliczamy
    dojscie = [w["distance"] for w in tabela["destinations"]]
    pieszo = {}
    for i, (lat, lon) in enumerate(cele, start=1):
        d = tabela["distances"][0][i]
        if d is not None:
            pieszo[f"{lat},{lon}"] = round(d + dojscie[0] + dojscie[i])
    if not pieszo:
        raise RuntimeError("brak trasy do żadnej toalety")

    cel = min(pieszo, key=pieszo.get)
    lat, lon = map(float, cel.split(","))
    trasa = osrm("route", [tu, (lat, lon)], overview="full", geometries="geojson")
    ksztalt = [(y, x) for x, y in trasa["routes"][0]["geometry"]["coordinates"]]
    ksztalt = uprosc([tu, *ksztalt, (lat, lon)], UPROSZCZENIE_M)
    return {
        "lat": s["lat"], "lon": s["lon"],
        "pieszo": pieszo,  # "lat,lon" toalety → m pieszo
        "cel": cel,
        "trasa": [[round(y, 5), round(x, 5)] for y, x in ksztalt],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Trasy piesze przystanek → toaleta (OSRM)")
    cel = parser.add_mutually_exclusive_group(required=True)
    cel.add_argument("--dzielnica", help="np. Ochota")
    cel.add_argument("--wszystkie", action="store_true")
    parser.add_argument("--serwer", help="lokalny OSRM, np. http://localhost:5000 (bez limitu zapytań)")
    args = parser.parse_args()
    global serwer, odstep_s
    if args.serwer:
        serwer, odstep_s = args.serwer.rstrip("/"), 0.0
    sys.stdout.reconfigure(line_buffering=True)  # postęp widać też w logu, nie tylko w konsoli

    toalety = wczytaj_toalety()
    przystanki = [
        s for s in wczytaj_przystanki(wczytaj_dzielnice())
        if args.wszystkie or s["dzielnica"] == args.dzielnica
    ]
    if not przystanki:
        sys.exit(f"Nie ma słupków w dzielnicy „{args.dzielnica}”")

    cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}
    zrobione = lambda s: s["id"] in cache and (cache[s["id"]]["lat"], cache[s["id"]]["lon"]) == (s["lat"], s["lon"])  # noqa: E731
    do_zrobienia = [s for s in przystanki if not zrobione(s)]
    print(f"Słupków: {len(przystanki)}, w cache: {len(przystanki) - len(do_zrobienia)}, "
          f"do policzenia: {len(do_zrobienia)} · serwer: {serwer}")

    CACHE.parent.mkdir(parents=True, exist_ok=True)
    zapisz = lambda: CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")  # noqa: E731
    bledy = []
    start = time.time()
    for n, s in enumerate(do_zrobienia, start=1):
        try:
            cache[s["id"]] = policz_slupek(s, toalety)
        except RuntimeError as e:
            bledy.append(s["id"])
            print(f"  {s['id']} {s['nazwa']}: {e}")
        if n % 20 == 0 or n == len(do_zrobienia):
            zapisz()
            print(f"  {n}/{len(do_zrobienia)}  ({time.time() - start:.0f} s)")

    print(f"Gotowe w {time.time() - start:.0f} s, błędów: {len(bledy)} {' '.join(bledy)}")
    print("Teraz: .venv/Scripts/python.exe src/ulotki_dane.py")


if __name__ == "__main__":
    main()
