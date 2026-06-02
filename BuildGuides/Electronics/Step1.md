# Electronics Step 1: Systemplanung und Verkabelung

## Ziele

- Modulare, sichere Stromversorgung fuer 8+ Stunden
- Saubere Kabelfuehrung im Unteranzug
- Alles auf dem Tisch testen bevor es in die Ruestung kommt

## 1. Komponentenliste finalisieren

### Kern (Pflicht)

| Komponente | Zweck | Kaufen bei |
| --- | --- | --- |
| Raspberry Pi Zero 2 W | HUD-Controller | Berrybase, Amazon |
| microSD 64 GB | Pi OS + Software | Amazon |
| Transparentes OLED 1.51" (SSD1309) | HUD-Display | BuyDisplay, Amazon, DFRobot |
| PiSugar 3 Plus (5000 mAh) | Pi-Stromversorgung (UPS) | pisugar.com, Amazon |
| Arduino Nano (Clone) | LED/Luefter-Steuerung | Amazon, AliExpress |

### LEDs

| Komponente | Menge | Zweck |
| --- | --- | --- |
| WS2812B Strip (60 LED/m) | 2m | Helm + Ruestungs-Akzente |
| 74AHCT125 Level Shifter | 1 | 3.3V -> 5V (wenn Pi LEDs steuert) |
| 330-470 Ohm Widerstaende | 5-10 | Datenleitung jeder LED-Sektion |
| 1000 uF Elkos | 3-5 | Stromglaettung pro LED-Sektion |

### Luefter und Audio

| Komponente | Menge | Zweck |
| --- | --- | --- |
| 40mm 5V Luefter | 2 | Helm-Belueftung |
| PAM8403 Verstaerker + 40mm Lautsprecher | 1 Set | Optional: Voice |
| MAX4466 Mikrofon | 1 | Optional: Voice Changer |

### Strom

| Komponente | Menge | Zweck |
| --- | --- | --- |
| 10.000 mAh USB Powerbank (schlank) | 1-2 | LED/Luefter/Audio Power |
| Sicherungen (2-3A fuse) | 2 | Logik-Schutz |
| Sicherungen (5-10A fuse) | 1 | LED-Schutz |

### Kabel und Stecker

| Komponente | Menge | Zweck |
| --- | --- | --- |
| JST-XH Kit (2/3/4-Pin) | 1 Set | Signal-Verbindungen |
| XT30 Stecker | 5 Paare | Power zwischen Modulen |
| XT60 Stecker | 1 Paar | Hauptbatterie |
| Kabel AWG 18 (rot+schwarz) | 3m je | Power-Leitungen |
| Kabel AWG 22 (rot+schwarz) | 3m je | Luefter, Audio |
| Kabel AWG 26 (diverse Farben) | 5m | Signalleitungen |
| Schrumpfschlauch Sortiment | 1 Set | Isolierung |
| Spiralschlauch 6mm | 3m | Kabelfuehrung im Suit |

## 2. Strombudget kalkulieren

Detailliert: `Documentation/Guides/Elektronik-Strombudget.md` und `Elektronik-Batterie.md`

**Schnell-Uebersicht (V2 typisch):**

| Komponente | Strom |
| --- | --- |
| Pi Zero 2 W (optimiert) | 0.30 A |
| OLED | 0.04 A |
| 2x Luefter | 0.20 A |
| 60 LEDs (50% gruen) | 0.60 A |
| Arduino | 0.03 A |
| Audio (intermittierend) | 0.10 A |
| **Gesamt** | **~1.27 A** |

**Laufzeit mit 2x 10.000 mAh Powerbank:** ca. 13+ Stunden — mehr als genug fuer eine Convention.

## 3. Verkabelungs-Schema planen

Detailliert: `Documentation/Guides/Elektronik-Verdrahtung.md`

### Systemarchitektur

