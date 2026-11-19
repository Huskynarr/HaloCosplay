# Halo Master Chief Cosplay Guide - Web-App

Durchklickbare Web-Version der Guides. Die App liest die Markdown-Dateien des
Repos live ein (per fetch zur Laufzeit) und rendert sie in einer Halo/HUD-Optik.
Fortschritt und Einkaufshaken werden ueber LocalStorage im Browser gespeichert.

## Lokal testen

Die App MUSS ueber einen Webserver laufen, nicht per file://, weil sie fetch
nutzt. Im Repo-Root starten:

    python3 -m http.server

Dann im Browser oeffnen:

    http://localhost:8000/web/

## Deploy

Der Deploy erfolgt automatisch via `.github/workflows/pages.yml` bei jedem push
auf den Branch main. In den Repo-Settings unter Pages muss als Source
"GitHub Actions" ausgewaehlt sein.

## LocalStorage

Fortschritt (abgehakte Schritte und Einkaufshaken) wird nur im jeweiligen
Browser gespeichert. Wechselst du Browser oder Geraet, ist der Stand nicht
vorhanden. Ein "Reset"-Knopf in der App loescht den gespeicherten Stand wieder.

## Hinweis

Die Markdown-Dateien bleiben die Single Source of Truth. Die Web-App rendert sie
nur - inhaltliche Aenderungen erfolgen weiterhin in den .md-Dateien des Repos.

## Sicherheit der Darstellung

- **Markdown ist nicht vertrauenswuerdig:** Jede Anleitung wird mit `marked`
  gerendert und danach mit DOMPurify bereinigt ([guide.js](guide.js)). Fehlt der
  Sanitizer, wird nichts eingefuegt. Formulare, Skripte, Styles, `id`, `class`
  und Inline-Handler aus Markdown werden entfernt; nur Aufgaben-Checkboxen bleiben.
- **Feste lokale Bibliotheken:** `marked` und DOMPurify liegen mit Version und
  SHA-256 in [vendor/](vendor/README.md); jsdelivr wird nicht mehr geladen.
- **Adressen:** Nur repo-relative `.md`-Pfade ohne `..`, Schema oder fuehrenden
  Schraegstrich werden geladen. Ungueltige oder fehlerhaft kodierte Adressen
  zeigen "Nicht gefunden".
- **Abschnittslinks:** `#abschnitt` und `Guide.md#abschnitt` werden zu
  `#Pfad/Guide.md#abschnitt` und springen innerhalb der App zur Ueberschrift.
- **Content-Security-Policy:** Jede Seite setzt per `<meta>` eine CSP ohne
  `unsafe-inline` fuer Skripte. Neue externe Hosts oder Inline-Handler muessen
  dort eingetragen bzw. vermieden werden. Das Inline-Skript des Cortana-Viewers
  ist per SHA-256 freigegeben; nach einer Aenderung nennt
  `node --test Tests/Automation/guide.test.cjs` den neuen Hash.
- **Lokal ausgeliefert:** Tailwind-CSS (`vendor/tailwind.css`, gebaut aus den
  tatsaechlich verwendeten Klassen), Schriften (`fonts/`) und model-viewer.
  Nach neuen Tailwind-Klassen in `index.html`, `app.js`, `content.js`,
  `guide.js` oder `products/products.js` das CSS neu bauen, siehe
  [vendor/README.md](vendor/README.md).
- **Noch extern:** Nur das Sentry-SDK (`monitoring.js`) und, falls
  `models/spartan.glb` fehlt, das Platzhaltermodell von modelviewer.dev.

## V4-Baukasten

V4 ist der Standard fuer neue Browserprofile. Bestehende V1-V3-Auswahl bleibt
erhalten. Die Haken dokumentieren Lesefortschritt, keine physische Bauabnahme.
Der Nachweisbericht im V4-Baukasten bleibt davon unabhaengig. Die separate
[Messeanzeige](../Code/Exhibition/README.md) arbeitet auch ohne Internet.

## Profile und Stuecklisten

- [Profil-Konfigurator](configurator/index.html): mehrere Profile, leere Messfelder,
  explizites Demobeispiel und JSON-Import/-Export. Lokale Speicherung nur nach Wahl.
  Browserkopien aus einem aelteren Formularstand werden angepasst; die unveraenderte
  oder unlesbare Kopie bleibt als herunterladbare Sicherung, bis die Speicherung
  ausgeschaltet wird.
