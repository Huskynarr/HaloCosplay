# MJOLNIR: vom Profil zum digitalen Baupaket

Ein Befehl erzeugt einen zusammenhaengenden Werkstattstand: Referenz und
Teileliste, Bauraum-CAD, fuenf editierbare Komponentenproben, Budget,
Technik-Arbeitsblatt sowie Finish- und Bewegungsprotokolle. Der Aufbau bleibt
fuer unterschiedliche Personen, Materialien und Ruestungsvarianten nutzbar.

Das Paket ist keine fertige Gesamt-Druckruestung. Es trennt vorhandene digitale
Arbeitsmittel von Detaildateien und Versuchsergebnissen, die noch fehlen.

## 1. Paket erzeugen

Python 3.11+, ab Repository-Wurzel, ohne zusaetzliche Python-Pakete:

```bash
python3 tools/suit_project.py --profile Design/Parametric/Profiles/Demo.json --concept --out build/WorkshopDemo
```

Das Demo ist synthetisch. Ein eigenes Projekt beginnt mit leeren Messfeldern:

```bash
python3 tools/suit_fit.py --init build/MySuit.local.json --name "My Suit"
```

Nach Eintragen der Werte gemaess [Messanleitung](Mjolnir-Massanpassung.md) und
der [Bauoptionen](Mjolnir-Konfiguration.md):

```bash
python3 tools/suit_project.py --profile build/MySuit.local.json --out build/MySuit-r1
```

Ohne `--concept` werden fehlende Masse abgewiesen. Fuer eine vorlaeufige Planung
ist die Option moeglich; synthetische Ergaenzungen bleiben gekennzeichnet.
Jede Revision benoetigt einen neuen Ausgabeordner. Ein bestehendes Paket wird
nicht ueberschrieben. Nach einem Fehler bleibt ein angefangener Ordner mit
`BUILD_INCOMPLETE.md` zur Diagnose erhalten und ist nicht als fertiges Paket zu
verwenden. Eigene Masse, Kaufmodelle und Berichte unter `build/` halten.

## 2. Inhalt und Entscheidungen

| Ausgabe | Konkreter Arbeitsnutzen | Noch real zu bestimmen |
| --- | --- | --- |
| `BuildPlan.md` | Baufolge und Befehle mit richtigen Projektpfaden | Werkstatttermine und tatsaechlicher Fortschritt |
| `profile.local.json`, `Fit/` | Unveraenderter Profilsnapshot, Bauraumhuelle, Oeffnungsansichten | Passform am Koerper, Kollisionen und Bewegungsfreiheit |
| `Reference.json`, `Parts.csv` | Quellen, Ansichten und 23 getrennte Bauteile | Referenzabgleich und Modellrevision je Teil |
| `assets.local.json` | Register fuer Modelldateien, Einheiten und Hashes | Eigene nutzbare Dateien und Rechteangaben |
| `Components/` | CAD-Proben fuer Visier, Luefter, Fugen, Gelenkabdeckung und Scharnier | Kaufteilmasse, Druckverhalten, Befestigung und Einbau |
| `Clamshell/` | Acht aufklappbare Arm-/Beinhuellen und Selbstanzieh-Prueffolge | Reale Konturen, Scharniere, Verschluesse und Erreichbarkeit |
| `integration.local.json`, `Integration.*` | Einbauzonen und getrennte Stromkreise gemaess Auswahl | Stecker, Groessen, Massen und kollisionsfreier Einbau |
| `engineering.local.json`, `Engineering/` | Strom-, Laufzeit-, Moment- und Sockelrechnung | Reale Verbraucher, Massen, Hebel, Akku- und Herstellerdaten |
| `thermal.local.json`, `Thermal/` | Getrennte LED-Kuehlkoerper, Farbchips und gemessene Luftwege | Waermeleistung, Widerstaende, Einbautemperatur und Grenzwerte |
| `BOM.local.json`, `Budget.md` | Editierbare vorhandene Kostenansaetze | Lieferangebote, Ausstattung, Bestandsmaterial und Mengen |
| `FinishSheet.svg` | A4-Protokoll fuer sechs Muster mit 50-mm-Druckkontrolle | Echte Farbmuster, Haftung und Biegung |
| `MovementTests.csv` | Sieben Bewegungs-, Geraeusch- und Ausstiegsproben | Ergebnis, Beobachtung und Nachweis |
| `readiness.local.json`, `Readiness.md` | Offene Nachweise, an Profilsnapshot gebunden | Bestandene Versuche mit identischer Revision |

