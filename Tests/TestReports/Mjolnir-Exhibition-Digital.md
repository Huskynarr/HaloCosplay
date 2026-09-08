# V4: Digitale Pruefung der Ausstellungserweiterung

Stand: 2026-09-08. Keine Aussage ueber einen realen Anzug oder Messefreigabe.

## Lokal ausgefuehrt

- 27 Python-Tests bestanden: bisherige Passform/BOM sowie neun neue Nachweistests.
- Sechs JavaScript-Tests bestanden: unbekannte Daten, Ablauf von Mess-Snapshots,
  Demokennzeichnung, Wertebereiche, Zeitstempel und Uhr-Ruecksprung.
- Syntaxchecks fuer Web-Navigation und Messeanzeige bestanden.
- Markdown-Verweise, ASCII-Konvention und Git-Whitespace geprueft.
- Generierte BOM und Nachweisbericht stimmen mit den Quelldateien ueberein.
- `--require exhibition` liefert erwartungsgemaess Exitcode 2: offene reale Gates.

## Grenzen der Pruefung

Eine visuelle Browserpruefung wurde versucht. Playwright ist vorhanden, aber
kein Browserbinary. Der Browserdownload war nicht erreichbar (Timeout); deshalb
keine behauptete Screenshot-, Mobilgeraete- oder Ende-zu-Ende-Abnahme.
Vor Messebetrieb die Bedienfolge aus Code/Exhibition/README.md im Zielbrowser
pruefen. Insbesondere Dateiauswahl, Fokus, Vollbild und Lesbarkeit am Monitor.

CAD wurde in dieser Erweiterung nicht veraendert. Die frueheren OpenSCAD-Pruefungen
bleiben im separaten Bericht; sie validieren keine fertigen Halo-Oberflaechen.
Sensoranbindung, Kalibrierung, Hardwaretests und physische Vorfuehrung stehen aus.
