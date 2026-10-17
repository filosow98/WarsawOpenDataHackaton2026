# Pomysł: upał na przystankach („Upał w podróży”)

Kontekst do pracy nad jednym projektem. Plik zbiera:

- pierwotną wersję pomysłu,
- krytykę wobec kryteriów jury i realiów zarządzania miastem,
- wersję po przeróbce, którą rekomendujemy,
- plan pracy i otwarte pytania.

Stan: 17.10.2026. **Wyzwanie: Twój ruch (wyzwanie 3).** Pomysł jest wstępnie
wybrany, decyzje trafiają do sekcji „Decyzje drużyny” w [AGENTS.md](../AGENTS.md).

Oryginalny opis pomysłu: [pomysł-z-przystankami.txt](pomysł-z-przystankami.txt).

---

## 1. Wersja pierwotna (przed przeróbką)

**Kluczowa obserwacja:** potrzeba cienia i potencjał fotowoltaiki (PV) to ten
sam wskaźnik, czyli nasłonecznienie. Przystanek, który najbardziej potrzebuje
zadaszenia, jest też najlepszym miejscem na panel.

**Co robimy:**

1. Bierzemy lokalizacje przystanków.
2. Nakładamy budynki, ich wysokości i drzewa.
3. Symulujemy ruch słońca i liczymy godziny bezpośredniego słońca na każdym przystanku.
4. Pokazujemy wynik na mapie.

**Mapa pokazuje trzy rzeczy:**

- potrzebę cienia (latem, w szczycie),
- potencjał PV (w skali roku),
- ranking priorytetów: gdzie wiata z panelem daje największy efekt.

**Dane według pierwotnego pomysłu:** przystanki z GTFS ZTM, budynki z OSM albo
z LiDAR-u GUGiK, pozycja słońca z obliczeń astronomicznych.

**Dla kogo:** miasto i ZTM, firmy PV i producenci wiat, mieszkańcy (jako
argument w budżecie obywatelskim).

**Ryzyka wskazane w samym pomyśle:**

- drzewa są słabo opisane w danych,
- nie wiadomo, kto miałby zapłacić za prąd z wiaty,
- ruch pasażerów zmienia priorytety.

---

## 2. Krytyka

### Co jest dobre

- **Pomysł jest nowy w Warszawie.** Istnieją mapy nasłonecznienia dachów
  (projekt miasta „Cities on Power”), ale nikt nie liczył tego dla
  przystanków. To mocny punkt w innowacyjności, która waży 25%.
- **Bardzo dobrze się prezentuje.** Mapa z cieniami robi wrażenie, a to
  kryterium prezentacji (20%).
- **Rozwiązuje bieżący problem miasta** i łączy się z naszym problemem nr 2
  z [10-problemy.md](10-problemy.md): tramwaje bez klimatyzacji.
- **Jest konkretny moment decyzji** (szczegóły w sekcji 3): miasto w ciągu
  1–2 lat przygotuje nowy przetarg na wiaty.

### Słabości wersji pierwotnej

1. **Z danych miasta jest tylko lista przystanków.** Budynki, drzewa i słońce
   pochodzą spoza portalu, więc kryterium „dane Warszawy” (20%) wypada słabo.
   GTFS jest zbędny, bo przystanki są w portalu.
2. **Nie wiemy, które przystanki mają wiatę.** Zbiór przystanków ma tylko
   zespół, słupek, nazwę, `id_ulicy` i współrzędne. Wiat jest ok. 1640, a
   słupków 6988. Bez tej informacji nie powiemy uczciwie „tu brakuje
   zadaszenia”.
3. **Fotowoltaika słabo pasuje do realiów miasta.**
   - Dach wiaty to najwyżej ok. 1 kWp, czyli ok. 1000 kWh rocznie. To nie jest
     historia o inwestycji.
   - Wiaty buduje i utrzymuje AMS w ramach koncesji reklamowej, więc pytanie
     „kto płaci za prąd” nie jest problemem miasta.
