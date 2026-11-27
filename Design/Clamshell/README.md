# Aufklappbare Arm- und Beinkassetten

Native OpenSCAD-Bauraumhuellen mit zwei getrennten Schalenhaelften und einer
gespiegelten Drehbewegung. Das Konzept setzt radialen Zugang an allen vier
Gliedmassentypen um: Oberarm, Unterarm, Oberschenkel und Schienbein. Kein
Durchschieben der Hand oder des Fusses durch eine geschlossene Ruestungsroehre.

**Status: ungepruefte Bauraummodelle.** Reale Scharniere, Offenhalter,
Rastverschluesse, Haut-/Gelenkabstaende und authentische Oberflaechen sind nicht
in diesen vereinfachten Zylinderschalen konstruiert. Die virtuelle Drehachse
wird nur in der Vorschau gezeigt; sie ist kein gedrucktes Gelenk.

Die am 2026-11-17 gewaehlte
[Bodenrahmen-Variante](../../Documentation/Guides/Exoskelett.md#3a-neues-entwicklungsziel-ruestungslast-zum-boden)
ist hier noch nicht modelliert. Diese Schalen sind keine lasttragenden
Beinstreben, Kniemodule oder Fussaufnahmen.

## Eigenes Profil exportieren

Ab Repository-Wurzel, ausschliesslich in einen neuen Ausgabeordner:

```bash
python3 tools/suit_clamshell.py --profile Design/Parametric/Profiles/Demo.json --concept --out build/ClamshellDemo-r1
```

Der Demo-Lauf verwendet erfundene Masse. Gemessene Profile werden ohne
`--concept` verarbeitet. Fehlende Masse erfordern explizit den Konzeptmodus;
synthetische Werte und fehlende Nachweise bleiben gekennzeichnet.

## Ansichten und Einzelhaelften

Im erzeugten Ordner:

```bash
openscad --hardwarnings -D 'part="forearm"' -D 'side="l"' -D 'open_fraction=1' -o forearm_l_open.stl LimbClamshell.scad
openscad --hardwarnings -D 'part="thigh"' -D 'side="r"' -D 'piece="rear"' -o thigh_r_rear.stl LimbClamshell.scad
```

| Selektor | Werte | Bedeutung |
| --- | --- | --- |
| part | upperarm, forearm, thigh, shin | Vier Bauraumtypen |
| side | l, r | Separater Profilumfang und eigene Laenge; gespiegelte Drehung |
| open_fraction | 0 bis 1 | Geschlossene bis offene Stellung |
| piece | assembly, rear, front | Gesamte Huelle oder einzelne Schalenhaelfte |

`assembly` ist keine Druckplattenanordnung. Die echte Schalenaufteilung folgt
der ausgewaehlten Halo-Referenz, der Handreichweite und den gemessenen
Querschnitten. Umfang geteilt durch Pi ist lediglich eine Kreislehre; damit
lassen sich elliptische oder sich verjuengende Gliedmassen nicht nachweisen.

`Parameters.scad` neben der Quelldatei ist ein synthetisches direkt oeffnbares
Beispiel. Ein Export enthaelt seine eigenen Parameter und Quellen. Die im
Manifest gespeicherten SHA-256-Werte gelten nur fuer den unveraenderten Export.

## Sechs Module

Vier Dateien setzen die Huellen zu den Modulen des
[Sechs-Module-Zielbilds](../../Documentation/Guides/Mjolnir-Selbstanziehen.md#0-zielbild-sechs-module-zum-zuklemmen)
zusammen. `ModuleCommon.scad` enthaelt die gemeinsamen Bausteine der Arm- und
Beinmodule und wird nicht einzeln geoeffnet.

| Datei | Modul | Inhalt | Verschlussflaechen |
| --- | --- | --- | --- |
| `LegModule.scad` | M1, M2 | Oberschenkel, Kniepad, Schienbein, Schuhcover | 2, dazu der Fersengurt |
| `TorsoModule.scad` | M3 | Zwei Rueckenfluegel, zwei Fronttueren, geteilter Guertel, vier Aufnahmen | 3 |
| `ArmModule.scad` | M4, M5 | Oberarm, Unterarm | 2 |
| `HelmetModule.scad` | M6 | Vordere Schale, hintere Schale | 1 |

```bash
openscad --hardwarnings -D 'side="l"' -D 'open_fraction=1' -D 'elbow_flex_deg=45' -o arm_l_open.stl ArmModule.scad
openscad --hardwarnings -D 'side="r"' -D 'segment="shin"' -D 'piece="rear"' -o shin_r_rear.stl LegModule.scad
openscad --hardwarnings -D 'piece="door"' -D 'side="l"' -o door_l.stl TorsoModule.scad
openscad --hardwarnings -D 'piece="rear"' -o helmet_rear.stl HelmetModule.scad
```

| Datei | Selektoren |
| --- | --- |
| ArmModule | side=l/r; open_fraction=0..1; elbow_flex_deg=0..150; piece=assembly/rear/front; segment=both/upperarm/forearm |
| LegModule | side=l/r; open_fraction=0..1; knee_flex_deg=0..150; piece=assembly/rear/front; segment=all/thigh/shin/kneepad/shoe |
| TorsoModule | side=l/r; open_fraction=0..1; piece=assembly/rear/door/belt_rear/belt_door |
| HelmetModule | hinge_side=l/r; open_fraction=0..1; piece=assembly/front/rear |

`assembly` ist eine Bewegungsansicht. Zum Drucken ein einzelnes Teil waehlen.

### Arm (M4, M5)

Beide Schalen oeffnen zur Innenseite. Oben an der hinteren Oberarmschale sitzt
die Gurtlasche zum Einhaengen, am Ellbogenende beider hinteren Schalen je eine
Lasche fuer die textile Verbindung. Die vorderen Haelften sind am Ellbogen
freigeschnitten (40 mm), der Spalt betraegt 60 mm.

### Bein (M1, M2)

Oberschenkel und Schienbein oeffnen wie die Armschalen. Am Knie sind die
**hinteren** Haelften freigeschnitten (70 mm, Spalt 90 mm), damit die Kniekehle
beim Beugen frei bleibt; die vorderen Haelften reichen bis an das Knie. Die
Laschen sitzen aussen-hinten: oben zum Hueftgurt, am Knie und am Knoechel fuer
Gurtband. Das Kniepad ist ein Bogen vor dem Knie ohne modellierte Befestigung.

Das Schuhcover ist eine Kappe ueber dem getragenen Schuh: unten offen, an der
Ferse offen und ueber dem Knoechel geschlitzt. Es wird von vorn aufgesetzt, der
Fuss muss durch nichts hindurch. Ein Fersengurt durch zwei seitliche Schlitze
haelt es; das ist der dritte Handgriff des Beinmoduls. Die Hoehe (110 mm) ist
eine Annahme, weil das Profil nur Schuhlaenge und -breite kennt.

Das Beinmodul ist eine Verkleidung. Es traegt keine Last zum Boden und ist
nicht an den [Beinantrieb X01](../../Documentation/Guides/Exoskelett-Eigenbau.md)
angepasst.

### Torso (M3)

Die Bewegung folgt dem [Einstieg](../../Documentation/Guides/Mjolnir-Einstieg.md):
Die Rueckenfluegel fahren je 50 mm seitlich aus, danach schwenken die
Fronttueren nach aussen. Der Guertel ist ein eigener, gleich geteilter Ring
20 mm unter dem Brustteil; die Taille bleibt ohne starre Verbindung. Zwei
Laschen oben an den Rueckenfluegeln nehmen die Armmodule auf, zwei unten am
Guertel die Beinmodule. Drei Verschlussflaechen liegen an der vorderen
Mittelfuge: zwei an den Tueren, eine am Guertel.

Nicht modelliert: der Traeger im Ruecken, die Fuehrung der Fluegel, Scharniere,
Schulterhauben (in der Vorschau als grauer Platzhalter), Kragen und Servicepod.
Ohne Traeger haelt die Huelle nichts zusammen; sie zeigt nur Teilung und
Schnittstellen.

### Helm (M6)

Ein unten flach abgeschnittenes Ellipsoid aus Breite, Tiefe und Hoehe des
Profils. Die hintere Schale schwenkt um eine seitliche virtuelle Achse, der
einzige Verschluss sitzt auf der Gegenseite unten und ist mit der Hand dieser
Seite erreichbar. `hinge_side` legt die Seite fest. Die Halsoeffnung ist mit
den Demo-Werten innen etwa 110 x 132 mm gross und damit kleiner als ein Kopf;
deshalb oeffnet die hintere Schale. Die Visieroeffnung ist ein einfacher
Ausschnitt. Visier, Polster, Halsabdeckung und Lueftung fehlen. Die Huelle ist
kein Schutzhelm.

### Verschluss und Laschen

Alle Verschlussflaechen sind eben und **ungebohrt**, solange
`latch_hole_spacing_mm` und `latch_hole_d_mm` null sind. Ein Verschluss ist
nicht ausgewaehlt. Nach dem Kauf:

1. Lochabstand und Schraubendurchmesser aus dem Datenblatt in
   `Parameters.scad` eintragen; es entstehen zwei Durchgangsloecher je Flaeche.
2. `latch_pad_mm` ([Laenge, Breite, Dicke]) an die Grundflaeche anpassen.
3. Ein Segment drucken und pruefen, ob Haken und Gegenstueck ueber die 2 mm
   breite Fuge greifen.

Ein Verschluss mit mehr als zwei Schrauben oder versetztem Gegenstueck passt
nicht in dieses Lochbild und braucht eine eigene Flaeche.

Die Laschen sind **nicht bemessen**: Gurtbreite (25 mm), Stegbreite und
Wandstaerke sind Annahmen. Die Laschen zum Torso tragen ein ganzes Modul; ob
ein Druckteil das kann, zeigt erst eine Belastungsprobe.

### Schaetzwerte im Plan

`ClamshellPlan.json` nennt je Arm- und Beinmodul einen geschaetzten freien
Beugewinkel: der Winkel, bei dem sich die freigeschnittenen Kanten zweier
gerader Rundhuellen treffen. Mit den Demo-Werten sind das 92 Grad am Ellbogen
und 92 Grad am Knie. Die Rechnung dreht um die Huellenmitte, nicht um die
echte Gelenkachse; Polster, Weichteile und Panzerkonturen aendern den Wert.
Gemessen wird am Prototyp (Pruefpunkt MOD04). Fuer das Torsomodul steht dort
die freie Einstiegsbreite bei ausgefahrenen Fluegeln, fuer den Helm die
Halsoeffnung.

## Einbau und Bedienung

- [Selbststaendiges An- und Ausziehen](../../Documentation/Guides/Mjolnir-Selbstanziehen.md)
- [Torso, Einstieg und Station](../../Documentation/Guides/Mjolnir-Einstieg.md)
- [Sechs lokale Komponentenproben inklusive Magnethalter](../Components/README.md)

ClamshellPlan.json laesst Kaufteile, Massen, Kraefte und Tests bewusst offen.
Checklists.csv enthaelt acht Kassetten, sechs Module und zwei uebergreifende Nachweise.
Softwareerfolg bestaetigt nur den Export. Selbststaendiges Anziehen entsteht
erst durch erreichbare Verschluesse und dokumentierte reale Gesamtproben.
