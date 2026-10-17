# Generator ulotek „Najbliższa toaleta” — plan aplikacji

Stan: 17.10.2026. Plan budowy narzędzia z pomysłu
[13-toalety-przy-przystankach.md](13-toalety-przy-przystankach.md): dla każdego
słupka przystankowego generujemy ulotkę do wywieszenia, skierowaną głównie do
seniorów. Na ulotce: odległość do najbliższej toalety, mapa, czy toaleta jest
<<<<<<< HEAD
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
=======
płatna, czynna w niedzielę, całoroczna czy sezonowa, identyfikator przystanku,
kod QR z trasą w aplikacji i maskotka — syrenka, która „zaciska krok”.

## W skrócie

- **Ulotka działa na trzy sposoby:** mapa na papierze (seniorzy), kod QR
  z nawigacją pieszą w telefonie (kto nie radzi sobie z mapą), syrenka
  i piktogram WC (obcokrajowcy).
- **Ulotki dla wszystkich przystanków drukują się automatycznie:** jedno
  polecenie daje 18 PDF-ów, po jednym na dzielnicę, ok. 5000 stron A4.
- **Dwa widoki, jedna paczka danych.** Ulotka (dla pasażera) i mapa luk (dla
  urzędu) czytają ten sam plik `ulotki.json`.
- **Python liczy, przeglądarka rysuje.** Ulotka to HTML + CSS z mapą Leaflet.
  Ten sam szablon służy do podglądu, do druku pojedynczej ulotki i do druku
  wsadowego (Playwright).
- Stronę da się wystawić na GitHub Pages, więc jury może ją otworzyć samo.
  Ten sam adres obsługuje kody QR.
>>>>>>> 56d2340 (Plan dla tworzenia ulotek z odległością toalet.)

## Co jest na ulotce

Format **A4 pionowo** (mieści się w ramce rozkładu albo jako laminat na
słupku).

```
┌─────────────────────────────────────────────┐
<<<<<<< HEAD
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
=======
│ ┌────────┐  NAJBLIŻSZA TOALETA · WC          │
│ │SYRENKA │  Nearest toilet                   │
│ │ogon w  │                                   │
│ │supeł   │  Przystanek: Sympatyczna 03       │
│ └────────┘                       nr 4225-03  │
├─────────────────────────────────────────────┤
│          350 m  ·  ok. 8 min pieszo          │
│   Inwalidów 3, Biblioteka Publiczna          │
│   Wskazówka: wejście od ul. Piekarskiej      │
├─────────────────────────────────────────────┤
│   [ MAPA:  ● JESTEŚ TUTAJ   🚻 TOALETA ]     │
│   [ linia przerywana, nazwy ulic       ]     │
├─────────────────────────────────────────────┤
│ ✔ BEZPŁATNA          ✘ W NIEDZIELĘ NIECZYNNA │
│ ✔ CZYNNA CAŁY ROK    ✔ DLA WÓZKÓW            │
│ Godziny: pon.–pt. 9–19 · sob. 9–15           │
├─────────────────────────────────────────────┤
│ W niedzielę najbliższa czynna:               │
│ 900 m, ul. Przykładowa 5 (bezpłatna)         │
├─────────────────────────────────────────────┤
│ ┌──────┐  Zeskanuj telefonem —               │
│ │  QR  │  aplikacja poprowadzi Cię           │
│ │ 4 cm │  do toalety krok po kroku.          │
│ └──────┘  Scan for walking directions.       │
>>>>>>> 56d2340 (Plan dla tworzenia ulotek z odległością toalet.)
├─────────────────────────────────────────────┤
│ Dane: dane.um.warszawa.pl, toalety IV 2026   │
│ Błąd na ulotce? Zadzwoń 19115, podaj 4225-03 │
└─────────────────────────────────────────────┘
```