4. **Drzewa są największym źródłem błędu.** Miasto prowadzi inwentaryzację
   drzew w serwisie mapowym, ale nie udostępnia jej jako otwartych danych.
   Bez drzew liczymy tylko cień budynków, więc wynik jest zawyżony.
5. **Cały projekt stoi na jednym trudnym elemencie: symulacji cienia.** Jeśli
   nie zadziała do rana, nie ma czego pokazać.
6. **Plik pomysłu jest ogólnikowy.** Ma termin „do środy 21.10”, czyli po
   deadlinie, i pyta, czy to projekt komercyjny. Nie był pisany pod ten
   hackaton.

### Słabości pierwszej przeróbki (wzór „słońce × kursy × tabor”)

7. **Wzór premiuje przystanki, na których czeka się najkrócej.** Czas
   w słońcu jednej osoby to mniej więcej połowa odstępu między kursami. Przy
   kursie co 3 minuty nikt nie czeka 8 minut. Mnożenie przez liczbę kursów
   wypycha na szczyt węzły z najkrótszym czekaniem, a hasło „czekasz 8 minut”
   pasuje do przystanków na obrzeżach, które wzór spycha w dół. Uczciwa miara
   (liczba pasażerów × średnie czekanie) wymaga liczby pasażerów, której nie
   mamy.
8. **Ranking nie mówi, czy wiatę da się postawić.** O lokalizacji wiaty
   decydują szerokość chodnika, sieci pod ziemią, ruch pieszy i zgoda
   zarządcy drogi, a rzadko słońce. Urzędnik zapyta: „a czy tam jest
   miejsce?”.
9. **Wiata to nie to samo co cień.** Dachy warszawskich wiat są z pleksi
   i nagrzewają się w upale. Na pojedynczych wiatach jest już rozchodnik
   (sedum). W Krakowie zmierzono do 5°C różnicy między wiatą z zielonym
   dachem a zwykłą. Pytanie „jaki dach” jest równie ważne jak „czy wiata”.
10. **Liczby taboru wymagają sprawdzenia.** W naszych danych jest 797
    tramwajów, a według stanu z lutego 2025 tabor to ok. 600 pojazdów (434
    niskopodłogowe + 165 wysokopodłogowych). Portal liczy pewnie osobno każdy
    wagon składu 105Na (jeżdżą parami). Wtedy „44% bez klimy” to udział
    wagonów, nie kursów.
11. **Pogoda ZOM to migawka z października.** Nie wnosi nic do analizy,
    a jury zobaczy, że jest dekoracją. Nie liczymy jej jako „wykorzystanych
    danych”.

### Ocena wobec kryteriów jury (szacunki, 1–5)

Kryteria są te same we wszystkich wyzwaniach.

| Wersja | Dane 20% | Innowacyjność 25% | Wdrożenie 20% | Realia 15% | Prezentacja 20% | Średnia ważona |
|---|---|---|---|---|---|---|
| Przystanki — pierwotna (cień + PV) | 3 | 4 | 2,5 | 2,5 | 5 | ≈3,5 |
| Przystanki — wzór „słońce × kursy × tabor” | 3,5 | 4 | 3 | 3 | 4,5 | ≈3,65 |
| **Przystanki — rama przetargowa (rekomendowana)** | 4 | 4 | 3,5 | 4,5 | 4,5 | **≈4,1** |
| Dla porównania: mieszkania (RCN) | 4,5 | 2,5 | 4,5 | 5 | 3,5 | ≈3,9 |

Mieszkania przegrały przede wszystkim na innowacyjności. Ceny transakcyjne
pokazują już rcn-szukaj miasta, Geoportal, Sonarhome i Otodom. Przewaga
przystanków jest jednak niewielka. Rozstrzygnie to, czy TOP 20 pokaże coś
nieoczywistego (patrz testy w sekcji 6).

---

