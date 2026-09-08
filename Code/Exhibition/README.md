# Offline-Messeanzeige

`index.html` direkt im Browser oeffnen. Alle Styles und Skripte liegen lokal;
keine CDN-, Font-, Cloud- oder Sensorverbindung. Alternativ im Repo-Root:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Dann `http://127.0.0.1:8000/Code/Exhibition/` oeffnen. Keine automatische
Veroeffentlichung und keine Verbindung zu Arduino, Exoskelett oder Aktorik.

## Bedienung

Start ohne Werte. "Beispieldaten zeigen" zeigt markierte synthetische Werte.
"Mess-Snapshot laden" liest eine lokale JSON-Datei; kein Upload und keine
Speicherung. "Anzeige leeren" entfernt die Werte. JSON-Dateien bis 16 KiB.
Alle Quelldaten werden als Text dargestellt, nicht als HTML interpretiert.

Ein Mess-Snapshot ist keine Live-Verbindung. Nach zehn Sekunden ab seinem
Messzeitpunkt werden seine Zahlen ausgeblendet. Zukuenftige Zeitstempel werden
abgelehnt. Uhr von Messgeraet und Anzeigerechner vor der Demo abgleichen.
Ungenaue Uhren koennen Daten als ungueltig/veraltet markieren. Die Datei kann ihre
Herkunft nicht beweisen: source=measured ist eine Angabe des Erstellers.

## Datenvertrag, Version 1

```json
{
  "schema_version": 1,
  "source": "measured",
  "device": "Akku A / Helm innen links / Luefter 1",
  "timestamp": "2026-09-08T12:00:00Z",
  "battery_pct": null,
  "temperature_c": null,
  "fan_rpm": null
}
```

Zeitstempel ersetzt die Platzhalterzeit durch den realen Aufnahmezeitpunkt.
Unbekannte Sensorwerte sind `null`, niemals ein erfundener Normalwert. Alle drei
Wertfelder muessen vorhanden sein. Plausibilitaetsbereiche 0-100 %, -40 bis 125 C
und 0-50000 rpm sind lediglich Parsergrenzen, keine sicheren Betriebsgrenzen.
Kalibrierung, Messort, Messintervall und konkrete Hardware separat dokumentieren.
Eine automatische Verbindung zur vorhandenen Sensor-Bridge ist noch nicht implementiert.

## Vorfuehrpruefung

Ohne Netzwerk laden; Start ohne Werte pruefen. Demo aktivieren und Kennzeichnung
lesen. Einen frischen Snapshot importieren; nach zehn Sekunden muessen die Zahlen
verschwinden. Defekte Datei laden: keine alten Messwerte duerfen sichtbar bleiben.
Diese Anzeige ersetzt weder reale Sicherheitsfunktionen noch Hardwarepruefung.

```bash
node --test Tests/Automation/exhibition.test.cjs
```

[Messebetrieb](../../Documentation/Guides/Mjolnir-Messebetrieb.md) und
[Nachweisbericht](../../Progress/Mjolnir-Readiness.md).

## Beliebige Projekte praesentieren

Die Anzeige enthaelt keine feste Person mehr. "Projektprofil laden" liest den
JSON-Export aus dem [Konfigurator](../../web/configurator/index.html). Projektname,
Ruestungsreferenz, Material und Betriebsart werden als reine Planangaben angezeigt.
Koerpermasse werden nicht ausgegeben. Die Anzeige prueft diese drei Angaben nur
als begrenzte Textfelder; die vollstaendige Profilpruefung erfolgt im Konfigurator
und in `tools/suit_fit.py`. Ein Import aendert keine Aktorik oder Sensorhardware.

Projektwechsel und "Projekt entfernen" leeren vorhandene Telemetrie, damit Werte
nicht versehentlich dem naechsten Anzug zugeordnet werden. Alle Daten bleiben
fluechtig im aktuellen Browserfenster; keine Speicherung oder Uebertragung.
