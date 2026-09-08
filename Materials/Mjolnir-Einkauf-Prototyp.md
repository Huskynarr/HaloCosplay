# Bezahlbare Einkaufsliste fuer den ersten Prototyp

Stand: 2026-09-08. Umfang: Helm-Belueftung, Elektronikpruefstand und manuell
aufklappbarer Torso als Muster. Noch keine komplette Ruestung und kein fertiges
Exoskelett. Vorhandene Powerbanks, Rechner und Werkzeuge zuerst verwenden.

## Preisgrundlage

Nur E11 ist ein abgelesener Shoppreis (inkl. MwSt., ohne Versand). Die uebrigen
Betraege sind eigene Einkaufsbudgets fuer die angegebene Gesamtmenge, keine
verifizierten Angebote. Verfuegbarkeit und konkretes Modell vor Bestellung pruefen.

- [ESP32 NMCU-ESP32-U bei BerryBase](https://www.berrybase.de/berrybase-nodemcu-esp32-dev-board-wroom32-240-mhz-dual-core-cp2102-34-gpio-5v-ungeloetet):
  6,80 EUR je Board, beim Abruf als verfuegbar gelistet. Ungeloetete Ausfuehrung.
- [Noctua NF-A4x10 5V](https://www.noctua.at/en/products/nf-a4x10-5v):
  Hersteller bestaetigt 40 x 10 mm und 5 V. Preis hier nur budgetiert.
- Die andere, bereits bestueckte BerryBase-Ausfuehrung NMCU-ESP32 war beim
  Abruf als nicht lieferbar gelistet; nicht mit NMCU-ESP32-U verwechseln.

## Auswahl fuer die erste Bestellung

Die Liste beschreibt einen Helm-/Torso-Pruefstand. Mengen sind Ausgangswerte,
keine Vorgabe fuer alle Koerperprofile oder Materialwege. Fuer einen rein
mechanischen Versuch entfallen Controller und Effektelektronik; bei vorhandener
Ausstattung nur Fehlmengen aufnehmen. Eine eigene BOM laesst sich im
[Budget-Editor](../web/budget/) anpassen und als JSON exportieren.

M-Positionen sind herstellerneutrale Einkaufsspezifikationen fuer Muster.
Baumarkt, Naeh-/Outdoor-Zubehoerhandel und Elektronikfachhandel eignen sich
als Bezugswege. Belastbare Datenblaetter haben Vorrang vor Verkaufsversprechen.

| ID | Menge | Konkrete Auswahl / Suchbezeichnung | Budget gesamt EUR | Verwendung |
| --- | --- | --- | ---: | --- |
| E11 | 2 | ESP32 NodeMCU WROOM32, BerryBase NMCU-ESP32-U, ungeloetet | 13.60 | Ein Controller und ein Ersatz; Stiftleisten/USB-Kabel pruefen. Kein Raspberry Pi erforderlich. |
| E12 | 2 | Noctua NF-A4x10 5V, 40 x 40 x 10 mm | 40-50 | Erste Wahl fuer leise Helm-Belueftungsversuche; 5-V-Version, nicht 12 V. Luftfuehrung separat testen. |
| E13 | 2 | 40-mm-Lueftergitter und passende Abstandshalter | 6-12 | Haar-/Fingerkontakt vermeiden, Luftweg freihalten. |
| E14 | 1 Satz | 5-V-Kabelbaum: Kupferlitze, passende Steckverbinder, Schrumpfschlauch, Sicherungshalter und Schalter | 25-45 | Sensor-/Leistungszweige trennen; Querschnitt und Sicherungswert nach gemessenem Strom festlegen. |
| E15 | 1 Satz | Lochraster, Stiftleisten, Widerstaende, kleines Gehaeuse | 10-18 | Geloeteter Aufbau fuer den Anzug; Steckbrett nur auf dem Tisch. |
| E16 | 1 | USB-Messgeraet fuer Spannung, Strom und Energie | 10-20 | Nur falls kein geeignetes Messgeraet vorhanden; Stecker muessen zur Powerbank passen. |
| M11 | 5 m | Polyester-Gurtband 25 mm | 8-15 | Modulbefestigungen; Breite und Verarbeitung an einem Muster testen. |
| M12 | 2 m | Polyester-Gurtband 50 mm | 5-10 | Breite Lastverteilung mit Polsterung; noch kein fertiger Hueftgurt. |
| M13 | 1 Satz | Vier 25-mm-Steckschnallen aus Acetal plus acht passende Dreistege | 10-18 | Dokumentierte Qualitaet, keine ungeprueften Dekoschnallen als alleiniger Torsohalt. |
| M14 | 3 m | Aufnaehbares Haken-/Flauschband, etwa 25 mm breit | 8-15 | Polster und leichte Abdeckungen; nicht alleiniger tragender Verschluss. |
| M15 | 1 Platte | Geschlossenzelliger EVA-Schaum, etwa 10 mm, mindestens 50 x 50 cm | 10-20 | Austauschbare Polster; Kontaktflaechen anprobieren. |
| M16 | 1 Satz | M3/M4-Maschinenschrauben, breite Scheiben und selbstsichernde Muttern | 15-25 | Musterbau. Schraubenlaenge nach Schichtaufbau; Lastbemessung nicht durch Sortiment ersetzt. |
| M17 | 4 | Kleine Metallscharniere, etwa 30-40 mm, ohne Feder | 12-24 | Nur erste ungetragene Tuerprobe; Schraubmontage mit Gegenplatten. |
| M18 | 2 | Mechanische Spannverschluesse mit separater Sicherung | 10-20 | Muster fuer Griffzugang und Entriegelung; keine elektrische Verriegelung. |
| M19 | 1 Satz | Pappmaterial plus 6-9-mm-Sperrholzreste und Holzleisten | 15-25 | 1:1-Passmodell und ungetragener Mechanikpruefstand, nicht fertiger Ruestungstraeger. |

Summe erste Bestellung: **197.60-330.60 EUR**, ohne Versand und Werkzeuge.
Mit 20 % eigener Einkaufsreserve: **237.12-396.72 EUR**.
Bei vorhandenem Messgeraet oder Befestigungsmaterial reduziert sich der Bedarf.
Diese Liste konkretisiert Teile von E01/P01/T03-T06 und dem Traegerbudget aus der
[Basis-BOM](Mjolnir-BOM.md). Nicht pauschal auf deren Gesamtsumme aufschlagen.

## Sinnvolle Ergaenzungen, noch nicht im Gesamtbetrag

| Menge | Bauteil | Budget gesamt EUR | Kaufbedingung |
| --- | --- | ---: | --- |
| 1 | DS18B20-Sensormodul mit dokumentierter 3,3-V-Beschaltung | 5-12 | Messort festlegen; Lufttemperatur, kein medizinischer Koerpersensor |
| 1 m | WS2812B, 5 V, 30 LEDs/m, plus 74AHCT125-Pegelwandler und Beschaltung | 15-25 | Erst Lichtpositionen bestimmen; LED-Strom separat, nicht aus GPIO |
| 2 | Kleine Mikroschalter mit Hebel plus Halter | 4-10 | Reine Positionsanzeige, keine Sicherheitsfreigabe |
| 1 | Fertiger Sprachverstaerker mit kabelgebundenem Mikrofon | 30-60 | Zuerst Sprachverstaendlichkeit mit Helm und Rueckkopplung testen |
| 1 | Fertige Marken-Powerbank, falls vorhandene ungeeignet | 25-45 | 5-V-Port, Abschaltverhalten bei kleiner Last und reale Laufzeit pruefen |

Keine automatische Sensorintegration ist bereits fertig. Der vorhandene
ESP32-Beispielcode muss an Board-Pinbelegung, Sensor und Versorgung angepasst
werden. Die Messeanzeige importiert bislang Dateien und steuert keine Hardware.

## Erst nach dem Passmodell bestellen

- **Seitliche Linearfuehrungen:** Schienenlaenge, Hub und Wagenanzahl aus der
  geoeffneten Tuergeometrie bestimmen. Fuer einen ungetragenen Holzversuch kann
  ein kompaktes Schubladenfuehrungspaar (Budget 20-40 EUR) die Bewegung zeigen;
  dessen Eignung am Koerper ist damit nicht bewiesen. Fuer die endgueltige
  Variante leichte Polymergleitfuehrungen mit Last-/Momentdaten vergleichen.
- **Endgueltiger Traeger/Hueftgurt:** zuerst einen gut sitzenden vorhandenen
  Rucksack-Hueftgurt als Passreferenz nutzen. Anprobe mit Last; kein blindes
  Kaufen eines schweren taktischen Plattentraegers. Eigene Halter bemessen.
- **Serien-Exoskelett:** Hypershell/DNSYS bleiben Anprobekandidaten aus dem
  Exoskelett-Guide. Kein Budgetgeraet ohne belegten Sitz und Integrationsraum kaufen.
- **Motoren, Gasfedern, Linearaktuatoren:** Auswahl erst aus realer Masse,
  Schwerpunkt, Hebelarm, Hub und Ausfallverhalten. Die manuelle Oeffnung liefert
  bereits den gewuenschten zusammenhaengenden Einstieg ohne Servokauf.
- **Visier:** erst Schablone und Durchsichtsmuster, dann passender Rohling/Form.
  Keine zufaellige Motorradvisierform fuer einen noch nicht modellierten Helm.
- **Anzug-STL-Set:** exakt zur gewaehlten Ruestungsreferenz passendes Set mit
  nachweisbarer Nutzungserlaubnis. Vor Vollkauf Helm/Torso und Teilbarkeit pruefen;
  Chief / Mark VI GEN3 und Mark VII nicht mischen.

## Elektrische Grundentscheidung

Komfortzweig mit Lueftern von der Anzeige-/Effektsteuerung trennen. Luefter
laufen unabhaengig vom ESP32; Ausstieg bleibt mechanisch. Powerbank liefert
5 V, ESP32-GPIO verwendet 3,3-V-Logik. Luefter/LEDs niemals direkt aus einem
GPIO versorgen. Kein PD-Trigger fuer hoehere Spannung am 5-V-Zweig.

Fuer jede Leitung vor Einbau Strom inkl. Einschaltspitze, Laenge, Querschnitt,
Steckerkapazitaet und passende Absicherung bestimmen. Vorhandene Powerbanks
nicht ohne deren Freigabe parallel verbinden oder waehrend des Tragens laden.

## Noch fehlende Detailmodelle

| Baugruppe | Konkrete fehlende Datei / Konstruktion |
| --- | --- |
| Helm | Originalgetreue Schale, Teilung, Visierkontur/Formwerkzeug, Polster-/Luefterhalter |
| Torso | Brust/Ruecken/Seitenhaut, Rahmen, Fuehrungs- und Scharnierhalter, Verschlussgegenstuecke |
| Schultern | Linke/rechte Aussenform, bewegliche Halterung und gepruefte Helmfreiraeume |
| Arme | Ober-/Unterarmschalen, Handschutz, Gelenkfreiraeume und bedienbare Verschluesse |
| Huefte | Bauchlamellen, flexible Uebergaenge, Gurtaufnahme und Sitzfreiheit |
| Beine | Oberschenkel, Knie, Schienbein, Schuhcover und individuelle Schalenhalter |
| Unteranzug | Schnittmuster/Passform, Texturauflagen und Servicezugang |
| Ausstellung | Standrahmen, Aufnahmen, Kippsicherung und Transporteinlagen |

Es fehlen dabei die **detaillierten Halo-Aussenformen und passend konstruierte
Verbindungen**, nicht nur eine STL-Exportfunktion. Das vorhandene CAD zeigt
Bauraum und Oeffnungsprinzip. Leere STL-Platzhalter sind keine Druckdateien.

Hardwareauslegung bedeutet konkret: reales Bauteil wiegen, Schwerpunkt/Lastpfad
bestimmen, Gelenke und Halter dagegen auslegen, Freiraeume nachweisen und am
Prototyp pruefen. Fuer Aktorik kommt die Kraft ueber den gesamten Weg hinzu.
Fuer den Staender fehlen reale Standlast, Schwerpunkt und offener Fussabdruck.

[Messanleitung](../Documentation/Guides/Mjolnir-Massanpassung.md) und
[ausfuellbares Messblatt](../Design/Parametric/Profiles/Messprotokoll.csv).
