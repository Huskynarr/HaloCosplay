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

## V4-Baukasten

V4 ist der Standard fuer neue Browserprofile. Bestehende V1-V3-Auswahl bleibt
erhalten. Die Haken dokumentieren Lesefortschritt, keine physische Bauabnahme.
Der Nachweisbericht im V4-Baukasten bleibt davon unabhaengig. Die separate
[Messeanzeige](../Code/Exhibition/README.md) arbeitet auch ohne Internet.

## Profile und Stuecklisten

- [Profil-Konfigurator](configurator/index.html): mehrere Profile, leere Messfelder,
  explizites Demobeispiel und JSON-Import/-Export. Lokale Speicherung nur nach Wahl.
- [Stuecklisten-Editor](budget/index.html): eigene Mengen, Budgetpreise und Zielmassen;
  JSON-Dateien fuer `tools/suit_budget.py`. Keine automatische Preissuche.

Beide Seiten benoetigen fuer lokale JSON-Referenzen einen HTTP-Server wie oben.
Sie versenden keine Formulardaten. Ein Export bleibt ein Entwicklungsprofil,
keine Druck-, Sicherheits- oder Zulassungsfreigabe.
