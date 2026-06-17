/* MJOLNIR Field Manual - client-side app.
 * Fetches the repo's markdown at runtime and renders it with progress
 * tracking in LocalStorage. The markdown files stay the source of truth. */
(function () {
  "use strict";

  var ROOT = "../"; // app in /web/, markdown at repo root
  var TOP_DIRS = ["Documentation/", "Code/", "Materials/", "Resources/", "Design/", "BuildGuides/", "Tests/", "Progress/"];
  var NS = "mfm:";
  var VARIANTS = ["V1", "V2", "V3"];

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
      '<h1>Master Chief Feldhandbuch</h1>' +
      '<p style="font-size:1.08rem;color:var(--dim)">Durchklickbare Version aller Guides. Inhalte kommen live aus den Markdown-Dateien des Repos - dein Fortschritt, erledigte Schritte und Einkaufs-Haken bleiben lokal in diesem Browser gespeichert.</p>' +
      '<h2>Waehle deinen Pfad</h2>' +
      '<div style="display:flex;gap:10px;flex-wrap:wrap;margin:.6em 0 1.4em">' + cards + '</div>' +
      '<div class="hud ticks" style="padding:18px 20px;margin:8px 0 22px;background:rgba(94,194,63,.05);">' +
      '<div class="font-disp" style="color:var(--accent);font-weight:700;letter-spacing:.06em;">' + esc(j.label) + ' - SCHNELLSTART</div>' +
      '<p style="margin:.4em 0 1em;color:var(--text)">' + esc(j.tag) + '. Schritt fuer Schritt durch den Build. ' + p.d + ' von ' + p.total + ' Schritten erledigt.</p>' +
      '<button class="btn btn-accent" id="start-journey">Schnellstart oeffnen &gt;</button>' +
      '</div>' +
      '<h2>So funktioniert es</h2>' +
      '<ul>' +
      '<li>Oben links <strong>V1 / V2 / V3</strong> waehlen - jede Variante hat ihren eigenen, geordneten Schnellstart.</li>' +
      '<li>Hake <strong>Schritte</strong> in Checklisten direkt ab - sie bleiben gespeichert.</li>' +
      '<li>In den Einkaufslisten hakst du ab, was du <strong>schon hast</strong>.</li>' +
      '<li>Der Balken oben zeigt den <strong>Fortschritt der gewaehlten Variante</strong>.</li>' +
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

  function route() {
    var file = decodeURIComponent(location.hash.replace(/^#/, ""));
    if (!file) { welcome(); return; }
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
