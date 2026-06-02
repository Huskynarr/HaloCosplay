# 3D-Druck Guide (Bambu Lab H2C)

Dieser Guide beschreibt den 3D-Druck-Workflow fuer ein vollstaendiges Master Chief MJOLNIR Armor Set mit dem Bambu Lab H2C.

## Drucker-Spezifikationen (H2C)

- Bauvolumen: ca. 325 x 320 x 325 mm (linke Duese), 305 x 320 mm (rechte Duese)
- Vortek-Hotend: 5-7 Filamente ohne Purge-Verschwendung (Multi-Material)
- CoreXY, geschlossener Bauraum
- Max Speed: ca. 500 mm/s, Qualitaetsdruck bei 150-200 mm/s

## Filament-Empfehlungen

| Material | Vorteile | Nachteile | Empfehlung |
| --- | --- | --- | --- |
| PLA+ | einfach zu drucken, scharfe Details, guenstig | spruede, hitzeempfindlich (~55-60 C), verformt sich im Auto/Sonne | Prototypen, Detailteile |
| PETG | schlagfest, hitzebestaendig (~75-80 C), leichter Flex | Stringing, schwerer zu schleifen, Supports haften stark | **Beste Wahl fuer tragbare Ruestung** |
| ASA | UV-bestaendig, hitzebestaendig (~100 C), gut schleifbar | Daempfe (Belueftung Pflicht), teurer, Warping | Outdoor-Einsatz, Langzeitprojekte |
| TPU | flexibel, stossdaempfend | nicht fuer starre Panzerteile | Dichtungen, flexible Gelenke |

**Empfehlung:** PETG als Hauptmaterial. PLA+ fuer Prototypen und feine Details. ASA nur bei haeufigem Outdoor-Einsatz.

## Slicer-Einstellungen (Bambu Studio)

### Waende und Infill

- **Wandanzahl:** 3-4 (bei 0.4 mm Duese = 1.2-1.6 mm Schalendicke)
- **Infill:** 10-15% Gyroid (bestes Verhaeltnis Festigkeit/Gewicht)
- **Top/Bottom Schichten:** 4-5
- **Arachne Wall Generator:** AN (Standard in Bambu Studio)

### Schichthoehe

- **0.20 mm** — Standard fuer Balance aus Speed und Qualitaet
- **0.28-0.32 mm** — mit 0.6 mm Duese fuer Koerperpanzer (spart ~40% Zeit)
- **0.12-0.16 mm** — nur fuer Visor/Detailteile

### Supports

- **Typ:** Tree Supports (Slim/Hybrid)
- **Interface-Schichten:** 2-3 mit 0.15-0.2 mm Z-Gap
- **Dichte:** 5-8%
- **"Support on build plate only"** wenn moeglich aktivieren
- Concentric Interface fuer Kurven

### Sonstiges

- **Brim:** 5-8 mm fuer grosse flache Teile (Warping-Schutz)
- **Nahtposition:** "Aligned" entlang Kanten die spaeter geschliffen werden
- **Druckgeschwindigkeit:** 150-200 mm/s fuer sichtbare Flaechen
- **Ironing:** AN fuer sichtbare Oberseiten (glatte Oberflaeche)

## Grosse Teile splitten

Ein Master Chief Helm ist ca. 280-320 mm hoch und 250-280 mm breit — passt oft nicht in einem Stueck.

### Bambu Studio Cut Tool (Taste C)

- Modell auswaehlen, C druecken, Schnittebene positionieren
- Automatische Schwalbenschwanz-/Pin-Verbinder moeglich
- Schnell und bequem — Schneiden und Slicen in einem Workflow
- Limitierung: nur ebene Schnitte (keine gekruemmten)

### Meshmixer (kostenlos, Autodesk)

- Edit > Plane Cut: Schnittebene positionieren, "Slice (Keep Both)"
- Alignment-Pins hinzufuegen (Edit > Add Pin)
- Gut fuer organische Schnitte entlang der Panzerlinien

### Best Practices beim Schneiden

- **Entlang bestehender Panel-Linien** schneiden (Naehte werden unsichtbar nach Fuellen)
- **45-Grad-Winkel** Schnitte erzeugen mehr Klebeflaeche und staerkere Verbindungen
- **Registrier-Pins** (2-3 mm Durchmesser) fuer Ausrichtung beim Zusammenbau
- Teile **unter 300 mm** in der groessten Dimension halten (Brim-Platz einrechnen)

## Druckorientierung

**Grundregel:** FDM-Teile sind am schwaechsten zwischen den Schichten (Z-Achse). Teile so orientieren, dass Belastung parallel zu den Schichten laeuft.

