# Pobranie katalogu — plan

Źródło: https://dane.um.warszawa.pl/pl/catalogue (23 zbiory, 7 kategorii, stan 13.10.2026).
Zbiory dzielimy na dwa typy, a każdy typ ma osobny skrypt.

## Zanim zaczniesz

1. Token w `.env` działa: `.venv/Scripts/python.exe src/sprawdz_setup.py`
2. Lista zbiorów i parametrów (bez tokenu): `.venv/Scripts/python.exe src/katalog.py`

---

## Typ 1: małe zbiory (18), jedno wywołanie = cały zbiór — **robimy teraz**

Skrypt: `src/pobierz_male.py`. Jedno uruchomienie daje **18 plików JSON**.

```bash
.venv/Scripts/python.exe src/pobierz_male.py
```

| Kategoria | Zbiory |
|---|---|
| Aktywni mieszkańcy | Konsultacje społeczne, Konsultacje dzielnice, Konsultacje kategorie, Trasy turystyczne |
| Sport | Otwarte boiska, Zajęcia sportowe |
| Transport | Pojazdy transportu publicznego, Przystanki, Utrudnienia w ruchu*, Wolne miejsca parkingowe* |
| Wydarzenia | Kalendarz wydarzeń |
| Zdrowie | Defibrylatory AED |
| Środowisko | Eko punkty, Segregacja odpadów, Toalety, Typy odpadów, Jakość powietrza*, Pogoda* |

\* **Realtime.** Plik pokazuje stan z chwili pobrania. Do trendów trzeba pobierać cyklicznie.

Jak działa skrypt:
- Każdy zbiór trafia do osobnego pliku `data/raw/male/<nazwa>.json` (np. `pogoda.json`,
  `defibrylatory_aed.json`, pełna lista: `--lista`). Opis trafia do
  wspólnego pliku `data/raw/opis_plikow.json` (małe i duże zbiory: data pobrania, liczba rekordów, status, parametry).
- Endpointy są wpisane w skrypcie. Spisałem je z oficjalnych plików `call_examples` portalu.
- Błąd jednego zbioru nie przerywa pozostałych. Skrypt zapisuje go w opis_plikow.json i idzie dalej.
- Przy ponownym uruchomieniu nadpisuje pliki, bo te zbiory są małe.

AED bez `defibrillator_id` zwraca wszystkie defibrylatory (potwierdza to dokumentacja portalu).

---

## Typ 2: duże zbiory (5), pętle po parametrach — **na razie NIE pobieramy**

| Zbiór | Po czym trzeba iterować | Skala |
|---|---|---|
| Linie na przystanku | każdy słupek (`zespol`/`slupek` z `przystanki.json`) | ~7 000 wywołań, ok. 1 h przy 2 zapytaniach/s, ok. 7 MB. **Próbka: Centrum i Metro Wierzbno, 16 słupków** |
| Odjazdy linii z przystanku | słupek × linia | dziesiątki tysięcy |
| Rejestr Cen Nieruchomości | dzielnica × rodzaj × rynek × rok | kilkaset wywołań. **Próbka: Śródmieście 2025 pobrana** |
| Budżet obywatelski | `rok` × `status` (oba **obowiązkowe**) | 2 wywołania na rok — **próbka 2025 pobrana** |
| Lokalizacja pojazdów (GPS) | strumień co 10 s, obsługuje go `src/zbieraj_gps.py` | — |

Wrócimy do nich, gdy wybierzemy temat projektu. Wtedy pobierzemy tylko potrzebny wycinek,
np. jedną dzielnicę RCN albo kilka linii. Skrypt `src/pobierz_duze.py` powstanie dopiero wtedy.

