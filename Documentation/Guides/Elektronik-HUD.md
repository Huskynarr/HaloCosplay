# Elektronik und HUD

> **Level:** [F] Fortgeschritten | [P] Profi  |  **Varianten:** V2/V3
> **Voraussetzungen:** Strombudget gerechnet (`Documentation/Guides/Elektronik-Strombudget.md`), Loetkenntnisse, Grundlagen Raspberry Pi/I2C.

Ziel ist ein tragbares, modulares HUD-System mit sicherer Stromversorgung. Die Basis ist ein Raspberry Pi Zero 2 W mit transparentem OLED-Display. Eine guenstige Alternative ist ein einfarbiges, gruener LED-HUD ohne AR-Funktionen.

## Display-Auswahl: vom Retro-OLED bis AR-Brille

Die Auswahl des HUD-Displays entscheidet, wie viel "Cortana" am Ende moeglich
ist. Vier Stufen, aufsteigend nach Preis und Moeglichkeiten:

| Stufe | Display | Preis ca. | Farbe/Aufloesung | Wofuer |
| --- | --- | --- | --- | --- |
| A | Transparentes OLED 1,51" (SSD1309, 128x64, SPI) | 20-30 EUR | einfarbig blau/weiss | Kompass, Pfeile, Munition, Radar-Punkte, Textzeilen |
| A+ | Transparentes OLED 0,71" (128x40) | 10-15 EUR | einfarbig | Minimal-HUD, wenn Platz knapp ist |
| B | Micro-OLED-Modul (0,39"/0,6", 1080p) + Halbspiegel vor dem Auge | 100-200 EUR | Farbe, volle Aufloesung | Echte schwebende Einblendungen, viel Bastelaufwand |
| C | AR-Display-Brille (Birdbath, Micro-OLED) im Helm | 270-600 EUR | Farbe, 1080p, 50-57 Grad FOV | Vollwertiges HUD inkl. Cortana-Einblendungen |

### Stufe A: Transparentes OLED (Repo-Baseline)

Das 1,51"-Modul (Waveshare, SSD1309) ist die Basis von `hud_display.py` - keine
Software-Arbeit noetig. AliExpress-Klone kosten ca. 6-10 EUR. Wichtig:

- Einfarbig reicht fuer das Halo-Gefuehl: Das Spiel-HUD ist selbst minimal
  (Kompass, Schild/Munition, Pfeile). Blau = Halo/Cortana-Look, Gruen = Military-
  Retro (Fallout-Stil), Amber = warm und gut lesbar. Alles drei lieferbar.
- **Kein Cortana-Portraet, keine Grafik** - 128x64 Pixel sind ein Text-/Icon-HUD.
- Schaerfe: Display wenige Zentimeter vor dem Auge braucht eine Lupe (+8 bis
  +10 dpt) oder den Spiegel-Trick (`HUD_MIRROR`, schraege Plexiglasscheibe).
- Der getoente Gold-Visor hilft hier sogar: dunkler Hintergrund = mehr Kontrast.

### Stufe C: AR-Display-Brillen im Helm (2026-Stand)

Display-Brillen (Birdbath-Optik, Sony Micro-OLED) sind heute die praktischste
"richtige HUD"-Loesung und passen - leicht demontiert - gut in Helme:

| Modell | Preis ca. | Panel | Bemerkung |
| --- | --- | --- | --- |
| RayNeo Air 3s | 270-300 EUR | 1080p, 650 Nits | Budget-Einstieg |
| XREAL One | 400-500 EUR | 1080p, 600 Nits | X1-Chip, elektrochromische Abdunklung |
| Rokid Max 2 | 400-450 EUR | 1200p, 600 Nits | schaerfstes Panel in der Klasse |
| XREAL One Pro / VITURE Beast | 550-650 EUR | 1200p, 700-1250 Nits | hellste Panels, 57-58 Grad FOV |

Vorteile: Vollfarbe (Cortana-Einblendungen, echte Grafik), scharf, Helligkeit
reicht gegen das Umgebungslicht, Modelle mit elektrochromischer Abdunklung
(XREAL 1S/One/One Pro) koennen die Sicht abdunkeln - ideal hinter Visor.

Haken und Loesungen:

- **Eingang ist USB-C DisplayPort, nicht HDMI.** Der Pi 5 hat keinen DP-Alt-Mode
  am USB-C-Port - Loesung: micro-HDMI auf USB-C-DP-Wandler (aktiv, ca. 25-40 EUR)
  oder der Pi rendert das HUD als Video-Signal. Latenz ist mit gutem Wandler
  unkritisch (<1 Frame).