<<<<<<< HEAD
**Dwa języki bez utraty czytelności:** polski duży, angielski pod spodem
mniejszą czcionką (ok. połowa wielkości), szarym, ale nadal z wysokim
kontrastem. Liczby (350 m, 8 min) i ikony są wspólne dla obu języków, więc
nie dublujemy ich. Angielski tylko w nagłówkach i etykietach, nie w adresie.

| Pole | Skąd | Uwagi |
|---|---|---|
=======
| Pole | Skąd | Uwagi |
|---|---|---|
| Syrenka + nagłówek PL/EN | stałe | „WC” i piktogram są zrozumiałe w każdym języku; opis w sekcji „Maskotka” |
>>>>>>> 56d2340 (Plan dla tworzenia ulotek z odległością toalet.)
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
<<<<<<< HEAD
=======
| Kod QR | liczone | prowadzi do nawigacji pieszej; opis w sekcji „Kod QR z trasą” |
>>>>>>> 56d2340 (Plan dla tworzenia ulotek z odległością toalet.)
| Stopka | stałe | data danych + 19115 (Warszawskie Centrum Kontaktu) z numerem przystanku |

**Zasady czytelności dla seniorów:**

- Odległość to najważniejsza liczba na kartce: co najmniej 60 pt. Treść co
  najmniej 20 pt.
<<<<<<< HEAD
- Czarne na białym, wysoki kontrast. Druk w czerni i bieli też musi działać.
=======
- Czarne na białym, wysoki kontrast. Druk w czerni i bieli też musi działać,
  łącznie z syrenką i kodem QR.
>>>>>>> 56d2340 (Plan dla tworzenia ulotek z odległością toalet.)
- Nie polegamy na samym kolorze ani ikonach: zawsze ✔/✘ **i** słowo.
- Pełne słowa zamiast skrótów i żargonu („czynna”, a nie „otw.”).
- Mapa ustawiona na północ, z dużymi znacznikami i podpisami
  „JESTEŚ TUTAJ” i „TOALETA”.
<<<<<<< HEAD
- Kod QR to dodatek dla osób z telefonem (turyści, młodsi, opiekunowie).
  Ulotka musi działać **bez** telefonu, bo właśnie tym różni się od miejskich
  tabliczek „Mapa WC” z samym kodem QR (patrz plik 13).

## Kod QR: nawigacja do toalety

Kod QR na ulotce otwiera **pieszą nawigację od przystanku do toalety**
w Google Maps. Link w oficjalnym formacie Google Maps URLs, bez klucza API:
=======
- **Ulotka działa bez telefonu.** Kod QR jest dodatkiem dla tych, którzy wolą
  nawigację, a nie jedynym źródłem informacji. Tym różnimy się od miejskich
  tabliczek „Mapa WC” z samym kodem QR (patrz plik 13).

## Kod QR z trasą

Dla osób, które nie radzą sobie z mapą na papierze i wolą, żeby telefon
prowadził je krok po kroku.

**Dokąd prowadzi:** do krótkiego adresu na naszej stronie, np.
`https://<konto>.github.io/<repo>/t.html?id=4225-03`. Strona `t.html` wczytuje
mały plik `dane/trasy.json` (numer przystanku → współrzędne przystanku
i toalety, ok. 200 KB) i od razu przekierowuje do nawigacji pieszej
w Google Maps:
>>>>>>> 56d2340 (Plan dla tworzenia ulotek z odległością toalet.)

```
https://www.google.com/maps/dir/?api=1&origin=52.2103,20.91986&destination=52.2081,20.9214&travelmode=walking
```

<<<<<<< HEAD
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
=======
Ten format adresu Google Maps nie wymaga klucza API. Na telefonie otwiera się
aplikacja Map z gotową trasą, wystarczy nacisnąć „Start”. Pod
przekierowaniem `t.html` pokazuje też przyciski zapasowe: Google Maps,
OpenStreetMap, Apple Maps.

**Dlaczego przez naszą stronę, a nie od razu do Google Maps:**

