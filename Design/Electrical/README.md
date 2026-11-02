# Elektrische Stromlaufplaene electrical-r1

Stand: 2026-09-09. Verdrahtungsentwurf mit Bauteilsymbolen, Pins, Netznamen,
Steckertabelle und maschinenlesbarer Netzliste. **Keine gefertigte Platine,
keine KiCad-ERC-Pruefung und keine elektrische Bauabnahme. Vor Klaerung der
unten genannten Einschalt-/Abschaltprobleme nicht am getragenen Anzug
bestromen.** Die SVGs sind ohne externe Symboldateien mit Inkscape editierbar.

## Dateien und Bearbeitung

| Datei | Inhalt |
| --- | --- |
| [01-Comfort.svg](01-Comfort.svg) | Eigene 5-V-Quelle, Sicherung, Schalter und vier Luefteranschluesse |
| [02-Effects-Power.svg](02-Effects-Power.svg) | PD-Schnittstelle, 15-V-Verteilung, lokale 5 V und Relaiskontakt |
| [03-Helmet-RGB.svg](03-Helmet-RGB.svg) | Drei LDD-Treiber und sechs LED-Chips des Helmpaars |
| [04-Nozzle-RGB.svg](04-Nozzle-RGB.svg) | Drei LDD-Treiber und sechs LED-Chips des Duesenpaars |
| [05-Control.svg](05-Control.svg) | Pegelpuffer, Eingangspulldown, MOSFET, Relaisspule und Freilaufdiode |
| [Netlist.json](Netlist.json) | Komponenten-/Pinzuordnung, Netze und offene Werte |
| [Connectors.md](Connectors.md) | Stecker- und Signalbelegung |
| [BOM.md](BOM.md) | Bauteilreferenzen, Werte und Herstellerquellen |
| [generate.py](generate.py) | Deterministische Schaltplanquelle und Topologiepruefer |
| [test_electrical.py](test_electrical.py) | Kurzschluss-, Polaritaets-, Netz- und stationaere Logiktests |

Aus dem Repository-Hauptordner:

```bash
python3 Design/Electrical/generate.py --check
python3 -m unittest discover -s Design/Electrical -p 'test_*.py' -v
```

`--check` liest nur und meldet geaenderte/veraltete Ausgaben. Aenderungen erfolgen
in `design()` und den Layoutfunktionen von `generate.py`; ohne `--check` werden
die acht erzeugten Textdateien neu geschrieben. Ein direkter SVG-Eingriff ist
moeglich, wird aber bei der naechsten Generierung ueberschrieben. Fuer eigene
Varianten einen neuen Ordner mit `--out` verwenden und die Quelldatei mitfuehren.
Im kopierten Werkstattpaket funktionieren dieselben Befehle mit dem dortigen
Pfad oder direkt im Ordner als `python3 generate.py --check`.

## Schaltungsentscheidungen

