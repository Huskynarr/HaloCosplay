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
freigeschnitten (50 mm). Der Spalt zwischen den Schalen ist das Doppelte des
Kantenabstands aus dem Profil (2 x 20 mm), denn jede Schale endet um diesen
Abstand vor der Gelenkmitte. Ein groesserer Spalt wuerde das Modul laenger
machen als den Arm.

### Bein (M1, M2)

Oberschenkel und Schienbein oeffnen wie die Armschalen. Am Knie sind die
**hinteren** Haelften freigeschnitten (95 mm, Spalt 40 mm wie am Arm), damit die Kniekehle
beim Beugen frei bleibt; die vorderen Haelften reichen bis an das Knie. Die
Laschen sitzen aussen-hinten: oben zum Hueftgurt, am Knie und am Knoechel fuer
Gurtband. Das Kniepad ist ein Bogen vor dem Knie ohne modellierte Befestigung.

Das Schuhcover ist eine Kappe ueber dem getragenen Schuh: unten offen, an der
Ferse offen und ueber dem Knoechel geschlitzt. Es wird von vorn aufgesetzt, der
Fuss muss durch nichts hindurch. Ein Fersengurt durch zwei seitliche Schlitze
haelt es; das ist der dritte Handgriff des Beinmoduls. Hoehe (110 mm) und
Abstand zum Schienbein (25 mm) sind Annahmen, weil das Profil nur Schuhlaenge
und -breite kennt. Beide zusammen muessen zur Knoechelhoehe im Schuh passen:
Die Schienbeinschale endet 20 mm ueber der Knoechelmitte.

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

### Scharnier

Arm- und Beinschalen tragen aussen abwechselnde Scharnieraugen: gerade Zaehlung
an der hinteren, ungerade an der vorderen Haelfte, je etwa 20 mm lang mit
0,4 mm Spiel. Ein durchgehender Stift von 3 mm (`hinge_pin_d_mm`) verbindet sie;
seine Laenge je Schale steht im Plan (`hinge_pins_mm`). Die Augen reichen ueber
die Laenge, die beide Haelften gemeinsam haben, also nicht in den Freischnitt
am Gelenk. Eine Kollisionspruefung im Modell zeigt ueber den ganzen Weg von 0
bis 110 Grad keine Durchdringung der Haelften.

Gedruckt ist davon nichts. Offen sind das Spiel am eigenen Drucker, die
Sicherung des Stifts, die Haltbarkeit der Augen quer zur Schicht und ein
Offenhalter. Torso und Helm drehen weiter um virtuelle Achsen: Am Torso
fehlt der Traeger, an dem Fluegel und Tueren laufen, am Helm folgt die Fuge
einer gekruemmten Flaeche.

### Teilung zu langer Teile

`split_z_mm` und `split_keep` teilen eine Schalenhaelfte an einer
Ueberlappungsfuge: Das untere Stueck traegt die innere Wandhaelfte 15 mm
(`split_lap_mm`) weiter, das obere die aeussere. `PrintPlan.csv` schlaegt fuer
jedes zu lange Teil eine Hoehe vor, 25 mm ueber der Mitte, damit die Fuge die
Verschlussflaeche nicht trifft.

```bash
openscad --hardwarnings -D 'segment="thigh"' -D 'piece="front"' -D 'split_z_mm=215' -D 'split_keep="lower"' -o thigh_front_lower.stl LegModule.scad
openscad --hardwarnings -D 'piece="door"' -D 'split_z_mm=240' -D 'split_keep="upper"' -o door_upper.stl TorsoModule.scad
```

Die Fuge wird geklebt. Klebstoff, Festigkeit der Klebung und der Verzug beider
Stuecke sind nicht untersucht; eine Fuge quer durch ein Scharnierauge ist zu
vermeiden.

### Verschluss und Laschen

Alle Verschlussflaechen sind eben und **ungebohrt**, solange `latch_holes_mm`
und `keeper_holes_mm` leer sind. Ein Verschluss ist nicht ausgewaehlt. Nach dem
Kauf:

1. `latch_hole_d_mm` auf den Bohrdurchmesser setzen.
2. Lochbild des Verschlusskoerpers in `latch_holes_mm` und das des Gegenhalters
   in `keeper_holes_mm` eintragen. Jeder Eintrag ist `[quer, laengs]`: Abstand
   von der Fugenmitte und Versatz entlang der Fuge ab Flaechenmitte, in mm.
   Der Abstand zwischen Verschluss und Gegenhalter ueber die Fuge steht im
   Datenblatt; er verteilt sich auf beide `quer`-Werte.
3. `latch_pad_mm` ([Laenge entlang der Fuge, Breite quer, Dicke]) so waehlen,
   dass Grundflaeche und Lochbild darauf passen. Loecher ausserhalb der Flaeche
   lehnt das Modell ab.
4. Ein Segment drucken und pruefen, ob der Verschluss ueber die 2 mm breite
   Fuge schliesst.

Der Verschlusskoerper sitzt an der vorderen Schalenhaelfte, am Torso an der
rechten Tuer und am Helm an der vorderen Schale; der Gegenhalter jeweils
gegenueber.

**Kandidaten.** Drei kleine Spannverschluesse mit veroeffentlichten Massen,
recherchiert am 2026-11-28. Die Herstellerseiten waren nicht abrufbar; die
Werte stammen aus Katalogseiten der Hersteller, die Haendler bereitstellen.
Die Lage der Loecher zur Zugrichtung und der Montageabstand sind vor dem
Eintragen aus der Zeichnung des gelieferten Teils zu nehmen. Keiner der drei
ist bestellt, montiert oder erprobt.

| Verschluss | Loecher Verschluss | Loecher Gegenhalter | Grundflaeche | Kraft laut Katalog | Hinweis |
| --- | --- | --- | --- | --- | --- |
| Southco 97-30-160-11/-12 mit Gegenhalter 97-37-103 | 2 x 3,3 mm, Abstand 9,5 mm | 2 x 3,3 mm, Abstand 5,5 mm | 21,6 x 12,6 mm | Spannkraft 135 N | Kleinster; passt auf die Standardflaeche. Sicherung nicht angegeben |
| Southco 97-50 (leichte Ausfuehrung) mit Gegenhalter 97-57-103 | 2 x 4,3 mm, Abstand 17,5 mm | 2 x 4,3 mm, Abstand 9,5 mm | 38,1 x 22,6 mm | 310 N | Zusaetzliche Sicherung 97-58-101 erhaeltlich; braucht groessere Flaeche |
| Ganter GN 831-100 (Gegenhalter liegt bei) | 2 x 4,2 mm, Abstand 14,3 mm quer zur Zugrichtung | 2 Loecher, Masse aus der Zeichnung nehmen | 26 x 25,5 mm, Gesamtlaenge 54 bis 67 mm | 1000 N Richtwert | Typ S mit Sicherung; 40 bis 60 g, groesste Bauform |

