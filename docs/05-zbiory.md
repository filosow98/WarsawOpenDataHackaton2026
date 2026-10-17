# Zbiory danych — katalog i trzy przykłady

Pełny katalog: **https://dane.um.warszawa.pl/pl/catalogue** — 23 zbiory
w 7 kategoriach. Przeglądasz go też z terminala, **bez tokenu**:

```bash
.venv/Scripts/python.exe src/katalog.py                     # wszystkie
.venv/Scripts/python.exe src/katalog.py --kategoria Transport
.venv/Scripts/python.exe src/katalog.py --szukaj powietrze
.venv/Scripts/python.exe src/katalog.py --szczegoly <id>    # parametry API
```

`--szczegoly` wypisuje oficjalne parametry wywołania i odpowiedzi dla
dowolnego zbioru — to samo źródło, z którego pochodzą opisy niżej.

Trzy zbiory opisane niżej to **przykłady użyte do sprawdzenia połączenia**,
nie wybór tematu projektu. Jeden token obsługuje wszystkie zbiory z tego portalu.

## Co jest w katalogu (stan 13.10.2026)

**Aktywni mieszkańcy**

- Budżet obywatelski — odświeżanie: Tygodniowo
- Konsultacje społeczne — odświeżanie: 2 godziny
- Konsultacje społeczne dzielnice — odświeżanie: 2 godziny
- Konsultacje społeczne kategorie — odświeżanie: 2 godziny
- Trasy turystyczne — odświeżanie: ?

**Nieruchomości**

- Rejestr Cen Nieruchomości — odświeżanie: codziennie

**Sport**

- Otwarte boiska — odświeżanie: Tygodniowo
- Zajęcia sportowe — odświeżanie: 2 godziny

**Transport**

- Linie dostepne na przystanku — odświeżanie: codziennie
- Lokalizacja pojazdów komunikacji miejskiej — odświeżanie: 10 sekund
- Lokalizacja przystanków komunikacji miejskiej — odświeżanie: codziennie
- Odjazdy linii z przystanku — odświeżanie: codziennie
- Pojazdy transportu publicznego — odświeżanie: codziennie
- Utrudnienia w ruchu drogowym — odświeżanie: 1 minuta
- Wolne miejsca parkingowe — odświeżanie: 1 minuta

**Wydarzenia**

- Kalendarz wydarzeń — odświeżanie: 2 godziny

**Zdrowie**

- Lokalizacja defibrylatorów (AED) — odświeżanie: codziennie

**Środowisko**

- Eko punkty — odświeżanie: Tygodniowo
- Monitoring jakości powietrza — odświeżanie: 10 minut
- Pogoda — odświeżanie: 10 minut
- Segregacja odpadów — odświeżanie: codziennie
- Toalety — odświeżanie: Tygodniowo
- Typy odpadów — odświeżanie: codziennie

Szczegółowe parametry dowolnego z nich: `src/katalog.py --szczegoly <id>`.

## Dwa różne API miasta

| | Stary (`api.um.warszawa.pl`) | **Nowy (`dane.um.warszawa.pl`)** |
|---|---|---|
| Metoda | GET | **POST** (GET → 405) |
| Klucz | `apikey` w query | **nagłówek `Authorization`** |
| Parametry | w URL-u | **w ciele JSON** |
| Wybór zasobu | `resource_id` | **nazwa endpointu** |
| Błędy | HTTP 200 + `result:"false"` | **status HTTP (401/404/500)** |
| Klucz z | api.um.warszawa.pl | **dane.um.warszawa.pl/pl/key-api** |

Zbiory z `dane.um.warszawa.pl/pl/catalogue/...` obsługuje klasa `WawApiNew`.

---

## Przykład 1. Lokalizacja pojazdów komunikacji miejskiej

`f319f602-...` · odświeżanie **co 10 sekund** · CC-BY · ZTM

Endpoint: `get_ztm_lokalizacja_pojazdow`

| Parametr | Typ | Opis |
|---|---|---|
| `type` | int | `1` = autobus, `2` = tramwaj |

Pola odpowiedzi: `Lat`, `Lon`, `Time` (czas sygnału GPS), `Lines`,
`Brigade`, `VehicleNumber`.

```python
from waw_api import WawApiNew
api = WawApiNew()
autobusy = api.lokalizacja_pojazdow(1)
tramwaje = api.lokalizacja_pojazdow(2)
```

