# Generator ulotek „Najbliższa toaleta” — plan aplikacji

Stan: 17.10.2026. Plan budowy narzędzia z pomysłu
[13-toalety-przy-przystankach.md](13-toalety-przy-przystankach.md): dla każdego
słupka przystankowego generujemy ulotkę do wywieszenia, skierowaną głównie do
seniorów. Na ulotce: odległość do najbliższej toalety, mapa, czy toaleta jest
płatna, czynna w niedzielę, całoroczna czy sezonowa, oraz identyfikator
przystanku.

## W skrócie

- **Dwa widoki, jedna paczka danych.** Ulotka do druku (dla pasażera) i mapa
  luk (dla urzędu). Oba czytają ten sam plik `ulotki.json`.
- **Python liczy, przeglądarka rysuje.** Skrypt w Pythonie liczy wszystko
  z góry. Strona to czysty HTML + JS z mapą Leaflet, bez serwera aplikacji.
  PDF powstaje przez „Drukuj → Zapisz jako PDF”.
- **Bez nowych zależności w Pythonie** w wersji podstawowej (tylko biblioteka
  standardowa). Na Windows nie ma się co zepsuć.
- Stronę da się wystawić na GitHub Pages, więc jury może ją otworzyć samo.
  To punkty za wdrożenie.
- **Projektujemy dla seniora, korzystają wszyscy** (decyzja 17.10). Ulotka
  jest dla każdego: mieszkańców, rodziców z dziećmi, turystów. Teksty po
  polsku i angielsku, a kod QR otwiera nawigację pieszą do toalety. Senior
  zostaje bohaterem opowieści: jeśli ulotka działa dla niego, zadziała dla
  każdego.

## Co jest na ulotce

Format **A4 pionowo** (mieści się w ramce rozkładu albo jako laminat na
słupku).

```
┌─────────────────────────────────────────────┐
│ 🚻 NAJBLIŻSZA TOALETA                        │
│    Nearest toilet                           │
│ Przystanek: Sympatyczna 03        nr 4225-03 │
├─────────────────────────────────────────────┤
│          350 m  ·  ok. 8 min pieszo          │
│                     approx. 8 min walk      │
│   Inwalidów 3, Biblioteka Publiczna          │
│   Wskazówka: wejście od ul. Piekarskiej      │
├─────────────────────────────────────────────┤
│                                             │
│   [ MAPA:  ● JESTEŚ TUTAJ   🚻 TOALETA ]     │
│   [        You are here     Toilet   ]     │
│                                             │
├─────────────────────────────────────────────┤
│ ✔ BEZPŁATNA / free   ✘ W NIEDZIELĘ NIECZYNNA │
│ ✔ CZYNNA CAŁY ROK    ✔ DLA WÓZKÓW            │
│ Godziny / hours: pon.–pt. 9–19 · sob. 9–15   │
├─────────────────────────────────────────────┤
│ W niedzielę najbliższa czynna:      ┌──────┐ │
│ 900 m, ul. Przykładowa 5            │  QR  │ │
│                                     │      │ │
│ Prowadź mnie / Navigate me  ──────► └──────┘ │
├─────────────────────────────────────────────┤
│ Dane: dane.um.warszawa.pl, toalety IV 2026   │
│ Błąd na ulotce? Zadzwoń 19115, podaj 4225-03 │
└─────────────────────────────────────────────┘
```

**Dwa języki bez utraty czytelności:** polski duży, angielski pod spodem
mniejszą czcionką (ok. połowa wielkości), szarym, ale nadal z wysokim
kontrastem. Liczby (350 m, 8 min) i ikony są wspólne dla obu języków, więc
nie dublujemy ich. Angielski tylko w nagłówkach i etykietach, nie w adresie.

| Pole | Skąd | Uwagi |
|---|---|---|
| Nazwa i nr przystanku | `przystanki.json`: `nazwa_zespolu`, `zespol`, `slupek` | ID w formacie `4225-03` (zespół-słupek) |
| Odległość, minuty | liczone | linia prosta × 1,3 (objazdy), tempo seniora 0,8 m/s, zaokrąglone w górę do 1 min; zawsze „ok.” |
| Adres toalety | `lokalizacja` | |
| Wskazówka | `uwagi`, gdy nie dotyczy sezonu | „poziom -1”, „przejście podziemne”, „wejście od ul. …” |
| Płatna / bezpłatna | `platnosc` 0/1 | zbiór nie mówi, jak się płaci (karta, moneta) |
| Niedziela | `godziny`, fragment `Niedziela: …` | podajemy godziny, nie samo TAK/NIE |
| Całoroczna / sezonowa | `uwagi` + `typ` | pokazujemy dosłowny okres, np. „od 1 maja do 31 października” |
| Dla wózków | `dostepnosc` 0/1 | |
| Godziny skrótem | `godziny` | sklejamy jednakowe dni: „pon.–pt. 9–19” |
| Alternatywa | liczone | tylko gdy najbliższa jest płatna, nieczynna w niedzielę albo sezonowa |
| Stopka | stałe | data danych + 19115 (Warszawskie Centrum Kontaktu) z numerem przystanku |

