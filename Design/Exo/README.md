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
| `pelvis_frame` | X01-B | Ganzer Beckenrahmen aus den vier folgenden Teilen |
| `pelvis_side` | X01-B | Seitenarm: Flachplatte von der Gelenkgabel nach hinten, zwei Schrauben in den Rohreinsatz |
| `rear_tube` | X01-B | Vierkantrohr 30 x 2 mm ueber den Ruecken mit vier Querbohrungen |
| `tube_insert` | X01-B | Klotz im Rohrende: Querbolzen durch das Rohr, zwei Gewinde fuer den Seitenarm |
| `belt_loop` | X01-B | Platte an der Koerperseite des Rohrs mit zwei Schlitzen fuer den Hueftgurt; Traeger fuer ein Polster |
| `motor_plate` | X01-H | Sitzt auf der Gehaeuseseite des Antriebs (8 x M3), traegt den Gelenkblock und beide Anschlaege |
| `output_arm` | X01-H | Sitzt auf dem Abtriebsflansch (6 x M4), reicht mit einer Nabe durch die Motorplatte, nimmt die Strebe auf |
| `strut` | X01-O | Flachstab mit Lochreihe im Raster 25 mm |
| `cuff` | X01-O | Halbring hinter dem Oberschenkel mit zwei Gurtschlitzen; der Gurt schliesst vorn |

Reihenfolge von innen nach aussen: Abtriebsarm, 4 mm Luft fuer die
Schraubenkoepfe, Motorplatte, Antrieb. Der Antrieb liegt damit ganz aussen;
sein Abtrieb zeigt zum Koerper.

**Rueckenrohr statt Flachstab.** Beim Gehen wirken die beiden Hueftmomente
gegeneinander und verdrehen den Stab ueber dem Ruecken. Ein Flachstab 60 x 5 mm
aus Aluminium wuerde sich bei 22 Nm um rund 7 Grad verdrehen, das Vierkantrohr
um 0,4 Grad ([Lastabschaetzung](LoadEstimate.md), I01 und I02). Das verlorene
Moment kaeme nicht am Bein an und der Rahmen wuerde auf dem Becken arbeiten.

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

## Lastabschaetzung und Werkstoff

`python3 tools/suit_loads.py` rechnet 14 Querschnitte und Schrauben fuer 22 Nm
Spitzenmoment mit Sicherheitsfaktor 3 nach und schreibt
[LoadEstimate.md](LoadEstimate.md). Eingaben sind `Parameters.scad` und
[LoadCase.json](LoadCase.json); nach jeder Aenderung dort neu ausfuehren
(`--check` meldet veraltete Ausgaben).

Ergebnis mit den Standardwerten:

- **Aluminium EN AW-6061-T6 und Stahl S235:** alle Querschnitte unter 0,5
  Auslastung, die Schrauben unter 0,5. Am hoechsten liegen der Anschlagblock
  (mit Stossfaktor 2) und die Schrauben des Rohreinsatzes.
- **Gedrucktes PETG:** jeder tragende Querschnitt ueber 1, bis 5,4 am Anschlag.
  Motorplatte, Abtriebsarm, Strebe, Seitenarm, Rohr und Einsatz sind deshalb
  Metallteile. Gedruckt werden nur Manschettenpolster, Abdeckungen und die
  Steuerbox.
- Die Strebe ist seitlich weich: 10 N Querkraft an der Manschette lenken sie
  in Aluminium rund 6 mm aus. Das gleicht kleine Fehler der Achslage aus,
  fuehrt das Bein aber seitlich kaum.

Das ist eine Ueberschlagsrechnung am Nennquerschnitt mit Handbuchwerten, keine
Festigkeitsfreigabe. Ermuedung, Kerben, Lasten quer zur Bewegungsebene und ein
Sturz sind nicht erfasst. Vor dem ersten Einsatz am Koerper stehen eine
Belastungsprobe am Pruefstand und die Pruefung durch jemanden, der Tragwerke
auslegt.

## Steuerbox

`X01ControlBox.scad` ist ein gedrucktes Gehaeuse fuer das ESP32-Board und den
CAN-Transceiver: Wanne mit Auflageleisten, Deckel mit Bohrungen fuer Taster
und Status-LED, Klemmstueck fuer das Rueckenrohr (`part` = tray, lid, clamp).
Die Platinenmasse in `Parameters.scad` sind Platzhalter und am gekauften Board
zu messen. Das Gehaeuse ist nicht dicht, hat keine ausgearbeitete
Zugentlastung und liegt ausserhalb jedes Lastpfads. Akku, Sicherung und
Not-Aus haben noch keinen Halter.

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