## 3. Wersja rekomendowana: rama przetargowa

### Jedno zdanie

**Za rok miasto zdecyduje, jakie wiaty i gdzie postawi w kolejnej umowie.
Pokazujemy, które przystanki stoją w pełnym słońcu, czego potrzebują i od
których zacząć.**

### Odbiorca i moment decyzji

Koncesja AMS z października 2025 obejmuje utrzymanie 1640 wiat. Zawarto ją
**tylko na rok**, z opcją przedłużenia o 3 × 6 miesięcy. Poprzednia umowa
(2013) trwała prawie 9 lat. Miasto (ZTM) musi więc w ciągu 1–2 lat
przygotować nowy przetarg: gdzie stoją wiaty i jakie mają dachy. Na jaki
okres zostanie zawarta kolejna umowa, nie wiemy — nie zakładamy, że znów na
ok. 9 lat.
Nasz wynik to gotowy wkład do opisu przedmiotu zamówienia.

To odwraca argument z pierwotnej krytyki. Koncesja nie przekreśla pomysłu,
tylko daje mu konkretnego odbiorcę, dokument i termin.

### Co się zmienia względem poprzednich wersji

| Wcześniej | Teraz |
|---|---|
| Oś: cień + PV po równo | **Oś: cień i upał.** PV to najwyżej jedno zdanie |
| Jeden ranking „priorytet” | **Klasa interwencji** dla każdego przystanku + kolejność w klasie |
| Mnożnik za liczbę kursów | **Punkty za węzeł przesiadkowy i wrażliwe miejsca** w pobliżu |
| Tabor bez klimy jako mnożnik | **Tabor jako osobna warstwa mapy** („łańcuch upału w podróży”) |
| „Gdzie postawić wiatę” | „Gdzie wiata, gdzie inny dach, gdzie drzewo”, z zastrzeżeniem, że miejsce trzeba sprawdzić w terenie |
| Dla kogo: firmy PV | Dla kogo: ZTM (przetarg), Zarząd Zieleni, AMS, mieszkańcy |

### Klasy interwencji

Każdy zespół przystankowy dostaje jedną klasę:

| Klasa | Sytuacja | Rekomendacja | Kto decyduje |
|---|---|---|---|
| **A** | Pełne słońce, brak wiaty | drzewo albo wiata (do sprawdzenia, czy jest miejsce) | Zarząd Zieleni, nowy przetarg na wiaty |
| **B** | Pełne słońce, wiata z pleksi | dach nieprzezroczysty albo zielony | specyfikacja nowego przetargu, AMS |
| **C** | Cień od budynków | nic nie trzeba | — |

„Pełne słońce” = co najmniej X godzin bezpośredniego słońca latem w godz.
12–18. Próg X dobieramy po pierwszym przebiegu.

### Kolejność w klasie (punkty)

Prosty system, który da się wytłumaczyć jury w 20 sekund:

```
punkty = węzeł      (1–3 pkt: liczba linii na zespole)
       + wrażliwi   (+1: przychodnia, szpital lub dom seniora w promieniu 300 m)
       + tabor      (+1: na liniach przystanku przeważają tramwaje bez klimy)
```

Nie mnożymy przez liczbę kursów (patrz punkt 7 krytyki). Liczba linii mówi,
jak ważny jest węzeł, i nie udaje liczby pasażerów.

### Warstwa „łańcuch upału”

Osobna warstwa mapy: przystanki w pełnym słońcu obsługiwane głównie przez
tramwaje bez klimatyzacji. Najpierw czekasz w słońcu, potem jedziesz
w nagrzanym wagonie. Problem jest realny w najbliższych latach, zanim
wymiana taboru się skończy. Pokazujemy go jako kontekst dla Tramwajów
Warszawskich, a nie jako główny wynik.

### Hasło na prezentację

