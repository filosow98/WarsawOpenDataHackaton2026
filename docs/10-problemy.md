# Problemy do rozwiązania — propozycje tematów

Pięć problemów Warszawy, które da się rozwiązać na danych z portalu, plus ocena
pomysłu z parkingami. Liczby policzone na danych pobranych 13.10.2026
(`data/raw/`). Temat nie jest jeszcze wybrany — to materiał do decyzji.

## W skrócie

| # | Problem | Kluczowa liczba | Mocna strona |
|---|---|---|---|
| 1 | AED niedostępne w nocy | tylko **14%** AED dostępnych całodobowo | najbezpieczniejszy, mocny pitch |
| 2 | Upał w tramwaju | **44%** tramwajów bez klimatyzacji | najbardziej innowacyjny |
| 3 | Prawdziwe ceny mieszkań | RCN = ceny z aktów, nie z ogłoszeń | ważny temat, ale jest konkurencja |
| 4 | Miasto z barierami | **43%** tramwajów wysokopodłogowych | łączy się z nr 2 |
| 5 | Niewidoczna oferta miasta | Targówek 107 zajęć, Mokotów **9** | pasuje do „Złap oddech” |

**Rekomendacja:** nr 2 + nr 4 (jeden projekt, najwyższa innowacyjność) albo
nr 1 (najprostszy, wszystkie dane już mamy).

---

## 1. Defibrylatory zamknięte, gdy są potrzebne

- **Problem:** przy zatrzymaniu krążenia liczą się minuty — defibrylacja
  w ciągu 3 min podnosi przeżywalność z <10% nawet do 75%.
- **Dane:** 710 AED, tylko 100 (14%) z `device_availability` = „Tak”.
  688 (97%) wisi w budynkach (sądy, przychodnie, urzędy) czynnych
  w dni robocze ok. 7–17. W nocy i w weekend sieć prawie znika.
- **Pomysł:** mapa zasięgu AED z suwakiem godziny + propozycje, gdzie postawić
  szafki zewnętrzne (przystanki, całodobowe toalety).
  szafki zewnętrzne (przystanki, całodobowe toalety).
- **Zbiory:** AED, przystanki, toalety (261 całodobowych), otwarte boiska.
- **Dla kogo:** Biuro Bezpieczeństwa — lista miejsc pod nowe AED.
- **Do sprawdzenia:** czy „Tak” w `device_availability` na pewno znaczy
  „całodobowo” (specyfikacja `_pa.json`). Od tego zależy główna liczba.

## 2. Upał w tramwaju (Warszawa 2076)

- **Problem:** upałów przybywa, prognozy mówią o dużym wzroście zgonów z gorąca.
- **Dane:** 353 z 797 tramwajów (44%) bez klimatyzacji, 363 sprzed 2006 r.
  Autobusy są klimatyzowane prawie wszystkie (1819 z 1839).
- **Pomysł:** GPS pojazdu (`VehicleNumber`) → rejestr taboru (`numerTaborowy`)
  → model (`klimatyzacja`). Widać na żywo, które linie jadą „saunami”.
  Do tego temperatura nawierzchni ze stacji pogodowych ZOM.
- **Dla kogo:** ZTM — kierowanie klimatyzowanych wagonów na gorące trasy;
  seniorzy — „poczekaj 4 min na chłodny tramwaj”.
- **Ryzyko:** GPS nie ma historii — zbieranie trzeba uruchomić od razu
  (`src/zbieraj_gps.py`).

## 3. Mieszkania: ceny z ogłoszeń zamiast prawdziwych

- **Problem:** dostępność mieszkań to jeden z największych problemów
  mieszkańców, a publikowane statystyki to prawie zawsze ceny ofertowe.
- **Dane:** RCN ma ceny transakcyjne z aktów notarialnych: powierzchnia,
  piętro, rynek, adres.
- **Pomysł:** „ile naprawdę kosztuje metr na tej ulicy” + indeks miasta
  15-minutowego (przystanki, boiska, AED, eko punkty) — ile płacisz za dostęp
  do usług.
- **Ryzyka:** istnieją portale z cenami (innowacyjność musi być w połączeniu
  z usługami); RCN jest duży — tylko wybrane dzielnice; współrzędne
  w EPSG:2178 do przeliczenia.

## 4. Miasto z barierami dla starzejącej się Warszawy

- **Problem:** w perspektywie 2076 będzie znacznie więcej seniorów i osób
  o ograniczonej mobilności.
- **Dane:** 340 tramwajów (43%) wysokopodłogowych, 400 z 695 toalet dostępnych,
  tylko 15 z 593 zajęć sportowych (2,5%) dla osób z niepełnosprawnościami.
- **Pomysł:** „Trasa bez barier” — GPS + rejestr taboru (`podloga`: LF/HF)
  mówi, czy nadjedzie wagon niskopodłogowy; po drodze dostępne toalety i AED.
