# Armor Step 2: Druck, Zusammenbau, Finish, Montage

## Voraussetzung

- Skalierung getestet (Step 1)
- Unteranzug und Tragesystem vorhanden
- Filament bestellt (mind. 4 kg PETG)

## 1. Drucken

Detaillierte Druckeinstellungen: siehe `Documentation/Guides/3D-Druck.md`

### Workflow pro Teil

1. STL in Bambu Studio laden
2. Skalierung anwenden (pro Koerperregion)
3. Falls noetig: Cut Tool (Taste C) zum Splitten
4. Druckorientierung waehlen (siehe 3D-Druck Guide)
5. Tree Supports aktivieren
6. Slicen und an Drucker senden
7. Nach dem Druck: Supports entfernen, Qualitaet pruefen

### Parallel arbeiten

- Waehrend ein Teil druckt, das vorherige schleifen/spachteln
- Multi-Plate Projekte nutzen fuer Ueber-Nacht-Drucke
- Linke und rechte Seite zusammen auf einer Plate

### Zusammenkleben (bei gesplitteten Teilen)

1. Klebenaehte anschleifen (120er)
2. CA-Kleber fuer sofortige Fixierung
3. Epoxy auf der Innenseite entlang der Naht fuer Struktur
4. 24h aushaerten lassen
5. Ueberstand auf der Aussenseite abschleifen

## 2. Oberflaechen-Finish

Detailliert: `Documentation/Guides/Lackierung-Finishing.md`

### Kurzversion pro Teil

1. **Grob-Schliff:** 120er Koernung — Layer Lines, Support-Narben, Naehte
2. **Fein-Schliff:** 240er Koernung
3. **Filler Primer** aufspruehen — trocknen — **320er schleifen**
4. Schritt 3 **wiederholen** (2-3 Zyklen bis Layer Lines weg)
5. **Spachtel:** Bondo/XTC-3D auf tiefe Stellen und Klebelinien
6. **Finaler Primer** — gleichmaessige Schicht
7. **Grundfarbe:** Oregano Satin (3-4 duenne Schichten)
8. **Trocknen:** 24-48h vor Weathering
9. **Weathering:** Wash > Dry Brush > Battle Damage > Schwamm
10. **Klarlack:** Matte Clear Coat (3-4 Schichten)
11. **Durchtrocknen:** 48h

### Reihenfolge Finish

Nicht alle Teile gleichzeitig! Arbeite in Batches:
- **Batch 1:** Helm (Schwerpunkt, laengstes Finish)
- **Batch 2:** Unterarme + Schienbeine (klein, schnell, gut zum Ueben)
- **Batch 3:** Brustplatte + Rueckenpanzer (gross, braucht Platz)
- **Batch 4:** Schultern + Oberschenkel
- **Batch 5:** Rest (Handplatten, Codpiece, Stiefelcover, Details)

## 3. Befestigungssystem einbauen

Detailliert: `Documentation/Guides/Unteranzug-Befestigung.md`

### Innen-Vorbereitung pro Teil

1. **Polsterung:** 6 mm EVA-Foam auf Innenseiten kleben (Kontaktkleber)
   - Fokus auf Druckstellen: Kanten die auf Haut treffen, Auflagepunkte
   - NICHT die gesamte Innenseite — Luft muss zirkulieren
2. **Klett-Felder:** Industrial Velcro (Hook-Seite) auf Innenseite kleben
   - Korrespondierende Loop-Seite auf Morphsuit naeaehen
3. **Magnete:** Neodym 10x3 mm in 3D-gedruckten Haltern mit Epoxy einkleben
   - **Polaritaet pruefen und markieren!** (mit Edding vor dem Einkleben)
4. **Gurt-Schlaufen:** Nylon-Gurtband (25 mm) Schlaufen an schweren Teilen mit Nieten oder Schrauben

### Schwere Teile (Brust, Ruecken, Oberschenkel)

1. Gurt-Schlaufen innen befestigen
2. Quick-Release Schnallen an Gurtband
3. Verbindung zum Klettergurt/MOLLE-Guertel
4. **Testen:** Teil anhaengen, bewegen, sicherstellen dass es nicht rutscht

### An- und Auszieh-Reihenfolge planen

1. Unteranzug anziehen
2. Klettergurt/Guertel anlegen
3. Schienbeine + Stiefelcover
4. Oberschenkel
5. Hueft-/Codpiece
6. Brustplatte + Rueckenpanzer
7. Schultern
8. Oberarme + Unterarme
9. Handplatten
10. **Helm zuletzt** (braucht volle Armbeweglichkeit zum Aufsetzen)

**Ausziehen:** Umgekehrte Reihenfolge. Helm zuerst runter.

## 4. Passform-Tests

### Test 1: Statisch

- [ ] Alle Teile sitzen an der richtigen Position
- [ ] Nichts rutscht oder faellt ab
- [ ] Kein Teil drueckt oder scheuert
- [ ] Gewicht fuehlt sich auf der Huefte an (nicht auf Schultern)

### Test 2: Bewegung

- [ ] Gerade gehen (10 Minuten)
- [ ] Treppen steigen und absteigen
- [ ] Sich setzen (auf Stuhl, auf Boden)
- [ ] Arme ueber den Kopf heben
- [ ] Sich buecken (etwas vom Boden aufheben)
- [ ] Sich umdrehen (360 Grad)
- [ ] Durch eine Standardtuer gehen

### Test 3: Alltag

- [ ] Toilette erreichbar ohne Komplett-Demontage (Codpiece/Oberschenkel schnell loesbar?)
- [ ] Trinken moeglich (CamelBak-Schlauch erreichbar?)
- [ ] Handy-Zugriff (Tasche in Unteranzug oder Handler-Loesung?)
- [ ] Kann jemand anderes dir beim Ausziehen helfen?

### Test 4: Ausdauer

- [ ] 30 Minuten am Stueck tragen (Minimum fuer Convention)
- [ ] Temperatur ertraeglich?
- [ ] Kein Taubheitsgefuehl oder starke Druckstellen?
- [ ] Notausstieg getestet (Schnellverschluesse funktionieren, Helm schnell ab)

## 5. Probleme und Loesungen

| Problem | Loesung |
| --- | --- |
| Teil rutscht nach unten | Mehr Klett/Magnete, Gummiband als Sicherung |
| Teil dreht sich | Zweiten Befestigungspunkt hinzufuegen |
| Reibung/Scheuern | Mehr EVA-Polsterung an der Stelle |
| Zu schwer auf Schultern | Last auf Guertel umverteilen, Gurtpunkte aendern |
| Kein Armheben moeglich | Schulterstueck kuerzen oder Ausschnitt vergroessern |
| Kann nicht sitzen | Oberschenkel-Befestigung lockerer, mehr Klett statt starrer Gurte |
| Lack platzt bei Bewegung | Flexibleren Klarlack nutzen, bewegliche Stellen nicht dick lackieren |
