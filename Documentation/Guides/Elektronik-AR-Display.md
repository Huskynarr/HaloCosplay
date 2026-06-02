# Elektronik: AR-Display fuer den Helm

> **Level:** [A] Stufe A (alle) | [F] Stufe B | [P] Stufe C (Profi)  ·  **Varianten:** Stufe A alle, Stufe C nur V3
> **Voraussetzungen:** Fuer Stufe C solides Strom-/Hitzebudget (`Documentation/Guides/Elektronik-Strombudget.md`), Linux/OpenCV-Kenntnisse und zwingend ein Sicherheits-Failsafe (Abschnitt 3).

Dieser Guide behandelt das Thema "Augmented Reality" im Master-Chief-Helm (HALO INFINITE, MJOLNIR GEN3) ehrlich und technisch fundiert. Das Wunschziel vieler Builder ist ein Voll-AR-Helm mit Kamera-Passthrough wie im Spiel. Das ist machbar, aber teuer, schwer, stromhungrig und sicherheitskritisch. Dieser Guide erklaert die Stufen, das Endausbau-Konzept (V3) und vor allem die Grenzen und Risiken.

**Kurzfassung:** Fuer fast alle Conventions ist Stufe A (statischer HUD-Look) die richtige Wahl. Stufe C (Kamera-Passthrough) ist ein Showpiece fuer kontrollierte Umgebungen, kein Alltags-Setup.

## 1. Was bedeutet "AR" im Cosplay

Der Begriff "AR" wird im Cosplay sehr unscharf benutzt. In der Praxis gibt es drei klar trennbare Stufen mit komplett unterschiedlichem Aufwand und Risiko.

### Stufe A: Statischer HUD-Look (Empfehlung fuer alle)

Ein transparentes OLED zeigt eine fixe oder animierte HALO-Infinite-Grafik (Schildbalken, Munitionsanzeige, Wegpunkte, Boot-Sequenz). Das Bild ist Deko, es trackt nichts, es reagiert nicht auf die Umgebung. Die direkte Sicht durch den Visor bleibt vollstaendig erhalten.

- Sicher: kein Sichtverlust, kein Sturzrisiko durch Elektronik
- Leicht, stromsparend, bereits vollstaendig dokumentiert
- Genau das, was 99% der Betrachter als "AR-Helm" wahrnehmen

Details dazu in `Documentation/Guides/Elektronik-HUD.md` und zur optischen Umsetzung in `Documentation/Guides/LED-Visor-Forschung.md`.

### Stufe B: See-Through-Combiner (schwebendes Bild)

Ein kleines Display strahlt ueber einen halbdurchlaessigen Spiegel (Beamsplitter, "Combiner") in das Sichtfeld. Das HUD-Bild scheint zu schweben, die reale Umgebung bleibt durch das Glas hindurch sichtbar. Das ist optisch dem "echten" AR am naechsten, ohne die Sicht zu ersetzen.

- Sicht bleibt frei (Bild liegt ueber der Realsicht, nicht statt ihr)
- Deutlich aufwendiger als Stufe A: Optik, Fokus, Justage
- Im Helm wenig Platz fuer einen sauberen Combiner-Aufbau
- Realistisch eher monokular (ein Auge), zweiaeugig ist sehr fummelig

Stufe B ist ein guter Mittelweg fuer V2/V3, wenn man mehr will als ein statisches Bild, aber die Sicherheit der Realsicht nicht aufgeben moechte.

### Stufe C: Voll-AR mit Kamera-Passthrough (Showpiece)

Eine Kamera filmt die Umgebung, ein Rechner legt ein HUD-Overlay darueber, das Ergebnis geht auf ein Display direkt vor den Augen. Die direkte Sicht durch den Visor wird ersetzt. Das ist der Endausbau-Wunsch (V3) und das, was im Spiel passiert.

- Maximaler Wow-Effekt, echtes "Spiel-Feeling"
- Hoechster Aufwand, hoechste Kosten, hoechstes Gewicht
- **Sicherheitskritisch:** wer die Realsicht ersetzt, sieht bei jedem Fehler nichts mehr (siehe Abschnitt 3)

## 2. Stufe C im Detail (Kamera-Passthrough)

