# Rejestr Cen Nieruchomości — instrukcja od zera

Dla osoby, która robi to pierwszy raz. Zakłada tylko, że masz otwarty terminal
w katalogu `D:\hackaton Warszawa 2026`.

Odpowiedź na Twoje pytanie „czyli muszę jedynie pobrać klucz i co dalej":
**klucz + wklejenie go do pliku `.env` + uruchomienie jednego skryptu.**
Resztę (zapytanie POST, nagłówki, JSON) obsługuje już gotowy kod.

---

## Krok 1. Pobierz klucz API

1. Wejdź na **https://dane.um.warszawa.pl/pl/key-api**
2. Wpisz dowolny **nick** (jedyne wymagane pole — konta się nie zakłada).
3. Zaznacz akceptację **regulaminu**.
4. Przejdź reCAPTCHA, jeśli się pojawi.
5. Kliknij **„Pobierz klucz API"**.

Klucz to długi ciąg znaków, np. `3f7a9c21-8e45-4b12-...`

> **Skopiuj go od razu w bezpieczne miejsce.** Portal nie ma odzyskiwania
> klucza — przy zgubieniu generujesz nowy.

## Krok 2. Wklej klucz do pliku `.env`

W terminalu, w katalogu projektu:

```bash
cp .env.example .env
```

Otwórz `.env` w edytorze i podmień wartość `WAW_TOKEN`:

```
WAW_TOKEN=3f7a9c21-8e45-4b12-...
```

Zasady, które łatwo przeoczyć:

- **Bez cudzysłowów** i bez spacji wokół `=`.
- Nie zmieniaj nazwy `WAW_TOKEN` — skrypt szuka dokładnie jej.
- `WAW_API_KEY` niżej możesz na razie zostawić — dotyczy drugiego portalu.

Plik `.env` jest w `.gitignore`, więc klucz nie trafi do repozytorium.
**Nie wklejaj go do notebooków ani na slajdy dla jury.**

## Krok 3. Uruchom pobieranie

```bash
.venv/Scripts/python.exe src/pobierz_rcn.py
```

Domyślnie pyta o lokale z rynku pierwotnego na **Mokotowie za 2026**.

> **Uwaga o bieżącym roku:** rejestr opiera się na aktach notarialnych
> wprowadzanych z opóźnieniem. Dla Mokotowa 2026 dane są (3305 transakcji),
> ale dla innych kombinacji bieżący rok bywa pusty.
> Pusty wynik **nie znaczy, że coś zepsułeś**. Żeby automatycznie cofnąć się
> do rocznika, w którym są dane, dodaj `--fallback`:
>
> ```bash
> .venv/Scripts/python.exe src/pobierz_rcn.py --fallback
> ```
>
> Skrypt sprawdzi 2026, potem 2025, 2024... aż do 5 lat wstecz, i powie,
> którego rocznika ostatecznie użył.

Skrypt melduje każdy etap:

```
Krok 1/3: wczytuję token z pliku .env ...
  OK — token wczytany.
Krok 2/3: pytam API o nieruchomoscLokalowa / rynekPierwotny / Bemowo / 2022 ...
  OK — odpowiedź otrzymana.
Krok 3/3: zapisuję i podsumowuję ...
  Zapisano: data/cache/rcn_1760...json
  Liczba rekordów: 142

  Pola w pierwszym rekordzie:
    cena: 485000
    ...
```

Surowa odpowiedź ląduje w `data/cache/` — nie znika po zamknięciu terminala.

## Krok 4. Zmień zapytanie na własne

```bash
.venv/Scripts/python.exe src/pobierz_rcn.py --dzielnica Bemowo --rok 2022
```

| Flaga | Znaczenie | Uwaga |
|---|---|---|
| `--dzielnica` | nazwa dzielnicy | **bez polskich znaków, łącznie**: `pragapolnoc`, nie `Praga-Północ` |
| `--rodzaj` | rodzaj nieruchomości | np. `nieruchomoscLokalowa` |
| `--rynek` | rodzaj rynku | np. `rynekPierwotny`, `rynekWtorny` |
| `--rok` | rok dokumentu | np. `2023` (domyślnie `2026`) |
| `--fallback` | cofaj się rok po roku, aż znajdziesz dane | do 5 lat wstecz |

Dopuszczalne wartości `--rodzaj` i `--rynek` pochodzą z zał. nr 9 do
Rozporządzenia MRPiT z 27.07.2021. Jeśli któraś zwróci pustkę, najpewniej
nazwa jest inna — zacznij od działającego przykładu i zmieniaj po jednym
parametrze.

---

## Co jeśli zobaczysz błąd

### `500 — Service unavailable`

Mylący komunikat: **najczęściej to nie awaria, tylko zły typ parametru.**

`get_bgk_rcn` wymaga, by `rok` był **liczbą**, nie tekstem. Przykład curl
w dokumentacji miasta podaje `"rok": "2022"` (w cudzysłowach) i taki zapis
zwraca 500. Poprawnie: `"rok": 2022`.

Klient (`WawApiNew.ceny_nieruchomosci`) konwertuje to sam, więc przez skrypt
problem nie wystąpi. Zobaczysz go tylko przy ręcznym curl.

Jeśli 500 wraca mimo poprawnych typów — wtedy faktycznie może to być awaria
po stronie miasta. Sprawdź, czy inne endpointy odpowiadają:
`.venv/Scripts/python.exe src/sprawdz_setup.py`

### `Brak tokenu. Ustaw WAW_TOKEN w .env`

Nie wykonałeś kroku 2, albo w `.env` dalej jest `tu_wklej_swoj_token`.

### `401`

Klucz jest, ale API go nie przyjmuje — literówka przy kopiowaniu albo
dodatkowe spacje/cudzysłowy. Wygeneruj nowy i wklej ponownie.

### `ModuleNotFoundError`

Uruchomiłeś systemowym Pythonem. Używaj `.venv/Scripts/python.exe`, nie `python`.

Więcej przypadków: [04-troubleshooting.md](04-troubleshooting.md)

---

## Co dalej z tymi danymi

Zbiór zwraca **GeoJSON** — każdy rekord ma `properties` (cena, data, parametry
lokalu) i geometrię (współrzędne). Do pandas:

```python
import json
from pathlib import Path
import pandas as pd

plik = sorted(Path("data/cache").glob("rcn_*.json"))[-1]
geo = json.loads(plik.read_text(encoding="utf-8"))
rekordy = geo["features"] if isinstance(geo, dict) and "features" in geo else geo

df = pd.DataFrame([r.get("properties", r) for r in rekordy])
print(df.head())
print(df.columns.tolist())
```

Mając współrzędne w GeoJSON-ie, punkty transakcji naniesiesz na mapę
`folium` bez instalowania `geopandas`.

## Ważne przy prezentacji

Licencja tego zbioru jest **inna** niż CC-BY zbiorów ZTM — warunki:
https://mapa.um.warszawa.pl/warunki.html. Podaj źródło danych na slajdzie.

To dane o **rzeczywistych transakcjach z aktów notarialnych**. Nie łącz ich
z danymi osobowymi i nie prezentuj w sposób pozwalający zidentyfikować
konkretną osobę czy mieszkanie.
