# API otwartych danych Warszawy — jak to działa

> **Ten dokument opisuje STARY portal `api.um.warszawa.pl`.**
> Jeśli Twój zbiór pochodzi z linku `dane.um.warszawa.pl/pl/catalogue/...`,
> obowiązuje **nowy** portal i inne zasady — zobacz
> [05-zbiory.md](05-zbiory.md). Oba działają równolegle.

Bazowy URL:

```
https://api.um.warszawa.pl/api/action/<endpoint>/
```

Autoryzacja: parametr `apikey` w query stringu. Brak nagłówków, brak OAuth.

## Status weryfikacji

Rozróżnienie jest istotne, bo bez ważnego klucza nie da się potwierdzić wszystkiego.

| Co | Status |
|---|---|
| Nazwy endpointów (4 poniżej) | **Zweryfikowane** — odpowiadają na żywo (12.10.2026) |
| Format błędu `result:"false"` | **Zweryfikowane** |
| Brak CKAN (`package_list` → 404) | **Zweryfikowane** |
| Kolejność walidacji (klucz przed resource_id) | **Zweryfikowane** |
| Konkretne `resource_id` w tabelach niżej | **Niezweryfikowane** — z dokumentacji i publicznych repo |
| Nazwy pól w odpowiedziach | **Niezweryfikowane** — potwierdź przy pierwszym udanym zapytaniu |

Powód: API sprawdza `apikey` **przed** `resource_id`, więc każde zapytanie bez
ważnego klucza zwraca ten sam błąd — niezależnie od tego, czy ID jest poprawne.
Po zdobyciu klucza uruchom `src/sprawdz_setup.py`, żeby to domknąć.

---

## Endpointy

### `busestrams_get` — pozycje GPS w czasie rzeczywistym

| Parametr | Wymagany | Opis |
|---|---|---|
| `resource_id` | tak | `f2e5503e-927d-4ad3-9500-4ab9e55deb59` |
| `type` | **tak** | `1` = autobusy, `2` = tramwaje |
| `line` | nie | filtr po linii, np. `523` |
| `brigade` | nie | filtr po brygadzie |
| `apikey` | tak | Twój klucz |

Uwaga: `type` jest obowiązkowe — jego pominięcie zwraca błąd, a nie wszystkie pojazdy.
Ten endpoint używa `resource_id`, pozostałe używają `id`.

Oczekiwane pola rekordu: `Lines`, `Lon`, `Lat`, `VehicleNumber`, `Brigade`, `Time`.

```
https://api.um.warszawa.pl/api/action/busestrams_get/?resource_id=f2e5503e-927d-4ad3-9500-4ab9e55deb59&apikey=KLUCZ&type=1&line=523
```

### `dbstore_get` — dane słownikowe i statyczne

Przystanki, parkingi, toalety, defibrylatory itp. Parametr identyfikatora to `id`.

### `dbtimetable_get` — rozkłady jazdy ZTM

| Parametr | Opis |
|---|---|
| `id` | identyfikator zasobu (inny dla listy linii, inny dla odjazdów) |
| `busstopId` | numer przystanku, np. `3072` |
| `busstopNr` | numer słupka, np. `01` |
| `line` | numer linii (dla odjazdów) |

Polskie znaki w parametrze `name` muszą być zakodowane URL-em — `requests`
robi to automatycznie, więc przy użyciu klienta nie jest to problem.

### `wfsstore_get` — warstwy przestrzenne

Geometrie (granice dzielnic, trasy rowerowe, zieleń). Zwraca strukturę
GeoJSON-podobną, nie czysty GeoJSON — sprawdź kształt przed podaniem do `geopandas`.

---

## Resource ID — do potwierdzenia

Te wartości pochodzą z dokumentacji i publicznych projektów. **UM potrafi je
zmieniać.** Jeśli któryś zawiedzie przy ważnym kluczu, aktualny ID jest na
karcie zasobu po zalogowaniu na portalu.

| Zasób | ID | Endpoint |
|---|---|---|
| Pozycje pojazdów GPS | `f2e5503e-927d-4ad3-9500-4ab9e55deb59` | `busestrams_get` |
| Przystanki (słownik) | `ab75c33d-3a26-4342-b36a-6e5fef0a3ac3` | `dbstore_get` |
| Linie na przystanku | `88cd555f-6f31-43ca-9de4-66c479ad5942` | `dbtimetable_get` |
| Rozkład / odjazdy | `e923fa0e-d96c-43f9-ae6e-60518c9f3238` | `dbtimetable_get` |
| Wyszukiwanie przystanku po nazwie | `b27f4c17-5c50-4a5b-89dd-236b282bc499` | `dbtimetable_get` |

Pełny katalog zasobów (powietrze, hałas, rowery, wydarzenia) jest widoczny
po zalogowaniu na https://api.um.warszawa.pl oraz na https://dane.um.warszawa.pl

---

## Trzy pułapki, które kosztują czas

### 1. Błędy przychodzą z kodem HTTP 200

```json
{"result": "false", "error": "Błędny apikey lub jego brak"}
```

`raise_for_status()` **tego nie wykryje** — trzeba sprawdzać pole `result`.
Klient w `src/waw_api.py` robi to i podnosi `WawApiError`.

### 2. To nie jest CKAN

URL-e wyglądają jak CKAN (`/api/action/...`), ale `package_list`,
`datastore_search` czy `package_show` zwracają 404. Przykłady CKAN-owe
z internetu tu nie zadziałają.

### 3. Niejednolite nazwy parametrów

`busestrams_get` używa `resource_id`, a pozostałe endpointy `id`. Łatwo
to pomylić kopiując zapytanie.

---

## Limity

Oficjalny limit zapytań nie jest nigdzie podany. Zdroworozsądkowo:
odpytuj GPS nie częściej niż **co 10–15 sekund** (dane i tak odświeżają się
w tym tempie), a dane statyczne pobierz raz i trzymaj na dysku.
Zbieracz w `docs/03-dane.md` ma wbudowany odstęp.