Passthrough heisst: jeder Frame muss Kamera -> Rechner -> Overlay -> Display in moeglichst unter 20-30 ms durchlaufen. Alles darueber fuehlt sich wie "Schwimmen" an, verursacht Uebelkeit (Motion Sickness) und macht das Gehen gefaehrlich. Deshalb gilt:

> **ESP32, Arduino und Raspberry Pi Zero reichen fuer Passthrough NICHT aus.** Sie haben weder die Rechenleistung noch die Kamera-/Display-Bandbreite. Diese Boards bleiben fuer LEDs, Luefter und Sensorik.

### Rechner (das Herz)

| Plattform | Eignung Passthrough | Hinweis |
| --- | --- | --- |
| Raspberry Pi Zero 2 W | ungeeignet | nur fuer Stufe A (statischer HUD) |
| ESP32 / Arduino | ungeeignet | nur LEDs/Luefter/Sensorik |
| Raspberry Pi 4 (4-8 GB) | Minimum | CSI-Kamera + kleines Display, einfaches Overlay, mit Tuning Richtung niedrige Latenz |
| Raspberry Pi 5 | brauchbar | mehr Reserve, aber mehr Hitze und Strom |
| Jetson Nano / Orin Nano | gut | dedizierte GPU, ideal fuer schwerere Overlays/CV, teuer und durstig |

Realistisch: Pi 5 oder Jetson, wenn es fluessig sein soll. Pi 4 geht als Einstieg, wird aber schnell zum Latenz-Flaschenhals, sobald das Overlay aufwendiger wird.

### Kamera

- **CSI-Kamera** (direkt am Pi/Jetson) statt USB-Webcam: niedrigere Latenz, weniger CPU-Overhead
- Sichtfeld (FOV): moeglichst weit (90-120 Grad), sonst entsteht Tunnelblick (siehe Abschnitt 3)
- Globaler vs. Rolling Shutter: Rolling Shutter "verwischt" bei schnellen Kopfbewegungen
- Eine Kamera mittig ist einfach, erzeugt aber einen Parallaxe-Versatz zur echten Augenposition (man greift daneben). Zwei Kameras fuer Stereo verdoppeln Aufwand und Latenz.
- Schwachlicht: Conventions sind oft dunkel; billige Kameras rauschen stark und werden langsam (laengere Belichtung = mehr Latenz)

### Display

- Ein kleines LCD/OLED pro Auge oder ein gemeinsames Display mit Optik vor beiden Augen
- Wichtig: Aufloesung, Helligkeit, und vor allem die Optik (Linse), damit das Bild ein paar Zentimeter vor dem Auge ueberhaupt scharf erscheint
- Hohe Bildrate (>= 60 fps) reduziert Uebelkeit
- Mehr Pixel und mehr Helligkeit = mehr Strom und mehr Hitze

### Software (Grundidee)

Die Pipeline ist im Kern simpel, die Tuecke steckt in der Latenz:

```
1. Kamera-Frame holen      (CSI, libcamera / picamera2)
2. Optional: entzerren     (OpenCV, falls Weitwinkel-Verzerrung)
3. HUD-Overlay zeichnen     (Schild, Munition, Wegpunkte)
4. Frame auf Display ausgeben (Pygame / Framebuffer / DRM)
5. zurueck zu 1 (Zielschleife unter 20-30 ms)
```

- **OpenCV** fuer Frame-Handling und einfache Bildverarbeitung
- **Pygame** oder direkter Framebuffer-/DRM-Zugriff fuer schnelle Ausgabe ohne Desktop-Overhead
- Kein Desktop, keine WLAN-Last, GPU-Pfad nutzen wo moeglich
- Jede zusaetzliche "intelligente" Funktion (Objekterkennung, Tracking) kostet Latenz und Strom

Beispielcode im Repo:
- **Stufe A (statisches OLED-HUD):** `Code/HelmetControl/hud_display.py`
- **Stufe C (Passthrough-Pipeline):** `Code/HelmetControl/AR/` — lauffaehiges Beispiel mit
  Kamera-Anbindung (picamera2/OpenCV), Halo-HUD-Overlay (`hud_overlay.py`), Latenzmessung
  und Sicherheits-Failsafe (`ar_passthrough.py`), dazu ein ESP32-Sensor-Feeder
  (`SensorFeeder/SensorFeeder.ino`). Hardwarefreier Test:
  `python3 ar_passthrough.py --selftest hud_test.png`. Details: `Code/HelmetControl/AR/README.md`.

