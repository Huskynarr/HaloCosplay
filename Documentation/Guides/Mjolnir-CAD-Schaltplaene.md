# CAD-Modelle und elektrische Schaltplaene

Dieser Ausbau liefert editierbare Einbauteile und elektrische Referenzentwuerfe.
Die Modelle enthalten reale Ausschnitte, Befestigerbohrungen und getrennte
Montageteile. Ihre Beispielmasse gehoeren zu keinem bestaetigten Kaufgeraet.
Die elektrische Verbindungstopologie ist dokumentiert; Sicherungen, Leitungen,
Temperaturgrenzen und Hardwareversuche bleiben projektspezifisch.

## 1. Modelle

| Baugruppe | Zweck | Anpassung vor dem Einbau |
| --- | --- | --- |
| Powerbankhalter | Offene, mit Gurten befestigte Aufnahme | Reale Geraetehuelle, Portlage, Gurt und Gewicht |
| Originalsenderhalter | Zugreifbare Funkkassette am Anzug | Senderabmessungen, Tasten, Antenne und Koerperabschattung |
| Kameragehaeuse | Sensorpod mit abnehmbarem Deckel und optischem Ausschnitt | Kameraplatine, Objektiv, Sichtfeld und Kabel |
| HUD-Traeger | Klappbare Halterung mit Gelenk und Einstellschlitzen | Vollstaendige Optik, Augenraum, Parkposition und Kabel |
| Duesengehaeuse | Trockene Licht-/Luftkomponenten um freien Zentralbereich | OEM-Nebelaustritt, Metallkuehlung, Abstand und trockener Luftweg |
| Elektronikfach | Belueftete Serviceaufnahme mit abnehmbarem Deckel | Platinen, Abstandshalter, Steckverbinder und Waerme |

[CAD-Quellen und Einzelteilregister](../../Design/HardwareKit/README.md).
Die neuen Teile ergaenzen die vorhandenen
[Clamshell-Modelle](../../Design/Clamshell/README.md) und
[Passproben](../../Design/Components/README.md). Eine vollstaendige
originalgetreue Halo-Aussenruestung wird dadurch nicht erzeugt.

Hardwareabmessungen werden nicht mit Koerpergroesse skaliert. Ein 40-mm-Luefter
bleibt bei unterschiedlichen Anzugprofilen gleich gross; nur seine Einbaulage
und die umgebende Schale aendern sich. Ohne ausgewaehlten AR-Bildgeber wird der
HUD-Traeger nicht als optisch passende Halterung fuer XREAL oder ENMESI behauptet.

Die Duesenblende ist eine trockene Lichtaufnahme. Eine abgesetzte heisse
OEM-Nebelkammer braucht einen eigenen, noch auszulegenden Halter. Technik,
Kammerverlaengerung und Alternativen: [Nebeltechnik](Mjolnir-Nebeltechnik.md).

## 2. Schaltblaetter

[Elektrischer Entwurf](../../Design/Electrical/README.md) enthaelt Symbole,
Leitungen, Anschlussbezeichnungen, Stuecklisten und maschinenlesbare Verbindungen.
SVG-Dateien koennen direkt betrachtet und als Vektorgrafik bearbeitet werden;
der Generator erzeugt sie erneut aus den Quelldaten.

Die wesentlichen Stromkreise sind:

- Eigene 5-V-Komfortversorgung mit Sicherung, Schalter und passenden Lueftern.
- Eigene 15-V-Effektversorgung mit aktiver PD-Aushandlung als Modulschnittstelle.
- Sechs Konstantstromkanaele fuer vier RGB-Stars: drei Farbkreise fuer das
  Helmpaar und drei fuer das Duesenpaar. Jeder Kreis enthaelt zwei gleichfarbige
  LED-Chips in Reihe. LED-Rueckleitungen bleiben von Versorgungsmasse getrennt.
- Pegelanpassung zwischen 3.3-V-Steuerung und LDD-Dimmeingaengen sowie ein
  separat schaltbarer LED-Leistungspfad. Ein Hardwareversuch muss das
  Einschalt-, Reset-, Abschalt- und Fehlerverhalten bestaetigen.

Originalsender, kommerzielle AR-Optik, Nebler und Exoskelett behalten ihre
Herstellerelektronik. Unbekannte proprietaere Pins werden nicht mit erfundenen
Belegungen verbunden. Das Robotersystem erhaelt keine Fahr-/Flugbefehle aus
den Lichtschaltplaenen. Schaltplanpruefungen sind keine thermische oder
funktionale Freigabe und ersetzen keine elektrische Abnahme am Aufbau.

