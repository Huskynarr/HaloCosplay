# Elektronik und HUD

Ziel ist ein tragbares, modulares HUD-System mit sicherer Stromversorgung. Die Basis ist ein Raspberry Pi Zero 2 W mit transparentem OLED-Display. Eine guenstige Alternative ist ein einfarbiges, gruener LED-HUD ohne AR-Funktionen.

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
- Arduino: `Code/HelmetControl/MainControlCode.ino`

## Guenstige HUD-Alternative

- Einfarbiger LED-Frame im Visor (gruener Akzent)
- Kein transparentes Display, nur optische Effekte
- Deutlich leichter, weniger Strom, schneller umzusetzen
