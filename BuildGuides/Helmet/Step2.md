# Helmet Step 2: Elektronik, Lackierung und Finish

> **Level:** [F] Fortgeschritten | [P] Profi  ·  **Varianten:** V2/V3 (HUD)  ·  **Voraussetzungen:** Step 1 abgeschlossen, Loet- und Lackier-Werkzeug, getestete Elektronik-Komponenten; Begriffe siehe `Documentation/Guides/Glossar.md`

## Voraussetzung

- Helm-Shell ist fertig (Step 1 abgeschlossen)
- Oberflaeche geschliffen und grundiert
- Visor eingepasst (aber noch herausnehmbar)
- Innenpolsterung vorhanden

## 1. Elektronik einbauen

### OLED-Display montieren

1. **Position:** Vor dem dominanten Auge, 3-5 cm Abstand
2. 3D-gedruckte Halterung einkleben oder mit Klett befestigen
3. Winkel so einstellen, dass das Display klar lesbar ist ohne den Blick zu blockieren
4. Optional: kleine Fresnel-Linse fuer besseren Fokus

### Raspberry Pi montieren

1. **Position:** Nackenbereich (innen oben hinten)
2. Pi mit Klett oder 3D-gedruckter Klammer befestigen
3. PiSugar 3 Plus direkt auf Pi montieren (Pogo-Pins)
4. **Kabelverbindung zum OLED:**
   - VCC -> 3.3V
   - GND -> GND
   - SDA -> GPIO 2 (Pin 3)
   - SCL -> GPIO 3 (Pin 5)
5. Kabel sauber mit Klett-Kabelhaltern fuehren

### Luefter einbauen

1. **Intake-Luefter:** unterer Hinterkopf/Kieferbereich — zieht kuehle Luft rein
2. **Exhaust-Luefter:** oberer Hinterkopf — drueckt heisse Luft raus
3. Mit Klett befestigen (fuer einfaches Entfernen/Reinigen)
4. Kabel zum Arduino oder direkt an Stromschiene
5. **Luftstrom testen:** Hand vor die Luefter halten, Richtung pruefen

### Visor-LEDs (optional)

- 6-10 WS2812B LEDs als Visor-Akzentbeleuchtung
- Entlang der oberen oder unteren Visor-Kante platzieren
- 330 Ohm Widerstand auf der Datenleitung
- Datenleitung zum Arduino

### Quick-Disconnect am Nacken

- **JST-XH 4-Pin** fuer I2C/Signal (VCC, GND, SDA, SCL)
- **XT30** fuer Power (5V, GND)
- Am Hals-/Nackenuebergang platzieren
- Erlaubt Helm abzunehmen ohne Kabel zu trennen/beschaedigen

## 2. Elektronik-Test (VOR der Lackierung!)

Alle Tests ausserhalb des Helms auf dem Tisch, DANN im Helm:

- [ ] Pi bootet sauber und HUD startet automatisch (systemd Service)
- [ ] OLED zeigt HUD an (i2cdetect zeigt 0x3C)
- [ ] Luefter drehen in richtiger Richtung (Intake rein, Exhaust raus)
- [ ] LEDs leuchten im gewuenschten Muster
- [ ] Laufzeittest: mindestens 2 Stunden am Stueck
- [ ] Temperatur im Helm messen (mit und ohne Luefter — Differenz sollte deutlich sein)
- [ ] Alles funktioniert auch bei Bewegung (Kopf drehen, nicken, buecken)

**WICHTIG:** Elektronik vor dem Lackieren komplett testen! Nach der Lackierung ist Zugang viel schwieriger.

## 3. Lackierung

Visor und Elektronik VOR dem Lackieren entfernen oder sorgfaeltig abkleben!

### Vorbereitung

1. Alle Elektronik-Komponenten ausbauen (Klett macht das einfach)
2. Visor herausnehmen
3. Oeffnungen (Visor, Luefter-Loecher) mit Malerkrepp abkleben
4. In gut belueftetem Bereich arbeiten (draussen oder mit Absaugung)

### Lackierschritte

1. **Grundfarbe:** Rust-Oleum Oregano Satin — 3-4 duenne Schichten, je 15-20 Min trocknen lassen
2. **Sekundaerfarben:** Schwarze Bereiche (Unterkiefer, Nacken-Spalte, Lueftungsschlitze) mit Matt-Schwarz
3. **Detail:** Gunmetal/Silber fuer technische Details
4. **Trocknen:** mindestens 24-48 Stunden vor Weathering

### Weathering

1. **Schwarze Wash:** verduennte schwarze Acrylfarbe (10:1 Wasser) in alle Vertiefungen — abwischen
2. **Dry Brushing:** Schwarz auf Kanten, dann Silber/Gunmetal auf Ecken und Hochpunkte
3. **Battle Damage:** Metallic Pen oder Rub 'n Buff an logischen Aufprallstellen
4. **Trocknen:** 24 Stunden

### Versiegelung

- **Rust-Oleum Matte Clear Coat** — 3-4 duenne Schichten
- Matte Oberflaeche ist entscheidend (Glanz = Spielzeug-Look)
- 48 Stunden durchtrocknen lassen

## 4. Endmontage

1. Malerkrepp entfernen
2. Elektronik wieder einbauen (Klett-Halterungen)
3. Visor einsetzen und mit Clips sichern
4. Alle Kabelverbindungen pruefen
5. Quick-Disconnect am Nacken anschliessen
6. Finaler Funktionstest

## 5. Abschluss-Checks

- [ ] HUD funktioniert im fertigen Helm
- [ ] Luefter laufen, Temperatur ist ertraeglich
- [ ] Visor klar, nicht beschlagen, Sicht ausreichend
- [ ] Lack/Weathering sieht gleichmaessig aus
- [ ] Quick-Disconnect funktioniert (Helm abnehmen/aufsetzen)
- [ ] Polsterung sitzt bequem
- [ ] Kinnriemen haelt
- [ ] Notausstieg: Helm kann in unter 10 Sekunden abgenommen werden
- [ ] 30-Minuten Tragetest bestanden