Die Budgetvorlage wird nicht aus der Koerpergroesse errechnet. Bei `pmi-cloud`
kommen genau die sechs Positionen der vorhandenen Nebel-BOM hinzu; `none`,
`external` und `water-mist` benoetigen bei Bedarf eigene Positionen. Komponenten-
Stuecklisten sind fuer Schnittstellen und Passproben gedacht und duerfen nicht
blind auf bereits erfasste Mengen aufaddiert werden.

## 3. Originalgetreue Modelle kontrolliert uebernehmen

Die [Detailgestaltung](Mjolnir-Detailgestaltung.md) legt Merkmale, weiche
Uebergaenge, verdeckte Trennstellen und Finish fest. Der
[Quellenkatalog](../References/ArmorReferenceLibrary.json) trennt Chief/Infinite
Mark VI GEN3, Mark VII und eine eigene Referenz. Bezugsmoeglichkeiten stehen in
[STL-Quellen](../../Resources/STL-Quellen.md); verlinkte Kaufmodelle sind nicht
im Repo enthalten.

Pro Bauteil werden in `assets.local.json` Quelle, Rechtehinweis, Referenzansichten,
Revision und lokale Dateien eingetragen. Pfade sind relativ zum Paketordner.
`reference_views` muss alle Ansichts-IDs aus `required_views` des jeweiligen
Referenzteils enthalten, etwa `front`, `left` und `right`; die Zuordnung zur
konkreten Quelle und Seite steht in `notes`. Der Pruefer kontrolliert die
eingetragenen IDs, betrachtet aber keine Bilder.
Starre Teile benoetigen eine bearbeitbare Quelldatei und einen STL-Export;
Unteranzug und Halsabschluss duerfen Schnittmuster sein. Bei Mesh-Quellen ist
die Bearbeitbarkeit auf die enthaltenen Netzdaten begrenzt.

```bash
python3 tools/suit_assets.py --manifest build/MySuit-r1/assets.local.json --report build/MySuit-r1/AssetReport.json
```

Der erste Lauf meldet vorhandene Datei-Hashes; erst nach bewusstem Abgleich
werden sie als `native_sha256` und `mesh_sha256` in das Register uebernommen.
`unit_scale_mm` bezeichnet Millimeter pro STL-Koordinate: beispielsweise 1 fuer
bereits in Millimetern exportierte Koordinaten. Einheiten werden nie erraten.

Geprueft werden Existenz, nichtleere Dateien, SHA-256, STL-Dreiecke, Groesse,
Oberflaeche und exakte Kantenpaarung mit entgegengesetzter Orientierung.
Der schnelle Pruefer begrenzt eine Datei auf 100 MiB und eine STL auf 300.000
Dreiecke. Groessere Modelle benoetigen eine geeignete Teilung oder separate
Mesh-Pruefung; eine vereinfachte Pruefkopie belegt nicht das Originalmodell.
Selbstueberschneidungen, Wandstaerke, Referenztreue und Tragfaehigkeit werden
nicht automatisch nachgewiesen. Exitcode 2 bedeutet fehlende oder fehlerhafte
Eingaben; Exitcode 0 bestaetigt ausschliesslich die enthaltenen Dateipruefungen.

## 4. Schnittstellen und Technik ausarbeiten

Die [Komponentenanleitung](../../Design/Components/README.md) beschreibt
Parameter, Orientierung, Kaufteile und Auswertung jeder Probe. Eigene
Parameter lassen sich in einer JSON-Datei erfassen und separat exportieren:

```bash
python3 tools/suit_components.py --profile build/MySuit.local.json --config build/ComponentConfig.local.json --out build/Components-r2
```

Fuer Demo- oder unvollstaendige Profile ist auch hier `--concept` erforderlich.
Die fuenf Selektoren heissen `visor_retainer`, `fan_bracket`, `seam_coupon`,
`joint_cover` und `hinge_coupon`. Beispiel mit installiertem OpenSCAD:

```bash
openscad --hardwarnings -D 'component="fan_bracket"' -o build/Components-r2/fan_bracket.stl build/Components-r2/ComponentKit.scad
```

Die [Technikauslegung](Mjolnir-Technik-Auslegung.md) beschreibt die Eingaben
fuer Verbraucher, Akkus, Scharniere und Staender sowie reale Helm-, Sicht-,
Audio- und Luftversuche. Verbraucher und Spannungsschienen kommen aus dem
[Einbauplan](Mjolnir-Einbauplan.md); Mengen und 5-/15-V-Ziele sind Entwurfsangaben.
Leistungen, nutzbare Akkuenergie und thermische Messdaten beginnen unbekannt.
Nicht vorhandene Baugruppen werden ausdruecklich weggelassen, statt erfundene
Null-Lasten fuer vorhandene Technik einzutragen.

