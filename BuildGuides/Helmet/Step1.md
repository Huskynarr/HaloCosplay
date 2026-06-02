# Helmet Step 1: Shell, Visor, Innenraum

> **Level:** [F] Fortgeschritten | [P] Profi  ·  **Varianten:** V2/V3 (3D-Druck mit HUD)  ·  **Voraussetzungen:** Massband, 3D-Drucker und Slicer, Schleif-/Klebewerkzeug; Begriffe siehe `Documentation/Guides/Glossar.md`

## Ziele

- Stabiler Helm mit klarer Sicht und Platz fuer Elektronik
- Passform: eng genug dass er nicht wackelt, weit genug fuer Polster + Luefter + OLED

## Skalierung und Vorbereitung

1. **Kopfumfang messen** — Massband um die breiteste Stelle (Stirn ueber Hinterkopf), typisch 56-62 cm
2. **Kopfhoehe messen** — Kinn bis Scheitel
3. **STL skalieren:**
   - Galactic Armory: Standard-Skalierung ist 183 cm / 91 kg. Anpassen nach eigenen Massen
   - MakerWorld MJOLNIR GEN3: kommt bei 20% — auf 100% hochskalieren, dann nach Koerpermassen anpassen
   - **Tipp:** Innenraum des Helms muss mindestens Kopfumfang + 3-4 cm sein (Polsterung + Luefter)
4. **Testdruck:** Ein kleines Segment drucken und am Kopf pruefen bevor der ganze Helm gedruckt wird

## 3D-Druck des Helms

### Splitting

- Helm passt nicht in einem Stueck auf den H2C (ca. 280-320 mm hoch, 250-280 mm breit)
- **Horizontaler Schnitt** auf Visor-Hoehe oder **vertikaler Schnitt** (linke/rechte Haelfte)
- Bambu Studio Cut Tool (Taste C) nutzen, Schwalbenschwanz-Verbinder aktivieren
- Bei Galactic Armory Dateien: bereits vorgeschnitten

### Druckeinstellungen

- **Material:** PETG empfohlen (schlagfest, hitzebestaendig)
- **Schichthoehe:** 0.16-0.20 mm (Helm ist das Highlight-Stueck)
- **Waende:** 4-6 (Stabilitaet!)
- **Infill:** 10-15% Gyroid
- **Orientierung:** Visier/Gesichtsseite nach unten auf das Druckbett — Dome druckt aufwaerts
- **Supports:** Tree Supports, nur auf Druckplatte
- Geschaetzte Druckzeit: 18-28 Stunden (2-3 Teile)

### Zusammenbau

1. Stuetzstrukturen sauber entfernen (Zange, Cutter)
2. Klebenaehte anschleifen (120er Koernung)
3. **CA-Kleber (Sekundenkleber)** fuer initiale Fixierung — haelt sofort
4. **Epoxy (2K)** entlang der Innennaehte fuer strukturelle Staerke — 24h aushaerten lassen
5. Passstifte/Schwalbenschwaenze erleichtern die Ausrichtung

## Oberflaechenbearbeitung

Detailliert in `Documentation/Guides/Lackierung-Finishing.md`, hier die Helm-Kurzversion:

1. **Schleifen:** 120 > 240 > Filler Primer > 320 > Filler Primer > 400 (2-3 Zyklen)
2. **Naehte spachteln:** Bondo Spot Putty oder XTC-3D auf die Klebelinien, schleifen bis unsichtbar
3. **Finale Grundierung:** gleichmaessige Schicht normaler Primer
4. **Qualitaetscheck:** Helm gegen Licht halten — Unebenheiten werden sichtbar

## Visor

### Vakuumformen

1. **Visor-Buck drucken** — Positivform der Visor-Oeffnung, 1-2 mm kleiner als die Oeffnung
   - Infill: 30-50% (muss Vakuumdruck standhalten)
   - Glaett-Finish (schleifen + Primer)
2. **PETG-Folie (0.75-1 mm)** in Rahmen einspannen
3. Auf ca. 140-155 C erwaermen bis die Folie durchhaengt
4. Ueber Buck legen und Vakuum anlegen (Staubsauger reicht fuer DIY)
5. Abkuehlen lassen, mit Schere/Dremel zuschneiden

### Toenung

1. **iDye Poly (Gold/Orange)** im Heisswasserbad — dauerhafte Faerbung
2. **Krylon Looking Glass** auf die INNENSEITE spruehen (in die Luft spruehen, Visor durch Nebel fuehren)
3. Mehrere duenne Durchgaenge fuer gewuenschte Reflexion
4. Optional: duenner Klarlack ueber Chrome-Schicht innen zum Schutz

### Einbau

- Visor von innen mit 3D-gedruckten Clips oder Epoxy-Punkten befestigen
- **Nicht vollstaendig verkleben** — Visor muss austauschbar sein (geht kaputt, beschlaegt, etc.)
- 1-2 mm Spalt oben und unten fuer Luftzirkulation

## Innenraum vorbereiten

### Polsterung

- **Airsoft/Taktik-Helm-Padding Kit** (Klett-Rueckseite, Memory Foam)
- An den Seiten und oben positionieren — NICHT an Visor-Oeffnung oder Luefter-Positionen
- Klett-basiert = abnehmbar fuer Reinigung und Repositionierung
- **Kinnriemen** montieren (Motorrad- oder Fahrrad-Typ)

### Platz reservieren fuer Elektronik

Beim Innenausbau Platz freilassen fuer:
- OLED-Display: 3-5 cm vor dem dominanten Auge
- Pi Zero 2 W: Nackenbereich
- 2x 40 mm Luefter: unten hinten (Intake) + oben hinten (Exhaust)
- Kabelkanal: seitlich vom Pi zum Display
- Quick-Disconnect: Nacken/Hals-Uebergang

Halterungen fuer OLED und Pi koennen mitgedruckt oder separat gedruckt und eingeklebt werden.

## Passform-Check

Bevor du zum Finish (Step 2) gehst:

- [ ] Helm sitzt stabil auf dem Kopf (wackelt nicht)
- [ ] Visor gibt ausreichend Sicht (nach vorne, nach unten zu den Fuessen)
- [ ] Kinn/Nacken nicht zu eng (Kopf muss rein- und rauskoennen!)
- [ ] Genug Platz fuer Elektronik (Display, Pi, Luefter)
- [ ] Polsterung bequem bei 30+ Minuten Tragen
- [ ] Luftzirkulation moeglich (nicht alles luftdicht verschlossen)
