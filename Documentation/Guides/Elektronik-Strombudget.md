# Elektronik: Strombudget und Laufzeit

> **Level:** [A] Anfaenger | [F] Fortgeschritten | [P] Profi  |  **Varianten:** alle

Dieser Guide hilft beim realistischen Power-Budget und bei der Laufzeitplanung.

## Typische Stromwerte (Richtwerte)

| Komponente | Typischer Strom | Max Strom | Hinweis |
| --- | --- | --- | --- |
| Raspberry Pi Zero 2 W (idle, WiFi aus) | 0.12 A | 1.0 A | Stark abhaengig von CPU-Last |
| Raspberry Pi Zero 2 W (HUD-Betrieb) | 0.25-0.40 A | 1.0 A | WiFi aus, HDMI aus, GPU 16 MB |
| Raspberry Pi 5 (idle) | 0.4-0.6 A | 2.4 A | WiFi aus, HDMI aus |
| Raspberry Pi 5 (HUD + Sprachsteuerung) | 0.9-1.4 A | 2.4 A | Vosk + Kamera aktiv; siehe Pi-5-Abschnitt unten |
| Transparentes OLED (SSD1309) | 0.02-0.05 A | 0.05 A | Helligkeit entscheidend |
| 40 mm Luefter (5V) | 0.05-0.15 A | 0.15 A | Noctua: 0.05A, GDSTIME: 0.15A |
| Arduino Nano | 0.02-0.04 A | 0.05 A | Ohne angeschlossene Lasten |
| WS2812B LED (gruen, pro LED) | 0.02 A | 0.06 A (weiss) | Worst case = alle 3 Kanaele voll |
| WS2812B LED (50% gruen, pro LED) | 0.01 A | - | Realitischer Convention-Wert |
| PAM8403 Audio (aktiv) | 0.05-0.15 A | 0.30 A | Abhaengig von Lautstaerke |
| MAX4466 Mikrofon | < 0.01 A | 0.01 A | Vernachlaessigbar |

## Pi 5 Setup (Sprachsteuerung + Kamera, V2/V3 optional)

Der Pi 5 verbraucht mehr als der Zero 2 W, aber keineswegs durchgehend 25 W.
Realistisch fuer das Modul aus `Elektronik-Sprachsteuerung.md`:

### Schiene 1 (Pi-Rail, Powerbank A 5V/3A)

| Komponente | Typisch | Peak | Hinweis |
| --- | --- | --- | --- |
| Pi 5 (HUD + Vosk + Ansagen) | 0.9-1.4 A | 1.8 A | Vosk rechnet nur waehrend PTT |
| Active Cooler | 0.02-0.06 A | 0.06 A | Pflicht, siehe unten |
| AI Camera (IMX500) | 0.20 A | 0.25 A | Erkennungsnetz laeuft auf dem Chip |
| OLED (SSD1309) | 0.04 A | 0.05 A | |
| USB-Soundkarte + Nano | 0.03 A | 0.05 A | |
| PAM8403 (innen, Ansagen) | 0.03 A | 0.10 A | nur Piepen/Ansagen |
| **Summe Schiene 1** | **ca. 1.3-1.8 A** | **ca. 2.2 A** | bleibt unter 5V/3A |

### Schiene 2 (FX-Rail, Powerbank B 5V/3A + 3-A-Sicherung)

| Komponente | Typisch | Peak | Hinweis |
| --- | --- | --- | --- |
| 60 WS2812B (50% gruen) | 0.60 A | 3.6 A | Peak nur bei 100% Weiss |
| 2 Helm-Luefter | 0.20 A | 0.30 A | |
| MAX98357A (Helmfunk) | 0 A | 0.60 A | nur beim Sprechen |
| **Summe Schiene 2** | **ca. 0.8-1.5 A** | **ca. 4.4 A** | Peak nur Sekunden |

