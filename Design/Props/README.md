# Props

Parametrische Prop-Modelle fuer den Master-Chief-Kosplay. Alle Modelle sind
Konstruktionsmodelle ohne Freigabe; sie sind stumpf, ohne Spitze und ohne
Funktion als Waffe.

## Waffenrecht

Vor jedem Bau und Transport die WaffG- und Con-Regeln pruefen. Siehe
[Waffen-Prop-Guide](../Documentation/Guides/Waffen-Prop.md). Der Transport
erfolgt immer blickdicht und am Veranstaltungsort erst ausgepackt.

## Teile

| Teil | Datei | Hinweis |
| --- | --- | --- |
| Energy Sword | energy_sword.stl | Con-sicher, offensichtlich Sci-Fi. Klinge stumpf, ohne Spitze. |

## Export

```bash
~/tools/squashfs-root/usr/bin/openscad -o Design/Props/energy_sword.stl Design/Props/EnergySword.scad
```

## Offene Punkte

- Kabelkanal fuer LED-Beleuchtung vorhanden, Elektronik noch nicht integriert.
- Griff-Textur (Rillen) ist konstruktiv, nicht graviert.
- Material: PETG oder PLA+; Klinge in transparentem oder fluoreszierendem Filament.
