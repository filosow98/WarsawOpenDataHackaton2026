# Dokumentacja projektu — start

Hackaton Otwartych Danych Warszawy, **17–18.10.2026**, 42 Warsaw.
Deadline oddania projektu: **niedziela 11:00** (nie po południu — to ok. 22 h pracy).

## Od czego zacząć

| Dokument | Kiedy czytać |
|---|---|
| [01-setup.md](01-setup.md) | Teraz — zdobycie klucza i uruchomienie środowiska |
| [02-api.md](02-api.md) | Przed pisaniem zapytań — endpointy, parametry, pułapki |
| [03-dane.md](03-dane.md) | Przy pobieraniu — klient, zbieranie historii, wczytywanie |
| [05-zbiory.md](05-zbiory.md) | **Katalog zbiorów + 3 przykłady** |
| [06-rcn-krok-po-kroku.md](06-rcn-krok-po-kroku.md) | Przykład pobierania od zera (na zbiorze RCN) |
| [04-troubleshooting.md](04-troubleshooting.md) | Gdy coś nie działa |
| [09-kryteria-oceny.md](09-kryteria-oceny.md) | **Przy wyborze tematu i przed prezentacją — jak ocenia jury** |
| [10-problemy.md](10-problemy.md) | **Przy wyborze tematu — 5 propozycji problemów + ocena** |
| [11-pomysl-przystanki.md](11-pomysl-przystanki.md) | Pomysł „Upał na przystankach” — wersja pierwotna, krytyka, wersja po przeróbce, plan |
| [12-upal-na-przystankach.md](12-upal-na-przystankach.md) | **Bieżąca analiza pomysłu „Upał na przystankach” — wersja do przesłania dalej** |
| [13-toalety-przy-przystankach.md](13-toalety-przy-przystankach.md) | Pomysł „Toaleta w zasięgu przystanku” — luka toaletowa, tabliczki, źródła o odwodnieniu seniorów |
| [14-plan-generatora-ulotek.md](14-plan-generatora-ulotek.md) | **Plan aplikacji: generator ulotek „Najbliższa toaleta” + mapa luk** |
| [15-storytelling.md](15-storytelling.md) | **Historia na prezentację + liczby ze źródłami** |
| [16-skrypt-prezentacji.md](16-skrypt-prezentacji.md) | **Skrypt 5-minutowej prezentacji (tekst do powiedzenia + slajdy)** |

## Stan: połączenie działa (13.10.2026)

Token jest w `.env`, a wszystkie cztery sprawdzane zasoby zwracają dane:

```
OK  Lokalizacja pojazdów (autobusy): 1308 rekordów
OK  Lokalizacja pojazdów (tramwaje): 323 rekordy
OK  Linie na przystanku 5070/03: 4 rekordy
OK  Ceny nieruchomości: działa
```

Pobrane 3305 transakcji RCN → `data/cache/rcn_*.json`. To **dane testowe**,
pobrane tylko po to, by potwierdzić, że połączenie działa — temat projektu
nie jest jeszcze wybrany.

Weryfikacja w dowolnym momencie:

```bash
.venv/Scripts/python.exe src/sprawdz_setup.py
```

## Wybór tematu — przeglądanie katalogu

Katalog ma **23 zbiory** (transport, środowisko, zdrowie, sport, nieruchomości,
wydarzenia, aktywność mieszkańców): https://dane.um.warszawa.pl/pl/catalogue

Z terminala, bez tokenu:

```bash
.venv/Scripts/python.exe src/katalog.py --kategoria Transport
.venv/Scripts/python.exe src/katalog.py --szczegoly <id>
```

## Co zostało do zrobienia przed hackatonem

1. **Historia GPS** — jeśli projekt ma pokazywać zmiany w czasie, uruchom
   `src/zbieraj_gps.py` na kilka godzin w szczycie. Tych danych **nie da się
   pobrać wstecz** w sobotę.
2. **Mapy** — jeśli będą potrzebne, doinstaluj `folium` **przed** hackatonem.
   Uwaga: współrzędne w RCN są w układzie metrycznym (nie WGS84) i wymagają
   przeliczenia przed naniesieniem na mapę.
3. **Klucz do starego portalu** (opcjonalnie) — https://api.um.warszawa.pl,
   jako droga zapasowa dla danych GPS.

## Wyzwania

- **Warszawa 2076** — problemy miasta dziś w perspektywie 50 lat
- **Złap oddech** — work-life balance, odzyskiwanie relacji z miastem
- **Twój ruch** — dowolny projekt na otwartych danych

Zespoły 3–5 osób. Pula nagród 18 000 PLN (1. miejsce w wyzwaniu: 4 000 PLN).

Kryteria jury: dane Warszawy 20%, innowacyjność 25%, wdrożenie 20%,
związek z realiami miasta 15%, prezentacja 20% — szczegóły w
[09-kryteria-oceny.md](09-kryteria-oceny.md).

## Dwa API miasta — nie pomyl ich

| | `api.um.warszawa.pl` | `dane.um.warszawa.pl` |
|---|---|---|
| Metoda | GET | **POST** |
| Klucz | `apikey` w URL-u | nagłówek `Authorization` |
| Klasa w kodzie | `WawApi` | **`WawApiNew`** |

Linki `catalogue/...`, od których zaczynaliśmy, należą do **nowego** portalu.

## Trzy pułapki, które już kosztowały czas

1. **Token do `.env`, nie `.env.example`** — ten drugi to szablon trafiający
   do gita. Szczegóły: [04-troubleshooting.md](04-troubleshooting.md).
2. **`rok` w RCN musi być liczbą**, nie tekstem — string daje mylące
   HTTP 500 „Service unavailable". Dokumentacja miasta podaje tu błędny przykład.
3. **Konsola Windows w cp1251** wywala polskie znaki — naprawione w `waw_api.py`,
   dlatego każdy nowy skrypt powinien ten moduł importować.
