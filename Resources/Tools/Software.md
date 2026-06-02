# Software-Tools fuer Cosplay-Bau

## Skalierung und Passform

### Armorsmith Designer

- **Zweck:** Einzige Software speziell fuer Ruestungsskalierung auf den eigenen Koerper
- **Funktion:** Koerpermasse eingeben, Avatar erstellen, STL/OBJ importieren und auf Avatar platzieren, Passform pruefen
- **Preis:** ~30 USD einmalig (Gumroad)
- **Plattform:** nur Windows
- **Status:** Entwicklung eingestellt, Software funktioniert weiterhin, Community-Support ueber 405th
- **Quelle:** https://thearmoredgarage.gumroad.com/l/LMdGL
- **Guide:** https://www.405th.com/forums/threads/armorsmith-designer-beginners-guide.49836/

### Pepakura Designer / Viewer

- **Zweck:** 3D-Modelle in flache 2D-Schnittmuster auffalten fuer Foam- oder Papier-Bau
- **Viewer:** Kostenlos (bestehende Templates anzeigen und drucken)
- **Designer:** ~35 USD einmalig (Templates erstellen und bearbeiten)
- **Plattform:** nur Windows
- **Status:** Aktiv, weiterhin relevant fuer Foam-Builds
- **Foam-Tutorial:** https://www.405th.com/forums/threads/first-step-in-building-foam-pepakura-armor-tutorial.54538/

## 3D-Modellierung und STL-Bearbeitung

### Bambu Studio

- **Zweck:** Slicer mit erweiterten Cosplay-Features
- **Preis:** Kostenlos
- **Plattform:** Windows, Mac, Linux
- **Key Features:**
  - **Cut Tool (Taste C):** Modelle in druckbare Segmente schneiden, mit Schwalbenschwanz-Verbindern
  - **Multi-Plate:** Bis zu 36 Druckplatten in einem Projekt
  - **Paint-on Supports:** Manuell festlegen wo Supports stehen (kritisch fuer Visor-Kanaele)
  - **Modifier Meshes:** Verschiedene Druckeinstellungen pro Region (Infill, Wandstaerke)
- **Download:** https://bambulab.com/en-us/download/studio

### Blender

- **Zweck:** Maechtigstes kostenloses Tool fuer STL-Modifikation
- **Preis:** Kostenlos, Open Source
- **Plattform:** Windows, Mac, Linux
- **Cosplay-Einsatz:**
  - Boolean-Operationen (Teile zusammenfuegen/schneiden)
  - Kitbashing (Teile verschiedener Modell-Sets kombinieren)
  - Details hinzufuegen/entfernen, Dicke anpassen
  - Ruestungs-Visualisierung und Farbschema-Planung
- **Halo-spezifisch:** https://www.405th.com/forums/threads/kitbashing-in-blender-hemlock-and-other-attachments.56415/
- **Download:** https://www.blender.org/

### Meshmixer

- **Zweck:** Mesh-Bearbeitung fuer 3D-Druck-Vorbereitung
- **Preis:** Kostenlos (von Autodesk eingestellt, aber funktioniert noch)
- **Plattform:** Windows, Mac
- **Cosplay-Einsatz:**
  - Plane Cuts (Ruestung in druckbare Teile schneiden)
  - Hollowing (Wandstaerke hinzufuegen, Material sparen)
  - Alignment-Pins hinzufuegen
  - Mesh-Reparatur (Analysis > Inspector)
- **Download:** https://meshmixer.org/
- **Hinweis:** Keine Updates mehr. Langfristig auf Blender/Bambu Studio Cut Tool wechseln.

### Fusion 360

