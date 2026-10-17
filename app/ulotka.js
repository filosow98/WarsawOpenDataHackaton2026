// Szablon ulotki „Najbliższa toaleta” — wspólny dla index.html (podgląd)
// i druk.html (druk wsadowy). Ulotka niczego nie liczy: wszystkie pola
// przychodzą gotowe z app/dane/ulotki.json (src/ulotki_dane.py).
// Ulotka wisi na przystanku, więc informacje o toalecie pokazujemy
// piktogramami, a tekst ograniczamy do minimum.

(function () {
  const MAX_W_POBLIZU = 1500; // m — dalej: „W pobliżu nie ma toalety”

  // Druk wsadowy (src/ulotki_pdf.py) podaje klucz MapTiler; podgląd używa OSM.
  function warstwaKafelkow() {
    if (window.MAPTILER_KEY) {
      return L.tileLayer(
        "https://api.maptiler.com/maps/streets-v2/256/{z}/{x}/{y}.png?key=" + window.MAPTILER_KEY,
        { maxZoom: 19, crossOrigin: true }
      );
    }
    return L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", { maxZoom: 19 });
  }

  const TYP = {
    "przenośna": "Toaleta przenośna (kabina)",
    "toaleta METRO": "Toaleta w metrze",
    "stacjonarna automatyczna": "Toaleta automatyczna",
  };

  // Piktogramy kafelków (viewBox 48×48, kolor z CSS przez currentColor).
  const IKONY = {
    bezplatna: '<circle cx="24" cy="24" r="20" fill="none" stroke="currentColor" stroke-width="3.5"/>' +
      '<text x="24" y="30" text-anchor="middle" font-size="16" font-weight="700" fill="currentColor">0 zł</text>',
    platna: '<circle cx="24" cy="24" r="20" fill="currentColor"/>' +
      '<text x="24" y="31" text-anchor="middle" font-size="19" font-weight="700" fill="#fff">zł</text>',
    niedziela: '<rect x="5" y="8" width="38" height="34" rx="4" fill="none" stroke="currentColor" stroke-width="3.5"/>' +
      '<rect x="5" y="8" width="38" height="11" rx="4" fill="currentColor"/>' +
      '<line x1="15" y1="4" x2="15" y2="12" stroke="currentColor" stroke-width="3.5" stroke-linecap="round"/>' +
      '<line x1="33" y1="4" x2="33" y2="12" stroke="currentColor" stroke-width="3.5" stroke-linecap="round"/>' +
      '<text x="24" y="37" text-anchor="middle" font-size="14" font-weight="700" fill="currentColor">ND</text>',
    calyRok: '<path d="M39 17 A 17 17 0 1 0 41 27" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round"/>' +
      '<path d="M34 9 L 40 17 L 31 19" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>' +
      '<text x="24" y="29" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">365</text>',
    sezon: '<circle cx="24" cy="24" r="8" fill="currentColor"/>' +
      '<g stroke="currentColor" stroke-width="3.5" stroke-linecap="round">' +
      '<line x1="24" y1="4" x2="24" y2="10"/><line x1="24" y1="38" x2="24" y2="44"/>' +
      '<line x1="4" y1="24" x2="10" y2="24"/><line x1="38" y1="24" x2="44" y2="24"/>' +
      '<line x1="10" y1="10" x2="14" y2="14"/><line x1="34" y1="34" x2="38" y2="38"/>' +
      '<line x1="10" y1="38" x2="14" y2="34"/><line x1="34" y1="14" x2="38" y2="10"/></g>',
    wozek: '<circle cx="21" cy="8" r="4" fill="currentColor"/>' +
      '<path d="M21 14 L 21 27 L 33 27 L 37 39" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>' +
      '<path d="M21 19 L 30 19" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round"/>' +
      '<path d="M15 21 A 12 12 0 1 0 31 37" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round"/>',
    przekreslenie: '<line x1="6" y1="42" x2="42" y2="6" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>',
  };

  function el(tag, klasa, tekst) {
    const e = document.createElement(tag);
    if (klasa) e.className = klasa;
    if (tekst != null) e.textContent = tekst;
    return e;
  }

  function dwujezyczny(tag, klasa, pl, en) {
    const e = el(tag, klasa, pl);
    e.append(el("span", "en", en));
    return e;
  }

  function odleglosc(m) {
    return m >= 1000 ? (m / 1000).toFixed(1).replace(".", ",") + " km" : m + " m";
  }

  // Kafelek: piktogram + znacznik ✔/✘ + krótki podpis PL/EN (+ wartość, np. godziny).
  function kafelek(ok, ikona, pl, en, wartosc) {
    const k = el("div", "kafelek " + (ok ? "tak" : "nie"));
    k.innerHTML =
      '<span class="ikona"><svg viewBox="0 0 48 48" aria-hidden="true">' + ikona + "</svg>" +
      '<span class="znacznik">' + (ok ? "✔" : "✘") + "</span></span>";
    const podpis = el("span", "podpis", pl);
    if (wartosc) podpis.append(el("span", "wartosc", wartosc));
    podpis.append(el("span", "en", en));
    k.append(podpis);
    return k;
  }

  function linkNawigacji(r) {
    return (
      "https://www.google.com/maps/dir/?api=1&origin=" + r.lat + "," + r.lon +
      "&destination=" + r.glowna.lat + "," + r.glowna.lon + "&travelmode=walking"
    );
  }

  function naglowek(r) {
    const h = el("header", "u-naglowek");
    const img = el("img", "u-maskotka");
    img.src = "img/syrenka.svg";
    img.alt = "";
    const tytul = el("div", "u-tytul");
    tytul.append(el("h1", "", "NAJBLIŻSZA TOALETA"), el("p", "en", "Nearest toilet · WC"));
    const przystanek = el("div", "u-przystanek");
    przystanek.append(
      el("span", "etykieta", "Przystanek / Stop"),
      el("strong", "", r.nazwa + " " + r.id.split("-")[1]),
      el("span", "u-id", "nr " + r.id)
    );
    h.append(img, tytul, przystanek);
    return h;
  }

  function sekcjaOdleglosci(r) {
    const t = r.glowna;
    const s = el("section", "u-odleglosc");
    if (t.odl_m > MAX_W_POBLIZU) {
      s.append(dwujezyczny("p", "u-brak", "W pobliżu nie ma toalety.", "No toilet nearby."));
    }
    const wiersz = el("div", "u-liczby");
    wiersz.append(
      el("span", "u-metry", "ok. " + odleglosc(t.odl_m)),
      dwujezyczny("span", "u-minuty", t.min + " min pieszo", "approx. " + t.min + " min walk")
    );
    s.append(wiersz, el("p", "u-adres", t.adres));
    const dopiski = [TYP[t.typ], t.wskazowka].filter(Boolean);
    if (dopiski.length) s.append(el("p", "u-wskazowka", dopiski.join(" · ")));
    return s;
  }

  function dol(r) {
    const t = r.glowna;
    const s = el("section", "u-dol");
    const info = el("div", "u-info");
    const kafelki = el("div", "u-kafelki");
    kafelki.append(
      t.platna
        ? kafelek(false, IKONY.platna, "PŁATNA", "Paid")
        : kafelek(true, IKONY.bezplatna, "BEZPŁATNA", "Free"),
      t.niedziela
        ? kafelek(true, IKONY.niedziela, "NIEDZIELA", "Open on Sunday", t.niedziela)
        : kafelek(false, IKONY.niedziela, "NIEDZIELA", "Closed on Sunday", "ZAMKNIĘTA"),
      t.sezon
        ? kafelek(false, IKONY.sezon, "SEZONOWA", "Seasonal", t.sezon_krotko)
        : kafelek(true, IKONY.calyRok, "CAŁY ROK", "All year"),
      t.dla_wozkow
        ? kafelek(true, IKONY.wozek, "DLA WÓZKÓW", "Wheelchair")
        : kafelek(false, IKONY.wozek + IKONY.przekreslenie, "NIE DLA WÓZKÓW", "No wheelchair access")
    );
    const godziny = el("p", "u-godziny");
    godziny.innerHTML =
      '<svg viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="19" fill="none" stroke="currentColor" stroke-width="4"/>' +
      '<path d="M24 12 L 24 24 L 32 29" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round"/></svg>';
    godziny.append(el("span", "", t.godziny));
    info.append(kafelki, godziny);

    const qr = el("div", "u-qr");
    const kod = el("div", "kod");
    new QRCode(kod, { text: linkNawigacji(r), width: 360, height: 360, correctLevel: QRCode.CorrectLevel.M });
    qr.append(kod, dwujezyczny("p", "", "Prowadź mnie", "Navigate me"));
    s.append(info, qr);
    return s;
  }

  function stopka(r) {
    const f = el("footer", "u-stopka");
    f.append(
      el("span", "", "Dane: dane.um.warszawa.pl (toalety: kwiecień 2026) · Mapa © OpenStreetMap" +
        (window.MAPTILER_KEY ? " © MapTiler" : "")),
      el("strong", "", "Błąd na ulotce? Zadzwoń 19115, podaj nr " + r.id)
    );
    return f;
  }

  // Toaleta: pinezka, której ostry koniec wskazuje dokładny punkt.
  // Przystanek: kropka, której środek jest w punkcie.
  function pinezka(klasa, znak, pl, en, podpisZLewej) {
    const ksztalt = klasa === "pin-wc"
      ? '<svg class="znak" viewBox="0 0 44 58" aria-hidden="true">' +
        '<path d="M22 56 C 18 46, 2 34, 2 22 A 20 20 0 1 1 42 22 C 42 34, 26 46, 22 56 Z" fill="#fff" stroke="#111" stroke-width="4" stroke-linejoin="round"/>' +
        '<text x="22" y="28" text-anchor="middle" font-size="15" font-weight="700" fill="#111">' + znak + "</text></svg>"
      : '<span class="znak"></span>';
    return L.divIcon({
      className: "pin " + klasa + (podpisZLewej ? " lewa" : ""),
      html: ksztalt + '<span class="podpis">' + pl + "<i>" + en + "</i></span>",
      iconSize: null,
    });
  }

  // Zwraca Promise<boolean>: true, gdy kafelki mapy się wczytały.
  function mapa(r, kontener) {
    const m = L.map(kontener, {
      zoomControl: false, attributionControl: false, dragging: false, scrollWheelZoom: false,
      doubleClickZoom: false, boxZoom: false, keyboard: false, touchZoom: false,
      fadeAnimation: false, zoomAnimation: false,
    });
    const tu = [r.lat, r.lon];
    const wc = [r.glowna.lat, r.glowna.lon];
    // Podpisy po zewnętrznych stronach, żeby nie nachodziły na siebie;
    // margines poziomy mieści podpis, górny — pinezkę WC nad punktem.
    const wcZLewej = r.glowna.lon < r.lon;
    m.fitBounds([tu, wc], { paddingTopLeft: [190, 80], paddingBottomRight: [190, 30], maxZoom: 18 });
    L.polyline([tu, wc], { color: "#111", weight: 5, dashArray: "4 10", lineCap: "round" }).addTo(m);
    L.marker(tu, { icon: pinezka("pin-tu", "", "JESTEŚ TUTAJ", "You are here", !wcZLewej) }).addTo(m);
    L.marker(wc, { icon: pinezka("pin-wc", "WC", "TOALETA", "Toilet", wcZLewej), zIndexOffset: 1000 }).addTo(m);
    return new Promise((resolve) => {
      const limit = setTimeout(() => resolve(false), 30000);
      warstwaKafelkow()
        .once("load", () => { clearTimeout(limit); resolve(true); })
        .addTo(m);
    });
  }

  function renderuj(r, kontener) {
    const u = el("article", "ulotka");
    const mapaEl = el("div", "u-mapa");
    u.append(naglowek(r), sekcjaOdleglosci(r), mapaEl, dol(r), stopka(r));
    kontener.append(u);
    return mapa(r, mapaEl);
  }

  async function wczytajUlotki() {
    if (location.protocol === "file:") throw new Error(BLAD_FILE);
    const odp = await fetch("dane/ulotki.json");
    if (!odp.ok) throw new Error("Brak dane/ulotki.json — uruchom src/ulotki_dane.py");
    return odp.json();
  }

  // Przeglądarka nie wczyta JSON-a ze strony otwartej z dysku (file://).
  const BLAD_FILE =
    "Strona otwarta z dysku, więc przeglądarka blokuje wczytanie danych. Uruchom serwer " +
    "w katalogu projektu: uv run python -m http.server 8000 --directory app " +
    "i otwórz http://localhost:8000";

  window.Ulotka = { renderuj, wczytajUlotki, odleglosc, BLAD_FILE };
})();
