# Upał na przystankach — pomysł na hackaton

Stan: 17.10.2026. Wyzwanie: **Twój ruch**. Bieżąca analiza pomysłu, uzupełniana
w trakcie hackatonu (oddanie w niedzielę 18.10 o 11:00). Pełna historia pomysłu
i krytyka wcześniejszych wersji: [11-pomysl-przystanki.md](11-pomysl-przystanki.md).

## W skrócie

Pokazujemy, które przystanki w Warszawie stoją latem w pełnym słońcu i co na
każdym z nich zrobić: posadzić drzewo, postawić wiatę albo wymienić dach z pleksi
na taki, który daje cień (zielony albo z panelem PV). Robimy to teraz, bo umowa na
utrzymanie 1640 wiat jest roczna i miasto w ciągu 1–2 lat przygotuje nowy
przetarg. To, co trafi do jego specyfikacji, zapłaci operator wiat.

## Problem i moment decyzji

Upałów w Warszawie przybywa, a czekanie na przystanku w pełnym słońcu to
codzienność dla seniorów, dzieci i osób dojeżdżających do pracy. Wiata nie zawsze
pomaga: większość warszawskich wiat ma dach z pleksi, czyli przezroczysty.
Chroni przed deszczem, ale słońce przechodzi przez niego niemal swobodnie.

Istnieją lepsze dachy. W Krakowie pod wiatą z zielonym dachem (rozchodnik)
zmierzono do 5°C mniej niż pod zwykłą. W Warszawie zielone dachy wiat były już
finansowane z budżetu obywatelskiego, ale tylko na pojedynczych przystankach.

**Moment decyzji:**

- Wiaty buduje i utrzymuje firma AMS w ramach koncesji reklamowej.
- Obecna koncesja z października 2025 obejmuje 1640 wiat i jest zawarta
  **tylko na rok**, z opcją przedłużenia o 3 × 6 miesięcy (najdłużej do ok. 2027).
- Poprzednia umowa, z 2013 r., trwała prawie 9 lat. Na jaki okres zostanie
  zawarta kolejna, nie wiemy, ale do jej końca o wiatach będzie decydować to,
  co zapisze się w przetargu.
- Właśnie teraz miasto decyduje, gdzie będą stały wiaty i jakie będą miały dachy.
  Nasz wynik może być wkładem do specyfikacji przetargu.

Nie wiemy jeszcze, czy przetarg już się przygotowuje, na jaki okres zostanie
zawarta kolejna umowa i czy miasto nie zmieni modelu. To pytania do mentora z ZTM (ostatnia sekcja).

## Rozwiązanie: trzy klasy przystanków

Każdy z 2935 zespołów przystankowych dostaje jedną klasę. „Pełne słońce” oznacza
co najmniej X godzin bezpośredniego słońca latem w godz. 12–18. Próg X dobierzemy
po pierwszym przebiegu.

| Klasa | Sytuacja | Rekomendacja | Wartość dla miasta | Kto płaci |
|---|---|---|---|---|
| **A** | Pełne słońce, brak wiaty | Drzewo albo wiata (miejsce do sprawdzenia w terenie) | Lista miejsc, gdzie ludzie czekają w upale bez żadnej ochrony. Drzewo chłodzi bardziej niż wiata i służy dziesiątki lat | Wiata: operator w ramach koncesji, jeśli miasto wpisze lokalizację do przetargu. Drzewo: Zarząd Zieleni, budżet obywatelski, fundusze na adaptację do klimatu |
| **B** | Pełne słońce, wiata z pleksi | Dach nieprzezroczysty: zielony albo z panelem PV | Najtańsza poprawa, bo wiata już stoi. Zmienia się tylko dach | Operator, jeśli typ dachu trafi do specyfikacji przetargu. Wcześniej: pilotaż z budżetu miasta lub budżetu obywatelskiego |
| **C** | Cień od budynków | Nic nie trzeba | Wiedza, gdzie nie wydawać pieniędzy | — |

**Panele PV jako typ dachu.** Panel na dachu wiaty jest nieprzezroczysty, więc
daje cień tak jak zielony dach. Dach wiaty mieści ok. 1 kWp, czyli ok. 1000 kWh
rocznie. To za mało na inwestycję energetyczną, ale wystarczy, żeby wiata sama
zasilała oświetlenie LED, tablicę odjazdów albo ładowarkę USB, bez przyłącza do
sieci. Ta sama symulacja słońca da od razu roczny uzysk energii dla każdego
przystanku klasy B.