## Koerpermasse und Messbogen

`Parameters.scad` enthaelt sechs Koerpermasse als **Platzhalter**. Keines steht
in den 32 Profilmassen. Sie werden an der Person aufgenommen, im spaeteren
Unteranzug, stehend, mit einer zweiten Person. Die Lage der Hueftachse ist
dabei das wichtigste Mass.

**Hueftachse markieren.** Im Stand den grossen Rollhuegel (Trochanter major)
seitlich an der Huefte ertasten: der Knochenvorsprung, der sich beim Drehen des
Beins unter den Fingern bewegt. Die Beugeachse liegt in dieser Gegend, aber
nicht genau dort; der Punkt ist ein Ausgangswert. Auf dem Unteranzug markieren,
Bein langsam heben und pruefen, ob der Punkt in etwa stehen bleibt. Die
endgueltige Lage ergibt sich erst am stromlosen Gestell (P3).

| Parameter | So messen | Wert links | Wert rechts |
| --- | --- | --- | --- |
| `pelvis_clear_width_mm` | Gerade Breite zwischen den beiden markierten Punkten, mit zwei parallelen Brettern; dazu je Seite den Abstand, den Polster und Abtriebsarm brauchen | ein Wert | |
| `abduction_axis_z_mm` | Senkrechter Abstand vom markierten Punkt bis zur Hoehe, auf der das Abspreizgelenk Platz hat (ueber dem Antrieb, unter dem Beckenkamm) | | |
| `back_offset_mm` | Waagerechter Abstand vom markierten Punkt nach hinten bis zur Rueckseite des Beckens, plus Polster | | |
| `hip_to_cuff_mm` | Vom markierten Punkt entlang des Oberschenkels bis zur Mitte der Manschette, etwa eine Handbreit ueber der Kniescheibe | | |
| `thigh_cuff_d_mm` | Umfang des Oberschenkels an dieser Stelle geteilt durch 3,14 | | |
| `hip_to_knee_mm` | Vom markierten Punkt bis zur Kniemitte (nur fuer Stufe K) | | |

Dazu ohne Parameter, aber fuer die Anschlaege noetig:

| Mass | So messen | Wert links | Wert rechts |
| --- | --- | --- | --- |
| Schmerzfreie Streckung | Im Stand Bein gestreckt nach hinten fuehren, Winkel zur Senkrechten | | |
| Schmerzfreie Beugung | Knie zur Brust ziehen, Winkel des Oberschenkels zur Senkrechten | | |
| Abspreizen beim Gehen und seitlichen Schritt | Winkel des Beins zur Senkrechten von vorn gesehen | | |

Das Modell rechnet mit einem Wert fuer beide Seiten. Weichen links und rechts
ab, je Seite mit eigenen Parametern exportieren. `stop_extension_deg` und
`stop_flexion_deg` muessen kleiner sein als die gemessenen schmerzfreien
Winkel; sind sie es nicht, zuerst die Winkelgrenzen in `exo_core.h` enger
stellen und die Anschlaege nachziehen. Ein automatischer Test
(`Tests/Automation/test_exo_mechanics.py`) prueft, dass die Anschlaege 2 bis
10 Grad ausserhalb der Stoergrenzen der Steuerung liegen.

## Pruefstand fuer einen Antrieb

`X01TestRig.scad` ist das Gestell fuer die Nachweisstufen P1 und P2: ein
einzelner Antrieb auf einem Brett, ohne Person.

| Teil (`part`) | Aufgabe |
| --- | --- |
| `bracket` | Stehende Platte mit dem Gehaeuse-Bohrbild auf einem Fuss mit vier Bohrungen fuer das Brett |
| `lever` | Hebel auf dem Abtriebsflansch; die Bohrung an der Spitze liegt 250 mm von der Achse |
| `limiter` | Gabel um den Hebel, begrenzt den Weg an der Spitze auf 12 mm nach oben und unten |

Die Waage steht unter der Hebelspitze; eine Schraube in der Spitzenbohrung
drueckt auf die Waagschale. Moment = Kraft mal Hebelarm:

| Kommandiertes Moment | Kraft an der Spitze | Anzeige der Waage |
| --- | --- | --- |
| 0,5 Nm | 2,0 N | 204 g |
| 1,0 Nm | 4,0 N | 408 g |
| 2,0 Nm | 8,0 N | 816 g |

Das Eigengewicht des Hebels zeigt die Waage schon bei Moment null an; diesen
Wert vorher ablesen und abziehen. Der Antrieb drueckt nur in einer Drehrichtung
auf die Waage; die Gegenrichtung faengt die Gabel ab.

Der Sketch hat dafuer einen Pruefstand-Modus (`#define BENCH_TEST 1` in
`LegAssist.ino`): ein Antrieb, Sollmoment ueber die serielle Schnittstelle.

| Eingabe | Wirkung |
| --- | --- |
| `t 1.0` | Sollmoment 1,0 Nm, begrenzt auf 2 Nm und 5 Nm/s Anstieg; faellt nach 5 s ohne neue Eingabe auf null |
| `z` | Sollmoment null |
| `s` | Keine CAN-Kommandos mehr senden, um das Verhalten des Antriebs ohne Kommandos zu beobachten (P1) |
| `r` | Wieder senden, beginnt bei null |

Zehnmal je Sekunde erscheint eine Zeile mit Sollmoment, Lage, Rohwerten fuer
Drehzahl und Strom, Temperatur, Fehlercode, Zahl der Rueckmeldungen und deren
Abstand. Die Logik (`bench_core.h`) ist auf dem Host getestet, der Modus an
keinem Antrieb.

**Vor dem Einschalten:** Die Gabel ist das einzige, was den Hebel bei einem
durchgehenden Antrieb aufhaelt, und sie ist nicht bemessen. Bei 22 Nm
Spitzenmoment wirken an ihr rund 110 N (Moment geteilt durch 0,2 m). Ein
250 mm langer Hebel, der frei durchdreht, verletzt. Gestell auf das Brett
schrauben, Brett festspannen, Not-Aus in die Motorleitung, niemand in der
Hebelebene.

## Ansichten und Export

```bash
openscad --hardwarnings -D 'hip_flex_deg=30' -D 'abduction_deg=10' -o x01.png Design/Exo/X01Frame.scad
openscad --hardwarnings -D 'part="motor_plate"' -D 'side="r"' -o motor_plate_r.stl Design/Exo/X01Frame.scad
openscad --hardwarnings -D 'part="lever"' -o rig_lever.stl Design/Exo/X01TestRig.scad
```

| Selektor | Werte | Bedeutung |
| --- | --- | --- |
| part | assembly, motor_plate, output_arm, strut, cuff, pelvis_frame | Gesamtansicht oder Einzelteil |
| side | l, r | Spiegelt Motorplatte, Abtriebsarm und Manschette |
| hip_flex_deg | -36 bis 112 | Beugung in der Gesamtansicht, begrenzt durch die Anschlaege |
| abduction_deg | 0 bis 30 | Abspreizen in der Gesamtansicht |
| show_stage_k | true, false | Platzhalter fuer den Knieantrieb |

## Was fehlt

- Festigkeit: Es gibt eine Ueberschlagsrechnung, keinen Nachweis. Ermuedung,
  Kerben, Querlasten und die Belastungsprobe fehlen.
- Lagerung und Sicherung des Abspreizgelenks, Schraubensicherung, Passung der
  Zentrierung.
- Abstuetzung des Gegenmoments am Becken: Der Rahmen haengt an zwei
  Gurtplatten. Polster, Beckenschalen und der Gurt selbst sind nicht
  konstruiert; ob das Becken das Moment ohne Verrutschen aufnimmt, ist offen.
- Drehung der Manschette um die Beinachse, Polster, Schnellverschluss.
- Kabelweg, Halter fuer Akku, Sicherung und Not-Aus.
- Freigang zu den Ruestungsschalen und zum Traeger T01.
- Stufe K vollstaendig. Sie ist bewusst nicht vorgezeichnet: Am Knie muss der
  Anschlag gegen Ueberstreckung enger sitzen als die heutige Stoergrenze der
  Steuerung (-10 Grad), und die wandernde Achse braucht einen Ausgleich. Beides
  wird erst festgelegt, wenn Stufe H am Pruefstand und am Koerper gelaufen ist.