**Komfort:** J10 erhaelt geregelte 5 V aus einer eigenen Quelle. F10 liegt nahe
am Ausgang, S10 schaltet nur diesen Kreis. J11...J14 verwenden die native
Noctua-Vierpolbelegung: 1 GND, 2 Versorgung, 3 Drehzahl, 4 PWM. Fuer passende
5-V-Modelle bleiben 3 und 4 jeweils offen; ohne PWM laufen diese Luefter mit
Nenndrehzahl. Keine 12-V-Variante ungeprueft einsetzen. Quelle:
[Noctua PWM White Paper](https://www.noctua.at/pub/media/wysiwyg/Noctua_PWM_specifications_white_paper.pdf).

Eine konkrete 60-mm-5-V-PWM-SKU wird damit nicht vorausgesetzt. Dreiadrige
5-V-Luefter benoetigen eine gepruefte, angepasste Dreipol-Steckerbelegung;
deren Anschluss folgt nicht automatisch der hier gezeichneten Vierpolform.

**Effekte:** J20 stellt die Ausgangsschnittstelle des SparkFun DEV-15801 dar.
Die STUSB4500-PDOs werden im NVM konfiguriert; der Plan verlangt nachgewiesene
15 V. Ein passiver USB-C-Adapter reicht nicht. Die Konfiguration ist noch nicht
in dieser Software enthalten. Quelle:
[SparkFun DEV-15801](https://www.sparkfun.com/sparkfun-power-delivery-board-usb-c-qwiic.html).

U20 ist ein fertiger Pololu D24V10F5. VIN/GND/VOUT sowie unbenutzte PG/SHDN sind
explizit eingezeichnet. Die etwaige 1-A-Angabe ist kein garantierter Strom im
warmen Einbau. C20 ist ein Entwurfswert gegen moegliche LC-Spitzen; die reale
Leitung bleibt zu messen. SHDN nicht an einen GPIO anschliessen: der interne
Pull-up fuehrt zu VIN. Quelle: [Pololu #2831](https://www.pololu.com/product/2831).

**LEDs:** U30...U35 sind ausschliesslich LDD-350L, Pinbauform. Das Datenblatt vom
2024-08-02 zeigt in der Unteransicht: 1 +Vin, 3 DIM, 4 -Vin, 5 -Vout, 6 +Vout.
Jeder Ausgang betreibt zwei gleichfarbige Chips in Reihe. Die LED-Ausgaenge
bleiben vom Versorgungsrueckleiter getrennt. Der LDD erwartet LOW unter 0,5 V,
HIGH ueber 3,5 V bis 8 V oder einen offenen Eingang; offen bedeutet EIN.
100...1000 Hz sind der dokumentierte PWM-Bereich. Quelle:
[MEAN WELL LDD-L](https://www.meanwell.com/Upload/PDF/LDD-L/LDD-L-SPEC.PDF), Seiten 1/3/5.

**Pegel:** B30...B35 sind SN74AHCT1G125DBVR mit 5-V-Versorgung, 10-kohm-
Eingangspulldown und je 100 nF unmittelbar am IC. /OE bleibt an Masse.
Pins: 1 /OE, 2 A, 3 GND, 4 Y, 5 VCC. Die TTL-Schwellen passen zu einer
qualifizierten 3,3-V-Quelle. DIM-Strom sowie HIGH/LOW direkt am LDD muessen
gemessen werden; das LDD-Datenblatt begrenzt den internen DIM-Pull-up-Strom
nicht ausreichend fuer eine pauschale Freigabe. Quelle:
[TI SN74AHCT1G125 Rev. P](https://www.ti.com/lit/ds/symlink/sn74ahct1g125.pdf).

**Freigabe:** K20 ist G5LE-1A DC5, mit offenem Ruhekontakt 1 COM / 3 NO und
Spule 2/5. Q20 schaltet nur die Spule. Sein 10-kohm-Gatepulldown sperrt bei
offenem READY-Signal. D20 liegt mit Kathode an 5 V und Anode am Drain.
Der AO3400A ist bei 2,5 V Gate-Ansteuerung spezifiziert; SOT-23-Pins sind
1 Gate, 2 Source, 3 Drain. Quellen:
[Omron G5LE](https://omronfs.omron.com/en_US/ecb/products/pdf/en-g5le.pdf),
[AO3400A](https://www.aosmd.com/res/data_sheets/AO3400A.pdf),
[Vishay 1N400x](https://www.vishay.com/docs/88503/1n4001.pdf).

Der Controller wird aus E5_CTRL versorgt und braucht einen dokumentierten
5-V-Eingang mit eigener 3,3-V-Regelung. J30 fuehrt keine Versorgung zum GPIO.
READY darf erst nach initialisierten LOW-PWM-Pins gesetzt werden. GPIOs mit
Boot-Pull-up oder Startimpulsen sind zu vermeiden. Sechs Kanaele sind in der
Netzliste vollstaendig vorhanden; Blatt 05 zeigt den einen sechsmal identisch
aufzubauenden Pufferkanal.

## Noch offene Hardwareentscheidungen

- Sicherungstyp, Nennstrom, Abschaltvermoegen, Leitungsquerschnitt und
  Steckerfamilie folgen realen Maximal-/Einschaltstroemen und Leitungswegen.
  Ein `TBD` ist kein baubarer Sicherungswert.
- J21 erwartet eine potentialfreie Temperaturkontaktkette. Bauteile,
  Messpositionen, Grenzwerte und Wiedereinschaltsperre sind noch auszulegen.
  Ohne diese Kette bleibt der Anschluss offen und das Relais abgefallen.
- Der logische Reset-AUS-Nachweis gilt stationaer fuer hochohmige GPIOs.
  **Konkreter offener Fehlerfall:** E15_LED bleibt kurz vorhanden, waehrend
  E5_CTRL zusammenbricht oder F21 oeffnet. Der interne DIM-Pull-up kann ueber
  die Ausgangsschutzstruktur des AHCT-Puffers nach E5_CTRL rueckspeisen.
  Fuer diesen Puffer wird keine Ioff-Funktion angenommen. D20 kann zudem das
  Abfallen von K20 verzoegern. Diese Schaltung beseitigt das moegliche
  Zwischenaufleuchten bzw. Rueckspeisen noch nicht nachweislich. Am Tisch DIM,
  E5_CTRL und E15_LED gleichzeitig beim 5-V-Ausfall, F21-Oeffnen, Start und
  MCU-Reset aufzeichnen; eine eventuelle Schutzstufe danach neu auslegen.
- Kontaktprellen und Abschaltzeiten sind mit realer Last zu messen. Ein
  Relais-Datenblattwert ohne Freilaufdiode gilt nicht fuer diesen Aufbau.
  Verschweisste Kontakte, durchlegierter MOSFET oder haengender MCU sind
  nicht fehlertolerant abgefangen. S20 trennt die Energie direkt. Es gibt
  keinen implementierten Hardware-Watchdog und keine fertige Leistungskanal-
  Firmware.
- Nebelgeraet, AR-Brille und Begleitroboter-Sender behalten Originalelektronik
  und Herstellerakkus. Hier gibt es keine Verbindung zu Robotermotoren,
  Drohnensteuerung oder unbekannten OEM-Pins. HUD/USB, Audio und trockene
  Duesenluefter brauchen eigene gepruefte Abgaenge; sie sind in dieser Revision
  nicht an F21 angeschlossen.

## Pruefung am Tisch

Zuerst ohne LEDs: Spannung, Polung, Sicherungsweg, K20-Ruhezustand und getrennte
Versorgungsnetze pruefen. Danach die beschriebenen DIM-/Versorgungsproben bei
Start, Reset, abgezogenem J30, offenem J21 und 5-V-Ausfall aufnehmen. Erst dann
ein gekuehltes RGB-Paar am Tisch pruefen. Gemessene Last, Stromtoleranzen,
Temperaturen, Kamerabanding und Spannungsabfaelle bestimmen die naechste
Revision. Topologietests ersetzen weder diese Messungen noch Trageproben.