**Wartość całego narzędzia:**

- Analiza jest prawie darmowa: otwarte dane miasta i OSM zamiast pomiarów
  w terenie na 2935 zespołach przystankowych.
- Przychodzi w dobrym momencie: co miasto zapisze w specyfikacji przetargu, za to
  zapłaci operator. Czego nie zapisze, tego nie dostanie do końca umowy.
- Dzieli pracę między instytucje: klasa A trafia do Zarządu Zieleni i ZTM,
  klasa B do specyfikacji przetargu, a mieszkańcy dostają gotowe uzasadnienie do
  wniosku w budżecie obywatelskim.

Model finansowania (operator płaci za wiaty, zarabia na reklamach) to nasza
interpretacja. Trzeba go potwierdzić z mentorem z ZTM.

## Kolejność w klasie i łańcuch upału

W klasach A i B ustawiamy przystanki według prostej sumy punktów, którą da się
wytłumaczyć jury w 20 sekund:

| Składnik | Punkty | Skąd dane |
|---|---|---|
| Węzeł przesiadkowy | 1–3 (wg liczby linii na zespole) | linie na przystanku, portal miasta |
| Wrażliwe miejsca | +1 (przychodnia, szpital lub dom seniora w promieniu 300 m) | OSM |
| Tabor | +1 (na liniach przystanku przeważają tramwaje bez klimatyzacji) | rejestr taboru + GPS, portal miasta |

Nie mnożymy przez liczbę kursów. Przy częstych kursach każdy czeka krótko, więc
taki wzór premiowałby przystanki, na których w słońcu stoi się najkrócej. Liczba
linii mówi, jak ważny jest węzeł, i nie udaje liczby pasażerów, której nie mamy.

**Łańcuch upału** to osobna warstwa mapy: przystanki w pełnym słońcu obsługiwane
głównie przez tramwaje bez klimatyzacji. Najpierw czekasz w słońcu, potem jedziesz
nagrzanym wagonem. W danych 353 z 797 tramwajów nie ma klimatyzacji, za to autobusy
mają ją prawie wszystkie (1819 z 1839). Wymiana taboru trwa, więc warstwa dotyczy
najbliższych lat i jest kontekstem dla Tramwajów Warszawskich, a nie głównym
wynikiem.

**Hasło na prezentację:** „W Warszawie jest N przystanków, na których w lipcu
stoisz w pełnym słońcu. Na M z nich wiata ma dach z pleksi, który nie chroni przed
słońcem. Miasto i tak rozpisze przetarg na wiaty. Oto lista, od której warto
zacząć.”

## Dane

### Z portalu miasta (dane.um.warszawa.pl)

| Zbiór | Co daje | Stan |
|---|---|---|
| Przystanki | 6988 słupków w 2935 zespołach, współrzędne WGS84 | pobrane: `data/raw/male/przystanki.json` |
| Linie na przystanku | liczba linii na zespole → punkty za węzeł | do pobrania: 1 zapytanie = 1 słupek, ok. 7000 zapytań w tle |
| Odjazdy linii z przystanku | rozkład dla wybranych przystanków (przykłady na slajd) | tylko próbka |
| Pojazdy transportu publicznego | numer taborowy → model → klimatyzacja, podłoga | pobrane: `data/raw/male/pojazdy_transportu_publicznego.json` |
| Lokalizacja pojazdów (GPS) | które wozy jeżdżą na jakich liniach | bez historii, trzeba zbierać: `src/zbieraj_gps.py` |

Pogody ZOM nie używamy w analizie: to migawka z października, a symulujemy lato.

### Spoza portalu

| Dane | Źródło | Uwagi |
|---|---|---|
| Budynki i ich wysokość | OSM (`height`, `building:levels`) | dobre pokrycie w centrum, luki na obrzeżach |
| Wiaty | OSM: `shelter=yes/no` na przystankach; lista z ZTM, jeśli ją dostaniemy | **kluczowe dla podziału na klasy A i B** |
| Wrażliwe miejsca | OSM: `amenity=clinic`, `hospital`, `social_facility` | do punktów „wrażliwi” |
| Drzewa | OSM `natural=tree` (rzadkie) albo NDVI z Sentinel-2 | miejska inwentaryzacja drzew nie jest otwartymi danymi |
| Pozycja słońca | `pvlib` lub `pysolar` | standardowe obliczenia |

