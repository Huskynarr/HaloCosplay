# Elektronik: Pi Zero 2 W Einrichtung und Autostart

> **Level:** [F] Fortgeschritten | [P] Profi  |  **Varianten:** V2/V3
> **Voraussetzungen:** Raspberry Pi Zero 2 W mit microSD, OLED verkabelt (`Documentation/Guides/Elektronik-HUD.md`), Grundlagen Linux-Kommandozeile (SSH, systemd = Linux-Dienstverwaltung fuer Autostart).

Schritt-fuer-Schritt Anleitung zur Einrichtung des Raspberry Pi Zero 2 W fuer das Helm-HUD.

## 1. OS flashen

1. **Raspberry Pi Imager** herunterladen und installieren
2. **Raspberry Pi OS Lite** (ohne Desktop) auswaehlen
3. In Imager-Einstellungen vorab konfigurieren:
   - WiFi-Zugangsdaten (fuer initiales Setup)
   - SSH aktivieren
   - Benutzername und Passwort setzen
4. Auf microSD flashen und in Pi einsetzen

## 2. Erste Verbindung

```bash
# Per SSH verbinden (Pi muss im gleichen Netzwerk sein)
ssh pi@raspberrypi.local
```

## 3. I2C aktivieren

```bash
sudo raspi-config
# Interface Options > I2C > Enable
```

Test:
```bash
sudo apt install -y i2c-tools
i2cdetect -y 1
# Sollte 0x3C oder 0x3D anzeigen wenn OLED angeschlossen
```

## 4. Dependencies installieren

```bash
sudo apt update && sudo apt install -y python3-pip python3-pil
pip3 install luma.oled
```

## 5. HUD-Software testen

Das Repository liegt in dieser Anleitung unter `/home/pi/HaloCosplay`. HUD und
alle Bruecken laufen aus demselben Verzeichnis `Code/HelmetControl`, damit sie
dieselbe `hud_state.json` verwenden.

```bash
cd /home/pi/HaloCosplay/Code/HelmetControl

# config.json erstellen
cp config.example.json config.json

# HUD starten
python3 hud_display.py
```

Konfig anpassen in `config.json` (siehe `config.example.json` fuer alle Optionen).

## 6. Autostart als systemd Service

Erstelle `/etc/systemd/system/hud.service`:

```ini
[Unit]
Description=Halo HUD Display
After=multi-user.target

[Service]
Type=idle
User=pi
WorkingDirectory=/home/pi/HaloCosplay/Code/HelmetControl
Environment=HUD_STATE_DIR=/run/halo-hud
ExecStart=/usr/bin/python3 -u /home/pi/HaloCosplay/Code/HelmetControl/hud_display.py
Restart=on-failure
RestartSec=5
StandardOutput=append:/var/log/hud.log
StandardError=inherit

[Install]
WantedBy=multi-user.target
```

### Laufzeitdateien auf tmpfs

Die Bruecken schreiben `hud_state.json` und `battery.json` 10-15 mal pro
Sekunde. Auf der SD-Karte kostet das Lebensdauer. `HUD_STATE_DIR` legt beide
Dateien fuer HUD und Bruecken in ein gemeinsames Verzeichnis; `/run` ist ein
tmpfs im Arbeitsspeicher. Das Verzeichnis beim Booten anlegen lassen, Datei
`/etc/tmpfiles.d/halo-hud.conf`:

```
d /run/halo-hud 0755 pi pi -
```

Einmalig sofort anlegen: `sudo systemd-tmpfiles --create /etc/tmpfiles.d/halo-hud.conf`.
Die Werte sind nach einem Neustart weg; das ist gewollt, weil alte Live-Werte
nach dem Booten falsch waeren. Ohne `HUD_STATE_DIR` liegen die Dateien wie
bisher neben den Skripten. Alle Dienste muessen denselben Wert verwenden.

### Sensor-Bruecke (optional, mit SensorFeeder)

Ohne diesen Dienst bleiben Kompass und Akkuanzeige in der Demo bzw. zeigen
nach 30 s `AKKU ?`. Erstelle `/etc/systemd/system/hud-sensors.service`
(seriellen Port anpassen):

```ini
[Unit]
Description=Halo HUD Sensor Bridge
After=multi-user.target

[Service]
User=pi
WorkingDirectory=/home/pi/HaloCosplay/Code/HelmetControl
Environment=HUD_STATE_DIR=/run/halo-hud
ExecStart=/usr/bin/python3 -u /home/pi/HaloCosplay/Code/HelmetControl/sensor_bridge.py --port /dev/ttyUSB0
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

Weitere Bruecken (`robot_bridge.py`, `vision_bridge.py`, `voice_control.py`)
bekommen bei Bedarf eigene Units nach demselben Muster: gleiches
`WorkingDirectory`, gleiches `HUD_STATE_DIR`.

Aktivieren:
```bash
sudo systemctl daemon-reload
sudo systemctl enable hud.service hud-sensors.service
sudo systemctl start hud.service hud-sensors.service
```

**Hinweise:**
- `-u` Flag deaktiviert Output-Buffering fuer korrektes Logging
- `Type=idle` wartet bis alle anderen Boot-Services fertig sind
- `Restart=on-failure` startet bei Absturz automatisch neu
- Das HUD faengt Einzelfehler selbst ab: ein kaputter Wert in `hud_state.json`
  oder ein kurzer I2C-Aussetzer kostet einen Frame, nicht den Prozess. Eine
  kaputte `config.json` fuehrt zu Standardwerten und dem Hinweis `CFG?`.

## 7. Stromspar-Optimierungen

In `/boot/config.txt` hinzufuegen:

```
# HDMI deaktivieren (spart ~25 mA)
hdmi_blanking=2

# Bluetooth deaktivieren (spart ~30 mA)
dtoverlay=disable-bt

# GPU-Speicher reduzieren (kein Desktop noetig)
gpu_mem=16
```

Unnoetige Dienste deaktivieren:
```bash
sudo systemctl disable bluetooth
sudo systemctl disable avahi-daemon
sudo systemctl disable triggerhappy
```

Optional WiFi deaktivieren (wenn nach Setup nicht mehr gebraucht):
```bash
# In /boot/config.txt
dtoverlay=disable-wifi
```

## 8. Stromverbrauch nach Optimierung

| Zustand | Strom ca. |
| --- | --- |
| Idle (WiFi aus, HDMI aus) | ~120 mA |
| Idle (WiFi an) | ~170 mA |
| HUD-Betrieb (typisch) | ~200-400 mA |
| Volllast | ~600-1000 mA |

## 9. Nuetzliche Befehle

```bash
# Service-Status pruefen
sudo systemctl status hud.service

# Logs ansehen
journalctl -u hud.service -f

# Service neustarten
sudo systemctl restart hud.service

# Service stoppen
sudo systemctl stop hud.service

# I2C Geraete scannen
i2cdetect -y 1

# CPU-Temperatur anzeigen
vcgencmd measure_temp

# Spannung pruefen (Unterspannung erkennen)
vcgencmd get_throttled
# 0x0 = alles ok, andere Werte = Spannungsprobleme
```