```
[Powerbank 1] ---XT60--- [Verteiler]
                              |
                   +----------+----------+
                   |          |          |
              [PiSugar]  [Arduino]  [Luefter]
                   |          |
              [OLED]     [LED Strips]
                         [Lautsprecher]

[Powerbank 2] ---XT30--- [LED +5V Schiene]
```

### Verkabelungsregeln

- **AWG 18-20** fuer Power-Leitungen (LEDs, Hauptversorgung)
- **AWG 22-24** fuer Luefter, Audio, moderate Lasten
- **AWG 26** NUR fuer Signalleitungen (I2C, LED-Data)
- **GND aller Systeme verbinden!** — gemeinsame Masse ist Pflicht
- **Sicherungen nahe der Batterie** — immer!
- **Strain Relief** an jedem Stecker (Schrumpfschlauch + Heisskleber)

### Stecker-Zuordnung

| Verbindung | Stecker-Typ | Pin-Belegung |
| --- | --- | --- |
| Hauptbatterie | XT60 | +5V, GND |
| Modul-zu-Modul Power | XT30 | +5V, GND |
| I2C (Pi<->Arduino, Pi<->OLED) | JST-XH 4-Pin | VCC, GND, SDA, SCL |
| Luefter | JST-XH 2-Pin | +5V, GND |
| LED-Sektion Data | JST-XH 3-Pin | +5V, GND, DATA |
| Audio | JST-XH 2-Pin | Signal, GND |
| Helm Quick-Disconnect | JST-XH 4-Pin + XT30 | Signal + Power getrennt |

## 4. Kabelwege im Unteranzug

1. **Hauptkabel-Strang:** Vom Backpack (Powerbank-Tasche, Ruecken) nach oben zum Nacken (Helm-Disconnect)
2. **Brust-Abzweig:** Vom Ruecken ueber Schulter zur Brustplatte (LEDs)
3. **Arm-Abzweig:** Von Schulter entlang Oberarm zu Unterarm (LEDs)
4. **Bein-Abzweig:** Vom Guertel entlang Oberschenkel zu Schienbein (LEDs)

Alle Kabel in **6 mm Spiralschlauch** buendeln und mit **Klett-Kabelbindern** am Unteranzug fixieren.

## 5. Loeten und Zusammenbau

### Loet-Reihenfolge

1. **JST/XT-Stecker** an alle Kabelenden loeten und mit Schrumpfschlauch isolieren
2. **LED-Sektionen** vorbereiten: Widerstand auf Data-In, Elko auf Power-Eingang
3. **Arduino Nano:** Header-Pins einloeten, Anschluss-Kabel vorbereiten
4. **Verteilerplatine** (optional): kleine Lochrasterplatine als Power-Verteiler

### Loettipps

- Loetkolben auf 320-350 C (bleifreies Lot)
- Kabel vorher verzinnen, dann zusammenloeten
- Schrumpfschlauch VOR dem Loeten auf Kabel schieben (klassischer Fehler!)
- Jede Loetstelle auf Kurzschluss pruefen (Multimeter Durchgangspruefung)

## 6. Tisch-Test (Pflicht!)

Alles auf dem Tisch aufbauen und testen BEVOR es in die Ruestung kommt:

- [ ] Pi bootet und HUD startet (systemd)
- [ ] OLED zeigt Bild (i2cdetect -y 1 zeigt Adresse)
- [ ] Arduino empfaengt I2C Befehle vom Pi
- [ ] Alle LED-Sektionen leuchten korrekt
- [ ] Luefter drehen in richtiger Richtung
- [ ] Audio funktioniert (wenn vorhanden)
- [ ] Batterie-Laufzeit messen: Stoppuhr starten, System laufen lassen bis leer
- [ ] Keine ueberhitzenden Komponenten (alles anfassen nach 30 Min)
- [ ] Alle Stecker halten bei leichtem Ziehen (Strain Relief ok)

**Erst wenn alles auf dem Tisch funktioniert, geht es in die Ruestung.**
