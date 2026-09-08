# Parametrisches MJOLNIR-Einstiegssystem

**Entwicklungsmodell, keine fertige Druckruestung.** Die Geometrie zeigt Schalen,
Scharnierachsen, Oeffnungsbewegung und Bauraum. Sie enthaelt keine belastbaren
Gelenke, fertigen Verschluesse oder originalgetreuen Halo-Oberflaechen.

![Kompilierte Baugruppenansicht geschlossen und offen](Preview.png)

## Schnellstart

Ab Repository-Wurzel, Python 3.11+ ohne Zusatzpakete:

```bash
python3 tools/suit_fit.py --concept --out Design/Parametric/Generated
python3 -m unittest discover -s Tests/Automation -v
```

Danach `MjolnirEntry.scad` in OpenSCAD oeffnen. `open_fraction` zwischen 0 und 1
veraendern; geschlossen = 0, offen = 1. Animation: Ausdruck `$t` fuer
`open_fraction` setzen und Animation aktivieren. Zuerst fahren die Seiten aus,
danach schwenken die Tueren. Das ist eine idealisierte
Schwenkbewegung, kein nachgewiesener kollisionsfreier Mechanismus.

```bash
openscad -o build/torso-closed.csg -D 'view="torso"' Design/Parametric/MjolnirEntry.scad
openscad -o build/torso-open.csg -D 'view="torso"' -D open_fraction=1 Design/Parametric/MjolnirEntry.scad
openscad -o build/forearm-ring.stl -D 'view="forearm_ring"' Design/Parametric/MjolnirEntry.scad
```

`build/` vorher anlegen. Die Ring-STL ist eine **synthetische Testlehre**, solange
`concept_only=true` gilt. Keine komplette Ruestung daraus drucken.

Die PNG-Vorschau stammt aus den tatsaechlich kompilierten Baugruppen-Meshes.
Zur Neuberechnung werden zusaetzlich `matplotlib` und `numpy` benoetigt:

```bash
openscad --hardwarnings -o build/assembly-closed.stl Design/Parametric/MjolnirEntry.scad
openscad --hardwarnings -o build/assembly-open.stl -D open_fraction=1 Design/Parametric/MjolnirEntry.scad
```

Diese Befehle ab Repository-Wurzel ausfuehren, `build/` vorher anlegen.
Anschliessend: `python3 tools/suit_render.py`.
Die Vorschau faerbt Oberflaechen schematisch ein; Geometrie und Posen stammen
aus OpenSCAD. Herstellerspezifische Exoskelett-Volumina sind nicht enthalten.

## Dateien und Status

| Datei | Zweck | Verlaesslichkeit |
| --- | --- | --- |
| [Profiles/Huskynarr.json](Profiles/Huskynarr.json) | 1660 mm, breite Schultern, offene Messfelder | Groesse angegeben; Rest offen |
| [Generated/FitReport.md](Generated/FitReport.md) | Jedes verwendete Mass mit Herkunft | Beispielmasse ausdruecklich sichtbar |
| [Generated/OpeningEnvelope.svg](Generated/OpeningEnvelope.svg) | Geschlossene/offene Torso-Tueren | 2D-Huelle, kein Durchgangsnachweis |
| [MjolnirEntry.scad](MjolnirEntry.scad) | 3D-Baugruppen und Oeffnungsanimation | Huelle/Packaging |
| [Generated/parameters.scad](Generated/parameters.scad) | Reproduzierbare Dimensionen | Vom Generator abgeleitet |

## Gemessene Variante

1. Profil nach `Design/Parametric/Profiles/Huskynarr.local.json` kopieren.
2. Alle Nullwerte mit mm-Werten aus [Massanpassung](../../Documentation/Guides/Mjolnir-Massanpassung.md) fuellen.
3. Ohne `--concept` in ein lokales Ausgabeverzeichnis rechnen:

```bash
python3 tools/suit_fit.py --profile Design/Parametric/Profiles/Huskynarr.local.json --out build/SuitFit
```

Fuer lokale CAD-Arbeit `MjolnirEntry.scad` nach `build/MjolnirEntry.scad` kopieren
und dessen erste Include-Anweisung auf `include <SuitFit/parameters.scad>` setzen.
Dadurch bleiben private Messwerte ausserhalb der versionierten Konzeptansicht.
`*.local.json` und `build/` werden ignoriert. `MEASURED_ENVELOPE_NOT_VALIDATED`
bedeutet nur: alle Eingaben liegen vor. Passform, Schalen-Schnittfuehrung und
Gelenkfreiheit bleiben physisch zu pruefen.

## Koordinaten und Grenzen

- X: links/rechts; positive X-Seite = rechte Modellseite, keine Anatomiezuordnung.
- Y: positiv nach hinten, Front liegt bei negativem Y; Z: oben; Einheit mm.
- `side=l` nutzt die separat erfassten linken Unterarmmasse.
- Oeffnung 0..105 Grad ist ein **Entwurfsbereich** mit noch festzulegenden Anschlaegen.
- Cyan: eigener Traeger; Orange: Scharnierachsen; Gruen: kosmetische Schalen.
- Rote transparente Bloecke sind generische Freihalter; Hersteller-CAD fehlt.
- Schulter-, Knie-, Helm- und Fusspositionen sind Darstellungsannahmen. Das Modell
  bildet kein Skelett ab. Eine aus den Segmenten resultierende Gesamthoehe kann
  deshalb von 1660 mm abweichen; 1660 mm ist Koerpergroesse, keine Ruestungshoehe.
- Kein STL-Set aus dem Netz wurde kopiert. Bestehende leere STL-Platzhalter bleiben
  als Altbestand erkennbar; dieses Modell ersetzt sie nicht durch angebliche Endteile.

Konstruktiver Zusammenhang: [Systementwurf](../../Documentation/Guides/Mjolnir-Systementwurf.md).
