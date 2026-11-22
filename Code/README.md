# Code

Dieses Verzeichnis enthaelt Beispielcode fuer Helm- und Ruestungs-LEDs sowie das HUD.

## HelmetControl

### HUD (Python, Raspberry Pi Zero 2 W)

- `hud_display.py` - Animiertes Halo-HUD fuer transparentes OLED (SSD1309):
  Boot-Sequenz, Schild mit Recharge, Scroll-Kompass, Motion-Tracker, Ammo,
  Akku-Warnung. Hardwarefreier Test: `python3 hud_display.py --selftest hud_test.png`
- `helmet_control.py` - **Pi-Steuerung des Helm-Arduinos** per I2C (Gegenstueck zu
  `HelmetMultiEffects.ino`): `brightness 128`, `fan 180`, `effect heartbeat`, `demo`.
  Luefterwerte unter 180 gelten nur mit `--hold` dauerhaft (Failsafe, siehe
  `Documentation/Guides/Elektronik-Luefter.md`)
- `sensor_bridge.py` - **Bruecke** SensorFeeder (ESP32, Serial-JSON) ->
  `hud_state.json` + `battery.json`, damit Kompass und Akku live sind. Laeuft
  parallel zum HUD. Test ohne Hardware: `python3 sensor_bridge.py --selftest`
- `robot_bridge.py` - **Konzept-Bruecke** Begleit-Roboter (WLAN/UDP) ->
  `hud_state.json`, zeigt den Robo als Marker auf dem Motion-Tracker. Siehe
  [Begleitguide](../Documentation/Guides/Begleitroboter-Integration.md).
  Nur Anzeige, keine Bewegungssteuerung; Schreibzugriff gesperrt ueber
  `hud_state.py`, Datenalter bei Prozessausfall noch offen. Test:
  `python3 robot_bridge.py --selftest`
- `voice_control.py` - **Sprachsteuerung + Helmfunk (Pi 5, optional)**: Push-to-Talk,
  Offline-Erkennung (Vosk), Befehle an Helm-Arduino (I2C) und per Optokoppler an
  Schubduesen-/Ruestungs-Taster, Helmfunk-Stimme (Audio Option C).
  Test: `python3 voice_control.py --selftest`, Tippen statt Sprechen: `--keyboard`
- `vision_bridge.py` - **Bruecke** Raspberry Pi AI Camera (IMX500) -> `hud_state.json`,
  echte Kontakte auf dem Bewegungsmelder. Test: `python3 vision_bridge.py --selftest`
- `hud_state.py` - gemeinsamer, gesperrter Schreibzugriff auf `hud_state.json` fuer
  alle Bruecken (verhindert, dass sie sich gegenseitig Werte ueberschreiben).
  Mit der Umgebungsvariable `HUD_STATE_DIR` (z.B. `/run/halo-hud`) liegen
  `hud_state.json` und `battery.json` fuer HUD und Bruecken gemeinsam auf einem
  tmpfs statt auf der SD-Karte (siehe `Elektronik-Autostart.md`)
- `voice_config.example.json` / `requirements-voice.txt` - Konfiguration und
  Zusatz-Dependencies der Sprachsteuerung. Anleitung:
  `Documentation/Guides/Elektronik-Sprachsteuerung.md`
- `requirements.txt` - Python-Dependencies (`pip install -r requirements.txt`)
- `config.example.json` - Beispiel-Konfiguration (als `config.json` kopieren).
  Eine kaputte `config.json` stoppt das HUD nicht: Standardwerte + Hinweis `CFG?`
  `refresh_ms` ist die Bildperiode (Render- und I2C-Zeit eingerechnet). Mit
  `log_path` wird das Log ab `log_max_kb` (Standard 512) nach `<name>.1` verschoben
- `battery.example.json` - Beispiel fuer Batteriestatus-Datei. Wird die Datei
  laenger als `battery_max_age_s` (Standard 30 s) nicht aktualisiert, zeigt das
  HUD `AKKU ?` statt des letzten Werts; `0` schaltet die Pruefung ab (nur fuer
  eine bewusst von Hand gepflegte Datei). `AKKU!`/`AKKU ?` erscheinen auch ohne
  `show_battery`
- `hud_state.example.json` - Beispiel fuer Live-Werte (Schild/Ammo/Heading), die
  andere Module dem HUD entkoppelt ueber eine JSON-Datei zuspielen koennen

### AR-Passthrough (V3, Python, Raspberry Pi 4/5)

Im Unterordner `HelmetControl/AR/` (eigene `README.md` dort):

- `ar_passthrough.py` - Voll-AR-Pipeline: Kamera -> HUD-Overlay -> Display, mit
  Failsafe (Watchdog/Latenz-Warnung/Akku-Warnung) und Latenzmessung
- `hud_overlay.py` - Halo-HUD-Zeichenmodul (Schild, Kompass, Bewegungsmelder,
  Munition, Status, Warnbanner), hardwarefrei testbar
