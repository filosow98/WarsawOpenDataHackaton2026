# Co zawierają zbiory danych Warszawy

Opis 23 zbiorów z katalogu https://dane.um.warszawa.pl/pl/catalogue: co jest w każdym
z nich i ile danych udostępnia miasto. Stan na 13–16.10.2026.

Przy każdym zbiorze są dwie informacje:
- **Całość:** co udostępnia portal.
- **Mamy:** co już pobraliśmy.

Zbiory oznaczone ⏱ pokazują tylko stan bieżący. API nie przechowuje historii, więc do
analizy zmian w czasie trzeba je pobierać samodzielnie co jakiś czas.

---

## Aktywni mieszkańcy

### Budżet obywatelski
Projekty zgłoszone przez mieszkańców i wybrane do realizacji w ramach budżetu
obywatelskiego. Każdy projekt ma:
- tytuł, opis i uzasadnienie,
- dzielnicę, opis miejsca i punkty na mapie,
- koszt całkowity i wstępny kosztorys,
- kategorie tematyczne (np. zieleń, edukacja, komunikacja) i grupy odbiorców (dzieci, seniorzy…),
- informację, czy projekt jest ogólnomiejski czy dzielnicowy,
- datę zgłoszenia, komentarze mieszkańców i link do strony projektu.

Zawiera też imię i nazwisko autora projektu.

- **Całość:** kolejne edycje budżetu, osobno projekty zrealizowane i będące w realizacji.
  Nie sprawdzaliśmy, od którego roku sięgają dane.
- **Mamy:** edycję „na rok 2025”: 228 projektów zrealizowanych i 61 w realizacji,
  łącznie ok. 100 mln zł.
- **Uwaga:** liczba głosów jest w danych zawsze równa 0, więc wyników głosowania z tego zbioru nie odczytamy.

### Konsultacje społeczne
Konsultacje prowadzone przez urząd w serwisie konsultacje.um.warszawa.pl. Każda konsultacja ma:
- tytuł i opis (czego dotyczy, cel zmian),
- termin rozpoczęcia i zakończenia,
- kategorię tematyczną,
- adresatów (mieszkańcy albo organizacje pozarządowe),
- zdjęcie i link do strony.

Przykładowe tematy: uchwała krajobrazowa, komunikacja po otwarciu nowych stacji metra,
wycinka pomników przyrody.

- **Całość:** konsultacje opublikowane obecnie w serwisie. ⏱
- **Mamy:** wszystko, czyli 7 konsultacji (stan z 13.10.2026).

### Konsultacje społeczne — dzielnice
Słownik 18 dzielnic z adresem urzędu każdej dzielnicy, uzupełniony o pozycję dla całego miasta.
Służy do łączenia ze zbiorem konsultacji.
- **Całość = mamy:** 19 pozycji.

### Konsultacje społeczne — kategorie
Słownik 10 kategorii tematycznych konsultacji (np. plany miejscowe, przestrzeń publiczna,
sport i rekreacja).
- **Całość = mamy:** 10 kategorii.

### Trasy turystyczne
Wybrane trasy spacerowe po Warszawie, np. „Śladami PRL”, „Warszawa walcząca”,
„Trakt Królewski”. Każda trasa ma:
- opis,
- długość w km,
- przebieg narysowany na mapie (ciąg punktów),
- listę punktów turystycznych po drodze.

- **Całość = mamy:** 9 tras.

---

## Nieruchomości

### Rejestr Cen Nieruchomości (RCN)
Transakcje kupna i sprzedaży nieruchomości w Warszawie na podstawie aktów notarialnych. Każda transakcja ma:
- cenę brutto (czasem z VAT) i datę aktu,
- rynek: pierwotny (od dewelopera) albo wtórny,
- stronę sprzedającą i kupującą (osoba fizyczna, firma, Skarb Państwa, samorząd),
- udział w prawie, np. 1/1 albo 1/2.

Dla lokalu jest też:
- funkcja (mieszkanie, garaż, lokal usługowy),
- powierzchnia, liczba izb i piętro,
- adres budynku.

Dla działki i budynku jest:
- numer działki i powierzchnia,
- rodzaj budynku (mieszkalny, biurowy…),
- obrys na mapie.

Jest tam także nazwisko notariusza. Dane nie zawierają nazwisk kupujących ani sprzedających.

- **Całość:** cała Warszawa w podziale na dzielnice (18), rodzaje nieruchomości (lokale, budynki,
  działki zabudowane, działki niezabudowane), rynki (pierwotny, wtórny) i lata. Na pewno są lata
  2022–2026. Nie sprawdzaliśmy, od którego roku zaczynają się dane.
- **Mamy:** Śródmieście, rok 2025:
  - lokale z rynku pierwotnego: 68 transakcji,
  - lokale z rynku wtórnego: 1343 transakcje,
  - działki zabudowane z rynku wtórnego: 6 transakcji.