- **Wydrukowany kod można zaktualizować.** Gdy toaleta zostanie zamknięta,
  wystarczy przeliczyć `trasy.json`, a stare ulotki zaczną prowadzić do nowej
  najbliższej toalety. Papier zostaje bez zmian.
- **Krótszy adres to mniejszy i prostszy kod QR,** łatwiejszy do zeskanowania
  starszym telefonem.
- Możemy policzyć skanowania (licznik odwiedzin), co daje dowód na
  prezentacji wdrożenia albo w pilotażu.
- Ryzyko: gdy nasza strona przestanie działać, kody przestaną prowadzić
  dokądkolwiek. Docelowo adres powinien być w domenie miasta (pytanie do
  mentora).

**Wymagania techniczne:**

- Bok co najmniej **4 cm**, margines wokół kodu (quiet zone), korekcja błędów
  M. Kod musi się zeskanować z ok. 40 cm.
- Generowany w przeglądarce biblioteką JS (np. `qrcodejs` z cdnjs). Działa
  offline, więc nie spowalnia druku wsadowego.
- Test przed oddaniem: wydruk w czerni i bieli, skan trzema różnymi
  telefonami (w tym starszym Androidem).

## Maskotka: syrenka zaciskająca krok

Cel: obcokrajowiec w sekundę rozumie, że kartka dotyczy toalety, nawet gdy
nie zna polskiego. Syrenka przy okazji mówi „to jest Warszawa”, co dobrze
wygląda na prezentacji.

**Projekt:**

- **Syrenka ma ogon, nie nogi.** Gest „zaciskam krok” trzeba więc oddać inaczej:
  ogon skręcony w supeł albo spleciony, zaciśnięte dłonie, zaniepokojona
  mina, kropla potu.
- Zamiast miecza i tarczy z herbu proponujemy **tarczę z piktogramem WC**.
  Odwołuje się do herbu, a jednocześnie wprost mówi „toaleta”.
- Sama maskotka nie wystarczy: obcokrajowiec może nie znać syrenki. Dlatego
  zawsze stoi obok napisu „WC” i angielskiego „Nearest toilet”.
- Styl: gruby czarny kontur, mało szczegółów, czytelna w czerni i bieli przy
  ok. 5 cm na A4.
- Ta sama syrenka jako logo strony, favicon i postać na slajdach.

**Wykonanie:** jeden plik `app/img/syrenka.svg`. Szkic z generatora obrazów
albo ręcznie, potem wektoryzacja (np. Inkscape → „Trace Bitmap”). Czas
ok. 1–1,5 h dla osoby od projektu. Plan B: standardowy piktogram WC zamiast
syrenki. Ulotka bez maskotki nadal działa.

**Uwaga prawna:** rysujemy własną syrenkę, nie kopię herbu Warszawy (syrenka
na czerwonej tarczy z koroną). Używanie herbu jest uregulowane przez miasto.
Na hackaton wystarczy własny rysunek. Przy wdrożeniu o wyglądzie zdecyduje
miasto (pytanie do mentora).
>>>>>>> 56d2340 (Plan dla tworzenia ulotek z odległością toalet.)

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

<<<<<<< HEAD
=======
Kod QR prowadzi do toalety głównej. Wyjątek: gdy główna jest sezonowa i poza
sezonem, prowadzi do alternatywy (sprawdzane w `t.html` w chwili skanowania).

## Druk dla wszystkich przystanków

Jedno polecenie generuje ulotki dla całego miasta:

```bash
.venv/Scripts/python.exe src/ulotki_pdf.py --wszystkie        # ok. 5000 stron
.venv/Scripts/python.exe src/ulotki_pdf.py --dzielnica Wola   # jedna dzielnica
.venv/Scripts/python.exe src/ulotki_pdf.py --id 4225-03       # jeden przystanek
```

**Jak działa `ulotki_pdf.py`:**

