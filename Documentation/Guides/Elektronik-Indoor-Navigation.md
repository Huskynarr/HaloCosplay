# Elektronik: Indoor-Navigation (Gamescom, IFA, Messegelaende)

> **Level:** [F] Fortgeschritten | [P] Profi  |  **Varianten:** V2/V3 (optional)
> **Voraussetzungen:** HUD laeuft (`Elektronik-HUD.md`), SensorFeeder mit MPU6050
> (`Code/HelmetControl/AR/SensorFeeder/`), Sprachsteuerung optional
> (`Elektronik-Sprachsteuerung.md`), Strombudget (`Elektronik-Strombudget.md`).

Dieses Modul bringt Wegbeschreibungen auf das HUD: "300 m, naechste links,
Halle 6". Es ist bewusst als **Wegweiser, nicht als Google-Maps-Ersatz** gebaut.
Der Guide erklaert zuerst, was in einer Messehalle technisch moeglich ist - und
was nicht - damit die Erwartungen stimmen, bevor Geld ausgegeben wird.

## 1. Was drinnen funktioniert - und was nicht

| Methode | Drinnen nutzbar | Warum |
| --- | --- | --- |
| GPS | Nein | Kein Signal in Hallen; draussen vor der Messe ja |
| WLAN-Positionierung | Nein | Braucht Vermessungsdaten des Gelaendes, gibt es nicht oeffentlich |
| Bluetooth-Beacons | Nein | Messebetreiber stellen keine oeffentlichen Beacons bereit |
| Visual Positioning (Kamera) | Nein (praktisch) | Braucht Kartendaten + Internet + viel Rechenleistung; Menschenmasse |
| Koppelnavigation (IMU) | Ja | Gyro + Schrittzahl, driftet aber - braucht Ankerpunkte |
| Magnetometer | Eingeschraenkt | Stahlhallen und Menschenmassen verfalschen das Erdmagnetfeld |
| **Manuelle Ankerpunkte** | **Ja, zuverlaessig** | "Position Halle 3 Eingang Nord" per Sprachbefehl oder Taster |

**Ehrliche Kernaussage:** Eine automatische "Wo bin ich"-Position wie draussen
gibt es drinnen fuer Hobby-Budgets nicht. Was sehr gut funktioniert: **Koppeln
zwischen Ankerpunkten**. Wer einmal pro Halle/Wechselgang seine Position
bestaetigt, dem zeigt das HUD die restliche Strecke als Pfeile + Distanz - und
das reicht voellig, weil die Fehlerstrecke zwischen zwei Ankern nur wenige
Prozent der Distanz betraegt.

## 2. Architektur

```
  SensorFeeder (ESP32, MPU6050)          Pi 5
  heading (Gyro, relativ)  --> sensor_bridge --> hud_state.json
                                           nav_bridge.py
                                             |  liest routes.json (Wegpunkte)
                                             |  zaehlt Schritte (Beschleunigung)
                                             |  schreibt nav_* Schluessel
                                             v
                                       hud_display.py
                                       Pfeile + Distanz + Hallen-Icon
```

Neu ist nur `nav_bridge.py` (gleiche Bruecken-Logik wie `sensor_bridge.py`):

- **routes.json:** vor der Con geplante Routen als Wegpunktliste:
  ```json
  {
    "gamescom_halle1_zu_halle6": [
      {"name": "Halle 1 Ausgang Nord", "dist_m": 0},
      {"name": "Wechselgang Richtung Sued", "dist_m": 180},
      {"name": "Halle 6 Eingang West", "dist_m": 320},
      {"name": "Booth XYZ", "dist_m": 90}
    ]
  }
  ```
- **Position:** aktuelle Distanz entlang der Route = zurueckgelegte Schritte
  (Beschleunigungssensor) minus Korrektur. Jeder Wegpunkt ist ein natuerlicher
  Anker: an der "Halle 6 Eingang West" angekommen, springt der Zaehler auf den
  Wegpunkt-Wert - Drift wird bei jedem Wegpunkt geloescht.
- **hud_state.json:** `nav_route`, `nav_distance_m`, `nav_turn` (links/gerade/
  rechts), `nav_label` ("Halle 6 Eingang West").
- **Sprachbefehle:** "navigation halle 6", "position eingang nord", "navigation
  aus", "wo bin ich" (sagt Route + Restdistanz). Neue Routen per Datei, nicht
  per Sprache - beim Sprechen in voller Montur ist weniger Vokabular mehr.

## 3. Hardware

| Teil | Preis ca. | Zweck | Notwendig? |
| --- | --- | --- | --- |
| MPU6050 (vorhanden im SensorFeeder) | 0 EUR | Gyro-Heading + Schritterkennung | ja |
| Magnetometer QMC5883L | 2-4 EUR | absoluter Heading, mit Gyro fusioniert | empfohlen |
| USB-GPS-Empfaenger | 20-30 EUR | Anker draussen (Wechselgaenge, Anreise) | optional |

