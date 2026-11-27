# X01-Mechanik: Beckenrahmen, Hueftmodul, Strebe, Manschette

Parametrisches OpenSCAD-Konzept fuer die Mechanik des
[Eigenbau-Beinantriebs X01](../../Documentation/Guides/Exoskelett-Eigenbau.md),
Stufe H (nur Hueftantriebe).

**Status: Konzeptgeometrie, nicht bemessen, nicht gebaut, nicht erprobt.** Das
Modell zeigt Schnittstellen, Stapelfolge und Bewegung. Keine Wandstaerke,
kein Querschnitt und kein Werkstoff ist fuer Last ausgelegt. Nichts davon
gehoert an den Koerper, bevor die
[Nachweisfolge](../../Documentation/Guides/Exoskelett-Eigenbau.md#9-nachweisfolge)
bis P3 durchlaufen ist.

## Teile

| Teil (`part`) | ID | Aufgabe |
| --- | --- | --- |
| `pelvis_frame` | X01-B | Stab ueber den Ruecken, zwei Seitenarme nach vorn, je eine Gabel fuer das Abspreizgelenk, zwei Schlitze fuer den Hueftgurt |
| `motor_plate` | X01-H | Sitzt auf der Gehaeuseseite des Antriebs (8 x M3), traegt den Gelenkblock und beide Anschlaege |
| `output_arm` | X01-H | Sitzt auf dem Abtriebsflansch (6 x M4), reicht mit einer Nabe durch die Motorplatte, nimmt die Strebe auf |
| `strut` | X01-O | Flachstab mit Lochreihe im Raster 25 mm |
| `cuff` | X01-O | Halbring hinter dem Oberschenkel mit zwei Gurtschlitzen; der Gurt schliesst vorn |

Reihenfolge von innen nach aussen: Abtriebsarm, 4 mm Luft fuer die
Schraubenkoepfe, Motorplatte, Antrieb. Der Antrieb liegt damit ganz aussen;
sein Abtrieb zeigt zum Koerper.

**Abspreizen.** Der Gelenkblock oben an der Motorplatte dreht in der Gabel des
Beckenrahmens um eine Achse in Gehrichtung. Das Gelenk ist frei und nicht
angetrieben. Es liegt 90 mm ueber der Beugeachse und nicht im Hueftgelenk; wie
gut das zur Person passt, zeigt erst P3.

**Anschlaege.** Der Stab des Abtriebsarms laeuft zwischen zwei Bloecken an der
Motorplatte. Voreinstellung: 36 Grad Streckung, 112 Grad Beugung. Die Werte
liegen knapp ausserhalb der Stoergrenzen der Steuerung (-33 und +108 Grad mit
den Standardwerten in `exo_core.h`), damit zuerst die Software abschaltet. Ob
sie im schmerzfreien Bereich der Person liegen, ist nicht geprueft; beide
Winkel sind an der Person festzulegen.

Der Stab trifft die Bloecke bei etwa 28 mm Radius. Dort entstehen bei 22 Nm
Spitzenmoment rund 790 N, bei der Softwaregrenze von 9 Nm rund 320 N
(Moment geteilt durch Radius, ohne Stoss). Die Bloecke im Modell sind
Platzhalter fuer diese Stelle, keine bemessenen Anschlaege.

**Stufe K.** `show_stage_k=true` blendet in der Vorschau einen Antrieb am Knie
ein. Kniemodul, Unterschenkelstrebe und der Ausgleich der wandernden Knieachse
sind nicht konstruiert.

## Antriebsschnittstelle

Aus der 2D-Zeichnung des Herstellers zum AK80-9 V3.0
([PDF](https://www.cubemars.com/data/cms/202602/ak80-9-v3-0-robotic-actuator-2d-drawing.pdf),
abgerufen am 2026-11-27):

| Mass | Wert |
| --- | --- |
| Aussendurchmesser | 98 mm |
| Gesamthoehe | 38,5 mm +/- 0,5 |
| Gehaeuse, beide Stirnseiten | 8 x M3 auf Teilkreis 85 mm |
| Abtriebsflansch | 6 x M4 auf Teilkreis 28 mm, Flansch 48 mm, Zentrierung 37 mm |
| Ueberstand des Flanschs | 3 mm |

Die Zeichnung nennt keine Gewindetiefen und keine Winkellage der Bohrungen.
Im Modell ist die Winkellage frei gewaehlt. Vor dem Bohren am gelieferten
Antrieb nachmessen; ein anderer Antrieb braucht andere Werte in
`Parameters.scad`.

## Koerpermasse

`Parameters.scad` enthaelt sechs Koerpermasse als **Platzhalter**: freie Breite
zwischen den Abtriebsarmen, Hoehe des Abspreizgelenks, Abstand zum Rueckenstab,
Abstand Hueftachse zu Manschette und Knie, Oberschenkeldurchmesser an der
Manschette. Keines steht in den 32 Profilmassen. Sie werden an der Person
aufgenommen; die Lage der Hueftachse ist dabei das wichtigste Mass.

## Ansichten und Export

```bash
openscad --hardwarnings -D 'hip_flex_deg=30' -D 'abduction_deg=10' -o x01.png Design/Exo/X01Frame.scad
openscad --hardwarnings -D 'part="motor_plate"' -D 'side="r"' -o motor_plate_r.stl Design/Exo/X01Frame.scad
```

| Selektor | Werte | Bedeutung |
| --- | --- | --- |
| part | assembly, motor_plate, output_arm, strut, cuff, pelvis_frame | Gesamtansicht oder Einzelteil |
| side | l, r | Spiegelt Motorplatte, Abtriebsarm und Manschette |
| hip_flex_deg | -36 bis 112 | Beugung in der Gesamtansicht, begrenzt durch die Anschlaege |
| abduction_deg | 0 bis 30 | Abspreizen in der Gesamtansicht |
| show_stage_k | true, false | Platzhalter fuer den Knieantrieb |

## Was fehlt

- Festigkeit: Werkstoff, Dicken und Querschnitte aller Teile. Ein gedrucktes
  Teil gehoert ohne Belastungsprobe nicht in den Lastpfad.
- Lagerung und Sicherung des Abspreizgelenks, Schraubensicherung, Passung der
  Zentrierung.
- Abstuetzung des Gegenmoments am Becken: Der Rahmen haengt bisher nur an zwei
  Gurtschlitzen. Polster, Beckenschalen und Gurt sind nicht konstruiert.
- Drehung der Manschette um die Beinachse, Polster, Schnellverschluss.
- Kabelweg, Halter fuer Steuerung, Akku und Not-Aus.
- Freigang zu den Ruestungsschalen und zum Traeger T01.
- Stufe K vollstaendig.