**Zasady czytelności dla seniorów:**

- Odległość to najważniejsza liczba na kartce: co najmniej 60 pt. Treść co
  najmniej 20 pt.
- Czarne na białym, wysoki kontrast. Druk w czerni i bieli też musi działać.
- Nie polegamy na samym kolorze ani ikonach: zawsze ✔/✘ **i** słowo.
- Pełne słowa zamiast skrótów i żargonu („czynna”, a nie „otw.”).
- Mapa ustawiona na północ, z dużymi znacznikami i podpisami
  „JESTEŚ TUTAJ” i „TOALETA”.
- Kod QR to dodatek dla osób z telefonem (turyści, młodsi, opiekunowie).
  Ulotka musi działać **bez** telefonu, bo właśnie tym różni się od miejskich
  tabliczek „Mapa WC” z samym kodem QR (patrz plik 13).

## Kod QR: nawigacja do toalety

Kod QR na ulotce otwiera **pieszą nawigację od przystanku do toalety**
w Google Maps. Link w oficjalnym formacie Google Maps URLs, bez klucza API:

```
https://www.google.com/maps/dir/?api=1&origin=52.2103,20.91986&destination=52.2081,20.9214&travelmode=walking
```

- `origin` = współrzędne słupka, `destination` = współrzędne toalety (z
  `ulotki.json`). Na telefonie link otwiera aplikację Google Maps, jeśli jest
  zainstalowana, a jeśli nie, przeglądarkę.
- Kod generujemy w przeglądarce, przy renderze ulotki: biblioteka
  `qrcodejs` 1.0.0 z cdnjs (`https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js`).
  Bez zmian w Pythonie. Czas: ok. 30 min.
- **Rozmiar:** kod skanuje się z odległości ok. 10× jego boku, więc na
  ulotce co najmniej 4 cm. Poziom korekcji błędów M lub wyższy (ulotka na
  zewnątrz, zabrudzenia).
- Podpis przy kodzie w obu językach: „Prowadź mnie / Navigate me”.
- Sprawdzić przed prezentacją: zeskanować wydruk dwoma telefonami (Android
  i iPhone).
- Na prezentacji pokazać na żywo: skan → nawigacja do toalety. Dobry moment
  dla jury.
- Wariant na później: kod prowadzi na naszą stronę `?id=4225-03` (ulotka
  w telefonie, aktualne godziny, wybór Google Maps / Apple Maps / OSM).
  Daje miastu kontrolę nad treścią, ale wymaga stałego hostingu.

## Którą toaletę pokazujemy

Proponowana reguła (do potwierdzenia przez drużynę):

1. **Główna** = najbliższa toaleta dowolnego typu. Pokazujemy uczciwie jej
   cechy, także gdy to toi-toi albo toaleta płatna.
2. **Alternatywa** = najbliższa toaleta „pewna”: bezpłatna, całoroczna, czynna
   w niedzielę, nie przenośna. Dopisujemy ją tylko wtedy, gdy główna nie
   spełnia tych warunków.
3. Gdy główna jest dalej niż 1,5 km, nagłówek brzmi „W pobliżu nie ma
   toalety. Najbliższa: 1,8 km”. Taki przystanek trafia też na mapę luk.

Dlaczego tak: jedna toaleta na ulotce to za mało. Najbliższa bywa toi-toiem
czynnym do 31 października albo toaletą w urzędzie zamkniętym w niedzielę,
a w niedzielę senior jedzie do kościoła albo na cmentarz.

## Pułapki w danych (sprawdzone 17.10)

- **Godziny** mają jeden stały format: `Dzień: HH:MM - HH:MM` / `Całodobowo` /
  `nieczynne`, rozdzielony `; `. Parser to kilka linijek.
- **`uwagi` miesza dwie rzeczy:** okres działania (ok. 90 toalet, np.
  „do 31 października”, „od 1 maja do 30 września w weekendy”) i wskazówki
  dojścia („poziom -1”, „wejście od ul. Piekarskiej”). Trzeba je rozdzielić.
- Obecna funkcja `sezonowa()` w `src/luka_toaletowa.py` myli się na
  pojedynczych rekordach: toaleta z godzinami „styczeń–maj… październik–grudzień”
  wychodzi jako sezonowa, choć działa cały rok. Rekordów z okresem jest
  kilkanaście rodzajów, więc można je oznaczyć ręcznie w słowniku.
