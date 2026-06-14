# Elektronik: Helm-Belueftung (Luefter)

> **Level:** [A] Anfaenger | [F] Fortgeschritten | [P] Profi  |  **Varianten:** alle
> **Voraussetzungen:** 5V-Stromversorgung im Helm vorhanden; fuer PWM-Regelung Arduino (`Documentation/Guides/Elektronik-Verdrahtung.md`).

Luefter im Helm sind bei Convention-Tragen nahezu Pflicht. Sie verhindern Beschlagen des Visiers und halten die Temperatur ertraeglich.

## Empfohlene Luefter

| Luefter | Groesse | Lautstaerke | Luftstrom | Strom | Preis ca. |
| --- | --- | --- | --- | --- | --- |
| Noctua NF-A4x10 5V | 40x40x10 mm | 17.9 dBA (fast unhoerrbar) | 4.8 CFM | 50 mA | 15 EUR/Stueck |
| GDSTIME 40mm USB (3-Speed) | 40x40x10 mm | 22-26 dBA | 4.5-6.1 CFM | 80-150 mA | 10 EUR/2er-Pack |
| Wathai 50mm USB (3-Speed) | 50x50x10 mm | 25-28 dBA | 7-9 CFM | 100-200 mA | 12 EUR/2er-Pack |

**Noctua NF-A4x10 5V** ist der Gold-Standard fuer leisen Betrieb. **GDSTIME** ist der beliebteste in der 405th Community wegen Preis und 3-Stufen-Schalter.

## Platzierung (2-Luefter-Setup)

```
       +------ Exhaust (oben hinten) ------+
       |          heisse Luft raus          |
       |                                    |
       |         +------+                   |
       |         | Helm |                   |
       |         |      |                   |
       |         +------+                   |
       |                                    |
       +------ Intake (unten hinten) -------+
                  kuehle Luft rein
```

- **Intake-Luefter:** unterer Hinterkopf (Kinn-/Kieferbereich), zieht kuehle Luft rein
- **Exhaust-Luefter:** oberer Hinterkopf, drueckt heisse Luft und Feuchtigkeit raus
- Erzeugt Luftstrom ueber das Gesicht und verhindert Visor-Beschlagen
- Mit Klett befestigen fuer einfaches Entfernen
- Kabel entlang der Innenpolster-Kanaele fuehren

## Axial vs. Radialluefter

- **Axialluefter** (Standard-PC-Luefter): mehr Gesamtluftvolumen, gut fuer allgemeine Kuehlung
- **Radialluefter** (Blower): koennen Luft durch Kanaele gezielt zum Visor leiten, besser gegen Beschlagen

## Anschluss

- 5V direkt von der Stromschiene (gleiche Versorgung wie Pi/Arduino)
- Optional per PWM vom Arduino steuern (Geschwindigkeitsregelung, Batterie sparen)
- JST-XH 2-Pin Stecker fuer einfaches Trennen

## Stromverbrauch (2 Luefter)

- Noctua: 2 x 50 mA = 0.1 A
- GDSTIME (max): 2 x 150 mA = 0.3 A