## Jak to zrobimy

1. Zespoły przystankowe: średnia współrzędnych słupków.
2. Budynki z OSM dla Warszawy. Wysokość: `height`, a gdy jej brak,
   `building:levels × 3 m`, a gdy i tego brak, wartość domyślna.
3. Przeliczenie geometrii do układu metrycznego (EPSG:2180 lub 2178).
4. Dla wybranych dni lata (np. 21.06 i 15.07) i godzin 12–18: pozycja słońca
   i sprawdzenie, czy promień do przystanku przecina budynek (`shapely` +
   `STRtree`). Skala jest mała: 2935 punktów × ok. 14 chwil.
5. Dołączenie wiat, linii, wrażliwych miejsc i taboru; przypisanie klasy A/B/C
   i punktów.
6. Mapa w `folium` z warstwami „słońce”, „klasa” i „łańcuch upału” oraz tabele
   TOP 20 dla klas A i B.

**Plan B** (gdy symulacja cienia nie zadziała do soboty 14:00): nasłonecznienie
przybliżamy prościej, np. brak budynków w promieniu X m oznacza „pełne słońce”.
Klasy, punkty i tabor działają bez zmian.

## Ryzyka i pytania otwarte

**Ograniczenia (mówimy o nich otwarcie na prezentacji):**

- **Brak drzew:** liczymy cień tylko od budynków, więc wynik jest najgorszym
  przypadkiem. Najbardziej zawyżone są przystanki w parkach.
- **Niepełna lista wiat:** OSM ma ją tylko częściowo. Bez listy z ZTM mówimy
  „przystanki do sprawdzenia”, a nie „przystanki bez wiaty”.
- **Nie sprawdzamy, czy jest miejsce na wiatę:** szerokość chodnika i sieci pod
  ziemią zostają do weryfikacji w terenie.
- **Liczba linii to nie liczba pasażerów:** traktujemy ją jako miarę ważności
  węzła.
- **GPS tylko z weekendu:** wystarczy do oceny udziału tramwajów bez klimatyzacji
  na linii.

**Pytania do mentora z ZTM:**

- [ ] Czy miasto przygotowuje już nowy przetarg na wiaty i na jaki okres planuje umowę?
- [ ] Czy można dostać listę lokalizacji wiat z typem dachu?
- [ ] Czy operator płaci za wiaty i zarabia na reklamach, a miasto może w przetargu
      narzucić lokalizacje i typ dachu?
- [ ] Czy na przystankach bez reklam operator też stawia wiaty?

**Do sprawdzenia w danych:**

- [ ] Ile przystanków ma w OSM znacznik `shelter`? Poniżej ok. 30% podział na
      klasy A i B się nie uda.
- [ ] Czy 797 tramwajów w `get_ztm_pojazdy` to pojazdy, czy pojedyncze wagony?
      Od tego zależy liczba „44% bez klimatyzacji”.
- [ ] Jakie pokrycie wysokościami budynków ma OSM poza Śródmieściem?

## Źródła

- [PAP Biznes: koncesja AMS na 1640 wiat (2025)](https://biznes.pap.pl/wiadomosci/firmy/agora-sa-212025-zawarcie-przez-ams-serwis-sp-z-oo-umowy-koncesji)
- [Bankier: umowa koncesji AMS Serwis (rok + 3 × 6 mies.)](https://www.bankier.pl/wiadomosc/AGORA-Zawarcie-przez-AMS-Serwis-sp-z-o-o-umowy-koncesji-9020491.html)
- [Radio Kraków: wiaty z zielonym dachem, pomiary temperatury](https://www.radiokrakow.pl/aktualnosci/krakow/w-przyszlym-roku-100-wiat-przystankowych-z-dachem-pokrytym-roslinnoscia-w-krakowie)
- [Eurobuild: wiata z zielonym dachem w Warszawie](https://eurobuildcee.com/news/45716-wiata-z-zielona-czupryna)
- [Eurobuild: inwentaryzacja drzew w Warszawie](https://eurobuildcee.com/news/43897-miejskie-drzewa-pod-kontrola)
- [300gospodarka: upały w Warszawie](https://300gospodarka.pl/analizy/pan-upaly-w-warszawie-miasta-zmiany-klimatu-adaptacja-mitygacja)
- Dane: portal otwartych danych m.st. Warszawy, https://dane.um.warszawa.pl