- **QMC5883L:** kleiner I2C-Chip, kommt auf den SensorFeeder. Allein unzuver-
  laessig in Stahlhallen, aber als langsamer Korrekturwert fuer den driftenden
  Gyro sehr wertvoll. Fusion: Gyro fuer schnelle Aenderungen, Magnetometer
  zieht den Mittelwert langsam zurueck (Komplementaerfilter, ~10 Zeilen Code).
- **GPS nur fuer draussen:** In den Wechselgaengen der Koelnmesse/Messe Berlin
  und auf dem Weg zur Con liefert ein USB-GPS-Stick echte Position. Drinnen
  schaltet das System automatisch auf Koppelnavigation zurueck. Nicht kaufen,
  bevor das Kernsystem steht.

## 4. Messegelaende konkret: Gamescom und IFA

- **Karten offline:** Hallenplaene von koelnmesse.de / messe-berlin.de vor der
  Con als PNG/SVG in `Code/HelmetControl/maps/` ablegen. Auf dem 128x64-OLED
  zeigt man NICHT den Gesamtplan, sondern nur das aktuelle Segment (z. B. den
  Wechselgang) als Pfeildiagramm. Der Gesamtplan gehoert auf Papier in die
  Guerteltasche - das ist der bewaehrte Fallback.
- **Gamescom (Koelnmesse):** Hallen 1-10, Gesamtlaenge ca. 1,5 km. Die langen
  Wege sind die Wechselgaenge zwischen den Hallen - genau dort helfen Pfeile
  am meisten, weil man sonst nur Menschenmassen sieht. Eingaenge Nord/Sued und
  die Rheinseite sind gute Ankerpunkte.
- **IFA (Messe Berlin):** Hallen 1-26 plus CityCube, noch groesser. Gleiche
  Logik: Routen zwischen den eigenen Prioritaets-Booths vorplanen, jeden
  Hallenuebergang als Anker.
- **Netz:** Con-WLAN ist zur Spitzenzeit unbenutzbar, Mobilfunk in der Menge
  gedeckelt. Alles muss offline laufen - tut es mit dieser Architektur von
  selbst (routes.json und Karten liegen lokal).
- **Menschenmasse:** Schritterkennung wird im Stop-and-Go ungenau. Deshalb:
  Anker setzen ist billig (ein Sprachbefehl), zu oft ist besser als zu selten.

## 5. Anzeige auf dem Display

| Display | Navigation-Darstellung |
| --- | --- |
| OLED 128x64 (Stufe A) | grosser Richtungspfeil, Distanz, Ziel-Label - ideal und sofort ueber `hud_display.py` erweiterbar |
| AR-Brille (Stufe C) | Segment-Karte als Overlay, Pfeile in der Sichtlinie |

Fuer reine Navigation muss es **keine AR-Brille sein**: Pfeil + "180 m" + 
"Halle 6" liest sich auf dem einfarbigen OLED im Blickwinkel genauso gut wie
auf einer 450-EUR-Brille. Die Brille lohnt erst fuer Karten-Overlays und
Cortana-Einblendungen obendrauf.

## 6. Testreihenfolge

1. `nav_bridge.py --selftest` (hardwarefrei, wie die anderen Bruecken)
2. Route mit 3 Wegpunkten auf dem Papier abgehen: Wegpunkt-Anker loeschen den Drift?
3. Koelnmesse-Wechselgang nachbauen (Parkhaus/Einkaufszentrum): 300 m ohne Anker - wie gross ist der Heading-Fehler?
4. Anker per Sprachbefehl in voller Montur setzen (Lautstaerke, hallende Halle)
5. Ausfalltest: `nav.service` stoppen - HUD und alle anderen Module laufen weiter

## 7. Grenzen und Sicherheit

- **Die Navigation ist ein Show-Feature, kein Sicherheitssystem.** Sie ersetzt
  keinen Blick auf den Hallenplan und keinen Handler (`Glossar.md`). Wer sich
  verlaeuft, haelt an und schaut auf das Papier - nicht ins HUD-Starren mitten
  im Menschenstrom.
- **Nicht waehrend des Gehens auf das Display schauen** in dichter Menge -
  Kollisionsgefahr ist real (siehe `Sicherheit.md`). Pfeile nur an Stationen
  und Wechselgaengen lesen.
- **Drift eingestehen:** Nach 500 m ohne Anker kann der Pfeil 30-60 Grad
  daneben liegen. Der Wegpunkt-Anker-Mechanismus ist kein optionaler Feinschliff,
  sondern Kern des Designs.

## Verwandte Guides

- HUD: [Elektronik-HUD.md](Elektronik-HUD.md) | Sensorik: `Code/HelmetControl/AR/`
- Sprachbefehle: [Elektronik-Sprachsteuerung.md](Elektronik-Sprachsteuerung.md)
- Sicherheit: [Sicherheit.md](Sicherheit.md) | Con-Alltag: [Convention-Alltag.md](Convention-Alltag.md)