- **Uwaga:** jedna transakcja składa się z kilku elementów (lokal, budynek, działka), dlatego
  pliki mają więcej rekordów niż transakcji. Położenie jest w polskim układzie współrzędnych
  PL-2000, a nie w GPS. Do pokazania na zwykłej mapie trzeba je przeliczyć.

---

## Sport

### Otwarte boiska
Szkolne boiska, bieżnie, korty i siłownie plenerowe, z których mieszkańcy mogą bezpłatnie
korzystać w wyznaczonych godzinach. Każdy obiekt ma:
- szkołę i jej adres, dzielnicę,
- typ obiektu (boisko do piłki nożnej, koszykówki, uniwersalne…),
- nawierzchnię oraz to, czy są trybuny i piłkochwyty,
- godziny otwarcia w każdym dniu tygodnia,
- uwagi i datę aktualizacji.

- **Całość = mamy:** 1227 obiektów przy ok. 300 placówkach.

### Zajęcia sportowe
Zajęcia z kalendarza sport.um.warszawa.pl, np. nauka pływania, fitness, nordic walking, sauna
czy tenis stołowy. Każde zajęcia mają:
- tytuł i opis,
- kategorię,
- dzielnicę i adres obiektu,
- dzień tygodnia i godzinę (czasem listę konkretnych dat),
- adresatów (dzieci, seniorzy, kobiety…),
- link.

- **Całość:** zajęcia obecnie opublikowane w kalendarzu. ⏱
- **Mamy:** wszystko, czyli 593 zajęcia (stan z 13.10.2026).

---

## Transport

### Lokalizacja przystanków komunikacji miejskiej
Wszystkie przystanki ZTM. Każdy słupek ma:
- nazwę zespołu przystankowego (np. „Dw. Centralny”),
- numer słupka,
- położenie na mapie.

To podstawa do łączenia z liniami i odjazdami.
- **Całość = mamy:** 6988 słupków w 2935 zespołach przystankowych.

### Linie dostępne na przystanku
Lista numerów linii, które zatrzymują się na danym słupku. Linie zaczynające się od N to linie
nocne, a od ZM to zastępcze za metro.
- **Całość:** osobna lista dla każdego z ok. 7000 słupków. Jedno zapytanie zwraca jeden słupek.
- **Mamy:** próbkę z 16 słupków (Centrum i Metro Wierzbno).
- **Uwaga:** lista obejmuje też linie, które zatrzymują się tu tylko wyjątkowo, np. podczas
  zjazdu do zajezdni.

### Odjazdy linii z przystanku
Rozkład jazdy jednej linii na jednym słupku. Każdy odjazd ma:
- godzinę,
- kierunek,
- brygadę,
- symbol trasy, z którego wynika, czy to zwykły kurs, czy zjazd albo wyjazd z zajezdni.

- **Całość:** rozkład każdej linii na każdym słupku, czyli dziesiątki tysięcy kombinacji.
- **Mamy:** 8 linii tramwajowych na słupku Metro Wierzbno 03, czyli 282 odjazdy.

### Lokalizacja pojazdów komunikacji miejskiej (GPS) ⏱
Bieżące położenie autobusów i tramwajów. Każdy pojazd ma:
- numer linii, brygadę i numer taborowy,
- współrzędne,
- godzinę sygnału GPS.

Portal odświeża dane co 10 sekund.
- **Całość:** tylko bieżąca migawka. API nie udostępnia historii przejazdów, więc żeby ją mieć,
  trzeba samemu zbierać migawki co kilkanaście sekund.
- **Mamy:** jedną migawkę z 13.10.2026, godz. 23:54: 1018 autobusów i 289 tramwajów.
- **Uwaga:** część pozycji jest nieaktualna, niektóre nawet z 2024 roku. Trzeba je odfiltrować
  według godziny sygnału.

### Pojazdy transportu publicznego
Rejestr taboru. Każdy pojazd ma:
- numer taborowy i rejestracyjny,
- operatora i zajezdnię,
- rok produkcji,
- malowanie i kolor tapicerki.

Osobna część opisuje modele pojazdów: markę, długość, liczbę miejsc siedzących i stojących,
miejsca na wózki oraz to, czy jest klimatyzacja.
- **Całość = mamy:** 1839 autobusów, 797 tramwajów, 223 wagony metra i 230 pojazdów SKM,
  a do tego opisy 367 modeli.

### Utrudnienia w ruchu drogowym ⏱
Remonty, zamknięcia ulic i zmiany organizacji ruchu z serwisu infoulice. Każde utrudnienie ma:
- tytuł i opis,
- rodzaj (np. zamknięcie ulicy, ruch jednokierunkowy),
- ulice, których dotyczy,
- datę początku i końca,
- przebieg na mapie.

- **Całość:** utrudnienia aktualnie opublikowane w serwisie.
- **Mamy:** wszystko, czyli 54 utrudnienia (stan z 13.10.2026).

