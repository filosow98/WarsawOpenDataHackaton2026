# AGENTS.md — instrukcje dla asystentów AI

Wspólny kontekst dla każdego agenta AI pracującego w tym repo (Claude Code,
Codex, Cursor, Copilot i inne). Plik jest w gicie, więc cała drużyna pracuje
na tych samych zasadach. Szczegóły są w [docs/](docs/00-start.md) — tutaj
tylko to, co trzeba wiedzieć zawsze.

## Kontekst

- **Hackaton Otwartych Danych Warszawy**, 17–18.10.2026, 42 Warsaw.
- **Oddanie projektu: niedziela 18.10, godz. 11:00.** Prezentacje 11:30–13:30.
  Łącznie ok. 22 h pracy.
- Wyzwania: **Warszawa 2076** (problemy miasta w perspektywie 50 lat),
  **Złap oddech** (work-life balance, relacja z miastem), **Twój ruch**
  (dowolny projekt na danych miasta).
- Zespół 3–5 osób. Komunikacja i dokumentacja po polsku.

## Decyzje drużyny

Uzupełniamy na bieżąco — to jest źródło prawdy o tym, co robimy.

- **Wyzwanie:** Twój ruch (wyzwanie 3)
- **Temat / pomysł:** wstępnie upał na przystankach — [docs/11-pomysl-przystanki.md](docs/11-pomysl-przystanki.md)
- **Wykorzystane zbiory:** _—_
- **Podział ról:** _—_

## Kryteria jury

Dane Warszawy 20% · innowacyjność **25%** · wdrożenie 20% · związek z realiami
miasta 15% · prezentacja 20%. Każdą propozycję (pomysł, funkcję, slajd)
oceniaj pod kątem tych kryteriów. Pełny opis: [docs/09-kryteria-oceny.md](docs/09-kryteria-oceny.md).

## Zasady pracy

- **Presja czasu.** Wybieraj sprawdzone, proste rozwiązania i gotowy kod
  z `src/`, a nie eksperymenty. Działające demo jest ważniejsze niż
  kompletność.
- **Każdy nowy skrypt importuje `waw_api`** (z `src/`). Moduł ustawia
  UTF-8 na konsoli, bez tego polskie znaki wywalają skrypt na Windows
  (cp1251).
- Łap `WawApiError` z klienta, nie polegaj na `raise_for_status()`.
- **Nie pobieramy pełnych dużych zbiorów** — tylko wycinki potrzebne do
  projektu. Dane do `data/raw/` (źródłowe) i `data/cache/` (snapshoty
  realtime); oba katalogi są poza gitem.
- **Sekrety:** token tylko w `.env`. Nigdy nie wpisuj go do `.env.example`
  ani do kodu — `.env.example` trafia do gita.
- Nowa wiedza o API albo danych (pułapka, działający parametr) → dopisz do
  odpowiedniego pliku w `docs/`, żeby reszta drużyny nie traciła czasu.

## Pułapki API (zweryfikowane)

Są **dwa różne API miasta** — nie myl ich:

| | `api.um.warszawa.pl` (stary) | `dane.um.warszawa.pl` (nowy) |
|---|---|---|
| Metoda | GET | **POST**, parametry w ciele JSON |
| Klucz | `apikey` w URL-u | nagłówek `Authorization` |
| Klasa w `src/waw_api.py` | `WawApi` | **`WawApiNew`** |
| Błędy | **HTTP 200** z `{"result":"false"}` | status HTTP |

- Nowy portal: **HTTP 500 to zwykle błąd walidacji, nie awaria.** Zanim
  uznasz usługę za niedostępną, sprawdź typy i wymagane parametry.
- RCN (`get_bgk_rcn`): `rok` musi być **liczbą** (`2022`, nie `"2022"`);
  wszystkie 4 parametry obowiązkowe; współrzędne w **EPSG:2178**, nie WGS84 —
  przelicz przed naniesieniem na mapę.
- Budżet obywatelski: `status` (`zrealizowane` / `w_realizacji`) jest de facto
  obowiązkowy.
- Odjazdy z przystanku: `line` obowiązkowy.
- GPS pojazdów: zwraca też stare pozycje (nawet z 2024) — **zawsze filtruj po
  `Time`**. Danych GPS nie da się pobrać wstecz.
- Pusty wynik to często `features: null`, a nie błąd.
- To **nie jest CKAN** — `/api/action/package_list` zwraca 404.
- Specyfikacja zbioru: `https://dane.um.warszawa.pl/files/<nazwa>_pa.json`
  (parametry) i `_pw.json` (przykłady) — pewniejsze niż strona HTML.

Więcej: [docs/02-api.md](docs/02-api.md), [docs/04-troubleshooting.md](docs/04-troubleshooting.md).

## Polecenia

Python z venv (Windows: `.venv/Scripts/python.exe`, Mac/Linux: `.venv/bin/python`):

```bash
.venv/Scripts/python.exe src/sprawdz_setup.py               # test połączenia
.venv/Scripts/python.exe src/katalog.py --kategoria Transport  # katalog zbiorów
.venv/Scripts/python.exe src/katalog.py --szczegoly <id>
```

Instalacja od zera: [docs/01-setup.md](docs/01-setup.md).

## Gdzie co jest

```
src/waw_api.py         klient obu API (retry, błędy, snapshot do cache)
src/katalog.py         przeglądarka katalogu 23 zbiorów
src/pobierz_male.py    pobranie 18 małych zbiorów w całości
src/pobierz_rcn.py     przykład: Rejestr Cen Nieruchomości
src/zbieraj_gps.py     zbieracz historii GPS
docs/05-zbiory.md      katalog zbiorów + przykłady wywołań
docs/08-opis-zbiorow.md  co zawiera każdy zbiór (pola, rozmiar)
docs/09-kryteria-oceny.md  kryteria jury
docs/10-problemy.md    propozycje tematów (5 problemów + parkingi)
docs/11-pomysl-przystanki.md  pomysł „Upał na przystankach” (pełny kontekst)
docs/12-upal-na-przystankach.md  bieżąca analiza pomysłu (wersja do przesłania)
docs/13-toalety-przy-przystankach.md  pomysł „Toaleta w zasięgu przystanku” + źródła
data/raw/opis_plikow.json  opis pobranych plików
```
