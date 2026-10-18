# Toaleta w zasięgu przystanku — pomysł na hackaton

Stan: 17.10.2026. Wyzwanie: **Twój ruch**. Pomysł alternatywny albo
uzupełniający wobec „Upału na przystankach”
([12-upal-na-przystankach.md](12-upal-na-przystankach.md)). Nie jest jeszcze
wybrany — decyzja trafi do sekcji „Decyzje drużyny” w [AGENTS.md](../AGENTS.md).

## W skrócie

Seniorzy w upale piją za mało: słabiej czują pragnienie, a część celowo
ogranicza picie, bo boi się, że poza domem nie znajdzie toalety. Sprawdzamy,
z ilu warszawskich przystanków da się w ciągu ok. 10 minut dojść do toalety,
z której senior naprawdę skorzysta (bezpłatnej, dostępnej, otwartej). Dla
każdego przystanku generujemy gotową do druku tabliczkę „najbliższa toaleta”.

## Problem

- W upale seniorzy (i dzieci) odwadniają się szybciej.
- **Teza:** seniorzy nie wychodzą z domu albo wychodzą (np. do lekarza) bez
  wody i piją mniej, bo nie wiedzą, gdzie po drodze jest toaleta.
- Teza ma dwa ogniwa i oba mają oparcie w źródłach (sekcja niżej):
  1. seniorzy słabo odczuwają pragnienie, także w upale;
  2. seniorzy ograniczają picie z obawy, że nie zdążą do toalety, a brak
     publicznych toalet to pogłębia.
- Nie znaleźliśmy badania, które łączy wprost upał, toalety i wychodzenie
  z domu. Na prezentacji mówimy „łączymy dwa udokumentowane zjawiska”, bez
  wymyślonych procentów.

## Źródła

### Polska