Das Beispiel ist bewusst schlank gehalten; eine produktive, ruckelfreie Passthrough-Pipeline
mit niedriger Latenz bleibt ein eigenes, groesseres Software-Projekt.

## 3. Sicherheit (zwingend lesen)

Sobald Stufe C die direkte Sicht ersetzt, ist die Elektronik sicherheitskritisch. Ein HUD-Bug ist harmlos, ein blinder Cosplayer auf einer Treppe nicht.

### Die konkreten Gefahren

- **Latenz/Ruckeln:** verzoegertes Bild = Uebelkeit, Fehleinschaetzung von Distanzen, Stolpern
- **Ausfall (Software-Crash, Kabelbruch, Akkuausfall):** Display wird schwarz = sofortige Blindheit mitten in der Bewegung
- **Tunnelblick:** Kamera-FOV ist kleiner als das menschliche Sichtfeld; Hindernisse seitlich werden nicht gesehen
- **Fehlende Tiefenwahrnehmung:** eine Mono-Kamera liefert kein echtes 3D; Treppenstufen, Tischkanten und Abstaende werden falsch eingeschaetzt
- **Parallaxe:** Kamera sitzt nicht exakt auf Augenhoehe -> man greift und tritt daneben
- **Hitze:** Pi/Jetson plus Display direkt am Kopf, im geschlossenen Helm

### Pflicht-Regeln fuer Stufe C

1. **Immer ein mechanischer Notausblick.** Visor in Sekunden hochklappbar oder absetzbar, ohne Werkzeug, ohne fremde Hilfe. Quick-Release am Visor ist Pflicht.
2. **Quick-Release am Helm/Visor** so positionieren, dass er auch mit Handschuhen blind erreichbar ist.
3. **Handler zwingend.** Eine begleitende Person, die fuehrt, warnt und im Notfall den Helm abnimmt. Nie allein mit aktivem Passthrough laufen.
4. **Nicht auf Treppen, Rolltreppen, Rampen oder in Menschenmengen** mit aktivem Passthrough. Vorher Visor hoch oder Helm ab.
5. **Sichtbarer Test vor jedem Einsatz:** Akkustand, Latenz, Bildausfall-Verhalten. Bei Ausfall sofort Notausblick nutzen.
6. **Akku-Reserve und sauberes Failsafe:** definiertes Verhalten bei Unterspannung; im Zweifel lieber rechtzeitig Visor hoch.
7. **Stationaer bevorzugen:** Passthrough am besten im Stehen/Sitzen auf der Buehne oder am Stand vorfuehren, nicht beim Laufen durch die Halle.

Mehr zu allgemeiner Tragesicherheit, Hitze und Notausstieg in `Documentation/Guides/Sicherheit.md`. Praxis im Con-Alltag (Gedraenge, Pausen, Handler) in `Documentation/Guides/Convention-Alltag.md`.

## 4. Realistische Empfehlung

Fuer den allergroessten Teil aller Auftritte ist **Stufe A (statischer HUD)** die richtige Wahl: sicher, leicht, robust, und vom Betrachter ohnehin nicht von "echtem" AR zu unterscheiden. Stufe B ist der ambitionierte Mittelweg, wenn man ein schwebendes Bild bei freier Sicht moechte. **Stufe C ist ein Showpiece** fuer kontrollierte Umgebungen (Buehne, Foto-Set, eigener Stand) mit Handler.

### Microcontroller-Rollenverteilung

Auch im Voll-AR-Helm bleibt die klassische Arbeitsteilung sinnvoll:

| Aufgabe | Plattform | Begruendung |
| --- | --- | --- |
| Kamera + Overlay + Display | Raspberry Pi 4/5 oder Jetson | braucht Rechenleistung und Bandbreite |
| LED-Effekte (Visor, Armor) | ESP32 / Arduino Nano | echtzeitfaehig, stromsparend, robust |
| Luefter-Steuerung (PWM, Temperatur) | ESP32 / Arduino | laeuft unabhaengig vom Grafik-Rechner weiter |
| Sensorik (Taster, Temperatur, Akku) | ESP32 / Arduino | entlastet den Pi, einfaches Failsafe |

