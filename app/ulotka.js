// Szablon ulotki „Najbliższa toaleta” — wspólny dla index.html (podgląd)
// i druk.html (druk wsadowy). Ulotka niczego nie liczy: wszystkie pola
// przychodzą gotowe z app/dane/ulotki.json (src/ulotki_dane.py).

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

  function cecha(ok, pl, en) {
    const li = el("li", ok ? "tak" : "nie");
    li.append(el("span", "znacznik", ok ? "✔" : "✘"), dwujezyczny("span", "", pl, en));
    return li;
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
    const dopiski = [TYP[t.typ], t.wskazowka && "Wskazówka: " + t.wskazowka].filter(Boolean);
    if (dopiski.length) s.append(el("p", "u-wskazowka", dopiski.join(" · ")));
    return s;
  }

  function cechy(t) {
    const ul = el("ul", "u-cechy");
    ul.append(
      t.platna ? cecha(false, "PŁATNA", "Paid") : cecha(true, "BEZPŁATNA", "Free"),
      t.niedziela
        ? cecha(true, "W NIEDZIELĘ: " + t.niedziela, "Open on Sunday")
        : cecha(false, "W NIEDZIELĘ NIECZYNNA", "Closed on Sunday"),
      t.sezon
        ? cecha(false, "SEZONOWA: " + t.sezon, "Seasonal")
        : cecha(true, "CZYNNA CAŁY ROK", "Open all year"),
      t.dla_wozkow
        ? cecha(true, "DLA WÓZKÓW", "Wheelchair accessible")
        : cecha(false, "NIE DLA WÓZKÓW", "Not wheelchair accessible")
    );
    return ul;
  }

  function dol(r) {
    const s = el("section", "u-dol");
    const alt = el("div", "u-alt");
    const pewna = !r.glowna.platna && !r.glowna.sezon && r.glowna.niedziela && r.glowna.typ !== "przenośna";
    if (r.alternatywa) {
      const a = r.alternatywa;
      alt.append(
        dwujezyczny("p", "etykieta", "Najbliższa bezpłatna, czynna cały rok i w niedzielę:",
          "Nearest free toilet, open all year and on Sundays:"),
        el("p", "u-alt-odl", "ok. " + odleglosc(a.odl_m) + " · " + a.min + " min"),
        el("p", "u-alt-adres", a.adres),
        el("p", "u-alt-godziny", a.godziny)
      );
    } else if (!pewna) {
      alt.append(dwujezyczny("p", "etykieta",
        "W promieniu 3 km nie ma toalety bezpłatnej, czynnej cały rok i w niedzielę.",
        "No free all-year toilet open on Sundays within 3 km."));
    }
    const qr = el("div", "u-qr");
    const kod = el("div", "kod");
    new QRCode(kod, { text: linkNawigacji(r), width: 360, height: 360, correctLevel: QRCode.CorrectLevel.M });
    qr.append(kod, dwujezyczny("p", "", "Prowadź mnie", "Navigate me"));
    s.append(alt, qr);
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

  function pinezka(klasa, znak, pl, en, podpisZLewej) {
    return L.divIcon({
      className: "pin " + klasa + (podpisZLewej ? " lewa" : ""),
      html: '<span class="znak">' + znak + '</span><span class="podpis">' + pl + "<i>" + en + "</i></span>",
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
    // margines poziomy mieści podpis, pionowy — sam znacznik.
    const wcZLewej = r.glowna.lon < r.lon;
    m.fitBounds([tu, wc], { padding: [190, 50], maxZoom: 18 });
    L.polyline([tu, wc], { color: "#111", weight: 5, dashArray: "4 10", lineCap: "round" }).addTo(m);
    L.marker(wc, { icon: pinezka("pin-wc", "WC", "TOALETA", "Toilet", wcZLewej) }).addTo(m);
    L.marker(tu, { icon: pinezka("pin-tu", "", "JESTEŚ TUTAJ", "You are here", !wcZLewej) }).addTo(m);
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
    u.append(naglowek(r), sekcjaOdleglosci(r), mapaEl, cechy(r.glowna),
      dwujezyczny("p", "u-godziny", "Godziny: " + r.glowna.godziny, "Opening hours"),
      dol(r), stopka(r));
    kontener.append(u);
    return mapa(r, mapaEl);
  }

  async function wczytajUlotki() {
    const odp = await fetch("dane/ulotki.json");
    if (!odp.ok) throw new Error("Brak dane/ulotki.json — uruchom src/ulotki_dane.py");
    return odp.json();
  }

  window.Ulotka = { renderuj, wczytajUlotki, odleglosc };
})();
