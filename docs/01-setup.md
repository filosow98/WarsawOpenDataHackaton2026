# Setup — od zera do pierwszych danych

Stan środowiska na 12.10.2026: Python 3.12.5, Node 24.18, git 2.45 — wszystko obecne.
Venv (`.venv/`) jest utworzony, rdzeń zależności zainstalowany.

---

## Krok 1. Klucz API (jedyny ręczny krok)

1. Wejdź na https://api.um.warszawa.pl
2. Zarejestruj konto (zakładka logowania w prawym górnym rogu).
3. Po aktywacji klucz znajdziesz w profilu użytkownika.

> **Zrób to możliwie wcześnie.** Jeśli aktywacja konta wymaga potwierdzenia
> mailowego lub ręcznej akceptacji, oczekiwanie w sobotę rano kosztuje
> godziny z 22-godzinnego budżetu hackatonu.

## Krok 2. Wklej klucz

```bash
cp .env.example .env
```

Otwórz `.env` i podmień wartość:

```
WAW_API_KEY=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

`.env` jest w `.gitignore` — klucz nie trafi do repozytorium. **Nie commituj go**
i nie wklejaj do notebooków, które pokażesz jury.

## Krok 3. Weryfikacja

```bash
.venv/Scripts/python.exe src/sprawdz_setup.py
```

Oczekiwany wynik:

```
[1/2] Pozycje pojazdów w czasie rzeczywistym...
  OK  autobusy: 1487 pojazdów
      linia 523 @ 52.2319, 21.0067
  OK  tramwaje: 312 pojazdów
[2/2] Zasoby statyczne...
  OK  Przystanki ZTM (dbstore): 7421 rekordów
```

Jeśli widzisz `FAIL` — zajrzyj do [04-troubleshooting.md](04-troubleshooting.md).

---

## Instalacja od zera (gdyby trzeba było odtworzyć)

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install --upgrade pip
.venv/Scripts/python.exe -m pip install requests python-dotenv pandas tenacity
```

### Pakiety opcjonalne — instaluj świadomie

`requirements.txt` zawiera też `geopandas`, `folium`, `matplotlib`, `jupyterlab`.
**Nie są zainstalowane**, bo `geopandas` ciągnie zależności geoprzestrzenne (GDAL)
i na Windows potrafi się budować kilkanaście minut.

Doinstaluj dopiero, gdy wiesz, że robisz mapy — i **zrób to przed hackatonem**,
nie o 2 w nocy:

```bash
.venv/Scripts/python.exe -m pip install geopandas folium matplotlib jupyterlab
```

Lżejsza alternatywa dla map, bez GDAL: `folium` sam w sobie wystarcza do
rysowania punktów i warstw na mapie i instaluje się w kilka sekund.

---

## Uruchamianie skryptów

Zawsze przez interpreter z venv, nie przez gołe `python`:

```bash
.venv/Scripts/python.exe src/sprawdz_setup.py
```

Albo aktywuj venv na stałe w sesji:

```powershell
.venv\Scripts\Activate.ps1   # PowerShell
```

Jeśli PowerShell zablokuje aktywację (`execution policy`):

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

---

## Struktura projektu

```
src/waw_api.py          klient API — retry, obsługa błędów, snapshoty
src/sprawdz_setup.py    test dymny
data/raw/               dane źródłowe (poza gitem)
data/cache/             snapshoty realtime (poza gitem)
notebooks/              eksploracja
docs/                   ta dokumentacja
.env                    klucz API (poza gitem)
```