## 3. Ein Paket mit CAD-Quellen und STL erzeugen

Ab Repository-Wurzel:

```bash
python3 tools/suit_hardware.py --out build/Hardware-r1 --render-stl
```

Erforderlich: Python 3.11+ und fuer den STL-Schritt OpenSCAD im Suchpfad.
Ohne `--render-stl` wird nur das bearbeitbare Quellenpaket ausgegeben. Dieses
enthaelt keine behauptete Geometriepruefung. Die OpenSCAD-Assertions pruefen
bei einer Kompilierung geometrische Randbedingungen, keine Materialfestigkeit.

| Ausgabe | Inhalt |
| --- | --- |
| CAD/ | Native OpenSCAD-Dateien, Beispielparameter und Einzelteilregister |
| Electrical/ | Schaltblaetter, Verbindungsdaten, Generator und Bauteilhinweise |
| STL/ | Einzelne Mesh-Exporte in mm, nur mit --render-stl |
| Logs/ | OpenSCAD-Kompilierprotokolle, nur mit --render-stl |
| Config.json | Tatsaechlich verwendete geometrische Parameter |
| HardwarePackage.json | Hashes, Parameterherkunft, Geometrieergebnisse und offene Hardwarepruefung |

Ein bestehender Ausgabeordner wird nicht ueberschrieben. Bei Fehler entsteht
`BUILD_INCOMPLETE.md`; eine solche Ausgabe ist nicht vollstaendig.
Die STL-Pruefung erfasst nichtleere Dreiecke, endliche Koordinaten und
konsistent orientierte geschlossene Kanten. Sie beweist keine Selbstschnitt-
oder Kollisionsfreiheit und keine druckbare Mindestwandstaerke.

Fuer eigene Geraetemasse
[ExampleConfig.json](../../Design/HardwareKit/ExampleConfig.json) nach
`build/Hardware.local.json` kopieren, reale Masse eintragen und exportieren:

```bash
python3 tools/suit_hardware.py --config build/Hardware.local.json --out build/Hardware-r2 --render-stl
```

Eine JSON-Datei darf auch nur einzelne bekannte Parameter enthalten. Alle
anderen bleiben als generische Beispiele gekennzeichnet. Dateipfade und
Programmausdruecke sind keine gueltigen Parameterwerte.

## 4. Zusammen mit einem Anzugprofil

Das [Baupaket](Mjolnir-Baupaket.md) enthaelt die Quellen standardmaessig unter
`Hardware/`, als optionalen Referenzbaukasten. Die Auswahl aller Dateien
bedeutet keine Kaufempfehlung fuer jedes Bauteil und keine automatische
Erweiterung der Profil-BOM.

```bash
python3 tools/suit_project.py --profile build/MySuit.local.json --hardware build/Hardware.local.json --out build/MySuit-r3
```

Fuer synthetische/unvollstaendige Profilbeispiele ist zusaetzlich `--concept`
erforderlich. Die Hardwareparameter bleiben unabhaengig von den Koerpermassen.
Nach Aenderung der Parameter neu exportieren, damit die dokumentierten Hashes
zu den Dateien passen.

## 5. Naechste Fertigungsschritte

1. Originalhardware vermessen und ihre Montage-/Temperaturangaben sichern.
2. Erst ein Bauteil als Tischprobe herstellen; Bohrungen und Spiel mit realen
   Schrauben, Kabeln und Gehaeusen pruefen.
3. Bei HUD und Kamera Freisicht, Bildausschnitt und Kabelbewegung pruefen.
4. Bei Powerbank und Sender Zugriff, Gurte, Lastpfad und Funkfenster pruefen.
5. Schaltung am Tisch mit passender Strombegrenzung und geeigneter Absicherung
   pruefen; anfangs keine Verbindung zu getragenen Bauteilen herstellen.
6. LED-Waermeweg mit echten Metallkuehlkoerpern auslegen und messen. Gedruckte
   Duesen-/Lampengehaeuse sind keine Kuehlkoerper.
7. Erst nach bestandenen Einzelproben in die Ruestung integrieren und die
   [Gesamtpruefung](../../Tests/TestReports/Mjolnir-Abnahme.md) durchfuehren.
