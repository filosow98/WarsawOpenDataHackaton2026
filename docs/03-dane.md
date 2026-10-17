# Pobieranie danych — praktyka

## Podstawowe użycie klienta

Skrypty uruchamiaj z katalogu projektu; `src/` jest na ścieżce importu,
gdy odpalasz plik z tego katalogu.

```python
from waw_api import WawApi, WawApiError, snapshot

api = WawApi()                      # klucz czytany z .env

autobusy = api.buses()              # wszystkie autobusy
linia = api.buses(line="523")       # jedna linia
tramwaje = api.trams()

snapshot(autobusy, "buses")         # zapis do data/cache/buses_<ts>.json
```

Zawsze łap błędy API — pojedyncze zapytanie potrafi paść, gdy backend ZTM
się zatnie:

```python
try:
    dane = api.buses()
except WawApiError as exc:
    print(f"API odmówiło: {exc}")
```

### Zasoby inne niż GPS

```python
przystanki = api.dbstore("ab75c33d-3a26-4342-b36a-6e5fef0a3ac3")
rozklad    = api.dbtimetable("e923fa0e-...", busstopId="3072", busstopNr="01", line="523")
warstwa    = api.wfsstore("<id>")
```

Dowolny endpoint spoza tych metod wywołasz surowo:

```python
api.call("dbstore_get", id="<resource_id>", jakis_parametr="wartosc")
```

---

## Zbieranie historii GPS (zrób to przed hackatonem)

Pozycje pojazdów to migawka. **Historii nie da się pobrać wstecz** — jeśli
projekt ma pokazywać punktualność, korki czy zmienność w ciągu doby,
dane muszą być zbierane zawczasu.

```bash
.venv/Scripts/python.exe src/zbieraj_gps.py --interval 20
```

Opcje:

| Flaga | Znaczenie |
|---|---|
| `--interval N` | odstęp w sekundach (domyślnie 20, minimum wymuszone 10) |
| `--limit N` | ile próbek pobrać; `0` = bez końca |
| `--tramwaje` | zbieraj też tramwaje |

Ctrl+C kończy czysto. Skrypt toleruje chwilowe błędy sieci i przerywa
dopiero po 10 nieudanych próbach z rzędu (zwykle znaczy to zły klucz).

**Ile to waży:** jedna próbka wszystkich autobusów to ok. 0,5–1 MB JSON-a.
Przy `--interval 20` to ~2–3 GB na dobę. Jeśli zbierasz dłużej niż kilka
godzin, zwiększ interwał do 60 s albo skonwertuj do Parquet (niżej).

Sensowny plan: uruchom na 2–3 godziny w szczycie (7–9 lub 16–18) i na
godzinę wieczorem. To wystarczy na pokazanie kontrastu pora szczytu / poza
szczytem, bez zapychania dysku.

---

## Wczytywanie zebranych danych

```python
import json
from pathlib import Path
import pandas as pd

pliki = sorted(Path("data/cache").glob("buses_*.json"))

ramki = []
for p in pliki:
    rekordy = json.loads(p.read_text(encoding="utf-8"))
    df = pd.DataFrame(rekordy)
    df["snapshot_ts"] = int(p.stem.split("_")[-1])   # czas pobrania z nazwy pliku
    ramki.append(df)

dane = pd.concat(ramki, ignore_index=True)
print(dane.shape, dane.columns.tolist())
```

Pole `Time` to czas raportowany przez pojazd, a `snapshot_ts` to moment
pobrania — przy analizie opóźnień to rozróżnienie bywa istotne.

### Konwersja do Parquet

JSON-y puchną. Po zebraniu warto skleić je raz i pracować na jednym pliku:

```python
dane.to_parquet("data/raw/gps_historia.parquet")
dane = pd.read_parquet("data/raw/gps_historia.parquet")   # dużo szybsze
```

Wymaga `pyarrow` (`pip install pyarrow`).

---

## Higiena pracy z danymi

- **Zapisuj surowe odpowiedzi** przed przetwarzaniem. Jeśli transformacja
  okaże się błędna o 3 w nocy, nie chcesz pobierać wszystkiego od nowa.
- **Dane statyczne pobierz raz** (przystanki, geometrie) i trzymaj w `data/raw/`.
  Nie odpytuj ich w pętli.
- **`data/` jest poza gitem.** Jeśli zespół ma dzielić dane, użyj dysku
  współdzielonego — nie commituj gigabajtów.
- **Sprawdź licencję** przed publikacją: warunki korzystania są na
  api.um.warszawa.pl. Zwykle wymagane jest podanie źródła danych —
  warto wrzucić taką notkę na slajd dla jury.
