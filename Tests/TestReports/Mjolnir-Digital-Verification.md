# Digitale Pruefung des MJOLNIR-Entwurfs

Datum: 2026-09-08. Grundlage: Konzeptprofil mit 1660 mm angegebener
Koerpergroesse und 31 ausdruecklich synthetischen linearen Beispielmassen.

| Pruefung | Ergebnis | Aussagegrenze |
| --- | --- | --- |
| Python-Unittests | 18 erfolgreich | Eingabevalidierung, getrennte Seiten, Zuschlaege, Oeffnungshuelle und Budgetarithmetik |
| Normale Erzeugung mit offenen Massen | Korrekt abgelehnt, kein Ausgabeordner angelegt | Keine stillen Standardmasse |
| Reproduzierbarkeit | Generierte JSON/SCAD/SVG/Markdown-Dateien stimmen mit Quellen ueberein | Keine Hardwarepruefung |
| ASCII-Konvention | Erfolgreich fuer Markdown/Python/Arduino | Repository-Konvention |
| Relative Markdown-Links | Keine defekten Dateiziele gefunden | Keine Pruefung externer Seiten/Anker |
| OpenSCAD 2021.01: vier Posen | CSG bei 0, 0.25, 0.5 und 1 erfolgreich, ohne Warnungen | Syntax und Geometrieaufbau, nicht Kollisionsfreiheit |
| OpenSCAD 2021.01: Testkoerper | Unterarmring, Lochbild-Coupon und geoeffneter Torso als STL erfolgreich | Konzept-/Tischmodell |
| OpenSCAD 2021.01: Gesamtmodell | Geschlossene und geoeffnete Baugruppe als STL erfolgreich | Mehrteilige Bauraumgeometrie |
| PNG-Vorschau | Aus den kompilierten Meshes erzeugt und visuell kontrolliert | Schematische Farbe, keine Endkonturen |

## Reproduktion

Ab Repository-Wurzel:

```bash
python3 -m unittest discover -s Tests/Automation -v
python3 tools/suit_budget.py --check
mkdir -p build
openscad --hardwarnings -o build/suit-open.csg -D open_fraction=1 Design/Parametric/MjolnirEntry.scad
openscad --hardwarnings -o build/ring.stl -D 'view="forearm_ring"' Design/Parametric/MjolnirEntry.scad
```

Die CI-Ergaenzung prueft Berechnung und CAD-Export bei relevanten Aenderungen.
Sie ist keine Freigabe fuer den getragenen Aufbau. Bestehende HUD-/Arduino-
Software wurde nicht funktional geaendert und hier nicht als Hardware getestet.

## Offene reale Nachweise

Koerpermessung, genaue Halo-Oberflaechen, Fertigungstoleranzen, 3D-Kollisionen,
Scharnier-/Fuehrungsauswahl, Lastfaelle, Gurtpassform, Serien-Exoskelett-Passprobe,
reale Massen, Tragbarkeit und Notausstieg. Die unter 5 Minuten Anziehzeit,
unter 60 Sekunden Befreiung und unter 12 kg Grundmasse sind Entwicklungsziele.
Keiner dieser physischen Zielwerte wurde gemessen oder als bestanden markiert.
