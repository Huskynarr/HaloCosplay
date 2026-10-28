# Thermische Planrechnung

Der Rechner trennt gemeinsame RGB-Kuehlkoerper, einzelne LED-Chips und gemessene
Elektronik-Luftkanaele. [Template.json](Template.json) enthaelt keine Messwerte.
[Demo.json](Demo.json) ist eine rein synthetische Rechenprobe: keine
Herstellerwerte, eingetragenen Temperaturgrenzen oder bestaetigten Luftstroeme.

## Verwendung

```bash
python3 tools/suit_thermal.py --init build/Projekt/thermal.local.json --name Projekt
python3 tools/suit_thermal.py --input build/Projekt/thermal.local.json --out build/Projekt/Thermal
python3 tools/suit_thermal.py --input build/Projekt/thermal.local.json --out build/Projekt/Thermal --check
```

Die Eingabedatei wird zwischen Initialisierung und Berechnung mit Projektdaten
ergaenzt. Ohne `--out` entsteht `<Eingabename>-thermal` neben der Eingabedatei.
`--check` prueft vorhandene Berichte und veraendert keine Dateien. Die
Initialisierung ueberschreibt keine Datei. Berichte koennen aktualisiert werden,
duerfen aber weder die Eingabe selbst noch einen Hardlink darauf ueberschreiben.

Der Export schreibt `ThermalReport.json` und `ThermalReport.md` mit dem SHA-256
der unveraenderten Eingabedatei. `null` bleibt unbekannt und wird nicht als null
Watt oder gemessener Luftstrom behandelt. `modules: []` oder `vents: []` laesst
den betreffenden Bereich explizit aus. Eingabestatus: `inputs_pending`,
`synthetic` oder `entered`; keiner davon bedeutet Hardwarefreigabe.

Die Python-Schnittstelle bietet `new_project(project)`, `calculate(data)`,
`render(report)` und `export(input_path, out=None, check=False)` an. `export`
liefert das berechnete Report-Dictionary zusaetzlich zu den beiden Dateien.

## Gemeinsamer Kuehlkoerper und RGB-Chips

Jeder Eintrag in `modules` beschreibt **einen** gemeinsamen Kuehlkoerper. Zwei
RGB-Stars auf getrennten Kuehlkoerpern sind zwei Module. Eine gemeinsame
Stromquelle oder elektrische Reihenschaltung macht daraus keinen gemeinsamen
thermischen Knoten. Ein raeumlich getrennter LED-Treiber wird an seinem eigenen
Einbauort bilanziert.

| Feld | Einheit | Bedeutung |
| --- | --- | --- |
| `heat_load_w` | W | Gesamte lokale Waermeleistung am gemeinsamen Kuehlkoerper |
| `ambient_c` | Grad C | Umgebungstemperatur unmittelbar am Kuehlkoerper |
| `sink_ambient_k_per_w` | K/W | Thermischer Widerstand vom Kuehlkoerper zur Umgebung im Einbauzustand |
| `surface_limit_c` | Grad C | Projektspezifisch begruendete zulaessige Oberflaechentemperatur, sonst `null` |
| `junction_paths[].heat_w` | W | Waermeleistung des einzelnen Chips, bereits in `heat_load_w` enthalten |
| `junction_paths[].junction_to_sink_k_per_w` | K/W | Vollstaendiger Chip-Kuehlkoerper-Pfad einschliesslich Kontaktlagen |
| `junction_paths[].junction_limit_c` | Grad C | Begruendete Betriebsgrenze des konkreten Chips, sonst `null` |

Die Formeln sind:

```text
Tsink = Ta + Pgesamt * Rsa
Tjunction = Tsink + Pdie * Rjunction-sink
Temperaturabstand = eingetragene Grenze - errechnete Temperatur
Maximales Rsa aus Oberflaechengrenze = (Grenze - Ta) / Pgesamt
```