1. Uruchamia w tle lokalny serwer HTTP dla katalogu `app/`.
2. Otwiera Chromium przez Playwright i ładuje `druk.html?dzielnica=Wola&od=0&ile=50`.
   To strona z 50 ulotkami, każda na osobnej stronie A4 (`break-after: page`).
3. Czeka, aż strona ustawi `window.gotowe = true`, czyli gdy wszystkie mapy
   wczytają kafelki, a kody QR się wygenerują. Limit czasu: 60 s na paczkę.
4. Zapisuje paczkę `page.pdf(format="A4", print_background=True)`.
5. Skleja paczki w jeden plik na dzielnicę (`pypdf`):
   `data/out/ulotki/Wola.pdf`.
6. Zapisuje `data/out/ulotki/spis.csv`: numer przystanku, nazwa, dzielnica,
   plik, numer strony. Ekipa rozwieszająca wie, która kartka gdzie idzie.
7. Na końcu sprawdza, czy liczba stron = liczba słupków, i wypisuje
   przystanki, dla których mapa się nie wczytała (do ponownego wydruku).

**Dlaczego paczki po 50:** 5000 map Leaflet na jednej stronie zabije
przeglądarkę, a 5000 osobnych otwarć strony trwa godzinami. Paczki po 50 to
ok. 100 przebiegów, szacunkowo poniżej godziny dla całego miasta. Pełny
przebieg puszczamy w nocy w tle.

**Kolejność w PDF:** dzielnica → nazwa zespołu → numer słupka. Słupki tego
samego zespołu leżą obok siebie, więc da się je rozwieszać po kolei.

**Przypisanie dzielnicy:** przystanki nie mają pola z dzielnicą. Bierzemy
granice 18 dzielnic z OSM (jeden plik GeoJSON, `admin_level=9`) i sprawdzamy,
w której leży słupek (punkt w wielokącie). Przy okazji odpadają słupki spoza
Warszawy, lepiej niż obecnym prostokątem.

**Kafelki mapy przy druku masowym:** regulamin serwerów kafelków OSM zabrania
masowego pobierania, a 5000 ulotek to dziesiątki tysięcy kafelków. Do druku
wsadowego trzeba innego źródła:

- **Na hackaton (zalecane):** darmowy klucz MapTiler (limit miesięczny
  wystarcza na jeden pełny przebieg). Klucz w `.env` jako `MAPTILER_KEY`,
  skrypt przekazuje go stronie. Nigdy nie wpisujemy go do kodu.
- **Docelowo:** własny wycinek map Warszawy w pliku PMTiles (Protomaps), bez
  zewnętrznego serwera i limitów. Albo serwer map miasta.
- Podgląd pojedynczej ulotki na stronie może korzystać z kafelków OSM.

**Nowe zależności** (do `requirements.txt`): `playwright` (+ jednorazowo
`playwright install chromium`) i `pypdf`. Potrzebne tylko do druku wsadowego,
podgląd na stronie ich nie wymaga.

>>>>>>> 56d2340 (Plan dla tworzenia ulotek z odległością toalet.)
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
<<<<<<< HEAD
  tego dochodzi alternatywa.
- **Linia prosta przez Wisłę i tory.** Najbliższa toaleta w linii prostej może
  być po drugiej stronie rzeki albo torów. Na demo wybieramy sprawdzone
  przystanki. Docelowo trasa piesza (krok 6).
- Słupki spoza Warszawy: obecny skrypt odcina je prostokątem. Na ulotki
  lepiej wziąć granicę miasta z OSM (jeden plik GeoJSON).
=======
  tego dochodzi alternatywa i aktualizowany kod QR.
- **Linia prosta przez Wisłę i tory.** Najbliższa toaleta w linii prostej może
  być po drugiej stronie rzeki albo torów. Kod QR częściowo to łagodzi (Google
  Maps poprowadzi prawdziwą trasą), ale odległość na papierze będzie
  zaniżona. Na demo wybieramy sprawdzone przystanki.