| Teil | Orientierung | Grund |
| --- | --- | --- |
| Helm (halbiert) | Visier/Gesicht nach unten auf Druckbett | Dome druckt aufwaerts, Schichten sind konzentrische Ringe |
| Brust/Torso | stehend (Schichten stapeln vertikal) | Schichtlinien horizontal = Aufprall verteilt sich |
| Unterarm/Schienbein (Rohrform) | vertikal, offenes Ende unten | Schichten bilden Ringe = sehr druckfest |
| Schulter-Pauldrons | Dome nach oben, offene Seite unten | Natuerliche Vasenform, minimale Supports |
| Flache Teile (Handplatten) | flach auf dem Bett | maximale Haftung, schnellster Druck |

## Multi-Plate Workflow

Bambu Studio unterstuetzt mehrere Druckplatten in einem Projekt:

1. **"Add Plate"** Button nutzen fuer separate Build Plates
2. Zusammengehoerige Teile auf eine Plate (z.B. linker + rechter Unterarm)
3. **"By Object"** Reihenfolge bei kurzen Teilen (unter ~200 mm)
4. AMS/Vortek nutzen fuer Akzentfarben pro Plate

**Geschaetzte Plates fuer ein komplettes Set: 25-35 Plates**

## Geschaetzte Druckzeiten und Filamentverbrauch

Annahme: 0.4 mm Duese, 0.20 mm Schichthoehe, 3 Waende, 15% Gyroid, PETG, 150-200 mm/s.

| Teil | Druckzeit | Filament (g) | Plates |
| --- | --- | --- | --- |
| Helm (2-3 Teile) | 18-28 h | 350-500 | 2 |
| Brust vorn + hinten | 20-30 h | 400-600 | 3-4 |
| Schulter-Pauldrons (L+R) | 10-16 h | 200-350 | 2 |
| Unterarme (L+R) | 12-18 h | 250-400 | 2-3 |
| Handschutz/Handplatten | 6-10 h | 100-200 | 1-2 |
| Hueft-/Codpiece | 8-12 h | 150-250 | 1-2 |
| Oberschenkel (L+R) | 14-22 h | 300-500 | 3-4 |
| Schienbein/Knieschutz (L+R) | 12-18 h | 250-400 | 2-3 |
| Stiefelcover | 8-12 h | 150-250 | 2 |
| Detailteile (diverse) | 6-10 h | 100-200 | 2-4 |
| **Gesamt** | **~115-175 h** | **~2.250-3.650 g** | **~25-35** |

### Kostenabschaetzung Filament

- PETG bei ca. 20-25 EUR/kg: **ca. 50-90 EUR**
- ASA bei ca. 25-35 EUR/kg: **ca. 60-130 EUR**
- Plus 10-15% Reserve fuer Fehldrucke, Supports und Testteile

### Zeitoptimierung

- **0.6 mm Duese** mit 0.28-0.32 mm Schichthoehe: ~40% weniger Druckzeit (Gesamt sinkt auf ~70-105 h)
- **0.8 mm Duese** fuer nicht-detaillierte Strukturteile
- Bei 24/7 Betrieb: komplettes Set in **1-2 Wochen** reine Druckzeit

## Haeufige Probleme und Loesungen

| Problem | Ursache | Loesung |
| --- | --- | --- |
| Warping/Ecken heben | Thermische Kontraktion | Brim 8 mm+, Bauraum geschlossen, Betttemp +5 C |
| Delamination | Schlechte Schichthaftung | Hotend-Temp +5-10 C, Bauraum geschlossen |
| Sichtbare Nahtlinien | Z-Seam Platzierung | Seam "aligned" auf harte Kante setzen |
| Stringing im Helm-Inneren | Travel-Bewegungen ueber offenen Innenraum | "Avoid crossing perimeters" aktivieren |
| Elephant's Foot | Bett zu nah, First Layer Squish zu hoch | Z-Offset kalibrieren, Elephant Foot Compensation 0.1-0.15 mm |
| Stuetzstruktur-Narben | Supports haften zu stark | Z-Gap auf 0.2 mm erhoehen, Interface-Dichte 100% |
| Teile passen nicht zusammen | Schrumpfung, Toleranz | 0.2-0.3 mm Toleranz auf Passflaechen, Testdruck eines kleinen Verbindungsstuecks |
| Hohle Teile klingen/wackeln | Zu wenig Infill | 15% Gyroid, oder Modifier-Mesh mit hoeherem Infill an Stresspunkten |

## STL-Quellen

Siehe `Resources/STL-Quellen.md` fuer eine kuratierte Liste der besten kostenlosen und kostenpflichtigen Quellen.
