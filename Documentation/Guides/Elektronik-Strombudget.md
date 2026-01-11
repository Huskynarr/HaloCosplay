# Elektronik: Strombudget und Laufzeit

Dieser Guide hilft beim realistischen Power-Budget und bei der Laufzeitplanung.

## Typische Stromwerte (Richtwerte)

| Komponente | Typischer Strom | Hinweis |
| --- | --- | --- |
| Raspberry Pi Zero 2 W | 0.2-0.4 A idle, 0.6-1.0 A load | stark abhaengig von WiFi/CPU |
| Transparentes OLED | 0.02-0.05 A | Helligkeit entscheidend |
| 40 mm Luefter (5V) | 0.08-0.15 A pro Stueck | Datenblatt pruefen |
| Arduino Nano | 0.02-0.04 A | ohne grosse Last |
| WS2812 LED | 0.02 A pro LED (gruen), 0.06 A (weiss) | worst case weiss |

## Beispielrechnung (V2)

Annahme:
- Pi Zero 2 W: 0.8 A
- OLED: 0.04 A
- 2x Luefter: 0.2 A
- 24 WS2812 LEDs gruen: 0.48 A
- Arduino: 0.03 A

**Gesamt:** ca. 1.55 A

## Laufzeit schaetzen

Formel:

```
Laufzeit (h) = Kapazitaet (mAh) / Strom (mA) * Effizienz
```

Beispiel mit 5000 mAh und 1.55 A (1550 mA), Effizienz 0.85:

```
5000 / 1550 * 0.85 = ca. 2.7 h
```

## Tipps fuer mehr Laufzeit

- Display-Helligkeit reduzieren
- LEDs dimmen (50% spart massiv)
- WiFi/Bluetooth abschalten
- Luefter per PWM steuern
- Zweiten Akku als Backup nutzen

## Pflicht

- Strom messen (Multimeter) vor dem Einbau
- 20-30% Reserve fuer Spitzenlast einplanen