>>>>>>> 56d2340 (Plan dla tworzenia ulotek z odległością toalet.)
- 54 toalety typu „toaleta METRO”: nie wiemy, czy są przed bramkami, czy za
  nimi. Pytanie do mentora.

## Architektura

```
<<<<<<< HEAD
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
=======
data/raw/male/{przystanki,toalety}.json  +  granice dzielnic (OSM GeoJSON)
            │
            ▼
src/ulotki_dane.py ──► app/dane/ulotki.json  (pełne dane ulotek, ok. 5000)
                   └─► app/dane/trasy.json   (id → współrzędne, dla QR)
                              │
       ┌──────────────────────┼──────────────────────┐
       ▼                      ▼                      ▼
 app/index.html          app/druk.html          app/mapa.html
 wyszukiwarka →          50 ulotek na stronę    mapa luk dla urzędu,
 podgląd ulotki →        dla druku wsadowego    statystyki dzielnic
 „Drukuj / PDF”                │
                               ▼
                    src/ulotki_pdf.py (Playwright)
                    → data/out/ulotki/<dzielnica>.pdf + spis.csv

 app/t.html — cel kodu QR: przekierowanie do nawigacji pieszej
>>>>>>> 56d2340 (Plan dla tworzenia ulotek z odległością toalet.)
```

**Pliki:**

| Plik | Co robi |
|---|---|
<<<<<<< HEAD
| `src/ulotki_dane.py` | wczytuje dane (funkcje z `luka_toaletowa.py`), dla każdego słupka liczy główną toaletę i alternatywę, parsuje godziny i sezon, zapisuje JSON |
| `app/index.html` + `ulotka.js` | pole „wpisz nazwę lub nr przystanku” (`?id=4225-03` w URL-u), render ulotki |
| `app/ulotka.css` | wygląd ulotki, `@page { size: A4 }`, ukrycie interfejsu przy druku |
| `app/mapa.html` | mapa luk + liczby na slajd (59% / 74%, patrz plik 13) |
| `src/ulotki_pdf.py` | opcjonalnie: wsadowe PDF-y (`--dzielnica Wola`) |
=======
| `src/ulotki_dane.py` | wczytuje dane (funkcje z `luka_toaletowa.py`), przypisuje dzielnice, liczy główną toaletę i alternatywę, parsuje godziny i sezon, zapisuje oba JSON-y |
| `app/ulotka.js` + `ulotka.css` | **jeden szablon ulotki** (mapa, QR, syrenka), używany przez `index.html` i `druk.html`; `@page { size: A4 }` |
| `app/index.html` | pole „wpisz nazwę lub nr przystanku” (`?id=4225-03`), podgląd, przycisk druku |
| `app/druk.html` | wiele ulotek na stronę, sygnał `window.gotowe` dla Playwright |
| `app/t.html` | cel kodu QR, przekierowanie do Google Maps + przyciski zapasowe |
| `app/mapa.html` | mapa luk + liczby na slajd (59% / 74%, patrz plik 13) |
| `app/img/syrenka.svg` | maskotka |
| `src/ulotki_pdf.py` | druk wsadowy: paczki → PDF na dzielnicę + `spis.csv` |
>>>>>>> 56d2340 (Plan dla tworzenia ulotek z odległością toalet.)

**Rekord w `ulotki.json`:**

```json
{
<<<<<<< HEAD
  "id": "4225-03", "nazwa": "Sympatyczna", "lat": 52.2103, "lon": 20.91986,
=======
  "id": "4225-03", "nazwa": "Sympatyczna", "dzielnica": "Wola",
  "lat": 52.2103, "lon": 20.91986,
>>>>>>> 56d2340 (Plan dla tworzenia ulotek z odległością toalet.)
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

<<<<<<< HEAD
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
=======
**Uruchomienie podglądu:**
>>>>>>> 56d2340 (Plan dla tworzenia ulotek z odległością toalet.)

```bash
.venv/Scripts/python.exe src/ulotki_dane.py
.venv/Scripts/python.exe -m http.server 8000 -d app
# → http://localhost:8000/?id=4225-03
```

Serwer jest potrzebny, bo przeglądarka nie wczyta JSON-a przez `file://`.
<<<<<<< HEAD
`app/dane/ulotki.json` to pochodna otwartych danych (ok. 2–3 MB), więc można
go wrzucić do gita. Wtedy GitHub Pages działa od razu.

