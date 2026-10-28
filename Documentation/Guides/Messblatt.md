# Messblatt fuer eigene Koerperprofile

Das [CSV-Messprotokoll](../../Design/Parametric/Profiles/Messprotokoll.csv)
enthaelt 32 leere Generatorfelder mit Platz fuer zwei Messungen, uebernommenen
Wert, Datum, Kleidung und Notizen. Die verbindlichen Endpunktdefinitionen
stehen in [Mjolnir-Massanpassung.md](Mjolnir-Massanpassung.md). Alle linearen
Werte werden in **Millimetern** erfasst.

Fuer jede Person und jeden abweichenden Tragezustand ein eigenes
[Projektprofil](Mjolnir-Konfiguration.md) anlegen. Die CSV dient der
Messaufnahme; gepruefte Werte werden in den Konfigurator oder in das JSON-Profil
uebertragen. Leere Felder bleiben unbekannt. Der Generator stoppt ohne
`--concept`, solange erforderliche Messwerte fehlen.

## Aufnahme

1. Koerpergroesse barfuss messen. Schalenmasse im geplanten Unteranzug aufnehmen.
2. Eine zweite Person fuehrt die Messung durch; Endpunkte und Haltung dokumentieren.
3. Gerade Breiten und Tiefen mit parallelen Messschenkeln abnehmen. Ein Massband
   ueber einer Rundung misst eine Bogenlaenge und ist keine gerade Kopfbreite.
4. Umfaenge an der definierten groessten Stelle horizontal anliegend messen,
   ohne Einschnueren oder zusaetzlichen Fingerabstand. Polsterzuschlag separat erfassen.
5. Seiten getrennt messen; starke Unterschiede zwischen Wiederholungen durch
   erneute Messung der Endpunkte klaeren, nicht blind mitteln.
6. Bereits enthaltene Polster nicht erneut addieren. Nach Aenderungen an
   Unteranzug, Polsterung, Schuhen oder Traeger betroffene Masse erneut aufnehmen.

## Messbereiche

| Bereich | Generatorwerte |
| --- | --- |
| Gesamt | Koerpergroesse |
| Torso | Schulterbreite, Brustbreite/-tiefe, Bauchbreite/-tiefe, Torsohoehe, Hueftbreite/-tiefe |
| Kopf | Gerade Breite, Stirn-Hinterkopf-Tiefe, Kinn-Scheitel-Hoehe |
| Arme je Seite | Oberarmlaenge/-umfang, Unterarmlaenge/-umfang |
| Beine je Seite | Oberschenkellaenge/-umfang, Knie-Knoechel-Laenge, Wadenumfang |
| Schuhe je Seite | Tatsaechliche Schuh-Aussenlaenge und groesste Aussenbreite |

## Zusaetzlich fuer Detailkonstruktion

Kopf-/Halsumfang, Ohren- und Handschuhfreiraum, Handgelenkquerschnitt, gebeugte
Ellbogen-/Kniequerschnitte, Segmentquerschnitte an mehreren Stellen, Spann- und
Knoechelhoehe sowie Gurtpositionen gesondert notieren. Diese Werte sind noch
keine automatisch verarbeiteten Generatorfelder.

EU-Schuhgroessen legen keine Aussenbreite fest. Bei breiten Fuessen einen
bereits bequem passenden Schuh vermessen; seine Schale wird darum entwickelt.
Koerpergewicht ist kein Generatorfeld und darf nicht aus Koerpergroesse oder
Trainingslast abgeleitet werden. Ein optionales Serien-Exoskelett benoetigt
seine eigenen Hersteller-Passmasse und gegebenenfalls Gewichtsangaben.

## Ausgabe und Speicherung

Eigene Messdateien und Berichte unter `build/` halten. Fuer weitere Projekte
separate Dateien und Ausgabeordner verwenden. Ein vollstaendiger Datensatz
ist die Grundlage einer Passprobe, kein Nachweis fuer Tragbarkeit oder
fertige Schalen. Siehe [Parametrisches CAD](../../Design/Parametric/README.md).
