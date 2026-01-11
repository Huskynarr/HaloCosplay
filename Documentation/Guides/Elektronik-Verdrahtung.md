# Elektronik: Verdrahtung und Power-Verteilung

Ziel: sichere, modulare Verkabelung mit sauberer Trennung von Logik und Leistung.

## Diagramm (SVG)

![Wiring diagram](Elektronik-Verdrahtung.svg)

## Grundschema (vereinfacht)

```
[BATTERIE]
    |
    +-- [Hauptschalter] -- [Sicherung 2-3A] -- [5V Regler] --+--> Pi Zero 2 W
                                                          +--> OLED
                                                          +--> Arduino
                                                          +--> Luefter

    +-- [Sicherung 5-10A] --------------------+--> LED +5V
                                             +--> (optional) Audio Amp

GND aller Systeme verbinden!
```

## LED-Verkabelung (WS2812)

- 5V direkt von der LED-Stromschiene
- Datenleitung von Arduino (oder Pi) ueber 330-470 Ohm Serienwiderstand
- 1000 uF Kondensator zwischen +5V und GND am LED-Strip
- Level-Shifter nutzen, wenn Pi direkt LEDs steuert (3.3V -> 5V)

## Helm-Module

- Helm als eigenes Modul mit Quick-Disconnect am Nacken
- Display, Luefter, LEDs im Helm
- Steckverbinder (JST-XH fuer Signal, XT30 fuer Power)

## Kabel und Querschnitt

- Signal/Low Power: AWG 22-26
- LED/Power: AWG 18-20
- Kabelwege moeglichst kurz und mechanisch entlastet

## Sicherheits-Check

- Sicherungen nahe der Batterie
- Keine blanken Kontakte
- Kabel gegen Zug sichern
- Not-Aus erreichbar

## Testreihenfolge

1. Nur Pi + OLED
2. Pi + Luefter
3. Arduino + LEDs
4. Alles zusammen (Kurzschluss-Check)
