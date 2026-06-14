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
| Echtzeit-Untertitel | Sprache-zu-Text auf dem HUD - https://github.com/la-wu/SubtitlesIRL | Mittel |
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

## Begleit-Roboter (Quadruped als Escort-Bot, Zukunftsidee)

Ein laufender Roboterhund, der dem Spartan folgt - thematisch ein Sensor-/Escort-Bot.
Aufwand: sehr hoch / teuer. Stand der Recherche: 2026.

### Warum Quadruped statt Drohne

- **Follow-Drohne:** real nur ~15-30 min Flugzeit, indoor auf Cons praktisch
  untersagt (Menschenmenge, Hausrecht). Fuer einen Con-Tag ungeeignet.
- **Quadruped:** Unitree Go2 ~1-2 h (bis ~4 h mit Langzeitakku), CyberDog 2 ~90 min,
  plus Wechselakku - grob 4-8x Einsatzzeit. Die einzig realistische Variante.

### Kaufbare Modelle (realistisch sortiert)

| Modell | Preis ca. | Akku real | SDK offen | Hinweis |
| --- | --- | --- | --- | --- |
| Unitree Go2 EDU | ab ~1.600 USD aufwaerts | 1-2 h (bis ~4 h) | Ja (Python + ROS 2) | einzige Go2 mit vollem SDK -> noetig fuer eigenes Verhalten |
| Unitree Go2 Air/Pro | ~1.600-3.800 USD | 1-2 h | Nein (nur App) | Follow per UWB-Remote, aber nicht frei programmierbar |
| Xiaomi CyberDog 2 | ~1.800 USD (CN) | ~90 min | Ja (Ubuntu + ROS 2) | KEINE offizielle EU-Verfuegbarkeit (nur Grauimport) |
| Unitree B2 | ~86.000 USD | 4-6 h | - | echter Traeger (40+ kg, IP67), fuer Hobby unrealistisch |

### "Follow" funktioniert ueber UWB-Tag, nicht Kamera

Wichtigste Erkenntnis fuers Cosplay: Der Go2-"Companion Mode" folgt einer
**UWB-Funkfernbedienung**, die man am Koerper traegt - nicht per Gesichtserkennung.
Reine Kamera-Tracker verlieren ihr Ziel in dichten, uniformen Mengen (genau das
Con-Szenario). UWB ist da robuster. Hersteller verlangt Sichtkontakt + min. 2 m Abstand.

### "Watch Guard Mode" - realistisch vs. heikel

- **Machbar (mit Edu-SDK):** folgt per UWB, dreht Kamera auf Annaehernde, spielt
  Sounds/Voicelines, Statuslichter, streamt Sensor-/Akkudaten ans Helm-HUD
  (ueber `hud_state.json`, siehe `Code/HelmetControl/sensor_bridge.py`).
- **Nicht realistisch:** echte autonome "Bewachung" mit Eingriff - dafuer nicht
  gebaut und in einer Menge ein Sicherheitsrisiko.

### Huerden vor dem Kauf (ehrlich)

- **Con-Genehmigung:** kaum oeffentliche Regeln zu Roboterhunden auf DE-Cons; ein
  ~15-kg-Geraet faellt vermutlich unter "potenziell gefaehrlich" -> vorher beim
  Veranstalter anfragen, Handler + ggf. Versicherung einplanen. Siehe
  `Documentation/Guides/Convention-Regeln.md`.
- **Toter Winkel:** Go2-LiDAR sitzt unter dem Kopf -> Kollisionsrisiko seitlich/hinten.
- **Security/Datenschutz:** fuer Unitree 2025/26 dokumentierte Befunde (Exploit
  CVE-2025-2894, verdaechtiger Traffic zu CN-Servern); kamerafuehrendes Geraet in
  der Oeffentlichkeit ist zudem ein DSGVO-Thema.

### Integration ins HUD

Wie der Roboter konkret per WLAN Daten ans Helm-HUD schickt (mit lauffaehiger,
hardwarefrei testbarer Software-Bruecke): `Documentation/Guides/Begleitroboter-Integration.md`.

### Quellen

- Unitree Go2: https://shop.unitree.com/products/unitree-go2
- Unitree SDK2 (Edu): https://github.com/unitreerobotics/unitree_sdk2
- Xiaomi CyberDog 2: https://newatlas.com/robotics/xiaomi-cyberdog-2/
- Sicherheitsbefunde Unitree: https://hackaday.com/2026/05/12/the-dark-side-of-unitree-robot-dogs/

## Realisierungshinweise

- Die meisten ambitionierten Ideen brauchen einen **Raspberry Pi 4/5** statt des Pi Zero 2 W (zu wenig Rechenleistung fuer KI)
- Kamera-basierte Features brauchen eine **Pi-Kamera** im Helm (Platz und Stromverbrauch beachten)
- Fuer Conventions ist **Einfachheit wichtiger als Features** - ein zuverlaessig laufendes HUD mit Batterieanzeige und Boot-Sequence beeindruckt mehr als ein absturzendes KI-System
- Echtzeit-Untertitel und RFID sind die realistischsten "fortgeschrittenen" Features
