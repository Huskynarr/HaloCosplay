/* MJOLNIR Field Manual - client-side app.
 * Fetches the repo's markdown at runtime and renders it with progress
 * tracking in LocalStorage. The markdown files stay the source of truth. */
(function () {
  "use strict";

  var ROOT = "../"; // app in /web/, markdown at repo root
  var TOP_DIRS = ["Documentation/", "Code/", "Materials/", "Resources/", "Design/", "BuildGuides/", "Tests/", "Progress/"];
  var NS = "mfm:";
  var VARIANTS = ["V1", "V2", "V3"];
  var VIEWER = "3d-viewer"; // sentinel hash for the interactive 3D armor model

  // ---- LocalStorage (namespaced) ----
  var store = {
    get: function (k) { try { return localStorage.getItem(NS + k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(NS + k, v); } catch (e) {} },
    reset: function () {
      try {
        var rm = [];
        for (var i = 0; i < localStorage.length; i++) { var key = localStorage.key(i); if (key && key.indexOf(NS) === 0) rm.push(key); }
        rm.forEach(function (k) { localStorage.removeItem(k); });
      } catch (e) {}
    }
  };

  // ---- state ----
  var variant = store.get("variant");
  if (VARIANTS.indexOf(variant) < 0) variant = "V3";
  var currentFile = "", docEl;

  function jr() { return CONTENT.journeys[variant]; }
  function steps() { return jr().steps; }

  // ---- helpers ----
  function $(sel) { return document.querySelector(sel); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function dirOf(f) { var i = f.lastIndexOf("/"); return i < 0 ? "" : f.slice(0, i + 1); }
  function normalize(p) {
    var out = [];
    p.split("/").forEach(function (seg) { if (seg === "..") out.pop(); else if (seg !== "." && seg !== "") out.push(seg); });
    return out.join("/");
  }
  function resolveHref(href, currentF) {
    for (var i = 0; i < TOP_DIRS.length; i++) { if (href.indexOf(TOP_DIRS[i]) === 0) return normalize(href); }
    return normalize(dirOf(currentF) + href);
  }
  function hashStr(s) { var h = 0, i; for (i = 0; i < s.length; i++) { h = (h << 5) - h + s.charCodeAt(i); h |= 0; } return Math.abs(h).toString(36); }
  var toastT;
  function toast(msg) {
    var t = $("#toast"); t.textContent = msg; t.style.display = "block";
    clearTimeout(toastT); toastT = setTimeout(function () { t.style.display = "none"; }, 1800);
  }

  // ---- journey + progress ----
  function journeyIndex(file) { var s = steps(); for (var i = 0; i < s.length; i++) { if (s[i].file === file) return i; } return -1; }
  function progress() {
    var s = steps(), d = 0;
    s.forEach(function (j) { if (store.get("done:" + j.file) === "1") d++; });
    return { d: d, total: s.length, pct: s.length ? Math.round((d / s.length) * 100) : 0 };
  }
  function renderProgress() {
    var p = progress();
    $("#progress-pct").textContent = variant + " " + p.pct + "%";
    $("#progress-bar").style.width = p.pct + "%";
  }

  // ---- sidebar ----
  function navLink(item, num) {
    var a = document.createElement("a");
    a.className = "navlink"; a.href = "#" + item.file; a.setAttribute("data-file", item.file);
    a.textContent = (num ? num + ". " : "") + item.title;
    if (item.sub) a.title = item.sub;
    if (store.get("done:" + item.file) === "1") a.classList.add("done");
    return a;
  }
  function variantSwitcher() {
    var wrap = document.createElement("div");
    wrap.style.cssText = "display:flex;gap:4px;padding:10px 10px 4px;";
    VARIANTS.forEach(function (v) {
      var b = document.createElement("button");
      b.className = "btn" + (v === variant ? " btn-accent" : "");
      b.style.cssText = "flex:1;padding:7px 0;font-size:12px;";
      b.textContent = v; b.title = CONTENT.journeys[v].label + " - " + CONTENT.journeys[v].tag;
      b.addEventListener("click", function () {
        if (variant === v) return;
        variant = v; store.set("variant", v);
        buildNav(); renderProgress(); updateJourneyFoot(currentFile);
        toast("Pfad: " + CONTENT.journeys[v].label);
      });
      wrap.appendChild(b);
    });
    return wrap;
  }
  function buildNav() {
    var nav = $("#nav");
    nav.innerHTML = "";
    nav.appendChild(variantSwitcher());
    var jh = document.createElement("div"); jh.className = "cat-head"; jh.style.color = "var(--accent)";
    jh.textContent = jr().label + " - Schnellstart";
    nav.appendChild(jh);
    steps().forEach(function (it, i) { nav.appendChild(navLink(it, i + 1)); });
    CONTENT.categories.forEach(function (cat) {
      var h = document.createElement("div"); h.className = "cat-head"; h.textContent = cat.name; nav.appendChild(h);
      cat.items.forEach(function (it) { nav.appendChild(navLink(it, 0)); });
    });
    setActive(currentFile);
    applySearch();
  }
  function markDone() {
    document.querySelectorAll("#nav .navlink").forEach(function (a) {
      a.classList.toggle("done", store.get("done:" + a.getAttribute("data-file")) === "1");
    });
  }
  function setActive(file) {
    document.querySelectorAll("#nav .navlink").forEach(function (a) {
      a.classList.toggle("active", a.getAttribute("data-file") === file);
    });
  }
  function applySearch() {
    var q = ($("#search").value || "").trim().toLowerCase();
    document.querySelectorAll("#nav .navlink").forEach(function (a) {
      a.style.display = (!q || a.textContent.toLowerCase().indexOf(q) !== -1) ? "" : "none";
    });
    document.querySelectorAll("#nav .cat-head").forEach(function (h) {
      var n = h.nextElementSibling, any = false;
      while (n && !n.classList.contains("cat-head")) { if (n.tagName === "A" && n.style.display !== "none") any = true; n = n.nextElementSibling; }
      h.style.display = (!q || any) ? "" : "none";
    });
  }

  // ---- rendering ----
  function postProcess(root, file) {
    root.querySelectorAll("a[href]").forEach(function (a) {
      var href = a.getAttribute("href");
      if (/^(https?:|mailto:)/.test(href)) { a.target = "_blank"; a.rel = "noopener"; return; }
      if (href.charAt(0) === "#") return;
      var res = resolveHref(href, file);
      if (/\.md$/i.test(res)) { a.setAttribute("href", "#" + res); }
      else { a.setAttribute("href", ROOT + res); a.target = "_blank"; a.rel = "noopener"; }
    });
    root.querySelectorAll("img[src]").forEach(function (img) {
      var src = img.getAttribute("src");
      if (!/^(https?:|data:)/.test(src)) img.setAttribute("src", ROOT + resolveHref(src, file));
      img.setAttribute("loading", "lazy");
      img.setAttribute("decoding", "async");
      if (!img.getAttribute("alt")) img.setAttribute("alt", "");
    });
    root.querySelectorAll('input[type="checkbox"]').forEach(function (cb, i) {
      cb.disabled = false;
      var key = "task:" + file + ":" + i;
      cb.checked = store.get(key) === "1";
      cb.addEventListener("change", function () { store.set(key, cb.checked ? "1" : "0"); });
    });
    if (typeof SHOPPING_FILES !== "undefined" && SHOPPING_FILES.has(file)) {
      root.querySelectorAll("table").forEach(function (tbl, ti) {
        var hr = tbl.querySelector("thead tr");
        if (hr) { var th = document.createElement("th"); th.textContent = "HABE"; hr.insertBefore(th, hr.firstChild); }
        tbl.querySelectorAll("tbody tr").forEach(function (tr) {
          var key = "buy:" + file + ":" + ti + ":" + hashStr(tr.textContent.trim());
          var td = document.createElement("td"); td.style.textAlign = "center";
          var cb = document.createElement("input"); cb.type = "checkbox";
          cb.checked = store.get(key) === "1"; if (cb.checked) tr.classList.add("bought");
          cb.addEventListener("change", function () { store.set(key, cb.checked ? "1" : "0"); tr.classList.toggle("bought", cb.checked); });
          td.appendChild(cb); tr.insertBefore(td, tr.firstChild);
        });
      });
    }
  }

  function welcome() {
    currentFile = ""; setActive("");
    $("#journey-foot").style.display = "none";
    var p = progress(), j = jr();
    var cards = VARIANTS.map(function (v) {
      var jj = CONTENT.journeys[v];
      return '<button class="btn variant-pick' + (v === variant ? " btn-accent" : "") + '" data-v="' + v + '" style="text-align:left;padding:12px 14px;flex:1;min-width:150px;">' +
        '<div class="font-disp" style="font-size:15px;color:var(--accent)">' + v + " " + esc(jj.label.replace(/^V\d\s*/, "")) + '</div>' +
        '<div style="color:var(--dim);font-size:12px;margin-top:2px">' + esc(jj.tag) + '</div></button>';
    }).join("");
    docEl.innerHTML =
      '<h1>Halo Master Chief Cosplay Guide (Vollständige Anleitung)</h1>' +
      '<p style="font-size:1.08rem;color:var(--dim)">Dies ist eine durchklickbare Schritt-für-Schritt-Anleitung für den Bau deiner eigenen Master Chief Cosplay-Rüstung (MJOLNIR). Die Inhalte basieren direkt auf den Dokumentationen im Repository. Dein Fortschritt, abgehakte Aufgaben und Haken auf Einkaufslisten werden lokal in deinem Browser gespeichert.</p>' +
      '<div class="hud" style="padding:15px 18px;margin:1.5em 0;border-left:3px solid var(--cyan);background:rgba(70,200,255,0.03);">' +
      '<div class="font-disp" style="color:var(--cyan);font-weight:600;font-size:0.95rem;letter-spacing:.05em;">HINTERGRUND: WAS BEDEUTET „MJOLNIR“?</div>' +
      '<p style="font-size:0.9rem;color:var(--text);margin:.4em 0 0;line-height:1.5;">' +
      'Die Rüstung des Master Chiefs trägt die offizielle Bezeichnung <strong>MJOLNIR Powered Assault Armor</strong>. Benannt nach dem legendären Hammer des nordischen Donnergottes Thor, symbolisiert dieser Name die extreme Stärke und Widerstandskraft der Rüstung. Dieser Guide liefert dir die vollständige Bauanleitung für dein eigenes tragbares Replika.' +
      '</p>' +
      '</div>' +
      '<h2>Wähl deinen Pfad</h2>' +
      '<div style="display:flex;gap:10px;flex-wrap:wrap;margin:.6em 0 1.4em">' + cards + '</div>' +
      '<div class="hud ticks" style="padding:18px 20px;margin:8px 0 22px;background:rgba(94,194,63,.05);">' +
      '<div class="font-disp" style="color:var(--accent);font-weight:700;letter-spacing:.06em;">' + esc(j.label) + ' - SCHNELLSTART</div>' +
      '<p style="margin:.4em 0 1em;color:var(--text)">' + esc(j.tag) + '. Schritt für Schritt durch den Build. ' + p.d + ' von ' + p.total + ' Schritten erledigt.</p>' +
      '<button class="btn btn-accent" id="start-journey">Schnellstart öffnen &gt;</button>' +
      '</div>' +
      '<h2>So funktioniert es</h2>' +
      '<ul>' +
      '<li>Wähle oben links deinen Schwierigkeitsgrad/Pfad (<strong>V1 Foam</strong> / <strong>V2 3D-Druck</strong> / <strong>V3 Profi-Exoskelett</strong>) – jede Variante führt dich strukturiert durch das Projekt.</li>' +
      '<li>Hake <strong>Schritte</strong> in den Checklisten direkt ab – dein Fortschritt wird automatisch gesichert.</li>' +
      '<li>Markiere auf den Einkaufslisten die Materialien und Komponenten, die du <strong>bereits besitzt</strong>.</li>' +
      '<li>Der Statusbalken im Header visualisiert deinen <strong>Gesamtfortschritt der ausgewählten Variante</strong>.</li>' +
      '</ul>';
    docEl.querySelectorAll(".variant-pick").forEach(function (b) {
      b.addEventListener("click", function () {
        var v = b.getAttribute("data-v");
        if (variant !== v) { variant = v; store.set("variant", v); buildNav(); renderProgress(); }
        welcome();
      });
    });
    var s = $("#start-journey");
    if (s) s.addEventListener("click", function () { location.hash = steps()[0].file; });
    window.scrollTo(0, 0);
  }

  function updateJourneyFoot(file) {
    var idx = journeyIndex(file);
    var foot = $("#journey-foot");
    if (idx < 0) { foot.style.display = "none"; return; }
    foot.style.display = "block";
    var s = steps(), doneKey = "done:" + file, isDone = store.get(doneKey) === "1";
    var dt = $("#done-toggle");
    dt.textContent = isDone ? "Erledigt - rueckgaengig" : "Schritt erledigt";
    dt.classList.toggle("btn-accent", !isDone);
    dt.onclick = function () {
      var nowDone = store.get(doneKey) !== "1";
      store.set(doneKey, nowDone ? "1" : "0");
      renderProgress(); markDone(); updateJourneyFoot(file);
      if (nowDone) toast("Schritt erledigt: " + s[idx].title);
    };
    var prev = $("#prev-btn"), next = $("#next-btn");
    if (idx > 0) { prev.disabled = false; prev.onclick = function () { location.hash = s[idx - 1].file; }; }
    else { prev.disabled = true; prev.onclick = null; }
    if (idx < s.length - 1) { next.disabled = false; next.onclick = function () { location.hash = s[idx + 1].file; }; }
    else { next.disabled = true; next.onclick = null; }
  }

  function loadDoc(file) {
    currentFile = file; setActive(file); closeNav();
    docEl.innerHTML = '<p class="font-mono" style="color:var(--dim)">// lade ' + esc(file) + ' ...</p>';
    fetch(ROOT + file, { cache: "no-cache" })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.text(); })
      .then(function (md) {
        docEl.innerHTML = marked.parse(md);
        docEl.classList.remove("glitch-in"); void docEl.offsetWidth; docEl.classList.add("glitch-in");
        postProcess(docEl, file);
        updateJourneyFoot(file);
        window.scrollTo(0, 0);
      })
      .catch(function () {
        $("#journey-foot").style.display = "none";
        docEl.innerHTML = '<h1>Nicht gefunden</h1><p>Die Datei <code>' + esc(file) +
          '</code> konnte nicht geladen werden. Laeuft die Seite ueber einen Webserver (nicht per file://)?</p>';
      });
  }

  // ---- 3D armor viewer (model-viewer + clickable component hotspots) ----
  // Each part maps a clickable marker on the model to a real build guide.
  // Positions are tuned for the humanoid placeholder; recalibrate (button
  // below) after dropping in a different model.
  // Amazon links are concrete /dp links lifted from Materials/Einkaufsliste-Links.md
  // (affiliate tag huskynarr-21). Search links are used only where the list itself
  // intentionally keeps a search (e.g. the Pi Zero board).
  var ARMOR_PARTS = [
    { id: "helm", label: "Helm", pos: "0 1.69 0.07", normal: "0 0.15 1", variant: "V1-V3",
      material: "EVA-Foam 6-10 mm (V1) oder PETG-Druck (V2/V3)",
      desc: "Die ikonische MJOLNIR-Helmschale. In V1 aus mehreren Foam-Schalen geformt, in V2/V3 mehrteilig gedruckt, gespachtelt und verschliffen.",
      guide: "Documentation/Guides/3D-Druck.md",
      buy: [{ t: "EVA-Foam (Staerken waehlbar)", u: "https://www.amazon.de/dp/B085WBSS5B?tag=huskynarr-21" }] },
    { id: "visier", label: "Visier", pos: "0 1.62 0.13", normal: "0 0 1", variant: "V1-V3",
      material: "Getoentes/verspiegeltes PETG oder Polycarbonat",
      desc: "Das goldene Visier. Thermogeformtes PETG, getoent und innen verspiegelt - Anti-Fog-Beschichtung nicht vergessen.",
      guide: "Documentation/Guides/Lackierung-Finishing.md",
      buy: [{ t: "PETG-Platte transparent", u: "https://www.amazon.de/dp/B01AC7WHOM?tag=huskynarr-21" },
            { t: "Anti-Fog-Spray", u: "https://www.amazon.de/dp/B088HGLNQV?tag=huskynarr-21" }] },
    { id: "hud", label: "HUD (im Helm)", pos: "0.07 1.66 0.10", normal: "0.3 0 1", variant: "V2-V3",
      material: "Raspberry Pi Zero 2 W + transparentes OLED (SSD1309)",
      desc: "Optionales Head-up-Display hinter dem Visier: Schild- und Akkustand auf transparentem OLED. Details im HUD-Guide.",
      guide: "Documentation/Guides/Elektronik-HUD.md",
      buy: [{ t: "Transparentes OLED 1.51\"", u: "https://www.amazon.de/dp/B0B8N46G24?tag=huskynarr-21" },
            { t: "Raspberry Pi Zero 2 W", u: "https://www.amazon.de/s?k=Raspberry+Pi+Zero+2+W&tag=huskynarr-21" },
            { t: "PiSugar (Pi-Zero-UPS)", u: "https://www.amazon.de/dp/B09QS12N1W?tag=huskynarr-21" }] },
    { id: "brust", label: "Brustpanzer", pos: "0 1.27 0.17", normal: "0 0 1", variant: "V1-V3",
      material: "EVA-Foam 6 mm + 2 mm Detaillagen / PETG",
      desc: "Brust- und Rueckenplatte. Traegt einen Grossteil der Optik und dient als Montagepunkt fuer Gurte und Elektronik.",
      guide: "Documentation/Guides/Foam-Bau.md",
      buy: [{ t: "EVA-Foam 6 mm", u: "https://www.amazon.de/dp/B07DCGMXQZ?tag=huskynarr-21" }] },
    { id: "schulter", label: "Schulterpanzer", pos: "0.27 1.42 0.04", normal: "0.8 0.2 0.6", variant: "V1-V3",
      material: "EVA-Foam 6 mm, warm gebogen",
      desc: "Die markanten Schulter-Pauldrons (UNSC-Logo links). Per Klett oder Magnet an der Brustplatte gehalten.",
      guide: "Documentation/Guides/Foam-Bau.md",
      buy: [{ t: "EVA-Foam 6 mm", u: "https://www.amazon.de/dp/B07DCGMXQZ?tag=huskynarr-21" }] },
    { id: "arm", label: "Unterarm / Gauntlet", pos: "0.34 1.05 0.10", normal: "0.8 0 0.6", variant: "V1-V3",
      material: "EVA-Foam 6 mm, als Roehre verklebt",
      desc: "Unterarmschienen mit Bedienfeld-Detail. Muessen ueber die Hand passen - innen offen oder mit Klettverschluss.",
      guide: "Documentation/Guides/Foam-Bau.md",
      buy: [{ t: "EVA-Foam 6 mm", u: "https://www.amazon.de/dp/B07DCGMXQZ?tag=huskynarr-21" }] },
    { id: "hand", label: "Handschuhe + Unteranzug", pos: "0 1.02 0.17", normal: "0 0 1", variant: "V1-V3",
      material: "Schwarzer Unteranzug + taktische Handschuhe",
      desc: "Die schwarze Basisschicht. Traegt Magnete/Klett fuer die Panzerteile und bestimmt den sicheren, beweglichen Sitz.",
      guide: "Documentation/Guides/Unteranzug-Befestigung.md",
      buy: [{ t: "Morphsuit (Unteranzug)", u: "https://www.amazon.de/dp/B00LEG800Q?tag=huskynarr-21" },
            { t: "Mechanix Handschuhe", u: "https://www.amazon.de/dp/B0001VNZZU?tag=huskynarr-21" }] },
    { id: "bein", label: "Oberschenkel + Beinpanzer", pos: "0.13 0.80 0.13", normal: "0.4 0 1", variant: "V1-V3",
      material: "EVA-Foam 6 mm + Schaumfutter",
      desc: "Oberschenkel- und Knieplatten. An einem Beingurt oder Strumpf fixiert, damit nichts rutscht.",
      guide: "Documentation/Guides/Foam-Bau.md",
      buy: [{ t: "EVA-Foam (Staerken waehlbar)", u: "https://www.amazon.de/dp/B085WBSS5B?tag=huskynarr-21" }] },
    { id: "stiefel", label: "Stiefel / Schienbein", pos: "0.13 0.20 0.13", normal: "0.3 0.3 1", variant: "V1-V3",
      material: "Stabile Stiefel + Foam-Schienbein-Cover",
      desc: "Schienbein-Panzer ueber festen Stiefeln. Auf sicheren Stand und Treppentauglichkeit achten.",
      guide: "Materials/Shoes.md",
      buy: [{ t: "EVA-Foam 6 mm (Cover)", u: "https://www.amazon.de/dp/B07DCGMXQZ?tag=huskynarr-21" }] },
    { id: "akku", label: "Akku + Elektronik", pos: "0 1.25 -0.20", normal: "0 0 -1", variant: "V2-V3",
      material: "LiFePO4-Akku / USB-Powerbank + Verteilung",
      desc: "Stromversorgung fuer HUD, Luefter, LEDs und Audio - meist im Rueckenteil verbaut. Strombudget vorher rechnen.",
      guide: "Documentation/Guides/Elektronik-Batterie.md",
      buy: [{ t: "Powerbank 10.000 mAh (schlank)", u: "https://www.amazon.de/dp/B0D4MDHB21?tag=huskynarr-21" },
            { t: "Powerbank 20.000 mAh (V3)", u: "https://www.amazon.de/dp/B0CZ9LH53B?tag=huskynarr-21" }] },
    { id: "exo", label: "Exoskelett", pos: "0.16 0.95 -0.10", normal: "0.6 0 -0.6", variant: "V3",
      material: "Alu-Profil 3030/2020 + Gelenke",
      desc: "Optionales Traggestell, das Gewicht auf die Huefte verlagert und Servo-/Aktuatorbewegung erlaubt. Nur V3.",
      guide: "Documentation/Guides/Exoskelett.md",
      buy: [{ t: "Aluprofil 3030 Nut 8", u: "https://www.amazon.de/dp/B097414JW7?tag=huskynarr-21" }] },
  ];
  var PLACEHOLDER_MODEL = "https://modelviewer.dev/shared-assets/models/Astronaut.glb";
  var LOCAL_MODEL = "models/spartan.glb"; // relative to /web/index.html
  var mvLoading = false;

  function partById(id) { for (var i = 0; i < ARMOR_PARTS.length; i++) { if (ARMOR_PARTS[i].id === id) return ARMOR_PARTS[i]; } return null; }

  function ensureModelViewer(cb) {
    if (customElements.get("model-viewer")) { cb(); return; }
    if (mvLoading) { customElements.whenDefined("model-viewer").then(function () { cb(); }); return; }
    mvLoading = true;
    var s = document.createElement("script");
    s.type = "module";
    s.src = "https://unpkg.com/@google/model-viewer@3.5.0/dist/model-viewer.min.js";
    s.onerror = function () { cb(new Error("load failed")); };
    document.head.appendChild(s);
    customElements.whenDefined("model-viewer").then(function () { cb(); });
  }

  function showPart(p) {
    var panel = $("#part-panel");
    if (!panel || !p) return;
    // Optional reference photo: shows only if web/img/parts/<id>.jpg exists,
    // otherwise the <img> removes itself on error (no broken-image icon).
    var img = '<img class="pp-img" src="' + ROOT + 'web/img/parts/' + p.id + '.jpg" alt="' + esc(p.label) +
      '" loading="lazy" decoding="async" onerror="this.remove()">';
    var buy = "";
    if (p.buy && p.buy.length) {
      buy = '<div class="pp-buy"><div class="pp-buy-head font-mono">Material kaufen</div>' +
        p.buy.map(function (b) {
          return '<a class="pp-buy-link" href="' + b.u + '" target="_blank" rel="noopener nofollow sponsored">' + esc(b.t) + ' &#8599;</a>';
        }).join("") +
        '<div class="pp-buy-note font-mono">Amazon-Partnerlinks (Tag huskynarr-21)</div></div>';
    }
    panel.innerHTML =
      '<div class="pp-head font-disp">' + esc(p.label) + '<span class="pp-var">' + esc(p.variant) + '</span></div>' +
      img +
      '<div class="pp-mat font-mono">' + esc(p.material) + '</div>' +
      '<p class="pp-desc">' + esc(p.desc) + '</p>' +
      '<a class="btn btn-accent pp-link" href="#' + esc(p.guide) + '">Zum Guide &gt;</a>' +
      buy;
    document.querySelectorAll(".mv-hotspot, .part-row").forEach(function (el) {
      el.classList.toggle("active", el.getAttribute("data-id") === p.id);
    });
  }

  function render3DViewer() {
    currentFile = VIEWER; setActive(VIEWER); closeNav();
    $("#journey-foot").style.display = "none";

    var hotspots = ARMOR_PARTS.map(function (p) {
      return '<button class="mv-hotspot" slot="hotspot-' + p.id + '" data-id="' + p.id +
        '" data-position="' + p.pos + '" data-normal="' + p.normal + '" data-visibility-attribute="visible"' +
        ' aria-label="' + esc(p.label) + '"><span class="mv-dot"></span>' +
        '<span class="mv-tip">' + esc(p.label) + '</span></button>';
    }).join("");
    var legend = ARMOR_PARTS.map(function (p) {
      return '<button class="part-row" data-id="' + p.id + '">' +
        '<span class="part-name">' + esc(p.label) + '</span>' +
        '<span class="part-var font-mono">' + esc(p.variant) + '</span></button>';
    }).join("");

    docEl.innerHTML =
      '<h1>3D-Rüstungsmodell</h1>' +
      '<p style="color:var(--dim)">Dreh die MJOLNIR-Rüstung mit Maus oder Finger und tippe die grünen Marker an, um zu sehen, welches Bauteil was ist - inklusive Material und direktem Link zum passenden Build-Guide. Auf dem Smartphone kannst du die Rüstung per <strong>AR</strong> sogar lebensgroß in dein Zimmer stellen.</p>' +
      '<div id="mv-banner" class="hud" style="display:none;padding:10px 14px;margin:12px 0;border-left:3px solid var(--cyan);background:rgba(70,200,255,.06);font-size:.9rem;"></div>' +
      '<div class="mv-wrap">' +
        '<model-viewer id="armor-mv" camera-controls touch-action="pan-y" auto-rotate rotation-per-second="16deg"' +
        ' interaction-prompt="none" shadow-intensity="1" exposure="1.05" environment-image="neutral" tone-mapping="neutral"' +
        ' ar ar-modes="webxr scene-viewer quick-look" camera-orbit="25deg 80deg 105%" field-of-view="30deg"' +
        ' alt="Interaktives 3D-Modell der Master-Chief-MJOLNIR-Rüstung">' +
          hotspots +
          '<button slot="ar-button" class="btn btn-accent mv-ar">In AR ansehen</button>' +
        '</model-viewer>' +
        '<div id="part-panel" class="hud ticks part-panel">' +
          '<div class="pp-empty font-mono" style="color:var(--dim)">// Marker antippen oder unten ein Bauteil wählen</div>' +
        '</div>' +
      '</div>' +
      '<div class="mv-toolbar">' +
        '<button class="btn btn-accent" id="mv-rotate">Auto-Rotation: an</button>' +
        '<button class="btn" id="mv-reset">Ansicht zurücksetzen</button>' +
        '<button class="btn" id="mv-calib" title="Klick-Koordinaten erfassen, um Hotspots an ein neues Modell anzupassen">Kalibrieren: aus</button>' +
      '</div>' +
      '<h2>Bauteile</h2>' +
      '<p style="color:var(--dim);margin-top:-.3em">Jedes Teil führt direkt zum passenden Guide.</p>' +
      '<div class="part-legend">' + legend + '</div>' +
      '<p id="mv-credit" class="font-mono" style="color:var(--dim);font-size:12px;margin-top:1.5em"></p>';

    docEl.classList.remove("glitch-in"); void docEl.offsetWidth; docEl.classList.add("glitch-in");
    window.scrollTo(0, 0);

    // Legend works even if the 3D component never loads (offline-safe).
    document.querySelectorAll(".part-row").forEach(function (row) {
      row.addEventListener("click", function () { showPart(partById(row.getAttribute("data-id"))); });
    });

    ensureModelViewer(function (err) {
      if (err) {
        $("#mv-banner").style.display = "block";
        $("#mv-banner").innerHTML = "Der 3D-Viewer konnte nicht geladen werden (evtl. offline). Die Bauteil-Liste unten funktioniert weiter.";
        return;
      }
      setupViewer();
    });
  }

  function setupViewer() {
    var mv = $("#armor-mv");
    if (!mv) return;
    var credit = $("#mv-credit"), banner = $("#mv-banner");

    function useSpartan() {
      banner.style.display = "none";
      credit.innerHTML = 'Modell: „Spartan Armour MKV" von McCarthy3D - ' +
        '<a href="https://sketchfab.com/3d-models/spartan-armour-mkv-halo-reach-57070b2fd9ff472c8988e76d8c5cbe66" target="_blank" rel="noopener">Sketchfab</a>, CC-BY 4.0.';
    }
    function usePlaceholder() {
      banner.style.display = "block";
      banner.innerHTML = 'Hinweis: Aktuell wird ein <strong>Platzhalter-Modell</strong> gezeigt. Lege deine eigene ' +
        '<code>web/models/spartan.glb</code> ab (siehe <a href="' + ROOT + 'web/models/README.md" target="_blank" rel="noopener">Kurzanleitung</a>), ' +
        'um die echte Spartan-Rüstung zu sehen. Danach ggf. „Kalibrieren" nutzen, um die Marker neu zu setzen.';
      credit.innerHTML = 'Platzhalter-Modell: „Astronaut" © Google, CC-BY. Echtes Modell: „Spartan Armour MKV" von McCarthy3D, CC-BY 4.0.';
    }

    mv.addEventListener("error", function () {
      if (mv.dataset.fellback) return;
      mv.dataset.fellback = "1"; mv.src = PLACEHOLDER_MODEL;
    });
    mv.addEventListener("load", function () {
      if (mv.dataset.fellback) usePlaceholder(); else useSpartan();
    });
    mv.src = LOCAL_MODEL;

    ARMOR_PARTS.forEach(function (p) {
      var btn = mv.querySelector('[slot="hotspot-' + p.id + '"]');
      if (btn) btn.addEventListener("click", function (e) { e.stopPropagation(); showPart(p); });
    });

    var rotBtn = $("#mv-rotate");
    rotBtn.onclick = function () {
      var on = mv.hasAttribute("auto-rotate");
      if (on) mv.removeAttribute("auto-rotate"); else mv.setAttribute("auto-rotate", "");
      rotBtn.textContent = "Auto-Rotation: " + (on ? "aus" : "an");
      rotBtn.classList.toggle("btn-accent", !on);
    };
    $("#mv-reset").onclick = function () {
      mv.cameraOrbit = "25deg 80deg 105%";
      mv.fieldOfView = "30deg";
      if (mv.resetTurntableRotation) mv.resetTurntableRotation();
      if (mv.jumpCameraToGoal) mv.jumpCameraToGoal();
    };

    // Calibration: click the model to capture data-position/data-normal for a
    // swapped model, copy-paste ready into ARMOR_PARTS.
    var calibOn = false, calibBtn = $("#mv-calib");
    calibBtn.onclick = function () {
      calibOn = !calibOn;
      calibBtn.textContent = "Kalibrieren: " + (calibOn ? "an" : "aus");
      calibBtn.classList.toggle("btn-accent", calibOn);
      mv.style.cursor = calibOn ? "crosshair" : "";
    };
    mv.addEventListener("click", function (e) {
      if (!calibOn || !mv.positionAndNormalFromPoint) return;
      var pn = mv.positionAndNormalFromPoint(e.clientX, e.clientY);
      if (!pn) return;
      var snippet = 'pos: "' + pn.position.toString() + '", normal: "' + pn.normal.toString() + '"';
      var panel = $("#part-panel");
      panel.innerHTML = '<div class="pp-head font-disp">Kalibrierung</div>' +
        '<p class="pp-desc">Position erfasst. In <code>app.js</code> beim passenden <code>ARMOR_PARTS</code>-Eintrag einsetzen:</p>' +
        '<textarea class="calib-out font-mono" readonly rows="3" onclick="this.select()">' + esc(snippet) + '</textarea>';
    });
  }

  function route() {
    var file = decodeURIComponent(location.hash.replace(/^#/, ""));
    if (!file) { welcome(); return; }
    if (file === VIEWER) { render3DViewer(); return; }
    loadDoc(file);
  }

  // ---- mobile nav ----
  function openNav() { $("#sidebar").classList.add("open"); $("#backdrop").classList.add("open"); }
  function closeNav() { $("#sidebar").classList.remove("open"); $("#backdrop").classList.remove("open"); }
  window.__closeNav = closeNav;

  // ---- init ----
  document.addEventListener("DOMContentLoaded", function () {
    docEl = $("#doc");
    if (typeof marked !== "undefined" && marked.setOptions) marked.setOptions({ gfm: true, breaks: false });
    buildNav();
    $("#search").addEventListener("input", applySearch);
    renderProgress();
    $("#menu-toggle").addEventListener("click", openNav);
    $("#reset-btn").addEventListener("click", function () {
      if (confirm("Gespeicherten Fortschritt (Schritte, Einkaufs-Haken) in diesem Browser loeschen?")) {
        store.reset();
        variant = "V3"; // keys gone; keep a sane default
        buildNav(); renderProgress(); markDone();
        if (currentFile) loadDoc(currentFile); else welcome();
        toast("Fortschritt zurueckgesetzt");
      }
    });
    window.addEventListener("hashchange", route);
    route();
  });
})();
