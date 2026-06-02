# Electronics Step 2: Software, Tests, Integration

> **Level:** [F] Fortgeschritten | [P] Profi  ·  **Varianten:** V2/V3 (HUD/LEDs)  ·  **Voraussetzungen:** Step 1 bestanden, Raspberry Pi und Arduino mit PC verbindbar, Grundkenntnisse Linux/SSH; Begriffe siehe `Documentation/Guides/Glossar.md`

## Voraussetzung

- Hardware auf dem Tisch getestet (Step 1 bestanden)
- Alle Kabel mit Steckern versehen
- Ruestung ist bereit fuer Elektronik-Einbau

## 1. Raspberry Pi Software einrichten

Detailliert: `Documentation/Guides/Elektronik-Autostart.md`

### OS Installation

```bash
# Raspberry Pi Imager verwenden:
# 1. Raspberry Pi OS Lite (64-bit) auswaehlen
# 2. Einstellungen: WiFi, SSH aktivieren, User/Passwort setzen
# 3. Auf microSD flashen
```

### Erste Konfiguration

```bash
# Per SSH verbinden
ssh pi@raspberrypi.local

# System updaten
sudo apt update && sudo apt upgrade -y

# I2C aktivieren
sudo raspi-config
# -> Interface Options -> I2C -> Enable

# Verifizieren
i2cdetect -y 1
# Sollte 0x3C (OLED) und ggf. 0x08 (Arduino) zeigen
```

### HUD-Software installieren

```bash
# Dependencies
sudo apt install -y python3-pip python3-pil i2c-tools
pip3 install luma.oled

# HUD-Dateien kopieren (vom Repo)
# config.json erstellen
cp config.example.json config.json

# Testen
python3 hud_display.py
# Ctrl+C zum Beenden
```

### Autostart einrichten

Datei `/etc/systemd/system/hud.service` erstellen:

```ini
[Unit]
Description=Halo HUD Display
After=multi-user.target

[Service]
Type=idle
User=pi
ExecStart=/usr/bin/python3 -u /home/pi/hud_display.py
Restart=on-failure
RestartSec=5
StandardOutput=append:/var/log/hud.log
StandardError=inherit

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable hud.service
sudo systemctl start hud.service

# Status pruefen
sudo systemctl status hud.service
```

### Stromspar-Konfiguration

In `/boot/config.txt`:
```
hdmi_blanking=2
dtoverlay=disable-bt
gpu_mem=16
```

```bash
sudo systemctl disable bluetooth avahi-daemon triggerhappy
```

## 2. Arduino Software flashen

### LED-Steuerung

Der vorhandene Code (`Code/HelmetControl/MainControlCode.ino`) empfaengt Helligkeit per I2C:
- I2C-Adresse: 0x08
- Empfaengt 1 Byte = Helligkeit (0-255)
- Steuert LED an Pin 6

### LED-Effekte

`Code/HelmetControl/LightingEffectsCode.ino` — einfacher LED-Lauf
`Code/ArmorControl/LightingEffectsCode.ino` — LED-Chase-Effekt

### Flashen

1. Arduino Nano per USB an PC anschliessen
2. Arduino IDE oeffnen oder `arduino-cli compile && arduino-cli upload`
3. Board: "Arduino Nano" (oder "ATmega328P Old Bootloader" bei Clones)
4. Port waehlen und hochladen

## 3. LED-Effekte anpassen

### Beliebte Muster fuer Cosplay

| Effekt | Beschreibung | Wirkung |
| --- | --- | --- |
| Breathing | Langsames Ein-/Ausblenden | Ruhiger, lebendiger Look |
| Pulsing | Schnelleres Pulsieren | Alarmsignal, Power-Up |
| Static Glow | Konstantes Leuchten | Einfach, zuverlaessig |
| Chase | Laufendes Licht | Bewegung, Tech-Look |
| Reactive Flicker | Zufaelliges Flackern | Beschaedigter / kampf-look |

**Farbe:** Gruenes Leuchten (RGB: 0, 255, 80) ist klassisch Master Chief. Alternativ Blau (Cortana-Effekt) oder Orange (Alarm).

### Helligkeit

- **50% Helligkeit** ist fuer Convention-Innenraeume ideal
- Spart massiv Strom (Laufzeit fast verdoppelt)
- Volle Helligkeit nur fuer Outdoor-Fotoshootings
- Optional: Helligkeits-Umschaltung per Taster

## 4. Konfiguration anpassen

