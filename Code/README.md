# Code

Dieses Verzeichnis enthaelt Beispielcode fuer Helm- und Ruestungs-LEDs sowie das HUD.

## HelmetControl

### HUD (Python, Raspberry Pi Zero 2 W)

- `hud_display.py` — HUD-Demo-Loop fuer transparentes OLED (SSD1309)
- `requirements.txt` — Python-Dependencies (`pip install -r requirements.txt`)
- `config.example.json` — Beispiel-Konfiguration (als `config.json` kopieren)
- `battery.example.json` — Beispiel fuer Batteriestatus-Datei

### AR-Passthrough (V3, Python, Raspberry Pi 4/5)

Im Unterordner `HelmetControl/AR/` (eigene `README.md` dort):

- `ar_passthrough.py` — Voll-AR-Pipeline: Kamera -> HUD-Overlay -> Display, mit
  Failsafe (Watchdog/Latenz-Warnung/Akku-Warnung) und Latenzmessung
- `hud_overlay.py` — Halo-HUD-Zeichenmodul (Schild, Kompass, Bewegungsmelder,
  Munition, Status, Warnbanner), hardwarefrei testbar
- `ar_config.example.json` — Konfiguration (als `ar_config.json` kopieren)
- `requirements.txt` — OpenCV, numpy, pyserial (picamera2 via apt)
- `SensorFeeder/SensorFeeder.ino` — ESP32: IMU + Akku -> JSON ueber Serial

Hardwarefreier Test: `python3 ar_passthrough.py --selftest hud_test.png`.
Hintergrund und **Sicherheit**: `Documentation/Guides/Elektronik-AR-Display.md`.

### Arduino (Helm)

- `MainControlCode.ino` — I2C-Slave, empfaengt Helligkeit vom Pi (Adresse 0x08)
- `LightingEffectsCode.ino` — Einfacher LED-Lauf (12 LEDs, Pin 6)
- **`HelmetMultiEffects.ino`** — Erweiterter Controller mit:
  - 5 Visor-LED-Effekte (Static, Breathing, Heartbeat, Chase, Flicker)
  - Taster-Umschaltung zwischen Effekten
  - I2C-Kommandos vom Pi (Helligkeit, Luefter-Speed, Effekt-Wahl)
  - Luefter-PWM Steuerung
  - Boot-Sequence beim Einschalten

## ArmorControl

- `MainControlCode.ino` — LED-Breathing (24 LEDs, Pin 5)
- `LightingEffectsCode.ino` — LED-Chase (24 LEDs, Pin 5)
- **`MultiEffects.ino`** — Erweiterter Controller mit:
  - 5 Effekte (Static, Breathing, Heartbeat, Chase, Flicker)
  - Taster-Umschaltung (Pin 2)
  - Boot-Sequence beim Einschalten
  - Konfigurierbarer Farbe und Helligkeit

## Pin-Belegung (Uebersicht)

### Helm-Arduino (HelmetMultiEffects.ino)

| Pin | Funktion | Hinweis |
| --- | --- | --- |
| 6 | Visor LED Data | WS2812B, ueber 330 Ohm Widerstand |
| 2 | Taster (Effekt-Wechsel) | Gegen GND, interner Pull-Up |
| 9 | Luefter PWM | 5V Luefter ueber MOSFET |
| A4 | I2C SDA | Zum Pi (Slave Adresse 0x08) |
| A5 | I2C SCL | Zum Pi |

### Ruestungs-Arduino (MultiEffects.ino)

| Pin | Funktion | Hinweis |
| --- | --- | --- |
| 5 | LED Strip Data | WS2812B, ueber 330 Ohm Widerstand |
| 2 | Taster (Effekt-Wechsel) | Gegen GND, interner Pull-Up |

## Anpassung

- `LED_COUNT` in jedem Sketch auf die eigene LED-Anzahl setzen
- `LED_PIN` auf den tatsaechlichen Daten-Pin anpassen
- Farbe ueber `COLOR_R/G/B` oder `VIS_R/G/B` Defines aendern
- Helligkeit ueber `BRIGHTNESS` Define (0-255, 128 = 50%)

## Weitere Guides

- LED-Effekte Erklaerung: `Documentation/Guides/LED-Effekte.md`
- Elektronik-Uebersicht: `Documentation/Guides/Elektronik-HUD.md`
- AR-Display (V3, Passthrough): `Documentation/Guides/Elektronik-AR-Display.md`
- Verdrahtung: `Documentation/Guides/Elektronik-Verdrahtung.md`
- Pi-Autostart: `Documentation/Guides/Elektronik-Autostart.md`