**Mapa na ulotce:** Leaflet 1.9.4 z cdnjs + kafelki OSM. Przed drukiem trzeba
poczekać, aż kafelki się wczytają (zdarzenie `load` warstwy), inaczej PDF
wyjdzie z szarą mapą. Regulamin kafelków OSM nie pozwala na masowe pobieranie,
więc na demo jest OK, ale przy druku całego miasta trzeba by użyć map miasta
(WMS z mapa.um.warszawa.pl) albo własnego serwera kafelków. Mówimy o tym na
prezentacji jako o kroku wdrożenia.
=======
Pliki w `app/dane/` to pochodne otwartych danych (kilka MB), więc można je
wrzucić do gita. Wtedy GitHub Pages i kody QR działają od razu. Wygenerowane
PDF-y (`data/out/`) zostają poza gitem.
>>>>>>> 56d2340 (Plan dla tworzenia ulotek z odległością toalet.)

## Kolejność prac

Każdy krok kończy się czymś, co działa. Jeśli czas się skończy, oddajemy
ostatni działający krok.

| # | Krok | Czas | Wynik |
|---|---|---|---|
<<<<<<< HEAD
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
=======
| 1 | `ulotki_dane.py`: dzielnice, najbliższa toaleta + alternatywa, parser godzin i `uwagi`, oba JSON-y | 2 h | sprawdzone ręcznie 5 przystanków |
| 2 | Szablon ulotki w HTML/CSS na sztywnych danych, z miejscem na QR i syrenkę | 1,5 h (równolegle z 1) | wygląd zatwierdzony, test wydruku w czerni i bieli |
| 3 | Syrenka: szkic → SVG | 1–1,5 h (równolegle) | `syrenka.svg`; plan B: piktogram WC |
| 4 | Podpięcie JSON + mapa Leaflet + kod QR + `t.html` + wyszukiwarka | 2 h | dowolny przystanek → ulotka → PDF; QR otwiera trasę w telefonie |
| 5 | `druk.html` + `ulotki_pdf.py`, klucz MapTiler | 2 h | PDF dla jednej dzielnicy; w nocy pełny przebieg dla miasta |
| 6 | Mapa luk dla urzędu + statystyki dzielnic | 1,5 h | slajd z liczbami i mapą |
| 7 | GitHub Pages + makieta ulotki na zdjęciu prawdziwego przystanku | 1 h | link dla jury, zdjęcie do prezentacji |
| 8 | *Opcjonalnie:* trasa piesza z OSRM (`routing.openstreetmap.de`, profil foot) zamiast linii prostej × 1,3 | 2 h | prawdziwa odległość na papierze |

**Punkty kontrolne:** kroki 1–4 gotowe w sobotę do ok. 23:00. Krok 5 do
północy, a pełny druk miasta puszczony w tle na noc. Kroki 6–7 do niedzieli
8:00. **Zamrożenie kodu w niedzielę o 9:00.** Potem tylko prezentacja
i próba. Oddanie o 11:00.

**Na demo:** gotowy PDF całego miasta („5000 ulotek, 18 plików”) plus na żywo
wydruk jednego przystanku i skan kodu QR telefonem. Pełnego przebiegu na żywo
nie puszczamy, bo trwa za długo.

**Podział ról (3–5 osób):**

- **Dane:** krok 1, potem 8.
- **Front:** kroki 2 i 4, potem 5 (razem z osobą od danych).
- **Projekt:** krok 3 (syrenka), wygląd ulotki z krokiem 2, makieta z kroku 7.
- **Mapa luk + prezentacja:** kroki 6–7, liczby, źródła z pliku 13, scenariusz
  pitchu.