„W Warszawie jest N przystanków, na których w lipcu stoisz w pełnym słońcu.
Na M z nich wiata ma dach z pleksi, który grzeje zamiast chronić. Za rok
miasto rozpisze przetarg na wiaty. Oto lista, od której warto zacząć.”

### Dla kogo

- **ZTM:** wkład do specyfikacji nowego przetargu na wiaty (lokalizacje, typ dachu).
- **Zarząd Zieleni:** przystanki klasy A, przy których drzewo zastąpi wiatę.
- **AMS** (operator wiat): lista wiat do wymiany dachu z uzasadnieniem.
- **Tramwaje Warszawskie:** warstwa „łańcuch upału”.
- **Mieszkańcy:** gotowy argument do wniosku w budżecie obywatelskim (zieleń to
  124 projekty w edycji 2025, zielone dachy wiat były już finansowane z BO).

---

## 4. Dane

### Z portalu miasta (mamy albo wiemy, jak pobrać)

| Zbiór | Endpoint | Co daje | Stan |
|---|---|---|---|
| Przystanki | `get_ztm_przystanki_komunikacji_miejskiej` | 6988 słupków / 2935 zespołów, WGS84 | ✅ `data/raw/male/przystanki.json` |
| Linie na przystanku | `get_ztm_lista_linii_na_przystanku` | linie na słupku → punkty za węzeł | ⚠️ 1 zapytanie = 1 słupek (~7000 zapytań, puścić w tle) |
| Odjazdy | `get_ztm_odjazdy_linii_z_przystanku` | rozkład, `line` obowiązkowy | ⚠️ tylko dla wybranych przystanków (przykłady na slajd) |
| Pojazdy (tabor) | `get_ztm_pojazdy` | `numerTaborowy` → model → `klimatyzacja`, `podloga` | ✅ `data/raw/male/pojazdy_transportu_publicznego.json` |
| GPS pojazdów | `get_ztm_lokalizacja_pojazdow` | które wozy jeżdżą na jakich liniach | ⚠️ bez historii, trzeba zbierać (`src/zbieraj_gps.py`) |
| Pogoda ZOM | `get_zom_pogoda` | temperatura powietrza i nawierzchni, 16 stacji | ⚠️ tylko migawka z października — nie używamy w analizie |

Liczby z taboru (do weryfikacji, patrz punkt 10 krytyki): **353 z 797
tramwajów bez klimatyzacji**, 363 sprzed 2006 r. Autobusy są klimatyzowane
prawie wszystkie (1819 z 1839), więc warstwa taboru dotyczy praktycznie
tylko tramwajów. Zanim liczba trafi na slajd, sprawdzamy, czy 797 to
pojazdy, czy wagony.

**GPS → tabor na linii:** migawki GPS zbierane co 30–60 s przez kilka godzin
pokażą, jakie wozy (z klimą czy bez) jeżdżą na każdej linii tramwajowej.
Łączymy to z listą linii na przystanku.

### Spoza portalu

| Dane | Źródło | Uwagi |
|---|---|---|
| Budynki + wysokość | OSM (`building:levels`, `height`) | dobre pokrycie w centrum, dziury na obrzeżach |
| Budynki 3D (opcja) | GUGiK, modele LoD1/LoD2 (CityGML) | dokładne, ale ciężkie w obróbce — raczej nie w 22 h |
| Wiaty | OSM: `shelter=yes` na przystankach | częściowe; zapytać mentorów ZTM o pełną listę — **kluczowe dla klas A/B** |
| Wrażliwe miejsca | OSM: `amenity=clinic`, `hospital`, `social_facility` (seniorzy) | do punktów „wrażliwi” |
| Drzewa | OSM `natural=tree` (rzadkie) / NDVI z Sentinel-2 | zastępstwo dla braku inwentaryzacji miejskiej |
| Pozycja słońca | `pvlib` albo `pysolar` | standard |

---

## 5. Technika (szkic)