**Głos Seniora (Stowarzyszenie MANKO), 15.10.2026:**
[„Toalety ratują życie! Głos Seniora walczy z wykluczeniem toaletowym i cyfrowym seniorów”](https://glosseniora.pl/2026/10/15/toalety-ratuja-zycie-glos-seniora-walczy-z-wykluczeniem-toaletowym-i-cyfrowym-seniorow/)

- Ogólnopolska kampania „Toalety ratują życie”: więcej bezpłatnych toalet
  publicznych, zmiana przepisów, dostępność dla osób z ograniczeniami
  ruchowymi.
- **20% seniorów przed wyjściem z domu sprawdza, czy na trasie można
  skorzystać z toalety.** Artykuł nie podaje źródła tej liczby — przed
  slajdem zapytać organizację albo podawać „według Głosu Seniora”.
- Ponad 3,5 mln osób w Polsce zmaga się z nietrzymaniem moczu, ryzyko
  rośnie z wiekiem.
- Cytaty (Łukasz Salwarowski, prezes):
  - „Jeżeli nie zapewnimy do nich dostępu, zamykamy osobę w czterech
    ścianach.”
  - „Samo istnienie toalety nie wystarczy, jeśli senior nie może z niej
    samodzielnie i bezpiecznie skorzystać.”
- **Wykluczenie cyfrowe:** toalety płatne tylko kartą, automatyczne drzwi,
  bilety i zniżki tylko w aplikacji. Postulat: obok rozwiązań cyfrowych
  zachować tradycyjne.
- Artykuł nie mówi o upale ani o Warszawie.

**Co z tego bierzemy:** kampania jest świeża (2 dni przed hackatonem), więc
temat jest aktualny. Wątek wykluczenia cyfrowego to najmocniejszy argument
za **fizyczną tabliczką na przystanku** zamiast kolejnej aplikacji.
Stowarzyszenie to naturalny partner przy wdrożeniu.

### Badania zagraniczne

- **Bhanu C., Avgerinou C., Kharicha K. i in. (2020).** „I've never drunk
  very much water and I still don't, and I see no reason to do so”: a
  qualitative study of the views of community-dwelling older people and
  carers on hydration in later life. *Age and Ageing*, 49(1), 111–118.
  [doi:10.1093/ageing/afz141](https://pmc.ncbi.nlm.nih.gov/articles/PMC6911653)
  (pełny tekst za darmo).
  - UCL, wywiady z 24 seniorami mieszkającymi samodzielnie i 9 opiekunami.
  - „Many older people experienced fear of incontinence leading to a highly
    restrictive pattern of fluid consumption. This was compounded by lack of
    access to public toilets.”
  - Seniorzy piją, gdy czują pragnienie, a to w późnym wieku „a known
    unreliable prompt”, także w upale.
  - Badanie jakościowe: pokazuje, że zjawisko istnieje, nie mówi, jak jest
    częste.
- **University of Melbourne (2007)**: starsi mężczyźni piją mniej niż
  młodzi przy tym samym odwodnieniu; autorzy łączą to z odwadnianiem się
  seniorów w falach upałów.
  [Opis: HealthDay](https://www.healthday.com/health-news/general-health/lack-of-strong-thirst-signals-leads-elderly-to-drink-too-little-610976.html)
- **Age Cymru (2012)**, opinia dla parlamentu Walii: seniorzy ograniczają
  picie, żeby uniknąć „wpadki” poza domem; brak toalet zniechęca do
  wychodzenia i skraca czas poza domem.
  [Age Cymru](https://www.agecymru.wales/latest-news/archive/age-cymru-gives-evidence-to-senedd-public-toilet-debate/)

## Dane

Oba zbiory są w portalu miasta (opis: [08-opis-zbiorow.md](08-opis-zbiorow.md)):

| Zbiór | Co mamy |
|---|---|
| Przystanki | 6988 słupków: zespół, słupek, nazwa, współrzędne |
| Toalety | 695 toalet (aktualizacja: kwiecień 2026): położenie, dzielnica, typ, zarządca, godziny otwarcia, dostępność dla osób z niepełnosprawnością (400), płatność (58 płatnych), przewijak; 261 całodobowych |

Pułapki:

- Część toalet jest **sezonowa** („do 31 października”) — przy liczeniu
  w październiku trzeba to uwzględnić, a latem (kiedy jest upał) wynik
  będzie inny. Liczymy wariant „lato” i „teraz”.
- Nie wiemy, czy zbiór mówi, **jak** się płaci (moneta, karta). Sprawdzić
  w danych — to ważne przy wykluczeniu cyfrowym.

## Rozwiązanie

### Część 1: luka toaletowa (analiza)

Dla każdego przystanku sprawdzamy, czy w zasięgu **600 m pieszo** po
chodnikach (10 minut tempem seniora 1,0 m/s; do 18.10 liczyliśmy 500 m
w linii prostej) jest toaleta, która jest:

- bezpłatna,
- dostępna dla osób z niepełnosprawnością,
- otwarta (o danej porze, w danym sezonie).

Jeśli nie ma — przystanek ma **lukę**. Wynik:

- jedno zdanie na slajd, np. „X% przystanków nie ma dostępnej, bezpłatnej
  toalety w zasięgu 10 minut” (liczbę policzymy),
- mapa luk,
- porównanie dzielnic.

Od 18.10 mapa luk i ulotki liczą odległość tak samo: prawdziwa trasa piesza
po chodnikach OSM (docs/14, sekcja „Trasy piesze”).

### Część 2: generator tabliczek (wdrożenie)

Skrypt tworzy dla każdego przystanku plik do druku:

```
┌─────────────────────────────────┐
│  🚻  NAJBLIŻSZA TOALETA         │
│                                 │
│  → 350 m  ·  ok. 5 min pieszo   │
│  ul. Przykładowa 12 (park)      │
│                                 │
│  bezpłatna · ♿ dostępna         │
│  czynna 6:00–22:00              │
│  [mała mapka z trasą]           │
└─────────────────────────────────┘
```

Na przystanku z luką tabliczka pokazuje najbliższą toaletę, nawet jeśli jest
daleko (np. „1,2 km”) — to sygnał dla miasta, gdzie brakuje toalet.

### Czego nie robimy

- **Rankingu jakości toalet.** Nie mamy danych o czystości ani ocen.
  Zamiast tego filtry na mapie: bezpłatna, dostępna, otwarta teraz.
- **Aplikacji dla seniorów.** Wykluczenie cyfrowe (Głos Seniora) — stawiamy
  na tabliczkę.
- ~~Dzieci jako drugiej grupy.~~ Zmiana 17.10: ulotka jest dla wszystkich
  (PL + EN, QR z nawigacją), ale w opowieści bohaterem zostaje senior, żeby
  nie rozmywać przekazu. Szczegóły: [14-plan-generatora-ulotek.md](14-plan-generatora-ulotek.md).

## Ocena wobec kryteriów jury (szacunki)

| Kryterium | Ocena | Dlaczego |
|---|---|---|
| Dane Warszawy 20% | mocne | oba zbiory z portalu miasta, bez danych spoza |
| Innowacyjność 25% | średnie → dobre | sama mapa toalet istnieje (Google, mapa miasta); nowe są luka i tabliczki generowane dla wszystkich przystanków |
| Wdrożenie 20% | dobre | gotowe pliki do druku; ZTM i tak wiesza informacje na przystankach |
| Realia miasta 15% | dobre | świeża kampania Głosu Seniora, starzejące się miasto, upały |
| Prezentacja 20% | dobre | wizualizacja tabliczki na prawdziwym przystanku + mapa luk |

Ryzyko: technicznie projekt jest prosty (kilka godzin). To zaleta przy
22 h, ale jury może uznać go za „za mały”. Dlatego luka i tabliczki są
obowiązkowe, nie opcjonalne.

## Związek z „Upałem na przystankach”

Toalety mogą być **jedną warstwą** wspólnego projektu „Upał w podróży”:
cień na przystanku + toaleta w zasięgu. To też zabezpieczenie: jeśli
symulacja cienia nie zadziała do rana, warstwa toalet i tak daje coś do
pokazania.

## Plan pracy

1. Pobrać toalety i przystanki do `data/raw/` (oba to małe zbiory).
2. Policzyć najbliższą toaletę dla każdego słupka, z filtrami → luka
   (wariant „lato” i „teraz”).
3. Mapa luk (folium) + statystyki po dzielnicach.
4. Szablon tabliczki (HTML → PDF) i generator dla wszystkich słupków.
5. Wizualizacja tabliczki na zdjęciu przystanku, slajdy.

## Wyniki wstępne (17.10, wieczór)

Skrypt: `src/luka_toaletowa.py` (parametr `--promien`). Odległość w linii
prostej, 5127 słupków w prostokącie wokół toalet (przybliżenie granic
Warszawy). Po chodnikach będzie gorzej.

„Dla seniora” = bezpłatna, dostępna dla osób z niepełnosprawnością, nie toi-toi.

| Wariant toalety | Ile toalet | Słupki bez toalety w 500 m | Mediana odległości |
|---|---|---|---|
| dowolna | 695 | 44% | 421 m |
| dla seniora | 291 | **59%** | 630 m |
| dla seniora, czynna w niedzielę | 137 | 74% | 984 m |

**Aktualizacja 17.10, wieczór** (linia prosta — nieaktualne, liczby na
slajd są niżej, w aktualizacji 18.10). Prostokąt
łapał też przystanki podmiejskie (daleko od miejskich toalet). Z granicami
dzielnic (`src/ulotki_dane.py`, mapa luk w `app/mapa.html`) zostaje **4433
słupki** w Warszawie i luka jest mniejsza:

| Wariant toalety | Słupki bez toalety w 500 m | Mediana odległości |
|---|---|---|
| dowolna | 35% | 350 m |
| bezpłatna | 36% | 362 m |
| dla seniora | **52%** | 524 m |
| dla seniora, czynna w niedzielę | **70%** | 809 m |

Najgorzej (dla seniora, 500 m): Wesoła 79%, Wawer 76%, Rembertów 70%,
Białołęka 68%. Granice dzielnic są uproszczone, więc pojedyncze słupki przy
granicy mogą trafić do sąsiedniej dzielnicy (np. Dw. Centralny 03 → Wola).

**Aktualizacja 18.10 — odległości piesze, liczby na slajd bierzemy stąd.**
Mapa luk liczy jak ulotki: trasa piesza po chodnikach OSM (OSRM), próg
**600 m pieszo** = 10 minut tempem seniora 1,0 m/s. Kategorie toalet
zmienione tego samego dnia: każda to jedno kryterium. 4433 słupki:

| Kategoria toalety | Ile toalet | Słupki bez toalety w 600 m pieszo | Mediana odległości pieszo |
|---|---|---|---|
| wszystkie | 695 | 40% (1780) | 478 m |
| bezpłatna | 637 | 41% (1809) | 492 m |
| dla osób z niepełnosprawnością (dostępna dla wózków) | 400 | **51%** (2258) | 613 m |
| czynna w niedzielę | 438 | **52%** (2311) | 629 m |

Dla porównania, przy 500 m pieszo: 48% / 49% / 60% / 60%.

Najgorzej (600 m pieszo):

- dla osób z niepełnosprawnością: Wesoła 80%, Wawer 79%, Ursus 71%,
  Rembertów 70%, Bemowo 68%,
- czynna w niedzielę: Wawer 90%, Wilanów 74%, Bemowo 74%, Białołęka 72%,
- wszystkie: Wawer 76%, Bemowo 59%, Białołęka 58%, Ursynów 53%.

Dawna kategoria „dla seniora” (bezpłatna + dostępna + nie toi-toi, 291
toalet) dawała przy 600 m pieszo 57%, a w niedzielę 73% — tych kategorii
nie ma już na mapie.

- 213 z 695 toalet to przenośne (toi-toi). Co najmniej 84 toalety są
  sezonowe (m.in. „do 31 października”), ale prawie wszystkie to toi-toie —
  w wariancie „dla seniora” sezonowość prawie nic nie zmienia.
- Zbiór **nie mówi, jak się płaci** — jest tylko `platnosc` 0/1.

**Konkurencja:** w lutym 2026 miasto (Centrum Komunikacji Społecznej)
powiesiło 350 tabliczek „Mapa WC” z kodem QR, głównie na latarniach
w najruchliwszych miejscach
([Spider's Web](https://spidersweb.pl/2026/02/warszawa-kod-qr-tabliczki-toalety.html)).
Pokazują tylko QR — bez kierunku i odległości, nie na przystankach. To
dokładnie wykluczenie cyfrowe, które krytykuje Głos Seniora; nasza tabliczka
musi działać bez telefonu.

## Otwarte pytania

- ~~Czy zbiór toalet mówi, jak się płaci (karta / moneta)?~~ Nie.
- Skąd liczba 20% w artykule Głosu Seniora?
- Kto w mieście odpowiada za informację na przystankach (ZTM) i za toalety
  (różni zarządcy) — do kogo kierujemy rekomendację?
- Czy łączymy z „Upałem na przystankach”, czy to osobny projekt?