- **Dla kogo:** Pełnomocnik ds. dostępności, organizacje pozarządowe.
- **Uwaga:** ta sama baza techniczna co nr 2 — warto połączyć.

## 5. Darmowa oferta miasta, której nikt nie widzi (Złap oddech)

- **Problem:** oferta jest rozproszona po różnych serwisach i nierówno
  rozłożona.
- **Dane:** 1227 otwartych boisk, 593 zajęcia, 655 wydarzeń. Targówek ma
  107 zajęć, Mokotów (największa dzielnica) — 9. 317 boisk (26%) zamkniętych
  w niedzielę.
- **Pomysł:** „Po pracy w 15 minut” — co zrobić dziś po 18:00 blisko domu,
  z dojazdem i filtrem jakości powietrza. Dla urzędu: mapa luk w ofercie.
  Budżet obywatelski (289 projektów, ok. 100 mln zł) pokazuje, czego ludzie
  chcą: przestrzeń publiczna (188), zieleń (124).

---

## Ocena wobec kryteriów jury (1–5)

| # | Dane 20% | Innowacyjność 25% | Wdrożenie 20% | Realia 15% | Pitch 20% |
|---|---|---|---|---|---|
| 1 AED | 4 | 4 | 5 | 5 | 5 |
| 2 Upał | 5 | 5 | 4 | 5 | 4 |
| 3 Mieszkania | 4 | 3 | 4 | 5 | 4 |
| 4 Bez barier | 5 | 4 | 4 | 4 | 4 |
| 5 Po pracy | 5 | 3 | 4 | 4 | 5 |

---

## A parkingi? (omówione osobno)

**Werdykt:** sama mapa wolnych miejsc — słaba. Jako część większego pomysłu —
sensowna.

- **Zbiór jest mały:** 14 parkingów, prawie wszystkie w Śródmieściu
  (ok. 2350 miejsc). Nie ma P+R (17 parkingów, ok. 4800 miejsc) ani miejsc
  w strefie płatnego parkowania na ulicach — a tam jest prawdziwy problem.
- **Już istnieje:** wtp.waw.pl pokazuje wolne miejsca na P+R, parkingi
  podziemne mają własne tablice. Jury może uznać to za nienowe.
- **Ciekawostki:** miejsca dla osób z niepełnosprawnościami podają tylko
  3 parkingi; miejsc z ładowarką jest łącznie **9**.
- **Brak historii:** tylko stan bieżący, odświeżany co minutę.

Jak to przerobić, żeby miało szansę:

1. **Ograniczenia ruchu wokół Starówki** (pierwszy raz w nocy 16/17.10.2026,
   potem w weekendy) — obok parkingi pl. Żelaznej Bramy, Boleść, Bednarska.
   Migawki z tego weekendu pokażą efekt zmiany. Aktualna, konkretna historia.
2. **„Autem czy tramwajem?”** — cennik parkingu vs odjazdy i GPS: koszt
   i czas dojazdu do centrum.
3. **Wydarzenia → parkingi** — kalendarz wydarzeń przy PKiN ostrzega, że
   parking się zapełni.
4. **Parkowanie bez barier i z ładowarką** — pasuje do nr 4.

Prognoza obłożenia jest ryzykowna: zbierając od 17.10 mamy tylko weekend,
bez typowego dnia roboczego — pokazywać jako demo metody.

---

## Zanim zaczniemy

- **Zbieranie GPS i migawek parkingów/powietrza uruchomić od razu** — API nie
  trzyma historii. W migawce z 13.10 aż 153 z 1018 pozycji autobusów było
  nieaktualnych — zawsze filtruj po `Time`.
- **W portalu nie ma liczby ludności** — wskaźniki „na mieszkańca” wymagają
  danych GUS jako uzupełnienia.

## Źródła zewnętrzne

- [Europa Regionum — AED i przeżywalność](https://wnus.usz.edu.pl/er/pl/issue/1207/article/19195/)
- [300gospodarka — upały w Warszawie](https://300gospodarka.pl/analizy/pan-upaly-w-warszawie-miasta-zmiany-klimatu-adaptacja-mitygacja)
- [Warszawa 19115 — Miejski Plan Adaptacji](https://warszawa19115.pl/pl/-/miejski-plan-adaptacji-warszawa-dla-klimatu)
- [Sonarhome — ceny mieszkań 2025](https://sonarhome.pl/blog/artykuly/ceny-mieszkan-warszawa-2025-ile-naprawde-kosztuje-metr)
- [WTP — parkingi P+R](https://www.wtp.waw.pl/en/parkings/)
- [ZTM — P+R Jeziorki](https://www.ztm.waw.pl/inwestycje/budowa-parkingu-pr-warszawa-jeziorki/)
