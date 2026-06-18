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