Quellen: Southco-Handbuch Seiten 282 und 283
([Kopie](https://www.marek.eu/katalog-obrazku/produkt-8375/19129-97-en.pdf)),
Ganter-Datenblatt GN 831
([Kopie](https://reiman.pt/pub/media/technical_data/GANTER/datasheets/GN%20831.pdf)).
Welche Spannkraft eine Schale braucht, ist nicht ermittelt. Ein Verschluss
ohne Sicherung kann beim Haengenbleiben aufgehen.

Die Laschen sind **nicht bemessen**: Gurtbreite (25 mm), Stegbreite und
Wandstaerke sind Annahmen. Die Laschen zum Torso tragen ein ganzes Modul; ob
ein Druckteil das kann, zeigt erst eine Belastungsprobe. Die geschaetzte
Schalenmasse je Modul steht im Plan (naechster Abschnitt) und ist die untere
Grenze fuer diese Last. Eine
[Ueberschlagsrechnung](../Exo/LoadEstimate.md#einhaengelaschen-der-ruestungsmodule)
kommt fuer ein 3 kg schweres Beinmodul mit dynamischem Faktor 3 auf ein Viertel
der angenommenen Druckfestigkeit; Kriechen und Schlag sind darin nicht erfasst.

### Druckplan und Massen

Der Export schreibt `PrintPlan.csv` mit einer Zeile je Druckteil: Huellmasse,
ob das Teil achsparallel in den Bauraum passt, in wie viele Stuecke es quer zur
laengsten Kante zu teilen waere, Schalenvolumen und geschaetzte Masse.

```bash
python3 tools/suit_clamshell.py --profile Design/Parametric/Profiles/Demo.json --concept \
  --build-volume 325 320 325 --density 1.24 --out build/ClamshellDemo-r1
```

Bauraum und Dichte sind Eingaben. Die Voreinstellung (325 x 320 x 325 mm,
1,24 g/cm3 fuer PLA) ist eine Annahme; den nutzbaren Bauraum am eigenen Drucker
pruefen. Mit den Demo-Werten passen 22 von 30 Teilen. Zu lang sind die
vorderen Oberschenkel- und Schienbeinhaelften sowie Tueren und Rueckenfluegel
des Torsos; sie waeren je einmal zu teilen. Die Schalen wiegen nach dieser
Rechnung zusammen etwa 8,9 kg: Torso 3,0 kg, je Bein 2,0 kg, je Arm 0,7 kg,
Helm 0,6 kg.

Grenzen der Rechnung:

- Masse = Schalenvolumen mal Dichte bei massiver 3-mm-Wand. Fuellung, duennere
  Waende oder anderes Material aendern den Wert direkt.
- Nicht enthalten: Laschen, Verschlussflaechen, Verschluesse, Polster, Gurte,
  Traeger, Lack, Elektronik und jede Halo-Detailform.
- Schuhcover und Helm sind grob angenaehert; die uebrigen Volumen weichen bei
  den Demo-Werten hoechstens 2 % vom OpenSCAD-Modell ab.
- Der Bauraumvergleich dreht die Teile nur um die Maschinenachsen. Diagonale
  Lage, Druckrichtung, Stuetzstruktur und die Gestaltung einer Teilungsfuge
  sind nicht bewertet.

### Gelenkbaender und Schnittstellen

`ClamshellPlan.json` nennt je Arm- und Beinmodul die Bandlaenge der
Gelenkverbindung: die gerade Strecke zwischen den beiden Gurtschlitzen bei
gestrecktem Gelenk, bei 45 und 90 Grad und beim geschaetzten freien
Beugewinkel. Mit den Demo-Werten:

| Gelenk | gestreckt | 45 Grad | 90 Grad | Band mindestens |
| --- | --- | --- | --- | --- |
| Ellbogen | 25 mm | 77 mm | 117 mm | 119 mm |
| Knie | 216 mm | 153 mm | 69 mm | 216 mm |

Am Ellbogen oeffnet sich die Rueckseite beim Beugen: Ein Band, das die Beugung
zulaesst, haengt gestreckt etwa 90 mm durch. Am Knie ist es umgekehrt. Ein
festes Gurtband haelt die Schalen deshalb nur in einer Endlage auf Abstand;
elastisches Band oder eine andere Lage der Laschen ist am Prototyp zu
entscheiden. Die Werte sind eine untere Grenze, weil das echte Band um das
Gelenk laeuft.

`interface_checks` im Plan vergleicht vier Groessen: beide Oberschenkelschalen
gegen die Hueftbreite der Huelle, den geschaetzten Beugewinkel gegen 90 Grad,
die Einstiegsbreite des Torsos gegen den Bedarf und die Halsoeffnung gegen die
Kopfbreite. `review` heisst: ansehen, nicht: unbrauchbar. Mit den Demo-Werten
sind die Oberschenkelschalen zusammen 6 mm breiter als die Huefthuelle, sie
beruehren sich also in der Mitte. Die Halsoeffnung ist erwartungsgemaess
kleiner als der Kopf.

`SuitAssembly.scad` zeigt alle sechs Module als einfache Koerper in einer Figur
und faerbt Ueberschneidungen rot. Die Hoehen folgen dem Modulstapel; die
seitliche Lage von Beinen und Armen (`leg_spread_mm`, `arm_gap_mm`) und die
Hoehe von Guertel und Helm sind Anzeigeannahmen. Mit den Demo-Werten ist die
Figur 1813 mm hoch bei 1800 mm Koerpergroesse im Profil.

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
PrintPlan.csv enthaelt 30 Druckteile mit Bauraumvergleich und Massenschaetzung.
Softwareerfolg bestaetigt nur den Export. Selbststaendiges Anziehen entsteht
erst durch erreichbare Verschluesse und dokumentierte reale Gesamtproben.
