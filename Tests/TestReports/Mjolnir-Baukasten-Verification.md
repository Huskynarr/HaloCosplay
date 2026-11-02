# Softwarepruefung: konfigurierbarer Baukasten

Dieser Bericht beschreibt die Umstellung auf allgemeine Projektprofile.
Er erteilt keine Fertigungs-, Trage- oder Messefreigabe.

## Lokal ausgefuehrte Pruefungen

- 41 Python-Tests bestanden: Passformparameter, Messherkunft, getrennte
  Projektverzeichnisse, portable CAD-Exporte, Budget, Nachweise und SVG-Ausschnitt.
- 29 Node-Tests bestanden: Profilimport und Python-Interoperabilitaet,
  Budgetberechnung, Messeanzeige, zeitliche Gueltigkeit und konkurrierende Importe.
- Generierte Budget- und Nachweisberichte sind aktuell; alle physischen
  Nachweisgruppen des Musterregisters bleiben offen.
- ASCII-Konvention, relative Markdown-Links, Python-/JavaScript-Syntax und
  Git-Whitespacepruefung bestanden.
- Dokumentierte CLI-Ablaeufe fuer leere Profile, Ablehnung fehlender Masse,
  ausdrueckliche Demo, eigene Budgetdatei und neues Nachweisregister ausgefuehrt.

## Browser und CAD in CI

`Tests/Browser/smoke.cjs` prueft die realen Oberflaechen: Profilwechsel,
Browser-Speicherung nach Einwilligung, JSON-Downloads und -Importe, Kosten und
getragene Planmasse, mobile Seitenbreite und Datenreset bei Projektwechsel.
Der GitHub-Workflow fuehrt diesen Test mit Chromium aus und legt Screenshots ab.
Lokal fehlte ein Browser; der Download war blockiert. Daher ist kein lokaler
Browser- oder visueller Prueferfolg dokumentiert. Den CI-Lauf des konkreten
Commits fuer dessen Ergebnis heranziehen.

Der CAD-Job kompiliert vier Konzeptstellungen, Testkoerper und eine unabhaengige
Profilausgabe. OpenSCAD war lokal nicht verfuegbar. Die neue portable Datei
enthaelt denselben Modellcode mit einem relativen Parameter-Include.

## Aussagegrenzen

Die Startvorlage enthaelt keine Koerpermasse. Demo und generierte Vorschauen
verwenden rein synthetische Werte. Referenz, Material und Technikoptionen
dokumentieren den geplanten Aufbau; sie erzeugen keine fertigen Halo-Detailmodelle
oder nachgewiesene Hardwareintegration. CAD bleibt eine vereinfachte Bauraumhuelle.
Nachweisdateien werden auf Zuordnung und Integritaet geprueft, nicht auf die
Wahrheit ihrer Messungen. Physische Pass-, Ausstiegs-, Last- und Funktionstests
bleiben je Projekt erforderlich.
