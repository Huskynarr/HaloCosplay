# Code

Dieses Verzeichnis enthaelt Beispielcode fuer Helm- und Ruestungs-LEDs sowie das HUD.

## HelmetControl

- `hud_display.py` - einfacher HUD-Demo-Loop fuer OLED
- `requirements.txt` - Python-Dependencies
- `config.example.json` - Beispiel-Konfiguration (als `config.json` kopieren)
- `battery.example.json` - Beispiel fuer Batteriestatus
- `MainControlCode.ino` - I2C-Empfang fuer LED-Helligkeit
- `LightingEffectsCode.ino` - einfacher LED-Lauf

## ArmorControl

- `MainControlCode.ino` - LED-Breathing
- `LightingEffectsCode.ino` - LED-Chase

## Hinweis

Anpassen auf die eigene Verkabelung (Pins, LED-Anzahl, Spannung).