- **Teraz jest październik.** Ulotka wydrukowana dziś wskaże toi-toia, który
  za dwa tygodnie zniknie. Dlatego okres działania zawsze jest na ulotce, a do
  tego dochodzi alternatywa.
- **Linia prosta przez Wisłę i tory.** Najbliższa toaleta w linii prostej może
  być po drugiej stronie rzeki albo torów. Na demo wybieramy sprawdzone
  przystanki. Docelowo trasa piesza (krok 6).
- Słupki spoza Warszawy: obecny skrypt odcina je prostokątem. Na ulotki
  lepiej wziąć granicę miasta z OSM (jeden plik GeoJSON).
- 54 toalety typu „toaleta METRO”: nie wiemy, czy są przed bramkami, czy za
  nimi. Pytanie do mentora.

## Architektura

```
data/raw/male/{przystanki,toalety}.json
            │
            ▼
src/ulotki_dane.py ──► app/dane/ulotki.json   (1 rekord = 1 słupek, ok. 5000)
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
     app/index.html                    app/mapa.html
     wyszukiwarka przystanku           mapa luk dla urzędu:
     → podgląd ulotki A4               słupki pokolorowane wg odległości,
     → „Drukuj / zapisz PDF”           filtry, statystyki dzielnic
              │
              ▼ (opcjonalnie)
     src/ulotki_pdf.py — Playwright: PDF dla całej dzielnicy naraz
```

**Pliki:**

| Plik | Co robi |
|---|---|
| `src/ulotki_dane.py` | wczytuje dane (funkcje z `luka_toaletowa.py`), dla każdego słupka liczy główną toaletę i alternatywę, parsuje godziny i sezon, zapisuje JSON |
| `app/index.html` + `ulotka.js` | pole „wpisz nazwę lub nr przystanku” (`?id=4225-03` w URL-u), render ulotki |
| `app/ulotka.css` | wygląd ulotki, `@page { size: A4 }`, ukrycie interfejsu przy druku |
| `app/mapa.html` | mapa luk + liczby na slajd (59% / 74%, patrz plik 13) |
| `src/ulotki_pdf.py` | opcjonalnie: wsadowe PDF-y (`--dzielnica Wola`) |

**Rekord w `ulotki.json`:**

```json
{
  "id": "4225-03", "nazwa": "Sympatyczna", "lat": 52.2103, "lon": 20.91986,
  "glowna": {
    "lat": 52.2081, "lon": 20.9214, "adres": "Inwalidów 3, Biblioteka Publiczna",
    "typ": "toaleta stacjonarna", "odl_m": 350, "min": 8,
    "platna": false, "dla_wozkow": true,
    "niedziela": null, "godziny": "pon.–pt. 9–19 · sob. 9–15",
    "sezon": null, "wskazowka": "wejście od ul. Piekarskiej"
  },
  "alternatywa": { "...": "te same pola" }
}
```

**Zasady pracy z `ulotki.json`:**

- **Wzór rekordu to umowa** między osobą od danych a osobą od ulotek.
  Zmianę nazwy albo znaczenia pola uzgadniamy we dwoje i od razu
  poprawiamy wzór powyżej. Inaczej ulotka po cichu pokaże puste miejsca.
- **Python liczy, przeglądarka tylko wyświetla.** Ulotka i mapa nie liczą
  odległości, godzin ani sezonu. Brakuje pola (np. „całodobowa”)? Dopisujemy
  je w `src/ulotki_dane.py` i uruchamiamy skrypt jeszcze raz. Dzięki temu
  liczby na ulotkach, mapie i slajdach zawsze się zgadzają.
- **Wyjątek:** link do nawigacji w kodzie QR ulotka składa sama z gotowych
  pól `lat`/`lon` przystanku i toalety (sekcja „Kod QR”).
- **Do czasu gotowego skryptu** osoba od ulotek trzyma przykładowy rekord
  w `app/dane/ulotki.json` (lista z 2–3 rekordami, ręcznie wpisanymi według
  wzoru). Skrypt potem nadpisze ten plik.

**Uruchomienie:**

```bash
.venv/Scripts/python.exe src/ulotki_dane.py
.venv/Scripts/python.exe -m http.server 8000 -d app
# → http://localhost:8000/?id=4225-03
```

Serwer jest potrzebny, bo przeglądarka nie wczyta JSON-a przez `file://`.
`app/dane/ulotki.json` to pochodna otwartych danych (ok. 2–3 MB), więc można
go wrzucić do gita. Wtedy GitHub Pages działa od razu.

