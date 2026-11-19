# Elektronik: Strombudget und Laufzeit

> **Level:** [A] Anfaenger | [F] Fortgeschritten | [P] Profi  |  **Varianten:** alle

Dieser Guide hilft beim realistischen Power-Budget und bei der Laufzeitplanung.

## Typische Stromwerte (Richtwerte)

| Komponente | Typischer Strom | Max Strom | Hinweis |
| --- | --- | --- | --- |
| Raspberry Pi Zero 2 W (idle, WiFi aus) | 0.12 A | 1.0 A | Stark abhaengig von CPU-Last |
| Raspberry Pi Zero 2 W (HUD-Betrieb) | 0.25-0.40 A | 1.0 A | WiFi aus, HDMI aus, GPU 16 MB |
| ESP32-S31 mit Linux (Developer Preview) | noch unklar | noch unklar | Keine belastbaren Verbrauchsangaben; siehe Elektronik-Sprachsteuerung, Abschnitt 3.2 |
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

### Laufzeit-Ziel: 10 Stunden und mehr

Fuer einen langen Con-Tag (Gamescom/DoKomi von Oeffnung bis Schluss) reicht das
Standard-Setup knapp nicht. Zwei Wege, beide kombinierbar:

**Weg 1: Groessere Powerbanks (einfach, aber schwer)**

| Schiene | Verbraucher | Fuer 10 h noetig | Empfehlung |
| --- | --- | --- | --- |
| Pi-Rail | ca. 8 W | ca. 80 Wh | 26.800 mAh (ca. 99 Wh, ca. 500 g) |
| FX-Rail | ca. 4-6 W | ca. 40-60 Wh | 20.000 mAh (ca. 63 Wh nutzbar, ca. 380 g) |

Gesamtgewicht nur Akkus: ca. 900 g. Achtung: Powerbanks ueber 100 Wh duerfen
nicht ins Flugzeug - bei Anreise mit dem Auto egal.

**Weg 2: Verbrauch senken (leichter, kostet Planung statt Geld)**

- LEDs auf 50% Helligkeit + gruener Kanal: FX-Rail faellt von 18 W Worst-Case
  auf 3-4 W - der groesste Hebel ueberhaupt
- Luefter per PWM auf 60% (der Arduino-Code macht das schon)
- OLED-Helligkeit reduzieren (im Helm reicht 50% locker)
- Show-Effekte (100% Weiss, Alarm) nur fuer Momente, nicht Dauerbetrieb

**Weg 3: Hot-Swap (schon im Standard-Setup machbar)**

Zweite Powerbank derselben Groesse in die Brust-/Guerteltasche, in einer Pause
(auf der Toilette, beim Essen) umstecken. 2x 20.000 mAh Pi-Rail = 15+ h. Voraussetzung:
die Nabelschnur/Verkabelung muss einen Wechsel ohne Halbausbau erlauben - beim
Bau der Stromverteilung einplanen (Stecker statt fest verloetet).

**Nebler:** haengen bewusst NICHT an den Powerbanks. Der MicroFogger o.ae. hat
einen eigenen, wechselbaren Akku - fuer einen langen Tag einen Ersatzakku und
100-200 ml Fluid einpacken. Begrenzend ist das Fluid, nicht der Akku.

**Realistische 10-h-Kombination:** Weg 2 (Disziplin bei den LEDs) + Weg 1 fuer
die Pi-Rail (26.800 mAh) + 20.000 mAh FX-Rail. Dann bleiben selbst bei viel
Show-Effekt 20-30% Reserve, wie es der Mess-Pflicht-Abschnitt unten fordert.

### Wichtige Grenzen

- **5V/3A pro Port:** Eine normale Powerbank liefert max. 15 W pro USB-C-Port. Die
  Pi-Rail bleibt mit ca. 9 W Peak darunter - ein 5-A-Netzteil ist im Helm nicht
  noetig. Der Pi 5 meldet an einer 3-A-Quelle "kein 5-A-Netzteil" und begrenzt USB
  auf 600 mA; das reicht, weil Soundkarte + Nano nur ca. 150 mA ziehen.