1. Wczytaj zespoły przystankowe, czyli średnią współrzędnych słupków.
2. Pobierz budynki z OSM dla Warszawy (Overpass albo plik `.pbf`). Wysokość:
   `height`, a gdy jej brak, `building:levels × 3 m`, a gdy i tego brak,
   wartość domyślna.
3. Przelicz geometrię do układu metrycznego (EPSG:2180 lub 2178).
4. Dla wybranych dat (np. 21.06 i 15.07) i godzin 12–18 policz azymut
   i wysokość słońca, a dla każdego przystanku sprawdź, czy promień przecina
   budynek. Do wyszukiwania budynków użyj `shapely` + `STRtree`. Skala jest
   mała (2935 punktów × ~14 chwil).
5. Zapisz godziny słońca dla każdego przystanku. Dołącz wiaty (OSM lub lista
   z ZTM), linie, wrażliwe miejsca i tabor. Przypisz klasę A/B/C i punkty.
6. Mapa: `folium` (doinstalować) z warstwami „słońce”, „klasa interwencji”
   i „łańcuch upału” oraz tabele TOP 20 dla klas A i B.

**Gotowe biblioteki do sprawdzenia:** `pybdshadow` (cienie budynków z OSM),
`pvlib`.

### Plan B (gdy symulacja cienia nie zadziała do ~14:00 w sobotę)

- Nasłonecznienie przybliżamy prościej: szerokość ulicy i średnia wysokość
  zabudowy w promieniu 30 m oraz kierunek ulicy względem południa.
- Albo jeszcze prościej: brak budynków w promieniu X m oznacza „pełne słońce”.
- Reszta (klasy, punkty, tabor) działa bez zmian. To nadal pełny projekt.

---

## 6. Plan pracy (szkic, do podziału ról)

| Kiedy | Co |
|---|---|
| Od razu | Uruchomić zbieranie GPS w tle (`src/zbieraj_gps.py`). Historii nie da się pobrać wstecz |
| Od razu | Puścić w tle pobieranie linii na przystankach (~7000 zapytań) |
| Pierwsze 2 h | **Testy „kontynuować czy zmieniać”** (niżej) |
| Sobota rano | Budynki z OSM, pozycja słońca, pierwszy wynik dla Śródmieścia |
| Sobota do 14:00 | **Punkt decyzji:** symulacja działa → cała Warszawa; nie działa → plan B |
| Sobota popołudnie | GPS → tabor → klimatyzacja; wiaty, wrażliwe miejsca, klasy A/B/C |
| Sobota wieczór | Punkty, mapa, TOP 20 dla klas A i B |
| Niedziela rano | Prezentacja, uczciwe ograniczenia, demo. **Oddanie 11:00** |

### Testy na pierwsze 2 godziny

1. **Rozmowa z mentorem z ZTM:** czy trwają prace nad nowym przetargiem na
   wiaty i czy można dostać listę lokalizacji wiat (z typem dachu). Ta jedna
   rozmowa albo potwierdza ramę projektu, albo każe ją zmienić.
2. **Pokrycie wiat w OSM:** jaki odsetek przystanków ma `shelter=yes` albo
   `shelter=no`. Poniżej ok. 30% i bez listy z ZTM podział na klasy A i B się
   nie uda. Zostaje wtedy mapa „gdzie jest słońce”, a to słabszy projekt.
3. **Zgrubny przebieg dla Śródmieścia:** jeśli TOP 20 to same oczywiste
   miejsca (duże ronda, place), szukamy wniosku w skali miasta, np. „X%
   węzłów przesiadkowych nie ma żadnego cienia”.
4. **Liczba tramwajów:** wyjaśnić, czy 797 to pojazdy, czy wagony.

---

## 7. Ryzyka i ograniczenia (mówimy o nich otwarcie w prezentacji)

- **Brak drzew:** liczymy najgorszy przypadek, czyli cień tylko od budynków.
  Najbardziej zawyżone są alejki w parkach, a na arteriach wynik jest bliski prawdy.
