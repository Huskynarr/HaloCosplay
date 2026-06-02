# Ideen und Referenzen

Sammlung von Erweiterungsideen fuer das HUD und die Ruestungselektronik. Von einfach bis ambitioniert.

## HUD-Referenzen (visuell)

- Pinterest Master Chief HUD: https://www.pinterest.de/pin/424112489902404943/
- DeviantArt HUD Concept: https://www.deviantart.com/blooderific/art/Halo-Master-Chief-hud-444610711

## Software-Ideen (nach Schwierigkeit)

### Einfach (Pi Zero 2 W reicht)

| Idee | Beschreibung | Aufwand |
| --- | --- | --- |
| Music Player | MP3-Wiedergabe ueber Lautsprecher im Helm | Niedrig |
| Batterie-Anzeige | Prozent/Spannung auf HUD (bereits implementiert) | Fertig |
| Boot-Sequence | Animierter HUD-Start beim Einschalten | Niedrig |
| Uhrzeit/Timer | Convention-Timer auf dem HUD | Niedrig |

### Mittel (Pi Zero 2 W + Kamera/Sensoren)

| Idee | Beschreibung | Aufwand |
| --- | --- | --- |
| Echtzeit-Untertitel | Sprache-zu-Text auf dem HUD — https://github.com/la-wu/SubtitlesIRL | Mittel |
| Echtzeit-Uebersetzung | Gehoertes uebersetzen und anzeigen | Mittel-Hoch |
| Distanz-Berechnung | Entfernungsmessung mit Ultraschall/ToF-Sensor | Mittel |
| RFID-Kontaktaustausch | NFC/RFID-Tag im Handschuh fuer digitalen Visitenkarten-Tausch | Mittel |

### Ambitioniert (leistungsstaerkerer Pi oder externe Verarbeitung)

| Idee | Beschreibung | Aufwand |
| --- | --- | --- |
| People Tracking | Personen erkennen und auf HUD markieren | Hoch |
| Object Recognition | Objekte erkennen und benennen | Hoch |
| AI / Cortana | Sprachassistent im Helm, Smart Home Steuerung | Sehr hoch |
| Indoor Navigation | AR-Navigation in Convention-Hallen | Sehr hoch |
| Movie Player | OLED verdunkeln statt transparent = kleiner Bildschirm | Mittel |

## GitHub-Referenzen

| Projekt | Beschreibung | Link |
| --- | --- | --- |
| Hololens IronMan HUD | AR-HUD Konzept (Inspiration) | https://github.com/xSmoking/Hololens_IronMan |
| Spartan Distance Calc | Entfernungsberechnung im Browser | http://blainefricks.github.io/spartan |
| SolarSystemExplorer | AR-Weltraum-Visualisierung (Inspiration) | https://github.com/DataMesh-OpenSource/SolarSystemExplorer |
| Kinect to Hololens | 3D-Echtzeit-Capture (experimentell) | https://github.com/hanseuljun/kinect-to-hololens |
| LiveScan3D Hololens | 3D-Scan zu Hololens (experimentell) | https://github.com/MarekKowalski/LiveScan3D-Hololens |
| WorldExplorer | Outdoor-Navigation (TNOCS) | https://github.com/TNOCS/WorldExplorer |

## Realisierungshinweise

- Die meisten ambitionierten Ideen brauchen einen **Raspberry Pi 4/5** statt des Pi Zero 2 W (zu wenig Rechenleistung fuer KI)
- Kamera-basierte Features brauchen eine **Pi-Kamera** im Helm (Platz und Stromverbrauch beachten)
- Fuer Conventions ist **Einfachheit wichtiger als Features** — ein zuverlaessig laufendes HUD mit Batterieanzeige und Boot-Sequence beeindruckt mehr als ein absturzendes KI-System
- Echtzeit-Untertitel und RFID sind die realistischsten "fortgeschrittenen" Features
