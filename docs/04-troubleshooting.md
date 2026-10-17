# Troubleshooting

Problemy uporządkowane od najczęstszych. Pierwsze trzy wystąpiły realnie
podczas budowy tego setupu.

---

## `UnicodeEncodeError: 'charmap' codec can't encode character`

**Objaw:** skrypt wywala się na polskim znaku (`ó`, `ł`, `ą`), często zaraz
po pierwszym `print`.

**Przyczyna:** konsola Windows na tej maszynie pracuje w **cp1251**, które
nie zawiera polskich znaków.

**Status: naprawione.** `src/waw_api.py` przestawia `stdout`/`stderr` na UTF-8
przy imporcie. Dlatego **każdy nowy skrypt w tym projekcie powinien
importować `waw_api`** — nawet jeśli nie korzysta z klienta.

Gdyby problem wrócił w skrypcie bez tego importu:

```python
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
```

Albo globalnie dla sesji:

```powershell
$env:PYTHONIOENCODING = "utf-8"
```

---

## Token wklejony, a skrypt mówi „Brak tokenu"

**Najczęstsza pomyłka — wystąpiła realnie 13.10.2026.** Token trafił do
`.env.example` zamiast do `.env`. To dwa różne pliki:

| Plik | Co zawiera | Git |
|---|---|---|
| `.env.example` | **atrapy** (`tu_wklej_swoj_token`) — szablon dla zespołu | śledzony |
| `.env` | **Twój prawdziwy token** | **ignorowany** |

Skrypty czytają **wyłącznie `.env`**. Sprawdź, gdzie wylądował token:

```bash
grep WAW_TOKEN .env .env.example
```

W `.env.example` powinna zostać atrapa. Jeśli wkleiłeś tam prawdziwy token,
przenieś go do `.env` i przywróć atrapę — inaczej klucz trafi do repozytorium
przy pierwszym commicie.

## `Błędny apikey lub jego brak`

Najczęstszy błąd API. Możliwe przyczyny, od najbardziej prawdopodobnej:

1. **`.env` nie istnieje** — `cp .env.example .env` i wklej klucz.
2. **Klucz nie został podmieniony** — w pliku dalej jest `tu_wklej_swoj_apikey`.
   Klient wykrywa ten przypadek i mówi wprost.
3. **Spacje lub cudzysłowy** wokół klucza w `.env`. Poprawnie:
   `WAW_API_KEY=abc-123` — bez cudzysłowów.
4. **Konto nieaktywowane** — sprawdź maila po rejestracji.
5. **Skrypt uruchomiony z innego katalogu** — `.env` jest szukany względem
   katalogu roboczego. Uruchamiaj z katalogu projektu.

> **Uwaga diagnostyczna:** API sprawdza klucz **przed** `resource_id`, więc ten
> sam komunikat dostaniesz przy zupełnie zmyślonym `resource_id`. Dopóki
> klucz jest nieważny, **nie da się odróżnić** błędu klucza od błędu ID.
> Najpierw napraw klucz, potem diagnozuj resztę.

---

## `WawApiError` przy konkretnym zasobie, gdy inne działają

Klucz jest w porządku — problem leży w `resource_id` albo w parametrach.

- **`resource_id` się zmienił.** UM je aktualizuje. Zaloguj się na
  api.um.warszawa.pl i odczytaj aktualny ID z karty zasobu.
- **Brak wymaganego parametru.** `busestrams_get` wymaga `type` (1 lub 2).
  `dbtimetable_get` wymaga `busstopId` i `busstopNr`.
- **Zły parametr identyfikatora.** `busestrams_get` używa `resource_id`,
  pozostałe endpointy używają `id`. To nie jest literówka w dokumentacji.

---

## Puste wyniki bez błędu

`result` to pusta lista. To zwykle nie awaria:

- **Pora dnia.** W nocy jeździ ułamek taboru; między 2 a 4 rano lista potrafi
  być prawie pusta.
- **Filtr `line` na nieistniejącej linii** albo linii aktualnie bez kursów.
- **Awaria po stronie ZTM.** Spróbuj za kilka minut bez filtrów.

---

## `ModuleNotFoundError: No module named 'requests'`

Skrypt poszedł systemowym Pythonem, nie tym z venv.

```bash
.venv/Scripts/python.exe src/sprawdz_setup.py    # tak
python src/sprawdz_setup.py                      # nie (chyba że venv aktywny)
```

---

## `ModuleNotFoundError: No module named 'waw_api'`

Uruchamiasz skrypt spoza `src/` bez ścieżki. Najprościej:

```bash
.venv/Scripts/python.exe src/sprawdz_setup.py
```

W notebooku w `notebooks/`:

```python
import sys; sys.path.append("../src")
from waw_api import WawApi
```

---

## PowerShell nie pozwala aktywować venv

```
... cannot be loaded because running scripts is disabled on this system
```

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Działa tylko w bieżącym oknie — bezpieczne.

---

## Zapytania wiszą albo lecą timeouty

Backend ZTM bywa przeciążony. Klient ma timeout 30 s i 3 próby z narastającym
odstępem — ale **ponawia tylko błędy sieciowe**. Błąd API (zły klucz, zły ID)
jest trwały i nie jest ponawiany, co jest celowe: retry na złym kluczu to
tylko strata czasu.

Jeśli timeouty się powtarzają, zwiększ limit:

```python
api = WawApi(timeout=60)
```

---

## Instalacja `geopandas` trwa wieczność albo pada

Znany ból na Windows — GDAL buduje się ze źródeł. Opcje:

1. **Nie instaluj.** Do rysowania punktów na mapie wystarczy `folium`
   (instalacja w sekundy, bez GDAL).
2. Użyj `pyogrio` zamiast `fiona` jako backendu.
3. Jeśli masz conda: `conda install -c conda-forge geopandas` idzie z binarek.

**Nie zaczynaj tej instalacji w trakcie hackatonu.** Jeśli wiesz, że będą
mapy — zrób to przed.

---

## Zbieracz GPS kończy się sam

Po 10 kolejnych błędach API skrypt przerywa celowo — zwykle znaczy to
nieważny klucz albo dłuższą awarię backendu. Komunikat w konsoli mówi który.
Pojedyncze błędy sieci są tolerowane i nie przerywają zbierania.

---

## `500 — awaria po stronie serwera` / `Service unavailable` (nowy portal)

Dotyczy `dane.um.warszawa.pl` (klasa `WawApiNew`).

**To nie jest problem z Twoim tokenem.** Potwierdzone: ten sam błąd wraca
także przy zapytaniu bez nagłówka `Authorization`, a nieistniejący endpoint
zwraca 404 — więc endpoint istnieje, tylko usługa za nim nie odpowiada.

Co zrobić:

1. Spróbuj ponownie później — awarie bywają przejściowe.
2. Dla danych GPS użyj **starego portalu** `api.um.warszawa.pl` (klasa
   `WawApi`) — serwuje te same pozycje pojazdów i odpowiadał normalnie.
3. Dla pozostałych zbiorów sprawdź, czy strona katalogu na
   dane.um.warszawa.pl nie zgłasza przerwy technicznej.

## `405 Method Not Allowed` (nowy portal)

Wysłałeś GET zamiast POST. Nowy portal przyjmuje **wyłącznie POST**
z parametrami w ciele JSON. Klasa `WawApiNew` robi to poprawnie — ten błąd
zobaczysz tylko przy ręcznym curl/przeglądarce.

## `401` (nowy portal)

Token nieprawidłowy lub brakujący. Token nowego portalu pobierasz z
https://dane.um.warszawa.pl/pl/key-api i **może być inny niż apikey**
starego portalu. W `.env` to osobna zmienna `WAW_TOKEN`.

## Trasy piesze: `429` albo skrypt liczy godzinami (`src/trasy_piesze.py`)

Publiczny serwer OSRM (`routing.openstreetmap.de`) ma limit zapytań i odpowiada
`429 Too Many Requests`. Skrypt ponawia z przerwą, więc wychodzi ok. 12 s na
słupek — całe miasto to ok. 15 h. Do większej liczby słupków postaw lokalny
OSRM w Dockerze i uruchom skrypt z `--serwer http://localhost:5000`
(instrukcja: docs/14, sekcja „Trasy piesze”; całe miasto w 7 minut).

## Docker w Git Bash: `osrm-extract` nie widzi pliku `/data/...`

Git Bash na Windows zamienia ścieżki typu `/data/plik` na `C:/Program
Files/Git/data/plik`. Przed `docker run` ustaw `export MSYS_NO_PATHCONV=1`
albo uruchom polecenia w PowerShellu.

## Docker: `failed to connect to the docker API ... dockerDesktopLinuxEngine`

Docker Desktop nie działa. Uruchom aplikację Docker Desktop (u nas
`%LOCALAPPDATA%\Programs\DockerDesktop\Docker Desktop.exe`) i poczekaj ok.
minuty, aż `docker info` przestanie zgłaszać błąd.