### Wolne miejsca parkingowe ⏱
Parkingi miejskie, m.in. ZTP, ZDM i Pałacu Kultury. Każdy parking ma:
- liczbę wolnych miejsc (zwykłych, dla osób z niepełnosprawnością i z ładowarką),
- liczbę wszystkich miejsc na każdym poziomie,
- cennik według typu pojazdu i godziny otwarcia,
- zarządcę, kontakt do niego i położenie.

Dane odświeżane są co minutę.
- **Całość:** tylko bieżący stan. Do analizy obłożenia w czasie trzeba pobierać cyklicznie.
- **Mamy:** jeden odczyt dla 14 parkingów.

---

## Wydarzenia

### Kalendarz wydarzeń
Wydarzenia z kalendarza na um.warszawa.pl: koncerty, warsztaty, spotkania, szkolenia, biegi.
Każde wydarzenie ma:
- tytuł, zajawkę i pełny opis,
- terminy (często kilka),
- dzielnicę, miejsce, adres i punkt na mapie,
- kategorie (np. kultura, sport, biznes),
- zdjęcie i link.

- **Całość:** wydarzenia obecnie opublikowane w kalendarzu, w tym zaplanowane na przyszłość. ⏱
- **Mamy:** wszystko, czyli 655 wydarzeń. Ich terminy sięgają do stycznia 2027.

---

## Zdrowie

### Lokalizacja defibrylatorów (AED)
Aktywne defibrylatory w Warszawie. Każde urządzenie ma:
- nazwę miejsca (np. sąd, przychodnia, stacja metra) i adres,
- położenie: wewnątrz albo na zewnątrz budynku, z opisem, gdzie dokładnie wisi,
- informację, czy jest publicznie dostępne, i w jakich godzinach,
- producenta.

- **Całość = mamy:** 710 urządzeń.

---

## Środowisko

### Monitoring jakości powietrza ⏱
Stacje i punkty pomiaru jakości powietrza w Warszawie i gminach dookoła. Każda stacja ma:
- ogólny indeks jakości (od „bardzo dobry” do „dostateczny”) z zaleceniem dla mieszkańców,
- najnowsze pomiary: pyły PM10, PM2.5 i PM1, dwutlenek azotu, a na części stacji także ozon,
  temperaturę, ciśnienie i wilgotność,
- właściciela stacji (miasto, GIOŚ, gminy) i adres.

- **Całość:** tylko ostatni pomiar, odświeżany co 10 minut. Historii w API nie ma.
- **Mamy:** jeden odczyt ze 140 stacji.

### Pogoda ⏱
Stacje meteorologiczne Zarządu Oczyszczania Miasta. Każda stacja podaje:
- temperaturę powietrza i nawierzchni,
- wilgotność,
- prędkość i kierunek wiatru,
- natężenie opadu.

Temperatura nawierzchni pomaga przewidzieć gołoledź.
- **Całość:** tylko ostatni pomiar, odświeżany co 10 minut.
- **Mamy:** jeden odczyt z 16 stacji.
- **Uwaga:** wartość -32000 oznacza najpewniej brak pomiaru.

### Eko punkty
Miejsca, w których można oddać przeterminowane leki, elektroodpady albo inne odpady problemowe:
apteki, punkty elektroodpadów, mobilne punkty zbiórki. Każde miejsce ma:
- typ,
- adres i dzielnicę,
- położenie na mapie,
- godziny otwarcia w każdym dniu,
- telefon i e-mail.

- **Całość = mamy:** 775 punktów.

### Segregacja odpadów
Wyszukiwarka „gdzie to wyrzucić” z serwisu segregujna5.um.warszawa.pl. Każdy przedmiot
(np. „deska do krojenia”, „aceton”) ma:
- synonimy,
- wskazówki,
- link do strony.

- **Całość = mamy:** 1079 przedmiotów.
- **Uwaga:** pole z rodzajem pojemnika jest w danych puste. Odpowiedź, do którego pojemnika
  wrzucić przedmiot, jest tylko na stronie, do której prowadzi link. W samym zbiorze jej nie ma.

### Typy odpadów
13 frakcji odpadów (bio, papier, szkło, metale i tworzywa…). Każda ma:
- listę, co do niej wyrzucamy, a czego nie,
- opis recyklingu,
- informację, co dalej dzieje się z odpadami.

- **Całość = mamy:** 13 frakcji.

### Toalety
Publiczne toalety: w parkach, przy plażach, w metrze, a także przenośne. Każda toaleta ma:
- położenie i dzielnicę,
- typ i zarządcę,
- godziny otwarcia,
- informację, czy jest dostępna dla osób z niepełnosprawnością (400 z 695), czy jest płatna
  (58 z 695) i czy ma przewijak.

Toalety sezonowe mają uwagę w rodzaju „do 31 października”.
- **Całość = mamy:** 695 toalet. Miasto zaktualizowało je w kwietniu 2026.