- **Strom:** Die Brille zieht Strom vom Quellgeraet - Wandlung + Brille mit ca.
  2-4 W einplanen (Strombudget oben erweitern).
- **Hitze/Gewicht:** 75-90 g, passiv gekuehlt - im Helm gut machbar, aber
  Helmluefter nicht sparen.
- **Einbau:** Buegel demontieren, Brillenkorpus vor dem dominanten Auge fixieren.
  Passt nicht in jeden Helm - vor dem Kauf Schablone aus Karton testen.

### Empfehlung nach Budget

- **Bis 30 EUR / Retro-Look:** 1,51" transparentes OLED in Blau. Passt zum
  Repo-Code, null Zusatzsoftware, authentisch minimalistisch.
- **"Was Gutes":** XREAL One oder Rokid Max 2 im Helm + HDMI-DP-Wandler. Erst
  damit werden Navigation in echt, Cortana-Einblendungen und Farb-Grafik moeglich.
  Die Stufe-A-OLED bleibt als Fallback eingebaut, falls die Brille auf der Con
  zickt (beide an den Pi, Umschalter im Code).

## Kernkomponenten

- Raspberry Pi Zero 2 W
- Transparentes OLED 1.51" (I2C/SPI, 128x64)
- PiSugar 3 Plus (5000 mAh) oder 5V/3A UPS
- Optional: Arduino Nano fuer LEDs/Luefter
- 40 mm Luefter (Helm), LED-Strips, Audio

## Systemdiagramm (Uebersicht)

```
+---------------------+
|   PiSugar 3 Plus    |
|     5000mAh         |
+----------+----------+
           | 5V/3A
           v
+---------------------+      I2C        +------------------+
|  Raspberry Pi       |<-------------> |  Transparent     |
|    Zero 2 W         |                |  OLED Display    |
+----------+----------+                +------------------+
           |
           | I2C/Serial
           v
+---------------------+
|  Arduino Nano       |
|  (optional)         |
+----------+----------+
           |
           +--> LED Strips
           +--> Helmet Fans
           +--> Audio Amp
```

## Verkabelung (OLED via I2C)

- VCC -> 3.3V
- GND -> GND
- SDA -> GPIO 2 (Pin 3)
- SCL -> GPIO 3 (Pin 5)

Test: `i2cdetect -y 1` (Adresse meist 0x3C/0x3D)

## Stromversorgung

- PiSugar 3 Plus direkt auf den Pi montieren
- Optionaler Backup-LiPo parallel (nur mit Schutzschaltung)
- Akku im Backpack montieren, Kabelkanal im Under-Suit
- Laden immer ausserhalb des Kostuems

## Montage im Helm

- OLED vor dem dominanten Auge, 3-5 cm Abstand mit Linse/Prisma
- Pi im Nackenbereich oder rueckwaerts im Helm
- Zwei Luefter fuer Belueftung
- Kabel sauber mit Klett/Spiralschlauch sichern

## Software

- Raspberry Pi OS Lite
- Python + luma.oled
- Beispiel: `Code/HelmetControl/hud_display.py`
- Dependencies: `Code/HelmetControl/requirements.txt`
- Konfig: `Code/HelmetControl/config.example.json` (als `config.json` kopieren)
- Batterie-Input: `Code/HelmetControl/battery.example.json`
- Live-Werte (Schild/Ammo/Heading): `Code/HelmetControl/hud_state.example.json`
  (als `hud_state.json` kopieren; andere Module schreiben hier rein)
- Arduino: `Code/HelmetControl/HelmetMultiEffects.ino` (empfohlen: Effekte, Luefter-PWM, I2C);
  `MainControlCode.ino` ist die Minimal-Variante (nur Helligkeit)
- Pi-Steuerung des Arduinos: `Code/HelmetControl/helmet_control.py`
  (z.B. `python3 helmet_control.py effect heartbeat`, `fan 180`)
- HUD ohne Hardware testen: `python3 hud_display.py --selftest hud_test.png`

## Weitere Guides

- Code-Uebersicht und Pin-Belegung: `Code/README.md`
- Strombudget: `Documentation/Guides/Elektronik-Strombudget.md`
- Verdrahtung: `Documentation/Guides/Elektronik-Verdrahtung.md`
- V3-Gesamtsystem (Module, Stromschienen): `Documentation/Guides/V3-Systemarchitektur.md`

## HUD-Erweiterungen (optional)

- Batterieanzeige aus Datei (siehe `battery.example.json`)
- Logging zu `hud_log.txt` (konfigurierbar)

## Guenstige HUD-Alternative

- Einfarbiger LED-Frame im Visor (gruener Akzent)
- Kein transparentes Display, nur optische Effekte
- Deutlich leichter, weniger Strom, schneller umzusetzen
