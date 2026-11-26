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

## Armmodul

`ArmModule.scad` setzt Oberarm- und Unterarmhuelle einer Seite zu einem Modul
zusammen, dem ersten Baustein des
[Sechs-Module-Zielbilds](../../Documentation/Guides/Mjolnir-Selbstanziehen.md#0-zielbild-sechs-module-zum-zuklemmen).
Beide Schalen oeffnen zur Innenseite. Neu gegenueber den Einzelhuellen:

- Gurtlasche oben an der hinteren Oberarmschale als Einhaengepunkt zur Schulter
- je eine Gurtlasche am Ellbogenende beider hinteren Schalen fuer die textile
  Verbindung; der Ellbogen selbst bleibt ohne starres Teil
- je eine ebene Flaeche an beiden Haelften jeder Schale fuer einen Kaufverschluss
  (zwei Verschluesse je Modul)
- Freischnitt der vorderen Haelften am Ellbogen, damit der Arm beugen kann

```bash
openscad --hardwarnings -D 'side="l"' -D 'open_fraction=1' -D 'elbow_flex_deg=45' -o arm_l_open.stl ArmModule.scad
openscad --hardwarnings -D 'side="r"' -D 'segment="forearm"' -D 'piece="rear"' -o forearm_r_rear.stl ArmModule.scad
```

| Selektor | Werte | Bedeutung |
| --- | --- | --- |
| side | l, r | Seite mit eigenen Profilmassen |
| open_fraction | 0 bis 1 | Geschlossen bis offen |
| elbow_flex_deg | 0 bis 150 | Beugung des Ellbogens in der Ansicht |
| piece | assembly, rear, front | Alles, nur hintere oder nur vordere Haelften |
| segment | both, upperarm, forearm | Zum Drucken ein einzelnes Segment waehlen |

Laschen und Verschlussflaechen sind **nicht bemessen**: Gurtbreite
(25 mm), Ellbogenspalt (60 mm) und Freischnitt (40 mm) sind Annahmen, Lochbilder
fehlen, weil kein Verschluss ausgewaehlt ist. Die Lasche oben muss spaeter das
ganze Modul tragen; ob ein Druckteil das kann, zeigt erst eine Belastungsprobe.

`ClamshellPlan.json` nennt je Modul einen geschaetzten freien Beugewinkel. Er
gilt fuer zwei gerade Rundhuellen: der Winkel, bei dem die Vorderkante des
Unterarms die Ebene der Oberarm-Vorderkante erreicht. Mit den Demo-Werten sind
das 92 Grad. Polster, Weichteile und echte Panzerkonturen aendern den Wert;
gemessen wird am Prototyp (Pruefpunkt MOD04).

## Einbau und Bedienung

- [Selbststaendiges An- und Ausziehen](../../Documentation/Guides/Mjolnir-Selbstanziehen.md)
- [Torso, Einstieg und Station](../../Documentation/Guides/Mjolnir-Einstieg.md)
- [Sechs lokale Komponentenproben inklusive Magnethalter](../Components/README.md)

ClamshellPlan.json laesst Kaufteile, Massen, Kraefte und Tests bewusst offen.
Checklists.csv enthaelt acht Kassetten, zwei Armmodule und zwei uebergreifende Nachweise.
Softwareerfolg bestaetigt nur den Export. Selbststaendiges Anziehen entsteht
erst durch erreichbare Verschluesse und dokumentierte reale Gesamtproben.