**Mapa na ulotce:** Leaflet 1.9.4 z cdnjs + kafelki OSM. Przed drukiem trzeba
poczekać, aż kafelki się wczytają (zdarzenie `load` warstwy), inaczej PDF
wyjdzie z szarą mapą. Regulamin kafelków OSM nie pozwala na masowe pobieranie,
więc na demo jest OK, ale przy druku całego miasta trzeba by użyć map miasta
(WMS z mapa.um.warszawa.pl) albo własnego serwera kafelków. Mówimy o tym na
prezentacji jako o kroku wdrożenia.

## Kolejność prac

Każdy krok kończy się czymś, co działa. Jeśli czas się skończy, oddajemy
ostatni działający krok.

| # | Krok | Czas | Wynik |
|---|---|---|---|
| 1 | `ulotki_dane.py`: najbliższa toaleta + alternatywa, parser godzin i `uwagi` | 1,5–2 h | `ulotki.json`, ręcznie sprawdzone 5 przystanków |
| 2 | Ulotka w HTML/CSS na sztywnych danych jednego przystanku | 1,5 h (równolegle z 1) | wygląd zatwierdzony przez drużynę, test wydruku w czerni i bieli |
| 3 | Podpięcie JSON + mapa Leaflet + wyszukiwarka | 1,5 h | dowolny przystanek → ulotka → PDF |
| 4 | Mapa luk dla urzędu + statystyki dzielnic | 1,5 h | slajd z liczbami i mapą |
| 5 | GitHub Pages + makieta ulotki na zdjęciu prawdziwego przystanku | 1 h | link dla jury, zdjęcie do prezentacji |
| 6 | *Opcjonalnie:* trasa piesza z OSRM (`routing.openstreetmap.de`, profil foot) tylko dla drukowanych przystanków | 2 h | prawdziwa odległość i trasa na mapie |
| 7 | *Opcjonalnie:* `ulotki_pdf.py` (Playwright), PDF-y dla całej dzielnicy | 1 h | „ulotki dla Woli w 2 minuty” na demo |

**Punkty kontrolne:** kroki 1–3 gotowe w sobotę do ok. 23:00. Kroki 4–5 do
niedzieli 8:00. **Zamrożenie kodu w niedzielę o 9:00.** Potem tylko
prezentacja i próba. Oddanie o 11:00.

**Podział ról (3 osoby, ustalony 17.10):**

- **Osoba 1 (Roman): dane + mapa.** Krok 1 (`ulotki.json`, z pomocą AI),
  potem krok 4 (mapa luk, statystyki dzielnic), opcjonalnie 6.
- **Osoba 2: ulotki.** Kroki 2–3 i kod QR, potem opcjonalnie 7. Do czasu
  gotowego `ulotki.json` pracuje na rekordzie z sekcji „Rekord w
  ulotki.json”.
- **Osoba 3: prezentacja i storytelling.** Scenariusz pitchu, slajdy, źródła
  z pliku 13, liczby z kroku 4, krok 5 (makieta ulotki na zdjęciu
  przystanku), próba prezentacji. Testy ulotki na kilkunastu przystankach
  (Wisła, tory, pętle) i pytania do mentora.

## Jak to wypada wobec kryteriów jury

- **Dane Warszawy (20%):** dwa zbiory z portalu, połączone w coś, czego żaden
  z nich osobno nie pokazuje.
- **Innowacyjność (25%):** nie „kolejna mapa toalet”, tylko informacja
  w miejscu, w którym senior czeka, bez telefonu. Do tego wniosek dla miasta:
  59% słupków nie ma w 500 m bezpłatnej, dostępnej toalety, a w niedzielę 74%.
- **Wdrożenie (20%):** gotowe PDF-y, koszt druku kilka zł za sztukę, działająca
  strona, numer 19115 do zgłaszania błędów.
- **Realia miasta (15%):** kampania „Toalety ratują życie” (Głos Seniora,
  15.10.2026), starzejące się miasto, upały.
- **Prezentacja (20%):** zdjęcie ulotki na prawdziwym przystanku + mapa luk.

## Decyzje do podjęcia przez drużynę

- [ ] Reguła wyboru toalety (główna + alternatywa) — czy przyjmujemy?
- [ ] Format: A4 czy A5?
- [x] Kod QR: tak, nawigacja piesza w Google Maps (sekcja „Kod QR”).
- [x] Dla kogo: wszyscy (mieszkańcy, turyści), teksty PL + EN; senior jako
  bohater opowieści.
- [ ] Czy robimy trasę pieszą (krok 6), czy zostajemy przy linii prostej × 1,3?

## Pytania do mentora

- Czy toalety „METRO” są dostępne bez biletu?
- Kto decyduje o tym, co wisi na przystankach (ZTM? operator wiat?) i czy
  dopuszcza ulotki innych instytucji?
- Czy miasto ma własny serwer map, z którego można drukować?
