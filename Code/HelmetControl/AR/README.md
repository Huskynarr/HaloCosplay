# AR-Passthrough (V3) - Beispielcode

Lauffaehiges Beispiel fuer **Stufe C** (Voll-AR mit Kamera-Passthrough) aus
`Documentation/Guides/Elektronik-AR-Display.md`. Kamera -> HUD-Overlay -> Display,
mit Sicherheits-Failsafe. Gedacht fuer Raspberry Pi 4/5 oder Jetson.

> **SICHERHEIT zuerst.** Passthrough ersetzt die direkte Sicht. Ein Ausfall ist
> kein Bug, sondern Blindheit in der Bewegung. Mechanischer Notausblick
> (hochklappbarer/absetzbarer Visor in Sekunden, ohne Werkzeug) und ein Handler
> sind **Pflicht**. Nicht auf Treppen/in Menschenmengen mit aktivem Passthrough.
> Vollstaendige Regeln: `Documentation/Guides/Elektronik-AR-Display.md` Abschnitt 3
> und `Documentation/Guides/Sicherheit.md`.

## Dateien

- `ar_passthrough.py` - Hauptprogramm (Kamera, Pipeline, Failsafe, Latenzmessung)
- `hud_overlay.py` - HUD-Zeichenmodul (Schild, Kompass, Bewegungsmelder, Munition,
  Status, Warnbanner). Nur numpy + OpenCV, hardwarefrei testbar.
- `ar_config.example.json` - Beispiel-Konfiguration (als `ar_config.json` kopieren)
- `requirements.txt` - Python-Dependencies
- `SensorFeeder/SensorFeeder.ino` - ESP32-Sketch: IMU + Akku -> JSON ueber Serial

## Installation (Raspberry Pi)

```bash
sudo apt update
sudo apt install -y python3-picamera2          # CSI-Kamera (empfohlen)
python3 -m pip install -r requirements.txt      # OpenCV, numpy, pyserial
cp ar_config.example.json ar_config.json        # und anpassen
```

Ohne CSI-Kamera/picamera2 nutzt das Programm automatisch eine USB-Webcam
(OpenCV). Backend erzwingen ueber `camera_backend` in der Config
(`auto` | `picamera2` | `opencv`).

## Starten

```bash
python3 ar_passthrough.py            # normaler Betrieb, ESC oder q beendet
```

### Hardwarefreier Selbsttest

Rendert das HUD auf ein synthetisches Bild - ohne Kamera, ohne Display:

```bash
python3 ar_passthrough.py --selftest hud_test.png
```

So prueft man Overlay und Lesbarkeit am Schreibtisch, bevor Hardware dranhaengt.

## Failsafe-Verhalten

- **Kein frischer Frame** laenger als `frame_timeout_ms`: roter Banner
  "SICHT PRUEFEN - VISOR HOCH". Das Bild wird nie kommentarlos schwarz.
- **Latenz ueber `latency_limit_ms`** (gleitender Mittelwert): gelbe Warnung
  "LATENZ HOCH". Latenz/FPS stehen dauerhaft unten links - das ist der
  Pflicht-Latenztest vor jedem Einsatz.
- **Akku unter `low_battery_percent`** (vom Sensor-Feeder): Banner
  "AKKU SCHWACH - VISOR HOCH".

## Sensor-Feeder (optional, empfohlen)

`SensorFeeder/SensorFeeder.ino` laeuft auf einem **eigenen** ESP32 und schickt
ueber USB/Serial JSON-Zeilen wie `{"heading":123,"battery":78,"temp":41}`.
In `ar_config.json` `sensor_serial_port` setzen (z.B. `/dev/ttyUSB0`).

Bewusst getrennter Controller: Akkuanzeige, Heading und (in deiner Erweiterung)
Luefter laufen unabhaengig vom Grafik-Rechner weiter, wenn der Pi abstuerzt.

## Autostart

Wie beim HUD per systemd starten - siehe
`Documentation/Guides/Elektronik-Autostart.md`. Fuer Passthrough zusaetzlich
einen Watchdog-Service erwaegen, der bei Absturz neu startet (aber: ein Neustart
dauert -> der mechanische Notausblick bleibt die eigentliche Absicherung).

## Anpassen

- Aufloesung/FPS: `width`, `height`, `target_fps` (mehr = mehr Latenz/Hitze)
- Kamera spiegeln: `flip_horizontal`, `flip_vertical`
- HUD-Farbe/Elemente: in `hud_overlay.py` (`HUD_GREEN`, Zeichenfunktionen)
- Schwellen fuer die Warnungen: `latency_limit_ms`, `frame_timeout_ms`,
  `low_battery_percent`
