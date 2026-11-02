# Produktkatalog: digitale Pruefung

Stand: 2026-09-11. Gilt fuer die Produktkatalog-Erweiterung im Entwurfs-PR.

## Umfang

- 52 Eintraege in zehn Kategorien; alle elf Ruestungsteile haben Zuordnungen.
- Zentrale JSON-Quelle, erzeugte Webdaten und erzeugte Markdown-Einkaufsliste.
- Hersteller-/Datenblattlinks getrennt von gekennzeichneten Amazon-Suchlinks.
- Filter nach Text, Baugruppe, Status, Quellentyp, Anleitung und Ruestungsteil.
- Eigene Mengen, JSON-/CSV-Download und validierter JSON-Import.
- Produktzuordnung im Bauhandbuch und in der Teileauswahl des 3D-Betrachters.

## Ergebnisse

- 106 Python-Projekttests bestanden, einschliesslich sechs Katalogtests.
- Zehn vorhandene elektrische Konsistenztests bestanden.
- 38 JavaScript-Tests bestanden, einschliesslich fuenf Katalogtests.
- Generatorvergleich, JavaScript-Syntax, ASCII, relative Markdown-Links und
  `git diff --check` bestanden.
- Chromium-Browsertest bestanden: bestehende Profil-/Budget-Workflows,
  Katalogfilter, Kennzeichnung von Affiliate-Links, Mengen und JSON-Download,
  Import, mobile Breite, leere Suchergebnisse, keine automatische Speicherung,
  Anleitungszuordnung, Offline-Teileauswahl und Ausstellungsanzeige.
- Desktop- und Mobil-Screenshots erzeugt und visuell geprueft.

Lokale Browserpruefung: Playwright 1.58.2 mit Chrome Headless Shell
145.0.7632.6 aus dem offiziellen Chrome-for-Testing-Download. Der Download
ueber das Playwright-CDN war nicht verfuegbar. CI verwendet weiterhin die
vorhandene Version Playwright 1.62.1 und installiert den Markdown-Parser 12
fuer die von externen CDNs unabhaengige Integrationspruefung.

## Grenzen

Die Tests belegen Softwareverhalten und Datenkonsistenz. Produktquellen sind
keine Nachweise fuer aktuelle Preise, Lieferbarkeit, Passform oder elektrische
Gesamtkompatibilitaet. Shop-Suchen bestaetigen keinen bestimmten Artikel.
Das Amazon-Partnerkonto und eine tatsaechliche Verguetung wurden nicht geprueft.
Neue Hardware-, CAD- oder Last-/Temperaturversuche fanden nicht statt.
Die Webseite wird erst mit dem vorhandenen Main-Deployment live aktualisiert.