- [Stuecklisten-Editor](budget/index.html): eigene Mengen, Budgetpreise und Zielmassen;
  JSON-Dateien fuer `tools/suit_budget.py`. Keine automatische Preissuche.

Beide Seiten benoetigen fuer lokale JSON-Referenzen einen HTTP-Server wie oben.
Sie versenden keine Formulardaten. Ein Export bleibt ein Entwicklungsprofil,
keine Druck-, Sicherheits- oder Zulassungsfreigabe.

## Fehlererfassung mit Sentry

Seit 2026-11-19 verwenden Bauhandbuch, Konfigurator, Budgetplaner, Produktkatalog
und Cortana-Viewer die gemeinsame [Initialisierung](monitoring.js). Sentry-Projekt:
`gardenpiratez/halocosplay-frontend`, Projekt-ID `57`, Plattform `javascript`,
Server `https://logging.gardenpiratez.de`. Die vollstaendige oeffentliche DSN
steht in `monitoring.js`; der Hostname allein ist keine DSN. Der API-Token aus
`~/.config/sentry-token` dient ausschliesslich der Administration und wird weder
versioniert noch an Browser oder GitHub Pages uebergeben.

Das offizielle Fehler-Bundle `11.14.0` wird asynchron von Sentrys CDN geladen:
feste Version, offizieller SHA-384-Integritaetshash, anonyme CORS-Anfrage, kein
Referrer. Unbehandelte JavaScript-Fehler und Promise-Rejections werden erfasst;
bis zum SDK-Start werden maximal 20 Fehler gepuffert. Ein blockiertes CDN oder
eine fehlgeschlagene Initialisierung verhindert nicht die Nutzung der App.
Ladefehler von Anleitungen, Konfigurator-Schema und den beiden Budgetbeispielen
werden auch nach ihrer Fehlerbehandlung gemeldet. Validierungsfehler beim Import
eigener Dateien, ein bereits eingefuegtes Nebelmodul und gewoehnliche BLE-Abbrueche
werden nicht eigens gemeldet.

Die Konfiguration aktiviert ausschliesslich Fehlererfassung: keine Replay-,
Tracing-, Sitzungs-, Konsolen- oder Klickaufzeichnung. Automatisches Sammeln
von Benutzerdaten, Cookies, HTTP-Headern/-Bodies und lokalen Stackvariablen ist
abgeschaltet. `beforeSend` entfernt zudem Benutzer, Extras, Breadcrumbs und
Kontexte; gemeldet werden Fehlertext/Stack und die Seitenadresse ohne Query
und Hash. Stackdatei-URLs werden ebenfalls bereinigt. Profilobjekte,
Formularwerte und LocalStorage werden nicht ausgelesen oder angehaengt.
Fehlermeldungen selbst sollten deshalb weiterhin keine privaten Eingaben
enthalten. Die separate Offline-Messeanzeige laedt kein Sentry.

Auf oeffentlichen HTTPS-Seiten ist die Umgebung `production`. Lokal, per HTTP
und bei `file://` wird standardmaessig weder das SDK geladen noch ein Ereignis
gesendet. Ein gezielter lokaler Test kann vor `monitoring.js` setzen:

```js
window.HaloMonitoringOptions = {enabled: true, environment: 'development'};
```

Nach dem SDK-Start laesst sich ein einzelner Testfehler senden:

```js
HaloMonitoring.captureException(new Error('HaloCosplay Sentry test'), 'manual-test');
await Sentry.flush(5000);
```

`window.HaloMonitoringOptions = {enabled: false}` vor der Initialisierung
deaktiviert das Monitoring. Ohne geladene Integration ist die Erfassungsfunktion
ein No-op. Die vorhandenen Dateien werden unminifiziert ausgeliefert;
zusaetzliche Source-Map-Uploads und ein API-Token im Deploy sind nicht notwendig.

Automatisierte Pruefung ohne Netzwerk oder Token:
`node --test Tests/Automation/monitoring.test.cjs`.
Die Sentry-Konfiguration folgt den offiziellen
[CDN-Bundles](https://docs.sentry.io/platforms/javascript/install/loader/#cdn),
[Optionen](https://docs.sentry.io/platforms/javascript/configuration/options/)
und [Integrationen](https://docs.sentry.io/platforms/javascript/configuration/integrations/).