`heat_load_w` umfasst die Summe aller am Kuehlkoerper wirksamen Waermequellen.
Die Chip-Leistungen werden daher **nicht erneut addiert**. Die Summe bekannter
Chip-Leistungen darf die angegebene Gesamtleistung nicht ueberschreiten. Ein
nicht einzelnen Chips zugeordneter Rest wird im Bericht ausgegeben.

Die volle elektrische Eingangsleistung lokal als Waerme anzusetzen ist eine
konservative Planannahme. Die synthetische Probe setzt insgesamt 4 W und 5 K/W
bei 20 Grad C an: Tsink = 40 Grad C. Der rote Beispielchip mit 1,5 W und 2 K/W
liegt im Modell bei 43 Grad C. Das sind keine Werte eines kaufbaren RGB-Moduls.

Das maximale Rsa beruecksichtigt nur die eingetragene Oberflaechengrenze. Die
einzelnen Chipgrenzen werden gesondert bewertet. Liegt die Umgebung bereits an
oder ueber der Grenze, liefert der Rechner bei positiver Waermeleistung keinen
positiven Widerstand als scheinbar brauchbaren Zielwert. Ohne Waermeleistung
entsteht keine sinnvolle Widerstandsobergrenze. Die jeweils konkrete Begruendung
steht in `surface_resistance_bound_note`.

Ein Katalogwert Junction-to-case darf nicht als kompletter Junction-to-sink-Pfad
uebernommen werden. Leiterplatte, Isolierfolie, Kontakt, Klebung und Geometrie
gehoeren zum Pfad. Das vereinfachte Modell nimmt einen gleichmaessig temperierten
Kuehlkoerper an und loest weder Hotspots noch die thermische Kopplung im LED-
Gehaeuse auf. Temperaturgrenzen und Materialeignung werden nicht erfunden.

## Elektronik-Luftkanal

| Feld | Einheit | Bedeutung |
| --- | --- | --- |
| `heat_w` | W | Elektronikwaerme, die der betrachtete Luftstrom im Modell aufnimmt |
| `measured_flow_m3_h` | m3/h | Gemessener Volumenstrom im fertig eingebauten Kanal |
| `ambient_c` | Grad C | Temperatur der eintretenden Luft |
| `rho_kg_m3` | kg/m3 | Zur Eingabesituation passende Luftdichte |
| `cp_j_kg_k` | J/(kg K) | Zur Eingabesituation passende spezifische Waermekapazitaet |

```text
Delta T = P / (rho * cp * Q / 3600)
Modell-Ablufttemperatur = Umgebung + Delta T
```

Die synthetische Probe mit 12 W, 6 m3/h, 1,2 kg/m3 und 1000 J/(kg K) liefert
einen Temperaturanstieg um 6 K. Der Freiluftwert eines Luefters ersetzt keine
Volumenstrommessung hinter Gitter, Filter, Schlauch und Einlass. Derselbe
Waermepfad darf nicht zweimal addiert werden: Kuehlkoerper- und Luftrechnung
sind getrennte Betrachtungen, keine automatisch summierte Gesamtbilanz.

Bei Null-Volumenstrom gibt es fuer positive Waermeleistung keine endliche
stationaere Loesung in diesem reinen Lufttransportmodell. Das Ergebnis bleibt
`null` mit ausdruecklichem Befund; damit wird weder eine reale unendliche
Temperatur noch das Fehlen anderer Waermewege behauptet.

Diese Rechnung bewertet sensible Elektronikwaerme. Koerperwaerme, Verdunstung,
Feuchtigkeit, Atemluft, Beschlag und menschlicher Waermekomfort sind nicht
Bestandteil des Modells. Ebenso fehlen Aufheizzeit, Pulsbetrieb, Sonneneintrag,
Rueckstrom heisser Abluft und Ausfaelle. Positive Temperaturabstaende sind
Rechenergebnisse und ersetzen keine Messung am aufgebauten Modul.