Wichtig: Luefter und Notbeleuchtung sollten **nicht** vom Grafik-Rechner abhaengen. Faellt der Pi aus, muessen Luefter und ein eventuelles Not-LED weiterlaufen.

## 5. Roadmap V1 -> V2 -> V3

Die Varianten bauen aufeinander auf. Man kann jederzeit auf einer Stufe bleiben.

| Variante | AR-Stufe | Hardware | Komplexitaet | Grobkosten (nur AR/HUD-Anteil) |
| --- | --- | --- | --- | --- |
| V1 (Foam, Einsteiger) | A (oder gar kein HUD) | einfache gruene LEDs / kleines OLED | gering | ca. 20-60 EUR |
| V2 (3D-Druck, Fortgeschritten) | A, optional B | Pi Zero 2 W + transparentes OLED, ggf. Combiner | mittel | ca. 80-200 EUR |
| V3 (Profi, Exoskelett) | C (Showpiece), faellt auf A zurueck | Pi 5 / Jetson + CSI-Kamera + Display(s) + Optik | sehr hoch | ca. 300-700+ EUR |

Empfohlener Pfad:

1. **V1/V2 starten mit Stufe A.** Funktioniert, sieht gut aus, ist sicher.
2. **Optional Stufe B testen** (Combiner an einem Auge), wenn Stufe A sitzt.
3. **Stufe C nur in V3**, mit voller Sicherheitsausstattung (Quick-Release, Handler) und immer mit Rueckfallebene auf Stufe A oder freie Sicht.

Allgemeine Variantenuebersicht: `Documentation/Guides/Varianten.md`. Exoskelett-Kontext fuer V3: `Documentation/Guides/Exoskelett.md`.

## 6. Strom und Hitze (der Knackpunkt von Stufe C)

Ein Pi 4/5 oder Jetson plus Display zieht ein Vielfaches eines Pi Zero mit OLED und erzeugt entsprechend Abwaerme, direkt am Kopf.

- **Pi Zero 2 W + OLED (Stufe A):** ca. 0.3-0.4 A bei 5 V, kaum Hitze
- **Pi 4 + Display + Kamera (Stufe C):** grob 1.5-3 A bei 5 V unter Last, deutliche Abwaerme
- **Pi 5 / Jetson (Stufe C):** noch mehr; aktive Kuehlung Pflicht

Konsequenzen, die vor dem Bau geklaert sein muessen:

1. **Strombudget neu rechnen.** Ein Stufe-C-Setup halbiert bis drittelt die Laufzeit gegenueber Stufe A. Akku entsprechend groesser dimensionieren. Details und Beispielrechnungen in `Documentation/Guides/Elektronik-Strombudget.md`.
2. **Aktive Kuehlung.** Pi/Jetson brauchen Kuehlkoerper plus Luefter; im geschlossenen Helm zusaetzlich Helmbelueftung. Siehe `Documentation/Guides/Elektronik-Luefter.md`.
3. **Akku-Auslegung und Sicherheit.** Groesserer LiPo/Powerbank, Schutzschaltung, sauberes Verhalten bei Unterspannung. Siehe `Documentation/Guides/Elektronik-Batterie.md`.
4. **Verkabelung.** Hoehere Stroeme = dickere Leitungen, sauberer Stecker, Zugentlastung. Siehe `Documentation/Guides/Elektronik-Verdrahtung.md`.

## Fazit

Voll-AR mit Kamera-Passthrough ist als V3-Showpiece machbar, aber es ist ein eigenes Hardware- und Software-Projekt mit echtem Verletzungsrisiko, sobald es die Sicht ersetzt. Wer einen zuverlaessigen, beeindruckenden Helm fuer den Con-Alltag will, faehrt mit **Stufe A** am besten. Stufe C nur bauen, wenn Latenz, Kuehlung, Akku und vor allem die Sicherheits-Rueckfallebene sauber geloest sind.
