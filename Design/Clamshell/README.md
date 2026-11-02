# Aufklappbare Arm- und Beinkassetten

Native OpenSCAD-Bauraumhuellen mit zwei getrennten Schalenhaelften und einer
gespiegelten Drehbewegung. Das Konzept setzt radialen Zugang an allen vier
Gliedmassentypen um: Oberarm, Unterarm, Oberschenkel und Schienbein. Kein
Durchschieben der Hand oder des Fusses durch eine geschlossene Ruestungsroehre.

**Status: ungepruefte Bauraummodelle.** Reale Scharniere, Offenhalter,
Rastverschluesse, Haut-/Gelenkabstaende und authentische Oberflaechen sind nicht
in diesen vereinfachten Zylinderschalen konstruiert. Die virtuelle Drehachse
wird nur in der Vorschau gezeigt; sie ist kein gedrucktes Gelenk.

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

## Einbau und Bedienung

- [Selbststaendiges An- und Ausziehen](../../Documentation/Guides/Mjolnir-Selbstanziehen.md)
- [Torso, Einstieg und Station](../../Documentation/Guides/Mjolnir-Einstieg.md)
- [Fuenf lokale Komponentenproben](../Components/README.md)

ClamshellPlan.json laesst Kaufteile, Massen, Kraefte und Tests bewusst offen.
Checklists.csv enthaelt acht Kassetten und zwei uebergreifende Nachweise.
Softwareerfolg bestaetigt nur den Export. Selbststaendiges Anziehen entsteht
erst durch erreichbare Verschluesse und dokumentierte reale Gesamtproben.
