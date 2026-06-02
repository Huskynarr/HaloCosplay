# Elektronik: Strombudget und Laufzeit

> **Level:** [A] Anfaenger | [F] Fortgeschritten | [P] Profi  ·  **Varianten:** alle

Dieser Guide hilft beim realistischen Power-Budget und bei der Laufzeitplanung.

## Typische Stromwerte (Richtwerte)

| Komponente | Typischer Strom | Max Strom | Hinweis |
| --- | --- | --- | --- |
| Raspberry Pi Zero 2 W (idle, WiFi aus) | 0.12 A | 1.0 A | Stark abhaengig von CPU-Last |
| Raspberry Pi Zero 2 W (HUD-Betrieb) | 0.25-0.40 A | 1.0 A | WiFi aus, HDMI aus, GPU 16 MB |
| Transparentes OLED (SSD1309) | 0.02-0.05 A | 0.05 A | Helligkeit entscheidend |
| 40 mm Luefter (5V) | 0.05-0.15 A | 0.15 A | Noctua: 0.05A, GDSTIME: 0.15A |
| Arduino Nano | 0.02-0.04 A | 0.05 A | Ohne angeschlossene Lasten |
| WS2812B LED (gruen, pro LED) | 0.02 A | 0.06 A (weiss) | Worst case = alle 3 Kanaele voll |
| WS2812B LED (50% gruen, pro LED) | 0.01 A | — | Realitischer Convention-Wert |
| PAM8403 Audio (aktiv) | 0.05-0.15 A | 0.30 A | Abhaengig von Lautstaerke |
| MAX4466 Mikrofon | < 0.01 A | 0.01 A | Vernachlaessigbar |

## Beispielrechnungen

### Minimal-Setup (nur HUD + Luefter)

| Komponente | Strom |
| --- | --- |
| Pi Zero 2 W (optimiert) | 0.30 A |
| OLED | 0.04 A |
| 2x Noctua Luefter | 0.10 A |
| **Gesamt** | **0.44 A** |

Laufzeit mit PiSugar 3 Plus (5000 mAh):
```
5000 / 440 * 0.85 = ca. 9.7 Stunden
```

### Standard V2 Setup

| Komponente | Strom |
| --- | --- |
| Pi Zero 2 W (optimiert) | 0.30 A |
| OLED | 0.04 A |
| 2x GDSTIME Luefter | 0.20 A |
| 60 WS2812B LEDs (50% gruen) | 0.60 A |
| Arduino Nano | 0.03 A |
| **Gesamt** | **1.17 A** |

Laufzeit mit 2x 10.000 mAh Powerbank:
```
20000 / 1170 * 0.85 = ca. 14.5 Stunden
```

### Voll-Setup (HUD + LEDs + Audio)

| Komponente | Strom |
| --- | --- |
| Pi Zero 2 W (optimiert) | 0.30 A |
| OLED | 0.04 A |
| 2x GDSTIME Luefter | 0.20 A |
| 60 WS2812B LEDs (50% gruen) | 0.60 A |
| Arduino Nano | 0.03 A |
| PAM8403 Audio (intermittierend) | 0.10 A |
| **Gesamt** | **1.27 A** |

Laufzeit mit 2x 10.000 mAh Powerbank:
```
20000 / 1270 * 0.85 = ca. 13.4 Stunden
```

## Laufzeit-Formel

```
Laufzeit (h) = Kapazitaet (mAh) / Strom (mA) * Effizienz
```

Effizienz = 0.85 (15% Verlust durch Spannungsregelung, Kabel, Waerme)

## Laufzeit-Tabelle (Schnellreferenz)

| Batterie | 0.5 A | 1.0 A | 1.3 A | 1.5 A | 2.0 A |
| --- | --- | --- | --- | --- | --- |
| 5.000 mAh (PiSugar) | 8.5 h | 4.3 h | 3.3 h | 2.8 h | 2.1 h |
| 10.000 mAh (1x Powerbank) | 17.0 h | 8.5 h | 6.5 h | 5.7 h | 4.3 h |
| 15.000 mAh (PiSugar + PB) | 25.5 h | 12.8 h | 9.8 h | 8.5 h | 6.4 h |
| 20.000 mAh (2x Powerbank) | 34.0 h | 17.0 h | 13.1 h | 11.3 h | 8.5 h |

## Tipps fuer mehr Laufzeit

### Groesster Hebel: LEDs

- LEDs sind der groesste Verbraucher (60 LEDs bei 100% weiss = 3.6 A!)
- **50% Helligkeit spart 75% Strom** (nicht-lineare Wahrnehmung)
- Nur gruenen Kanal nutzen = 1/3 des Stroms von weiss
- Weniger LEDs: 30 statt 60 halbiert den Verbrauch
- LEDs in nicht-sichtbaren Bereichen ausschalten

### Pi optimieren

- WiFi/Bluetooth abschalten (spart ~50 mA)
- HDMI deaktivieren (spart ~25 mA)
- GPU-Speicher auf 16 MB (kein Desktop)
- Siehe `Elektronik-Autostart.md` fuer Details

### Luefter optimieren

- Noctua statt Billig-Luefter (50 mA vs 150 mA pro Stueck)
- PWM-Steuerung: Luefter auf 60% = deutlich weniger Strom, kaum weniger Luftstrom
- Luefter nur bei Bedarf (Temperatur-gesteuert)

### Allgemein

- Zweiten Akku als Backup nutzen (Hot-Swap waehrend Pause)
- Display-Helligkeit reduzieren (OLED braucht wenig, aber jedes mA zaehlt)
- Audio nur bei Bedarf (Taster statt Dauerbetrieb)

## Strom messen (Pflicht vor Einbau!)

1. Multimeter in **Ampere-Modus** (Messbereich 10A)
2. In Reihe zwischen Batterie/Powerbank und Verbraucher schalten
3. System einschalten und Strom ablesen
4. Alle Modi testen (LEDs an/aus, Luefter an/aus, Audio an)
5. **Peak-Strom** notieren (beim Einschalten kurzzeitig hoeher)
6. 20-30% Reserve fuer Spitzenlast einplanen

## Sicherungen

| Schiene | Sicherung | Schuetzt |
| --- | --- | --- |
| Logik (Pi, Arduino, OLED) | 2-3 A Feinsicherung | Ueberlast, Kurzschluss |
| LEDs | 5-10 A Feinsicherung | LED-Strip Kurzschluss |
| Gesamt (nahe Batterie) | 10 A | Alles |

Sicherungen so nah wie moeglich an der Batterie montieren.
