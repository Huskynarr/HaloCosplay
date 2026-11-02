# MJOLNIR Ruestungsmodell (Master-Chief-inspiriert)

**Konstruktionsmodell, keine fertige Druckruestung.** Alle Teile sind
parametrische OpenSCAD-Schalen, proportioniert nach Master-Chief-Referenzen
und skaliert auf die Profilmasse aus Design/Parametric. Es liegt keine
Vermessung einer Person, keine Passfreigabe und keine Lastpruefung vor.

## Teile

| Teil | Datei | Hinweis |
| --- | --- | --- |
| Helm | armor-helmet.stl | Visier separat |
| Visier | armor-visor.stl | Transparentes Filament oder Abguss |
| Brust | armor-chest.stl | Mit Gurt-Schlitzen |
| Rueckenplatte | armor-back.stl | Mit Lueftung und Rucksack-Aufnahme |
| Schulter L/R | armor-shoulder_l.stl / armor-shoulder_r.stl | Mark-VI-Pauldron |
| Oberarm L/R | armor-upperarm_l.stl / armor-upperarm_r.stl | Split-Fuge fuer Einstieg |
| Unterarm L/R | armor-forearm_l.stl / armor-forearm_r.stl | Split-Fuge |
| Handschutz L/R | armor-gauntlet_l.stl / armor-gauntlet_r.stl | Ueber Unterarm |
| Oberschenkel L/R | armor-thigh_l.stl / armor-thigh_r.stl | Mit Panzerplatte |
| Schienbein L/R | armor-shin_l.stl / armor-shin_r.stl | Vorgezogener Schutz |
| Stiefel L/R | armor-boot_l.stl / armor-boot_r.stl | Mit Sohle |

## STL-Export

```bash
./Design/Armor/export_stl.sh ~/tools/squashfs-root/usr/bin/openscad
```

Die STLs liegen in Design/Armor/STL/. Alle Teile sind einzeln druckbar;
Schalen sind halboffen mit Gurtschlitzen fuer die Montage am Trager.
Die Stiefel werden mit reduzierter Aufloesung ($fn=24) exportiert.

## Zusammenbau

Die Schalen werden am eigenen Trager (siehe Exoskelett-Guide) mit Gurten
befestigt. Jede Schale hat eine Split-Fuge und Gurtschlitze. Visier und Helm
werden getrennt gefertigt und zusammengeklebt oder verschraubt.

## Offene Punkte

- Passform an reale Person: Profile in Design/Parametric ausfuellen.
- Lastverteilung: Trager-Konzept im Exoskelett-Guide, noch keine Pruefung.
- Visier-Material: PETG oder Guss, noch nicht entschieden.
- Oberflaechendetails (Gravuren, Kanten) fehlen; Grundform fuer erste Proben.