- **Wolna osoba:** testy na kilkunastu przystankach (Wisła, tory, pętle), skan
  QR różnymi telefonami, pytania do mentora.
>>>>>>> 56d2340 (Plan dla tworzenia ulotek z odległością toalet.)

## Jak to wypada wobec kryteriów jury

- **Dane Warszawy (20%):** dwa zbiory z portalu, połączone w coś, czego żaden
  z nich osobno nie pokazuje.
- **Innowacyjność (25%):** nie „kolejna mapa toalet”, tylko informacja
<<<<<<< HEAD
  w miejscu, w którym senior czeka, bez telefonu. Do tego wniosek dla miasta:
  59% słupków nie ma w 500 m bezpłatnej, dostępnej toalety, a w niedzielę 74%.
- **Wdrożenie (20%):** gotowe PDF-y, koszt druku kilka zł za sztukę, działająca
  strona, numer 19115 do zgłaszania błędów.
- **Realia miasta (15%):** kampania „Toalety ratują życie” (Głos Seniora,
  15.10.2026), starzejące się miasto, upały.
- **Prezentacja (20%):** zdjęcie ulotki na prawdziwym przystanku + mapa luk.
=======
  w miejscu, w którym się czeka, dla trzech grup naraz: papier dla seniorów,
  QR z nawigacją dla tych, którzy wolą telefon, syrenka dla obcokrajowców.
  Do tego wniosek dla miasta: 59% słupków nie ma w 500 m bezpłatnej, dostępnej
  toalety, a w niedzielę 74%.
- **Wdrożenie (20%):** gotowe PDF-y dla wszystkich przystanków z jednego
  polecenia, spis do rozwieszania, kody QR aktualizowane bez przedruku, numer
  19115 do zgłaszania błędów.
- **Realia miasta (15%):** kampania „Toalety ratują życie” (Głos Seniora,
  15.10.2026), starzejące się miasto, upały, turyści.
- **Prezentacja (20%):** syrenka jako bohaterka pitchu, zdjęcie ulotki na
  prawdziwym przystanku, skan QR na żywo, mapa luk.
>>>>>>> 56d2340 (Plan dla tworzenia ulotek z odległością toalet.)

## Decyzje do podjęcia przez drużynę

- [ ] Reguła wyboru toalety (główna + alternatywa) — czy przyjmujemy?
<<<<<<< HEAD
- [ ] Format: A4 czy A5?
- [x] Kod QR: tak, nawigacja piesza w Google Maps (sekcja „Kod QR”).
- [x] Dla kogo: wszyscy (mieszkańcy, turyści), teksty PL + EN; senior jako
  bohater opowieści.
- [ ] Czy robimy trasę pieszą (krok 6), czy zostajemy przy linii prostej × 1,3?
=======
- [ ] Format: A4 czy A5? (A5 to ok. 2× mniej papieru, ale mniejsza mapa i QR)
- [ ] Wygląd syrenki: ogon w supeł + tarcza z WC?
- [ ] Źródło kafelków do druku masowego: MapTiler na hackaton?
- [ ] Czy robimy trasę pieszą (krok 8), czy zostajemy przy linii prostej × 1,3?
>>>>>>> 56d2340 (Plan dla tworzenia ulotek z odległością toalet.)

## Pytania do mentora

- Czy toalety „METRO” są dostępne bez biletu?
- Kto decyduje o tym, co wisi na przystankach (ZTM? operator wiat?) i czy
  dopuszcza ulotki innych instytucji?
- Czy miasto ma własny serwer map, z którego można drukować?
<<<<<<< HEAD
=======
- Czy kody QR mogłyby prowadzić do adresu w domenie miasta?
- Czy własna syrenka (nie herb) na materiałach informacyjnych jest w porządku?
>>>>>>> 56d2340 (Plan dla tworzenia ulotek z odległością toalet.)
