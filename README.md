# Hackaton Otwartych Danych Warszawy — 17–18.10.2026

Setup do pracy z API otwartych danych m.st. Warszawy.

**Pełna dokumentacja: [docs/00-start.md](docs/00-start.md)** —
[setup](docs/01-setup.md) · [API](docs/02-api.md) ·
[pobieranie danych](docs/03-dane.md) · [**katalog zbiorów**](docs/05-zbiory.md) · [**RCN krok po kroku**](docs/06-rcn-krok-po-kroku.md) · [**pobranie całego katalogu**](docs/07-pobierz-wszystko.md) · [**co zawierają zbiory**](docs/08-opis-zbiorow.md) · [**kryteria oceny jury**](docs/09-kryteria-oceny.md) · [troubleshooting](docs/04-troubleshooting.md)

## Uruchomienie strony z ulotkami i mapą luk

Projekt: ulotki „Najbliższa toaleta” na przystankach + mapa luk toaletowych
(plan: [docs/14](docs/14-plan-generatora-ulotek.md)). Strona jest w `app/`,
dane w `app/dane/` są już w repo.

**Stronę trzeba uruchomić przez serwer.** Otwarta z dysku (podwójne kliknięcie
`index.html`, adres `file:///...`) nie wczyta danych, bo przeglądarka blokuje
wtedy pliki JSON.

Z katalogu projektu, przez [uv](https://docs.astral.sh/uv/):

```bash
uv run python -m http.server 8000 --directory app
```

albo bez uv:

```bash
.venv/Scripts/python.exe -m http.server 8000 -d app   # Mac/Linux: .venv/bin/python
```

Potem otwórz:

- http://localhost:8000 — podgląd i druk ulotki dla wybranego przystanku,
- http://localhost:8000/mapa.html — mapa luk (słupki bez toalety w zasięgu).

Serwer to biblioteka standardowa Pythona, nie wymaga instalacji pakietów.

### Przeliczenie danych i druk wsadowy

Jednorazowa instalacja (uv):

```bash
uv venv
uv pip install -r requirements.txt
uv run python -m playwright install chromium   # tylko do druku wsadowego
```

Polecenia:

```bash
uv run src/ulotki_dane.py                       # przelicza app/dane/*.json
uv run src/ulotki_pdf.py --id 7013-01,7016-02   # wybrane słupki → data/out/ulotki/wybrane.pdf
uv run src/ulotki_pdf.py --dzielnica Wola       # jedna dzielnica → data/out/ulotki/Wola.pdf
uv run src/ulotki_pdf.py --wszystkie            # całe miasto, plik na dzielnicę + spis.csv
```

Bez uv: te same skrypty przez `.venv/Scripts/python.exe src/...`.

**Druk powyżej 60 ulotek wymaga klucza MapTiler** (regulamin serwerów map OSM
zabrania masowego pobierania). Załóż darmowe konto na
https://cloud.maptiler.com i wpisz klucz do `.env` jako `MAPTILER_KEY=...`
(nie do `.env.example`).

**Nie działa?**

- Pusta strona albo komunikat „Strona otwarta z dysku” — otwórz przez
  `http://localhost:8000`, nie z pliku.
- W terminalu serwera `GET /dane/ulotki.json ... 404` — serwer nie został
  uruchomiony z `--directory app`.
- Używasz Live Server w VS Code — otwórz `/app/index.html`.

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
src/ulotki_dane.py    dane ulotek i mapy luk → app/dane/
src/ulotki_pdf.py     druk wsadowy ulotek do PDF → data/out/ulotki/
app/                  strona: index.html (ulotka), mapa.html (mapa luk), druk.html
docs/                 dokumentacja: setup, API, dane, troubleshooting
data/raw/             pobrane dane źródłowe (poza gitem)
data/cache/           snapshoty danych realtime (poza gitem)
notebooks/            eksploracja
```