Pułapki, gdy do tego dojdzie:
- **RCN:** `rok` podajemy jako **liczbę**, bo wartość w cudzysłowie daje HTTP 500.
  Dzielnice piszemy bez polskich znaków i łącznie (`pragapolnoc`). Gotowy przykład: [06-rcn-krok-po-kroku.md](06-rcn-krok-po-kroku.md).
  **Wszystkie 4 parametry są obowiązkowe.** Działające wartości `rodzajNieruchomosci`: `nieruchomoscLokalowa`,
  `nieruchomoscBudynkowa`, `nieruchomoscGruntowaZabudowana`, `nieruchomoscGruntowaNiezabudowana`.
  Sama `nieruchomoscGruntowa` daje HTTP 500. Brak transakcji to nie błąd: wtedy `features` ma wartość `null`.
  Próbka Śródmieście 2025: lokale z rynku pierwotnego 68 transakcji (0,7 MB), lokale z rynku wtórnego 1343 (14 MB),
  grunty zabudowane z rynku wtórnego 6. Pliki `data/raw/duze/rcn_srodmiescie_2025_*.json`.
  Jedna transakcja to kilka elementów GeoJSON (lokal, budynek, działka), stąd 208 / 4236 / 13 rekordów w plikach.
  Współrzędne są w układzie **PL-2000 strefa 7 (EPSG:2178)**, a nie w GPS. Do mapy trzeba je przeliczyć
  (`pyproj`, EPSG:2178 → EPSG:4326). Pole `tworcaDokumentu` to nazwisko notariusza.
- **Odjazdy:** pełny rozkład lepiej wziąć z GTFS ZTM niż z tysięcy wywołań API.
- **Budżet obywatelski:** wymaga **obu** parametrów: `rok` jako liczby oraz `status`
  (`zrealizowane` albo `w_realizacji`). Bez `status` serwer zwraca HTTP 500, choć dokumentacja
  nie mówi, że to pole jest obowiązkowe.
  Próbka: `data/raw/duze/budzet_obywatelski_2025_*.json` (228 + 61 projektów, zbiory rozłączne).
  Pole `status` w rekordach ma zawsze wartość `5`, więc status projektu trzeba brać z nazwy pliku.
  Pole `votes` jest zawsze równe 0, `lat`/`lng` są puste, a współrzędne leżą w `pins`.
  Rekordy zawierają **imię i nazwisko autora** projektu, o czym trzeba pamiętać przy publikacji.
- **Przystanki:** tabela parametrów na portalu podaje `apikey`, ale działa zwykły token
  i nowe API, tak jak w oficjalnym przykładzie wywołania.
  Odpowiedź ma format `{"values":[{"key":..,"value":..}]}` i trzeba ją spłaszczyć.
  Wszystkie wartości, również współrzędne, są tekstem. `zespol` i `slupek` to `busstopId` i `busstopNr`
  dla linii i odjazdów. Stare API (`dbstore`) zwracało 7421 rekordów, a nowe zwraca 6988.
- **Linie na przystanku:** odpowiedź to `[{"values":[{"key":"linia","value":"174"}]}, ...]`,
  czyli jeden rekord na linię. Próbka: `data/raw/duze/linie_na_przystanku_probka.json`
  (każdy wpis ma `zespol`, `slupek`, `nazwa_zespolu` i surową `odpowiedz`). Linie `N..` są nocne,
  a `ZM..` to zastępcze za metro.
- **Odjazdy:** `line` jest **obowiązkowy**. Bez niego lub z pustym tekstem serwer zwraca HTTP 500,
  a z `"line": "4"` działa (sprawdzone 13.10.2026). Jedno zapytanie = jedna linia na jednym słupku.
  Próbka: `data/raw/duze/odjazdy_metro_wierzbno_3114_03_probka.json` (8 tramwajów, 138 KB).
  Prefiks `trasa` mówi o rodzaju kursu: `TP-`/`TO-` to zwykła trasa (linie 18 i 31, ok. 100 odjazdów na dobę),
  `TD-` i `TZ-` wyglądają na kursy z i do zajezdni. Linie 4, 10, 11, 14, 15, 16 mają tu **tylko**
  takie kursy (7–20 rano), więc „linie na przystanku” wymieniają też linie, które normalnie tędy nie jeżdżą.
  Do analizy rozkładu filtruj po prefiksie `trasa`. `brygada` ma niespójny format (`"3"` i `"015"`).
- **GPS:** jedna migawka jest mała. 13.10 o 23:54 autobusy zajęły 164 KB (1018 rekordów), a tramwaje 45 KB (289).
  W dzień będzie ich więcej, ale i tak ok. 0,5 MB. Duże robi się dopiero zbieranie w czasie:
  co 20 s to ok. 1–3 GB na dobę. Pułapka: API zwraca też **stare pozycje**. W tej migawce
  tylko ok. połowa była świeża (≤ 2 min), a niektóre pochodziły z 2024 roku. **Zawsze filtruj po polu `Time`.**
  Próbki: `data/raw/duze/gps_autobusy_probka.json`, `gps_tramwaje_probka.json`.