- **Beide Schienen trennen:** LEDs nie an die Pi-Rail haengen - Spannungseinbrueche
  beim LED-Anlauf wuerden den Pi abstuerzen lassen.
- **Sicherungen** siehe Tabelle unten; FX-Rail mit 3 A sichern. Der Peak von
  4,4 A steht an dieser Schiene nicht zur Verfuegung: LED-Helligkeit in der
  Firmware so begrenzen, dass die Schiene unter ca. 2,5 A bleibt.

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
5000 / 1000 * 3,7 * 0,85 = 15,7 Wh;  15,7 Wh / (0,44 A * 5 V) = ca. 7.1 Stunden
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
20000 / 1000 * 3,7 * 0,85 = 62,9 Wh;  62,9 Wh / (1,17 A * 5 V) = ca. 10.8 Stunden
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
20000 / 1000 * 3,7 * 0,85 = 62,9 Wh;  62,9 Wh / (1,27 A * 5 V) = ca. 9.9 Stunden
```

## Laufzeit-Formel

```
Nutzbare Energie (Wh) = Kapazitaet (mAh) / 1000 * 3,7 V * 0,85
Laufzeit (h)          = Nutzbare Energie (Wh) / (Strom (A) * 5 V)
```

Die mAh-Angabe gilt fuer die 3,7-V-Zelle. mAh direkt durch den 5-V-Strom zu
teilen ergibt rund 35 % zu lange Laufzeiten. 0,85 = Verlust durch
Spannungswandlung, Kabel und Waerme.

## Laufzeit-Tabelle (Schnellreferenz)

| Batterie | 0.5 A | 1.0 A | 1.3 A | 1.5 A | 2.0 A |
| --- | --- | --- | --- | --- | --- |
| 5.000 mAh (PiSugar) | 6.3 h | 3.1 h | 2.4 h | 2.1 h | 1.6 h |
| 10.000 mAh (1x Powerbank) | 12.6 h | 6.3 h | 4.8 h | 4.2 h | 3.1 h |
| 15.000 mAh (PiSugar + PB) | 18.9 h | 9.4 h | 7.3 h | 6.3 h | 4.7 h |
| 20.000 mAh (2x Powerbank) | 25.2 h | 12.6 h | 9.7 h | 8.4 h | 6.3 h |

## Tipps fuer mehr Laufzeit

### Groesster Hebel: LEDs

- LEDs sind der groesste Verbraucher (60 LEDs bei 100% weiss = 3.6 A!)
- **50% Helligkeit halbiert den Strom** (annaehernd linear); wegen der
  nicht-linearen Wahrnehmung wirkt das kaum dunkler
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
| LEDs an Powerbank (max. 3 A) | 3 A traege | Kabel und JST-Stecker (3 A) |
| LEDs an LiPo + 5V/5A-Regler | 5 A hinter dem Regler | LED-Strip Kurzschluss; Pfad ohne JST-XH, Kabel mind. 0,75 mm2 |
| Roher LiPo (vor dem Regler) | passend zum Reglereingang, z.B. 5 A bei 3S | Akkukurzschluss; Pflicht |

Auslegungsregel: Die Sicherung muss kleiner sein als das schwaechste Glied
ihres Pfads (Stecker, Kabel, Quelle) und rund 25 % ueber dem gemessenen
Dauerstrom liegen. Eine 10-A-Sicherung hinter einer 3-A-Powerbank oder vor
einem 3-A-JST-Stecker loest nie aus und schuetzt nichts. Powerbanks begrenzen
den Strom selbst; die Sicherung schuetzt dort vor allem duenne Kabel und
Stecker. Sicherungen so nah wie moeglich an der Quelle montieren.