- `hud_main.py` - Einfaches Starter-AR-Kamerasystem mit Ziel-Simulation und HUD (OpenCV).
  Nur Demo/Einstieg - fuer den echten Helm-Einsatz `ar_passthrough.py` verwenden
- `ar_config.example.json` - Konfiguration (als `ar_config.json` kopieren)
- `requirements.txt` - OpenCV, numpy, pyserial (picamera2 via apt)
- `SensorFeeder/SensorFeeder.ino` - ESP32: IMU + Akku -> JSON ueber Serial

Hardwarefreier Test: `python3 ar_passthrough.py --selftest hud_test.png`;
nur Watchdog-/Sensorlogik ohne OpenCV: `python3 ar_passthrough.py --selftest-logic`.
Hintergrund und **Sicherheit**: `Documentation/Guides/Elektronik-AR-Display.md`.

### Arduino (Helm)

- `MainControlCode.ino` - I2C-Slave (Adresse 0x08), versteht `[cmd, wert]` wie
  HelmetMultiEffects, setzt aber nur die Helligkeit (0x01) um
- `LightingEffectsCode.ino` - Einfacher LED-Lauf (12 LEDs, Pin 6)
- **`HelmetMultiEffects.ino`** - Erweiterter Controller mit:
  - 5 Visor-LED-Effekte (Static, Breathing, Heartbeat, Chase, Flicker), 10 LEDs an Pin 6 (`VISOR_COUNT` anpassen)
  - Taster-Umschaltung zwischen Effekten
  - I2C-Kommandos vom Pi (Helligkeit, Luefter-Speed, Effekt-Wahl, Farbe `0x04 R G B`)
  - Luefter-PWM Steuerung (31 kHz, kein hoerbares Pfeifen) mit Failsafe:
    gedrosselte Werte verfallen nach 10 s ohne I2C-Lebenszeichen
  - Boot-Sequence beim Einschalten

## ArmorControl

- `MainControlCode.ino` - LED-Breathing (24 LEDs, Pin 5)
- `LightingEffectsCode.ino` - LED-Chase (24 LEDs, Pin 5)
- **`MultiEffects.ino`** - Erweiterter Controller mit:
  - 5 Effekte (Static, Breathing, Heartbeat, Chase, Flicker)
  - Taster-Umschaltung (Pin 2)
  - Boot-Sequence beim Einschalten
  - Konfigurierbarer Farbe und Helligkeit
  - Handler-Alarm (Pin 3, 1 s halten) mit Buzzer (Pin 9)
  - Shield-Hit ueber 4 TP223-Sensoren, nur mit `TOUCH_ENABLED 1` (Standard 0,
    weil offene Sensor-Pins zufaellige Treffer ausloesen)

## WeaponControl

- **`ammo_counter.ino`** - Arduino-Steuerung fuer den Munitionszaehler (MA40/MA5):
  - Libraries: Adafruit GFX, Adafruit SSD1306, JC_Button (alle im Library Manager)
  - OLED-Anzeige (SSD1306/SH1107 via I2C)
  - Schusszaehlung ueber Taster/Mikroschalter (Pin 2)
  - Magazinwechsel ueber Taster/Hall-Effekt-Sensor (Pin 4)
  - Magazingroessen-Auswahl (Pin 5)

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
| 2 | Taster (Effekt-Wechsel) | Gegen GND, interner Pull-Up; auch Optokoppler vom Pi |
| 3 | Alert-Taster (Handler-Alarm) | Gegen GND, interner Pull-Up; 1 s halten |
| 4 | TP223 Brust | HIGH bei Beruehrung; nur mit `TOUCH_ENABLED 1` |
| 6 | TP223 Ruecken | wie Pin 4 |
| 7 | TP223 Schulter links | wie Pin 4 |
| 8 | TP223 Schulter rechts | wie Pin 4 |
| 9 | Buzzer | Passiver Piezo, Plus-Seite ueber 100 Ohm |

Nicht bestueckte TP223-Pins brauchen 10 kOhm nach GND, bevor `TOUCH_ENABLED`
auf 1 gesetzt wird.

### Waffen-Arduino (ammo_counter.ino)

| Pin | Funktion | Hinweis |
| --- | --- | --- |
| 2 | Trigger Button | Mikroschalter am Abzug (Gegen GND) |
| 4 | Reload Button | Sensor im Magazinschacht (Gegen GND) |
| 5 | Mag Size Toggle | Taster zur Auswahl der Magazingroesse |
| A4 | I2C SDA | Zum OLED Display SDA |
| A5 | I2C SCL | Zum OLED Display SCL |

## I2C-Adressen (Uebersicht)

Helm und Waffe haben **getrennte** I2C-Busse - die doppelte Adresse 0x3C ist daher kein Konflikt:

| Bus | Geraet | Adresse |
| --- | --- | --- |
| Helm (Pi Zero, Bus 1) | Transparentes OLED (SSD1309) | 0x3C |
| Helm (Pi Zero, Bus 1) | Arduino Nano (HelmetMultiEffects, Slave) | 0x08 |
| Waffe (eigener Arduino) | OLED Munitionszaehler (SSD1306) | 0x3C |

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