- **Brak listy wiat:** OSM częściowo; w prezentacji mówimy „przystanki
  do sprawdzenia”, a nie „przystanki bez wiaty”.
- **Nie sprawdzamy miejsca na wiatę:** szerokość chodnika i sieci
  podziemne zostają do weryfikacji w terenie. Mówimy to wprost, zanim zapyta jury.
- **Liczba linii to nie pasażerowie:** traktujemy ją jako miarę ważności
  węzła, nie jako obciążenie.
- **GPS tylko z weekendu:** rozkład weekendowy różni się od roboczego.
  Do udziału wozów bez klimy na linii wystarczy.
- **Tabor się zmienia:** wymiana tramwajów trwa, więc warstwa „łańcuch upału”
  dotyczy najbliższych lat, nie dekady.
- **Październik:** w Warszawie nie ma teraz upału. Symulujemy lato (geometria
  słońca); danych pogodowych z października nie używamy.

---

## 8. Otwarte pytania

- [ ] Czy mentorzy z ZTM/miasta mogą dać listę lokalizacji wiat (z typem dachu)?
- [ ] Czy miasto przygotowuje już nowy przetarg na wiaty i w jakim terminie?
- [ ] Czy `pybdshadow` działa na naszym Pythonie / Windows?
- [ ] Jakie pokrycie wysokościami budynków ma OSM poza Śródmieściem?
- [ ] Ile przystanków ma w OSM znacznik `shelter`?
- [ ] Czy 797 tramwajów w `get_ztm_pojazdy` to pojazdy, czy wagony?
- [x] Które wyzwanie: Warszawa 2076 (upały, starzenie się) czy Twój ruch? → **Twój ruch**
- [ ] Łączymy z problemem nr 4 (tramwaje niskopodłogowe, `podloga`), czy
  zostajemy przy samym upale?

---

## Źródła

- [gramwzielone: mapa potencjału solarnego Warszawy](https://www.gramwzielone.pl/?p=3924)
- [PAP Biznes: koncesja AMS na 1640 wiat (2025)](https://biznes.pap.pl/wiadomosci/firmy/agora-sa-212025-zawarcie-przez-ams-serwis-sp-z-oo-umowy-koncesji)
- [Bankier: umowa koncesji AMS Serwis (2025, rok + 3 × 6 mies.)](https://www.bankier.pl/wiadomosc/AGORA-Zawarcie-przez-AMS-Serwis-sp-z-o-o-umowy-koncesji-9020491.html)
- [Bankier: aneks do umowy na wiaty](https://www.bankier.pl/wiadomosc/AGORA-Zawarcie-aneksu-do-umowy-koncesji-na-budowe-i-eksploatacje-wiat-przystankowych-w-Warszawie-przez-AMS-S-A-8725875.html)
- [Eurobuild: wiata z zielonym dachem](https://eurobuildcee.com/news/45716-wiata-z-zielona-czupryna)
- [Radio Kraków: 100 wiat z zielonym dachem, pomiary temperatury](https://www.radiokrakow.pl/aktualnosci/krakow/w-przyszlym-roku-100-wiat-przystankowych-z-dachem-pokrytym-roslinnoscia-w-krakowie)
- [Railway Gazette: kontrakt Hyundai Rotem w Warszawie](https://railwaygazette.com/modes/hyundai-rotem-plans-polish-factory-as-it-signs-warszawa-tram-contract/48715.article)
- [Rollingstock World: zamówienie tramwajów w Warszawie](https://rollingstockworld.com/lrv/warsaw-announces-large-procurement-of-lrvs/)
- [Eurobuild: inwentaryzacja drzew w Warszawie](https://eurobuildcee.com/news/43897-miejskie-drzewa-pod-kontrola)
- [300gospodarka: upały w Warszawie](https://300gospodarka.pl/analizy/pan-upaly-w-warszawie-miasta-zmiany-klimatu-adaptacja-mitygacja)