`config.json` — die wichtigsten Einstellungen:

```json
{
  "i2c_port": 1,
  "i2c_address": "0x3C",
  "width": 128,
  "height": 64,
  "refresh_ms": 100,
  "show_battery": true,
  "battery_path": "battery.json",
  "log_path": "hud_log.txt",
  "log_interval_s": 5
}
```

- `refresh_ms`: 100 = fluessig, 200-500 spart Strom
- `show_battery`: true zeigt Batteriestand (wenn `battery.json` vorhanden)
- `log_path`: Pfad fuer HUD-Log (leer = kein Log)

## 5. Integration in die Ruestung

### Helm

1. Pi + PiSugar im Nackenbereich montieren (Klett)
2. OLED vor dominantem Auge positionieren (3D-gedruckte Halterung)
3. Luefter einsetzen (Intake unten, Exhaust oben)
4. Visor-LEDs anbringen (WS2812B, entlang Visor-Kante)
5. Quick-Disconnect am Nacken verbinden (JST + XT30)
6. Kabel sauber mit Klett fuehren

### Ruestung

1. LED-Sektionen in Ruestungsteile einkleben (WS2812B Strips)
   - Brustplatte: 8-12 LEDs
   - Schultern: je 4-6 LEDs
   - Weitere Zonen nach Wunsch
2. Kabelstrecken im Unteranzug verlegen (Spiralschlauch)
3. An jedem Ruestungsteil: JST-Stecker fuer schnelles Trennen
4. Powerbank im Backpack oder Guertel-Tasche

### Backpack/Batterie-Montage

1. Powerbank(s) in Tasche am Ruecken des Unteranzugs
2. Kabel von Powerbank zum Verteiler (XT60)
3. Verteiler verteilt auf Module (XT30 pro Modul)
4. Tasche so positionieren, dass Gewicht auf der Huefte liegt

## 6. Integrations-Tests

### Test-Reihenfolge (wie bei echtem Space-Suit!)

1. **Nur Pi + OLED** — HUD funktioniert im Helm?
2. **Pi + OLED + Luefter** — Luftstrom ok, kein Vibrieren?
3. **Arduino + LEDs (auf dem Tisch)** — alle Sektionen korrekt?
4. **Alles zusammen (auf dem Tisch)** — Kurzschluss-Check mit Multimeter
5. **Alles in der Ruestung (stehend)** — Funktion bei realer Position?
6. **Bewegungstest** — Gehen, Setzen, Drehen — bleibt alles verbunden?

### Dauertest

- [ ] System mindestens **4 Stunden** durchgehend laufen lassen
- [ ] Temperatur pruefen (Helm-Innen, Pi, Powerbank — nichts heiss?)
- [ ] Batterie-Rest ablesen (wie viel Kapazitaet noch uebrig?)
- [ ] Alle LEDs noch an? Kein Flackern?
- [ ] HUD stabil? Kein Einfrieren?

## 7. Fehlersuche

| Problem | Diagnose | Loesung |
| --- | --- | --- |
| Display bleibt schwarz | `i2cdetect -y 1` — Adresse sichtbar? | Kabel pruefen, SDA/SCL tauschen, 3.3V statt 5V |
| Pi startet neu / friert ein | Unterspannung: `vcgencmd get_throttled` | Besseres USB-Kabel, staerkere Powerbank |
| LEDs flackern | GND verbunden? Datenleitung zu lang? | Gemeinsame Masse sicherstellen, Data-Kabel kuerzen |
| LEDs zeigen falsche Farbe | Falsche LED-Reihenfolge im Code | LED-Typ pruefen (WS2812B vs SK6812), Code anpassen |
| Luefter vibrieren | Lose Montage, Unwucht | Fester mit Klett fixieren, anderen Luefter testen |
| Audio brummt/rauscht | Ground Loop, zu lange Kabel | AC-Koppelkondensator pruefen, Kabel kuerzen |
| Batterie haelt nicht lang genug | Stromverbrauch hoeher als kalkuliert | LED-Helligkeit reduzieren, WiFi aus, zweite Powerbank |

## 8. Wartung und Pflege

- Nach jeder Convention: Helm-Polster trocknen lassen (Schweiss!)
- Stecker auf Korrosion pruefen
- Batterien auf 50-60% Ladung lagern (Lebensdauer)
- Software-Updates nur zu Hause testen, nie auf der Convention
- Ersatz-Kabel und -Stecker im Reparatur-Kit mitfuehren