- **Zweck:** Praezisions-CAD fuer mechanische Teile (Halterungen, Clips, Gelenke, Elektronik-Gehaeuse)
- **Preis:** Kostenlos fuer Hobby (Personal Use License, <1000 USD/Jahr Einnahmen)
- **Plattform:** Windows, Mac
- **Cosplay-Einsatz:**
  - Custom-Brackets fuer Ruestungsbefestigung
  - Scharnier-Mechanismen fuer bewegliche Teile
  - Elektronik-Halterungen (Luefter-Mounts, Batterie-Halter, Lautsprecher-Gehaeuse)
  - Snap-Fit Verbindungsstuecke
- **Download:** https://www.autodesk.com/products/fusion-360/overview

## Slicer

### Bambu Studio (siehe oben)

Fuer Bambu Lab Drucker (H2C) der primaere Slicer.

### Lychee Slicer

- **Zweck:** FDM/Resin-Slicer mit fortgeschrittenen Auto-Supports und Hollowing
- **Preis:** Kostenlos (Lite), Bezahlt fuer erweiterte Features
- **Neu (2025/2026):** "Lychee Gen" — KI-generierte 3D-Modelle aus Textbeschreibung
- **Download:** https://mango3d.io/

## Elektronik-Design

### Fritzing

- **Zweck:** Anfaengerfreundliches Breadboard-Diagramm-Tool
- **Preis:** ~8 EUR (Spenden-basiert)
- **Ideal fuer:** Visuelle Verdrahtungsdiagramme, Dokumentation, Teilen mit Community
- **Download:** https://fritzing.org/

### EasyEDA

- **Zweck:** Web-basiertes PCB-Design, direkt mit JLCPCB fuer Bestellung integriert
- **Preis:** Kostenlos
- **Ideal fuer:** Custom PCBs (LED-Treiber, Sound-Trigger-Boards)
- **Zugang:** https://easyeda.com/

### KiCad

- **Zweck:** Professionelles PCB-Design (Schaltplan, Layout, 3D-Vorschau)
- **Preis:** Kostenlos, Open Source
- **Ideal fuer:** Komplexere Elektronik-Projekte
- **Download:** https://www.kicad.org/

**Empfehlung:** Fritzing zum Dokumentieren, EasyEDA fuer Custom-PCBs, KiCad nur bei fortgeschrittenen Anforderungen.

## LED-Animation

### WLED

- **Zweck:** Firmware fuer ESP32/ESP8266, steuert adressierbare LEDs per WiFi/Web-Interface
- **Preis:** Kostenlos, Open Source
- **Features:** 150+ eingebaute Effekte und Paletten, Presets, Button-Trigger, Phone-Steuerung
- **Ideal fuer:** Standalone LED-Steuerung ohne PC, Phone-basierte Umschaltung zwischen Effekten
- **Quelle:** https://kno.wled.ge/

### FastLED

- **Zweck:** Arduino-Library fuer programmierbare LED-Strips
- **Preis:** Kostenlos, Open Source
- **Features:** Unterstuetzt WS2812B, WS2811, APA102 und viele mehr
- **Ideal fuer:** Custom-Animationen, synced mit Events (HUD-Boot, Sound-Reactive)
- **Quelle:** https://fastled.io/

### FastLED Animator

- **Zweck:** Visueller Simulator fuer FastLED-Animationen (ohne Hardware testen)
- **Preis:** Kostenlos
- **Zugang:** https://www.fastledanimator.com/

**Empfehlung:** WLED fuer einfache No-Code Steuerung mit Phone. FastLED fuer Custom-Animationen. Beides kombinierbar.

## Grafik und Referenzen

- **Inkscape** (kostenlos) — Vektor-Grafik, Schnittmuster
- **GIMP** (kostenlos) — Bild-Bearbeitung, Ruestung auf Koerperfotos ueberlegen
- **Blender** — 3D-Visualisierung, Farbschema-Planung

## Code und Entwicklung

- **Arduino IDE** — Arduino-Sketches fuer LEDs, Luefter, Sensoren
- **Thonny** oder **VS Code** — Python fuer Pi Zero 2 W HUD-Software
- **Raspberry Pi Imager** — OS auf SD-Karte flashen