Nebler haengen bewusst an ihrem eigenen Akku (MicroFogger o.ae.) und zaehlen
nicht in dieses Budget. Ihr Heizelement zieht zwar kurz ~40 W, stossweise.

### Fazit: Gesamtlast

- **Dauerlast typisch:** ca. 10-16 W (beide Schienen zusammen)
- **Kurzzeit-Peak:** ca. 30-35 W (alle LEDs 100% Weiss + Helmfunk + Kamera) - genau
  dagegen helfen die LED-Tipps unten (50% Helligkeit, gruener Kanal)
- Eine Dauerlast von 25-27 W entsteht nur, wenn alle LEDs dauerhaft auf 100% Weiss
  laufen - das ist ein Show-Moment, kein Betriebszustand.

### Laufzeit (Wh statt mAh rechnen!)

Powerbank-Angaben in mAh beziehen sich auf die 3,7-V-Zellenspannung, nicht auf die
5-V-Ausgangsspannung. Genauer ist die Rechnung ueber Wh:

```
Nutzbare Energie (Wh) = Kapazitaet (mAh) / 1000 * 3,7 V * 0,85 (Wandlungsverlust)
Laufzeit (h)          = Nutzbare Energie (Wh) / Dauerlast (W)
```

| Powerbank | Energie | Pi-Rail bei 8 W | FX-Rail bei 4 W |
| --- | --- | --- | --- |
| 10.000 mAh | 31 Wh | ca. 3,9 h | ca. 6,6 h |
| 20.000 mAh | 63 Wh | ca. 7,9 h | ca. 13,2 h |

Grobe Praxiswerte fuer das Gesamtsetup: **Pi-Rail 20.000 mAh = 5-7 h Con-Tag,
FX-Rail 10.000 mAh = 4-8 h** je nach LED-Effekt. Zwei Powerbanks im Ruecken
reichen also fuer einen vollen Con-Tag - mehr Akkus sind nicht noetig, aber
ca. 750-800 g zusaetzliches Gewicht muss der Guertel/Tragerahmen hergeben.

### Wichtige Grenzen

- **5V/3A pro Port:** Eine normale Powerbank liefert max. 15 W pro USB-C-Port. Die
  Pi-Rail bleibt mit ca. 9 W Peak darunter - ein 5-A-Netzteil ist im Helm nicht
  noetig. Der Pi 5 meldet an einer 3-A-Quelle "kein 5-A-Netzteil" und begrenzt USB
  auf 600 mA; das reicht, weil Soundkarte + Nano nur ca. 150 mA ziehen.
- **Beide Schienen trennen:** LEDs nie an die Pi-Rail haengen - Spannungseinbrueche
  beim LED-Anlauf wuerden den Pi abstuerzen lassen.
- **Sicherungen** siehe Tabelle unten; FX-Rail mit 3 A sichern.

### Kuehlung des Pi 5 im Helm

- **Active Cooler (offiziell, ca. 6 EUR) ist Pflicht.** Ohne Kuehlkoerper/Luefter
  drosselt der Pi 5 ab 80 Grad C den Takt und schaltet bei 85 Grad ab - mitten auf der Con.
- Der Active Cooler blaest nach oben. Die warme Abluft **nach aussen** fuehren
  (Oeffnung am Helmscheitel oder hinten), nicht Richtung Kopf.
- Der Helm hat eigene Luefter: ansaugen unten am Kinn, ausblasen oben/hinten. Die
  Pi-Abwaerme gehoert in diesen Luftstrom, nicht daneben.
- **Powerbanks nicht in Schaumstoff einpacken** - sie werden selbst warm und
  duerfen nicht hitzestauen. Guerteltasche oder Tragerahmen mit Luftkontakt.
- Praxis-Check vor der Con: 30 min alle Module an, Temperatur mit `vcgencmd
  measure_temp` loggen. Bleibt der Pi unter 70 Grad, ist die Kuehlung im Griff.

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

### Standard V2 Setup (ohne Audio)

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