> Drobna niespójność w dokumentacji miasta: tabela parametrów nazywa to pole
> `typ`, a przykłady curl i Swagger używają `type`. Klient wysyła **`type`**,
> zgodnie ze Swaggerem.

## Przykład 2. Linie dostępne na przystanku

`8eb065b6-...` · aktualizacja codzienna · CC-BY · ZTM

Endpoint: `get_ztm_lista_linii_na_przystanku`

| Parametr | Typ | Opis |
|---|---|---|
| `busstopId` | string | identyfikator przystanku, np. `"5070"` |
| `busstopNr` | string | numer słupka, np. `"03"` |

Odpowiedź ma zagnieżdżony kształt — lista obiektów `{"values":[{"value":"23",
"key":"linia"}]}`. Spłaszczenie:

```python
surowe = api.linie_na_przystanku("5070", "03")
linie = [v["value"] for rek in surowe for v in rek["values"] if v["key"] == "linia"]
```

Zbiór jest powiązany z „Lokalizacją przystanków" i „Odjazdami linii z przystanku" —
żeby dostać `busstopId`, potrzebujesz najpierw zbioru przystanków.

## Przykład 3. Rejestr Cen Nieruchomości

`2db4f9f9-...` · aktualizacja codzienna · Biuro Geodezji i Katastru

Endpoint: `get_bgk_rcn`

| Parametr | Typ | Opis |
|---|---|---|
| `dzielnica` | string | **bez polskich znaków, łącznie**, np. `pragapolnoc` |
| `rodzajNieruchomosci` | string | np. `nieruchomoscLokalowa` |
| `rodzajRynku` | string | np. `rynekPierwotny` |
| `rok` | int | rok sporządzenia dokumentu |

Zwraca **GeoJSON** (nie płaską listę) — dane transakcyjne z aktów notarialnych
siedzą w `properties`. Słownik wartości `rodzajNieruchomosci` / `rodzajRynku`
pochodzi z zał. nr 9 do Rozporządzenia MRPiT z 27.07.2021 (ewidencja gruntów
i budynków).

```python
geo = api.ceny_nieruchomosci("Bemowo", "nieruchomoscLokalowa", "rynekPierwotny", 2022)
```

Instrukcja krok po kroku dla tego zbioru: [06-rcn-krok-po-kroku.md](06-rcn-krok-po-kroku.md)

Licencja tego zbioru jest inna niż CC-BY zbiorów ZTM —
warunki: https://mapa.um.warszawa.pl/warunki.html

---

## Status weryfikacji

**Potwierdzone na żywo (13.10.2026):** wszystkie trzy endpointy istnieją
(zmyślona nazwa daje 404, te trzy nie), przyjmują wyłącznie POST, a parametry
powyżej pochodzą z oficjalnych plików specyfikacji portalu — nie ze zgadywania.

**Potwierdzone działanie (13.10.2026):** wszystkie trzy przykładowe zbiory
zwracają realne dane. RCN dla Mokotowa 2026 → 3305 transakcji (dane testowe,
pobrane wyłącznie do weryfikacji połączenia).

**Rozwiązana zagadka HTTP 500:** `get_bgk_rcn` zwracał „Service unavailable"
nie z powodu awarii, tylko dlatego, że parametr `rok` był wysyłany jako
**string**. Przykład curl w dokumentacji miasta podaje `"rok": "2022"` —
i ten zapis nie działa. Musi być liczba: `"rok": 2022`. Klient robi
`int(rok)` automatycznie.

### Co to znaczy dla Ciebie

To jest **ryzyko do przetestowania przed sobotą**, nie powód do paniki —
usługa może wrócić w każdej chwili. Ale sprawdź to wcześnie:

1. Pobierz token z https://dane.um.warszawa.pl/pl/key-api
2. Uruchom `src/sprawdz_setup.py` — sprawdza oba portale naraz
3. Jeśli nowy portal nadal daje 500, a potrzebujesz GPS — **stary portal
   `api.um.warszawa.pl` serwuje te same dane** i odpowiadał normalnie.
   Klasa `WawApi` jest gotowa.

Dla GPS masz więc zapasową drogę. Dla cen nieruchomości i linii na przystanku
odpowiednika w starym API nie potwierdziłem — jeśli projekt ma na nich stać,
zweryfikuj dostępność jak najszybciej i miej plan B.
