# Parametrisches MJOLNIR-Einstiegssystem

**Entwicklungsmodell, keine fertige Druckruestung.** Die Geometrie zeigt Schalen,
Scharnierachsen, Oeffnungsbewegung und Bauraum. Sie enthaelt keine belastbaren
Gelenke, fertigen Verschluesse oder originalgetreuen Halo-Oberflaechen.

![Technische 2D-Draufsicht des synthetischen Beispiels](Generated/OpeningEnvelope.svg)

## Eigenes Projekt

Ab Repository-Wurzel, Python 3.11+ ohne Zusatzpakete:

```bash
python3 tools/suit_fit.py --init build/MySuit.local.json --name "My Suit"
# Die unbekannten Felder in mm ausfuellen:
python3 tools/suit_fit.py --profile build/MySuit.local.json --out build/MySuit
```

Danach die erzeugte `build/MySuit/MjolnirEntry.scad` in OpenSCAD oeffnen.
Sie enthaelt einen passenden relativen Include auf die Parameter dieser Ausgabe.
Profile und Ausgaben unterschiedlicher Projekte werden getrennt gehalten.
`build/` und `*.local.json` werden nicht versioniert.

Ohne `--concept` wird bei fehlenden Massen abgebrochen. Ein vollstaendiges
Profil bedeutet nur, dass Eingaben vorliegen; Passform, Schalen-Schnittfuehrung
und Gelenkfreiheit bleiben physisch zu pruefen. Die Herkunft der Eingaben wird
im Fit-Bericht dokumentiert.

## Explizite Demonstration

```bash
python3 tools/suit_fit.py --profile Design/Parametric/Profiles/Demo.json --concept --out build/Demo
```

Alle Demo-Masse sind synthetisch. Sie sind keine Zielmasse fuer eine Person.
Die versionierte Ausgabe unter `Generated/` ist ausschliesslich eine solche
Beispielansicht. Der Generator kann mit `--concept` auch fehlende Werte eines
unvollstaendigen Profils fuer eine Konzeptansicht ergaenzen; die Ausgabe
bleibt dann als Konzept gekennzeichnet.

`open_fraction` zwischen 0 und 1 veraendern; geschlossen = 0, offen = 1.
Animation: Ausdruck `$t` fuer `open_fraction` setzen und Animation aktivieren.
Zuerst fahren die Seiten aus, danach schwenken die Tueren. Das ist eine
idealisierte Schwenkbewegung, kein nachgewiesener kollisionsfreier Mechanismus.

```bash
openscad -o "$PWD/build/Demo/torso-closed.csg" -D 'view="torso"' build/Demo/MjolnirEntry.scad
openscad -o "$PWD/build/Demo/torso-open.csg" -D 'view="torso"' -D open_fraction=1 build/Demo/MjolnirEntry.scad
openscad -o "$PWD/build/Demo/forearm-ring.stl" -D 'view="forearm_ring"' build/Demo/MjolnirEntry.scad
```

Diese Ring-STL ist eine synthetische Testlehre. Keine komplette Ruestung daraus
drucken. CSG-Zielpfade absolut angeben: OpenSCAD 2021.01 kann bei relativen
CSG-Pfaden eine Fehlermeldung trotz Exitcode 0 liefern. Deshalb zusaetzlich
pruefen, ob jede CSG-Ausgabedatei existiert und nicht leer ist.

## Dateien und Status

| Datei | Zweck | Verlaesslichkeit |
| --- | --- | --- |
| [Profiles/Template.json](Profiles/Template.json) | Leere Vorlage mit 32 unbekannten Messfeldern | Keine Personendaten |
| [Profiles/Demo.json](Profiles/Demo.json) | Explizites Rechenbeispiel | Synthetische Masse |
| [ProfileSchema.json](ProfileSchema.json) | Gemeinsame Felddefinitionen und Auswahlwerte | Eingabeformat, keine Passformfreigabe |
| [Generated/FitReport.md](Generated/FitReport.md) | Beispielberechnung mit Herkunft | Keine realen Passproben |
| [Generated/OpeningEnvelope.svg](Generated/OpeningEnvelope.svg) | Geschlossene/offene Torso-Tueren | 2D-Huelle, kein Durchgangsnachweis |
| [MjolnirEntry.scad](MjolnirEntry.scad) | Zentrales Baugruppenmodell | Huelle/Packaging |
| `build/MySuit/MjolnirEntry.scad` | Modell mit den Parametern des eigenen Profils | Eigenstaendige Ausgabe |

## Koordinaten und Grenzen

- X: links/rechts; positive X-Seite = rechte Modellseite, keine Anatomiezuordnung.
- Y: positiv nach hinten, Front liegt bei negativem Y; Z: oben; Einheit mm.
- `side=l` nutzt die separat erfassten linken Unterarmmasse.
- Oeffnung 0..105 Grad ist ein Entwurfsbereich mit noch festzulegenden Anschlaegen.
- Cyan: eigener Traeger; Orange: Scharnierachsen; Gruen: kosmetische Schalen.
- Rote transparente Bloecke sind generische Freihalter; Hersteller-CAD fehlt.
- Schulter-, Knie-, Helm- und Fusspositionen sind Darstellungsannahmen. Das Modell
  bildet kein Skelett ab; die resultierende Gesamthoehe ist keine gemessene
  Ruestungshoehe und muss nicht der Koerpergroesse entsprechen.
- Referenz und Material im Profil sind Planungsentscheidungen. Sie erzeugen
  keine Halo-Detailoberflaechen oder nachgewiesene Materialfestigkeit.
- Bestehende leere STL-Platzhalter sind keine druckfertigen Bauteile.

[Konfiguration und mehrere Profile](../../Documentation/Guides/Mjolnir-Konfiguration.md),
[Messdefinitionen](../../Documentation/Guides/Mjolnir-Massanpassung.md),
[Systementwurf](../../Documentation/Guides/Mjolnir-Systementwurf.md).
