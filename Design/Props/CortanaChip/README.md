# Cortana-Chip: Kontaktloses Daten-Dock

**Konzept-Prototyp.** Keine Passfreigabe, keine Lastfreigabe, keine
Beschaffung. Alle Bauteile sind Einzelnachweise; der ST60 ist Profi-Level.
Vollstaendige Einordnung: [Elektronik-Cortana-Chip.md](../../Documentation/Guides/Elektronik-Cortana-Chip.md)

## Funktionsweise

Der gedruckte Cortana-Chip enthaelt einen ESP32-S3 und eine kleine OLED.
Er haelt Charakter-Daten (Cortana, Husky) und stellt sie per BLE bereit.
Die Web-App (web/cortana/index.html) verbindet sich per Web BLE und zeigt
den Charakter auf dem Smartphone oder Laptop.

Der ST60A3H1 (60-GHz-mmWave) ist die spaetere kontaktlose Variante: Er
ersetzt die BLE-Strecke durch einen drahtlosen "Kabelersatz" im 1-2 cm
Spalt zwischen Chip und Dock. Bis dahin ist BLE der ehrliche Weg.

## Dateien

| Datei | Zweck |
| --- | --- |
| [CortanaChip.scad](CortanaChip.scad) | Gehaeuse mit ESP32-Ausschnitt, Antennenfenster, USB- und Gurtschlitzen |
| [STL/](STL/) | Druckteile: back, frame, front, assembly |
| [cortana_chip.ino](cortana_chip.ino) | ESP32-S3-Firmware: OLED, BLE-Service, Charakter-JSON |
| [characters/](characters/) | Charakter-Daten (cortana_v1.json, husky_v1.json) |
| [../../web/cortana/index.html](../../web/cortana/index.html) | Web-App: Web-BLE-Client fuer Smartphone/Laptop |

## Bauplan

### Schritt 1: Gehaeuse drucken

1. STLs aus STL/ drucken (PETG oder ASA, 3 Wandungen, 20-30 % Fill).
2. Frame ist das Hauptteil: enthaelt ESP32-Ausschnitt, Antennenfenster
   (freier Bereich ueber der Antenne, kein Filament), ST60-Bauraum und
   USB-C-Oeffnung.
3. Back hat zwei Gurtschlitze (25 mm Gurt), Front ist Deko mit Glow-Slots.

### Schritt 2: Elektronik verdrahten

| ESP32-S3-Pin | Verbunden mit | Hinweis |
| --- | --- | --- |
| 3V3 | OLED VCC | 3,3 V |
| GND | OLED GND | |
| GPIO6 | OLED SDA | I2C |
| GPIO7 | OLED SCL | I2C |
| GPIO0 | Taster nach GND | BOOT-Taster wechselt Seite |
| GPIO48 | Onboard-RGB | optional |

OLED: SSD1306 128x64, I2C-Adresse 0x3C (Standard).

### Schritt 3: Firmware flashen

1. Arduino IDE, ESP32-Core installieren (Boards: "ESP32S3 Dev Module").
2. Bibliotheken: Adafruit SSD1306, Adafruit GFX, ArduinoJson.
3. LittleFS-Partition aktivieren (Tools -> Partition Scheme -> mit SPIFFS).
4. characters/cortana_v1.json nach LittleFS-Data-Ordner kopieren und
   "ESP32 Sketch Data Upload" ausfuehren.
5. cortana_chip.ino flashen. Serial-Monitor zeigt Boot-Log.

### Schritt 4: Web-App testen

1. web/cortana/index.html oeffnen (Chrome/Edge, HTTPS oder localhost).
2. "Chip verbinden" klicken, Chip auswaehlen.
3. Charakter-Daten erscheinen; Schild regeneriert alle 5 Sekunden.

### Schritt 5: ST60-Nachruestung (optional, Profi)

1. EVALST60A3H1-Beschaffung klaeren (Verfuegbarkeit, Preis).
2. ST-Layoutguide lesen; Antennenfenster im Gehaeuse ist vorbereitet.
3. ST60-Tx in den Chip, ST60-Rx an den USB-C-Port des Anzeigegeraets.
4. Firmware auf UART-Tunnel umstellen; BLE bleibt als Fallback aktiv.

## Charakter-Wechsel

Zwei physische Chips mit unterschiedlichen IDs. Die Web-App erkennt die ID
(cortana_v1 vs husky_v1) und wechselt Design und Farben automatisch. Der
Tausch ist physisch, kein Software-Eingriff.

## Sicherheit und Grenzen

- Keine Freigabe fuer den Tragebetrieb; Vor dem ersten Einsatz Strombudget
  und Bauraum pruefen.
- LiPo im Chip nur mit Ladeschutz (TP4056) und Temperatursicherung.
- Antennenfenster muss frei von Filament und Metall bleiben, sonst keine
  Verbindung.
- Der ST60 ist ein Industrie-Bauteil; ohne eigene PCB-Design-Erfahrung
  erst beim BLE-Prototyp bleiben.
