# Hackaton Otwartych Danych Warszawy — 17–18.10.2026

Setup do pracy z API otwartych danych m.st. Warszawy.

**Pełna dokumentacja: [docs/00-start.md](docs/00-start.md)** —
[setup](docs/01-setup.md) · [API](docs/02-api.md) ·
[pobieranie danych](docs/03-dane.md) · [**katalog zbiorów**](docs/05-zbiory.md) · [**RCN krok po kroku**](docs/06-rcn-krok-po-kroku.md) · [**pobranie całego katalogu**](docs/07-pobierz-wszystko.md) · [**co zawierają zbiory**](docs/08-opis-zbiorow.md) · [**kryteria oceny jury**](docs/09-kryteria-oceny.md) · [troubleshooting](docs/04-troubleshooting.md)

## Stan: działa (13.10.2026)

Token jest w `.env`, połączenie z nowym portalem potwierdzone.
Sprawdzenie w dowolnym momencie:

```bash
.venv/Scripts/python.exe src/sprawdz_setup.py
```

Jeśli konfigurujesz od nowa (inny komputer, nowy token):

1. Pobierz token z https://dane.um.warszawa.pl/pl/key-api (wystarczy nick, bez konta).
2. `cp .env.example .env` i wklej token do `WAW_TOKEN` **w pliku `.env`**,
   nie w `.env.example` — ten drugi trafia do gita.
3. `.venv/Scripts/python.exe src/sprawdz_setup.py`

## Instalacja (już wykonana)

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
```

Rdzeń (`requests`, `pandas`, `python-dotenv`, `tenacity`) jest zainstalowany.
Pakiety do map (`geopandas`, `folium`, `jupyterlab`) doinstaluj, gdy będą potrzebne —
`geopandas` potrafi się długo budować.

## Użycie

```python
from waw_api import WawApi, snapshot

api = WawApi()
autobusy = api.buses(line="523")   # pozycje GPS, odświeżane co ~10 s
snapshot(autobusy, "buses")        # zapis do data/cache/ — dane realtime nie wracają
```

## Pułapki API (zweryfikowane)

- **Błędy przychodzą z HTTP 200** jako `{"result":"false","error":"..."}`.
  `raise_for_status()` ich nie wykryje — klient sprawdza pole `result`.
- **To nie jest CKAN**, mimo podobnych URL-i — `/api/action/package_list` zwraca 404.
- `resource_id` bywają zmieniane przez UM. Jeśli zasób przestanie działać,
  aktualny ID jest na karcie zasobu na portalu.
- Dane GPS są chwilowe — zbieraj je do `data/cache/` **przed** hackatonem,
  jeśli projekt ma pokazywać trendy w czasie.

## Struktura

```
src/waw_api.py        klient API (retry, obsługa błędów, cache)
src/sprawdz_setup.py  test dymny — uruchom po wklejeniu klucza
src/zbieraj_gps.py    zbieracz historii GPS (uruchom przed hackatonem)
src/katalog.py        przegladarka katalogu 23 zbiorow (bez tokenu)
src/pobierz_rcn.py    przyklad pobierania (Rejestr Cen Nieruchomosci)
docs/                 dokumentacja: setup, API, dane, troubleshooting
data/raw/             pobrane dane źródłowe (poza gitem)
data/cache/           snapshoty danych realtime (poza gitem)
notebooks/            eksploracja
```