```bash
python3 tools/suit_engineering.py --input build/MySuit-r1/engineering.local.json --out build/MySuit-r1/Engineering
python3 tools/suit_thermal.py --input build/MySuit-r1/thermal.local.json --out build/MySuit-r1/Thermal
python3 tools/suit_budget.py --bom build/MySuit-r1/BOM.local.json --out build/MySuit-r1/Budget.md
python3 tools/suit_readiness.py --manifest build/MySuit-r1/readiness.local.json --root build/MySuit-r1 --out build/MySuit-r1/Readiness.md
```

Der Technikstand steht in `Engineering/`; `--check` beim gleichen Befehl
prueft die Aktualitaet beider Berichte samt Hash der Eingabedatei.
Elektrische Rechnungen sind keine Schaltungs-, Leitungs- oder Sicherungsfreigabe;
statische Momente ersetzen keinen Lastversuch.

Mit `--integration <Datei.json>` am Baupaket-Befehl werden Kamera, HUD,
Highpower-/Pixellicht und Luftwege konfiguriert. Optionen und Beispiel stehen im
[Einbauplan](Mjolnir-Einbauplan.md). Die Auswahl veraendert keine vorhandene
Budgetdatei automatisch. [Licht-Einkauf](../../Materials/Mjolnir-Licht-Einkauf.md)
mit vorhandenen FOG-/Basispositionen abgleichen. Clamshell-Dateien und
[Selbstanziehfolge](Mjolnir-Selbstanziehen.md) bleiben auch ohne Elektronik nutzbar.

## 5. Reihenfolge bis zur Ausstellung

1. Helm, Brust/Ruecken und eine Schulter als leichte Passprobe abstimmen.
   Die Referenzproportionen an realen Innenraum anpassen; keine pauschale
   Skalierung aller Koerperachsen verwenden.
2. Visier, Luftfuehrung, weiche Uebergaenge und Handbewegung am Rohbau testen.
   Anschliessend eine komplette Arm- und Beineinheit entwickeln.
3. Oeffnungsmechanik ungetragen mit tatsaechlichen Lasten pruefen. Eine
   Scharnierlehre dient der Fertigungstoleranz, nicht der Lastabnahme.
4. Gesamtrohbau wiegen und Bewegung, Geraeusch, Waerme, Strom und Ausstieg
   protokollieren. Gegenseite individuell anpassen.
5. Sechs [Finishmuster](Mjolnir-Detailgestaltung.md) pruefen, Farb-/Glanzwirkung
   unter geplantem Licht vergleichen, erst dann die fertigen Schalen lackieren.
6. Nebel gemaess [Nebelmodul](Elektronik-Schubduesen.md) integrieren; geplanter
   Effekt und reale Veranstaltungsfreigabe bleiben getrennte Nachweise.
7. Staender und Transport mit realen Massen pruefen, Packfolge und
   Vorfuehrung proben; [Messebetrieb](Mjolnir-Messebetrieb.md) fuer das
   konkrete Veranstaltungsjahr und den Standbetrieb abschliessen.

## Softwarestand und verbleibende Arbeit

CI erzeugt ein synthetisches Workshop-Demo, kompiliert die fuenf Komponenten
sowie alle acht Arm-/Beinhuellen geschlossen und geoeffnet zu STL und stellt
es als Artefakt `concept-only-not-fabrication-approved`
bereit. Die Quellparameter und Dokumentation sind enthalten. Ein gruener
Softwaretest bestaetigt keine gedruckte oder getragene Ruestung.

Ausser den Koerpermassen fehlen weiterhin ein tatsaechlich vorliegendes und
angepasstes Gesamt-Detailmodellset, gemessene Kaufteil-/Lastdaten, reale
Pass-/Funktionsversuche sowie die Abstimmung mit der konkreten Veranstaltung.
Diese externen Arbeitsschritte bleiben in der [Projektliste](../TODO.md)
sichtbar; digitale Vorlagen werden nicht als physische Fertigstellung gezaehlt.

## Zusaetzliche Einbaumodelle und Schaltblaetter

`Hardware/` enthaelt sechs parametrische Einbaumodelle und die elektrischen
Referenzentwuerfe als portablen Quellenbaukasten. `--hardware` uebernimmt eine
eigene geometrische JSON-Konfiguration; Kaufteilmasse werden nicht mit dem
Koerper skaliert. Der separate Export mit `tools/suit_hardware.py --render-stl`
kompiliert Einzelteile und protokolliert ihre STL-Kantenpruefung.
[Dateien, Bearbeitung und Befehle](Mjolnir-CAD-Schaltplaene.md).
