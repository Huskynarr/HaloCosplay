# LED-Visor-Forschung: Praxiswissen fuer Cosplay-Helme

> **Level:** [A] Anfaenger | [F] Fortgeschritten | [P] Profi  |  **Varianten:** alle

Gesammelte Erkenntnisse zu LED-Problemen in Cosplay-Helmen und -Ruestungen, mit konkreten Loesungen, Produktnamen und Techniken aus der Community (405th, RPF, Hackaday, Adafruit, u.a.).

---

## 1. LED-Hotspots und Kamera-Probleme

### Das Problem

LEDs sind Punktlichtquellen. Kameras lesen sie als ueberbelichtete ("blown out") helle Flecken, waehrend das menschliche Auge einen sanften Glow sieht. In Fotos erscheinen LED-bestuekcte Helme oft als helle weisse Flecken statt als atmosphaerisches Leuchten.

### Diffusions-Techniken

| Material | Wirkung | Vorteile | Nachteile |
| --- | --- | --- | --- |
| **Frosted Acrylic (Milchglas-Acryl)** | Gleichmaessige Streuung, professioneller Look | Haltbar, gute Lichtverteilung, leicht zu schneiden | Starr, schlecht fuer Kurven, blockiert mehr Licht als Frosted |
| **Milky/Opal PETG** | Blendet LEDs komplett aus, gleichmaessige Lichtlinie | Bester "solid bar" Effekt, versteckt einzelne LEDs komplett | Blockiert mehr Licht als Frosted-Varianten |
| **Klares PETG/Acryl angeschliffen** | Guenstige DIY-Loesung | Kostet fast nichts, einfach | Ungleichmaessig, Ergebnis variiert |
| **Sanding (Anschleifen)** | Mattiert klare Oberflaeche | Einfach, reversibel (polieren) | Gleichmaessigkeit schwer zu kontrollieren |
| **Privacy Window Film (Sichtschutzfolie)** | Hervorragende Diffusion bei minimaler Dicke | Duenn (~4 mil), flexibel, auf PETG klebbar | Braucht Traegermaterial |
| **Wachspapier/Butterbrotpapier** | Sehr gute Diffusion | Kostenlos, leicht verfuegbar | Nicht haltbar, reisst, kein professioneller Look |
| **Frosted Glass Spray Paint** | Aufspruehbare Diffusion fuer Kurven | Funktioniert auf jeder Form, duenne Schichten moeglich | Schwer exakt zu kontrollieren |
| **LED Foam (Green Stuff World)** | Spezieller Cosplay-Lichtdiffusor-Schaumstoff | Speziell fuer Cosplay-LED-Diffusion entwickelt | Nischenprodukt |
| **Silikon-Diffusor (Dragonflex o.ae.)** | Weich, flexibel | Anpassbar an Kurven | Absorbiert zu viel Licht |

### Kritische Erkenntnis: Der 9mm-Luftspalt

**Wichtigste Erkenntnis aus Experimenten (Hackaday "I Love Lamp" Projekt):**

> "Der Luftspalt zwischen LED und Diffusor muss mindestens 9 mm (1/3 Zoll) betragen, um Hotspots zu eliminieren - unabhaengig vom Diffusionsmaterial."

- **Ziel-Lichttransmission:** 50-60% fuer optimale Diffusion
- Direkter Kontakt zwischen LED und Diffusor erzeugt IMMER Hotspots
- Je weiter der Abstand, desto gleichmaessiger das Licht, aber desto mehr Platz wird benoetigt

### Empfohlene Diffusions-Methode fuer Halo-Visor

1. WS2812B COB Strip an der Oberkante oder Unterkante des Visors montieren
2. Mindestens 9 mm Abstand zum Visor einhalten
3. Privacy Window Film auf die Innenseite einer klaren PETG-Schicht kleben (Spray-Kleber)
4. ODER: Milky PETG als Zwischenschicht hinter dem gold-getoenten Visor

### Mechanische Loesungen

| Loesung | Beschreibung | Einsatz |
| --- | --- | --- |
| **Klapp-Diffusor** | Schwenkbare Diffusionsschicht auf Scharnieren | Hochklappen fuer Fotomodus, runterklappen fuer Convention |
| **Abnehmbare Diffusionspanels** | Mit Magneten oder Klett befestigte Diffusor-Einsaetze | Schneller Wechsel zwischen Setups |
| **Dimmer-Taster** | Physischer Button am Helm/Handschuh fuer Helligkeitsstufen | Schnelle Anpassung an Umgebung |
| **Fernbedienung** | Kleiner IR- oder Bluetooth-Controller | Handler kann Helligkeit anpassen |

---

## 2. LED-Sichtbarkeit durch Gold/Chrome Visor-Toenung

### Wie Gold-Toenung funktioniert

Gold/Chrome-Visiere funktionieren als Farbfilter: Sie absorbieren bestimmte Wellenlaengen und lassen andere durch. Ein Goldfilter absorbiert hauptsaechlich **blaues und violettes Licht** und laesst warme Toene (Rot, Orange, Gelb, Gruen) besser durch.

### Farb-Durchlaessigkeit durch Gold-Visor

| LED-Farbe | Sichtbarkeit durch Gold-Visor | Empfehlung |
| --- | --- | --- |
| **Amber/Gold (R:255, G:180, B:20)** | Ausgezeichnet - wird verstaerkt | Beste Wahl fuer Master Chief Look |
| **Warm-Weiss (3000K)** | Gut - Blaualnteil wird gefiltert, bleibt warm | Gute Alternative |
| **Gruen (R:0, G:200, B:60)** | Gut - Gruen geht durch Gold-Toenung | Cortana/Tech-Akzente |
| **Rot (R:255, G:0, B:0)** | Gut - Rot wird kaum blockiert | Alarm-Effekte |
| **Kuehles Weiss (6000K+)** | Maessig - wirkt verwaschen durch Goldfilter | Vermeiden |
| **Blau (R:0, G:0, B:255)** | Schlecht - wird vom Goldfilter stark absorbiert | Ungeeignet hinter Gold-Visor |
| **Violett/UV** | Sehr schlecht - fast unsichtbar | Nicht verwenden |

### Praxis-Tipps

- **Reines Weiss vermeiden** - sieht durch goldene Toenung verwaschen und farbstichig aus
- **Amber/Gold LEDs** wirken am natuerlichsten hinter einem Gold-Visor, weil sie die Toenung verstaerken statt ihr zu widersprechen
- **Toenung-Intensitaet:** Je staerker die Gold-Toenung (geringere VLT = Visible Light Transmission), desto heller muessen die LEDs sein
- **Mirror/Chrome-Visiere** blockieren mehr Licht als getoente Visiere - LEDs brauchen deutlich mehr Helligkeit, um durchzudringen
- **Dual-Layer-Visor-Technik (405th):** Innen klarer Visor + aussen getoenter Visor mit Aussparungen - LEDs leuchten nur durch die gewollten Bereiche

### Dual-Layer-Visor fuer LED-Effekte

Eine bewaehrte 405th-Community-Technik:
1. Untere Schicht: Klarer oder leicht getoenter Motorrad-Visor (ungealtered)
2. Obere Schicht: Zweiter getoenter/verspiegelter Visor mit ausgeschnittenen Design-Elementen
3. LEDs hinter dem klaren Bereich platzieren - Licht strahlt nur durch die offenen Bereiche

---

## 3. Beste LED-Typen fuer Helm-Visiere

### Vergleich der LED-Technologien

| Technologie | Hotspot-frei? | Helligkeit | Steuerbar | Stromverbrauch | Flexibilitaet | Preis |
| --- | --- | --- | --- | --- | --- | --- |
| **WS2812B Strip (Standard, 60 LED/m)** | Nein - deutliche Punkte | Hoch | Individuell adressierbar | ~60 mA/LED bei Weiss | Gut | Guenstig (~5 EUR/m) |
| **WS2812B Strip (144 LED/m)** | Leicht - dichter, aber noch sichtbar | Hoch | Individuell adressierbar | ~60 mA/LED bei Weiss | Gut | Mittel (~10 EUR/m) |
| **WS2812B COB Strip (160 LED/m)** | Weitgehend ja | Mittel (dimmer als Standard) | Individuell adressierbar | ~1.8 A/m bei Einzelfarbe | Sehr gut | ~13 EUR/m |
| **WS2812B COB Strip (320 LED/m)** | Ja - dot-free | Mittel | Individuell adressierbar | ~8 W/m bei Einzelfarbe | Sehr gut | ~15-20 EUR/m |
| **SK6812 (RGBW, 320 LED/m COB)** | Ja - dot-free | Mittel-Hoch (weisser Kanal) | Individuell adressierbar | Aehnlich WS2812B | Sehr gut | ~18-25 EUR/m |
| **Standard COB Strip (nicht adressierbar)** | Ja | Hoch | Nur gesamt (ein/aus/dimmen) | Variiert | Sehr gut | Guenstig |
| **EL Wire** | Ja - 360-Grad-Glow | Niedrig | Nur ein/aus | Gering (~100 mA) | Hervorragend | Guenstig |
| **EL Panel** | Ja - voellig gleichmaessig | Niedrig | Nur ein/aus/dimmen | Gering | Begrenzt (flach) | Mittel |
| **Side-Emitting LED Strip** | Teilweise | Mittel | Je nach Typ | Aehnlich Standard | Gut | Mittel |
| **Fiber Optic (Side-Glow)** | Ja - gleichmaessige Linie | Niedrig-Mittel | Ueber Quell-LED | Sehr gering (1 LED pro Ende) | Hervorragend | Mittel |
| **LED Light Pipes/Light Guides** | Ja | Mittel | Ueber Quell-LED | Gering | Begrenzt | Mittel-Hoch |

### Empfehlung fuer Halo-Helm-Visor

**Beste Wahl: WS2812B COB Strip (320 LED/m)**

- Dot-free, gleichmaessiger Glow
- Adressierbar fuer Effekte (Breathing, Boot-Up, Chase)
- 5V Betrieb (kompatibel mit Arduino/Pi Setup)
- Vorinstallierter Silikon-Diffusor reduziert bereits Hotspots
- Konkrete Produkte:
  - **BTF-LIGHTING FCOB WS2812B** (Amazon, ~15-20 EUR/m)
  - **SuperLightingLED WS2812B COB 320 chips/m** (~13-18 EUR/m)

**Budget-Alternative: EL Wire**

- Fuer einfachen Akzent-Glow ohne Programmierung
- Kein Hotspot-Problem, 360-Grad-Glow
- Deutlich weniger hell - in hellen Convention-Hallen kaum sichtbar
- Braucht separaten Inverter/Driver (HV AC, leises Surren moeglich)
- Nicht lange haltbar bei Biegung (Phosphor degradiert)

### EL Wire vs LED Strip - Detailvergleich

| Eigenschaft | EL Wire | LED Strip (WS2812B) |
| --- | --- | --- |
| **Helligkeit** | Gering - in hellen Raeumen kaum sichtbar | Hoch - auch in hellen Hallen sichtbar |
| **Stromverbrauch** | Niedrig (~100-200 mA fuer 2m) | Hoch (bis 3.6 A fuer 60 LEDs weiss bei 100%) |
| **Akku-Laufzeit** | 10-20 Stunden mit 2x AA | 3-8 Stunden mit Powerbank (je nach Helligkeit) |
| **Flexibilitaet** | Extrem flexibel, biegbar in jede Form | Flexibel, aber nur in einer Ebene |
| **Gleichmaessigkeit** | Perfekt gleichmaessig | Hotspots bei Standard-Strips, gut bei COB |
| **Farbwechsel** | Nein (Farbe fest bei Kauf) | Ja, 16 Mio Farben, programmierbar |
| **Haltbarkeit** | Fragil - Phosphor degradiert bei Biegung | Robust - langlebig |
| **Waerme** | Kuehl | Leicht warm (siehe Abschnitt 5) |
| **Geraeusch** | Leises Surren vom Inverter moeglich | Lautlos |
| **Kamera-Verhalten** | Hervorragend - neonartiger, weicher Glow | Problematisch ohne Diffusion |

---

## 4. Visor LED-Montage: Techniken und Platzierung

### Montage-Optionen

| Methode | Beschreibung | Vorteile | Nachteile |
| --- | --- | --- | --- |
| **Hinter Diffusionsschicht** | LEDs hinter milchigem Material, vor dem Visor | Gleichmaessig, keine Hotspots bei genug Abstand | Braucht 9+ mm Tiefe, reduziert Sicht |
| **Inside-Top-Mount** | LED-Strip an der Oberkante innen im Helm, Licht nach unten auf Visor | Sicht nicht blockiert, einfache Montage | Ungleichmaessig (oben heller als unten) |
| **Inside-Bottom-Mount** | LED-Strip an der Unterkante, Licht nach oben | "Uplighting"-Effekt, dramatisch | Sicht etwas eingeschraenkt, Licht faellt auf Kinn |
| **Edge-Lit Acrylic** | LEDs in die Kante einer Acrylplatte eingespeist | Extrem gleichmaessig, professionell, sehr duenn | Komplex zu bauen, braucht praezises Acryl |
| **Hinter dem Visor (direkt)** | LEDs direkt auf die Visor-Innenseite geklebt | Einfach | Hotspots, blendet den Traeger, unprofessionell |
| **Zwischen Dual-Layer** | LEDs im Zwischenraum zweier Visor-Schichten | Geschuetzt, gleichmaessig | Aufwendig, schwer wartbar |

### Edge-Lit Acrylic - Detaillierte Technik

Edge-Lit ("kantenbeleuchtete") Acrylpanels funktionieren wie Laptop-Display-Hintergrundbeleuchtungen:

1. **Material:** Klares, poliertes Acrylglas (3-5 mm dick)
2. **Prinzip:** LEDs werden in die Kante bei 90 Grad zur Betrachtungsflaeche eingespeist
3. **Lichtleitung:** Licht prallt fiber-optisch-artig im Acryl umher
4. **Streuung:** Eine aufgebrachte Diffusionsschicht (Mattierung, Folie, Aetzung) auf der Vorderseite streut das Licht gleichmaessig nach vorne
5. **Muster:** Fuer gleichmaessige Ausleuchtung koennen Punkte oder Muster auf die Rueckseite gedruckt/geaetzt werden (wie bei Laptop-Displays), die die Lichtintensitaet von der Kante zur Mitte ausgleichen

**Vorteile fuer Helm-Visor:**
- Extrem duenner Aufbau (3-5 mm Gesamttiefe)
- Voellig gleichmaessig bei richtigem Design
- LEDs sind am Rand versteckt, nicht im Sichtfeld
- Kann gekruemmt werden (bei duennerem Acryl oder PETG)

**Nachteile:**
- Komplex in der Herstellung
- Schwieriger fuer stark gekruemmte Visor-Formen
- Licht wird zu den Kanten hin dunkler ohne Kompensation

### Empfohlene Montage fuer Halo Master Chief Helm

1. **LED-Strip:** WS2812B COB (320 LED/m) entlang der inneren Oberkante des Helms
2. **Abstand:** Mind. 9 mm zwischen Strip und Visor
3. **Diffusion:** Milky PETG Zwischenschicht ODER Privacy Film auf klarer PETG-Schicht
4. **Visor:** Gold-getoenter Visor als aeusserste Schicht
5. **Befestigung:** Klett-Befestigung fuer Wartbarkeit, alternativ Heisskleber fuer permanente Montage

---

## 5. LED und Waerme im Helm

### Waermeentwicklung von LEDs

| Szenario | Waerme | Beurteilung |
| --- | --- | --- |
| 10 WS2812B LEDs bei 50% | ~0.5 W Waerme | Vernachlaessigbar |
| 30 WS2812B LEDs bei 100% Weiss | ~5 W Waerme | Spuerbar in geschlossenem Helm |
| 10 COB LEDs bei 50% Einzelfarbe | ~0.3 W Waerme | Vernachlaessigbar |
| 60 LEDs bei 100% Weiss | ~10 W Waerme | Signifikant - entspricht kleiner Gluehbirne |

### COB Strip Temperatur-Messungen (aus Review)

Aus dem Hackaday/Crucible-Review von 240 LED/m COB WS2812B Strips:
- **Im offenen Aluprofile:** Temperaturanstieg von 22 C auf 58 C in 15 Minuten bei 75% Helligkeit
- **Empfehlung:** 80-100% Einzel-Farb-Helligkeit maximal 5 Minuten, dann abkuehlen lassen (in geschlossenen Roehren)
- **Fuer Helme:** Bei 50% Helligkeit und Einzelfarbe (nicht Weiss) ist die Waerme minimal

### Waermemanagement im Helm

| Massnahme | Wirkung | Empfehlung |
| --- | --- | --- |
| **LED-Helligkeit auf 50% begrenzen** | Halbiert Waerme UND Stromverbrauch | Immer als Default |
| **Einzelfarbe statt Weiss** | 1/3 der Waerme von Weiss | Gruenes/Amber Leuchten statt Weiss |
| **Luefter einbauen** | Aktive Kuehlung, auch fuer Komfort | 40 mm Luefter oben (Auslass) + unten (Einlass) |
| **Henry's Helmet Fans** | Bewaehltes Dual-Fan-System fuer Cosplay-Helme | 4500 RPM, Dual Ball Bearing, USB-betrieben |
| **Kurze LED-Segmente** | Weniger aktive LEDs = weniger Waerme | Nur den sichtbaren Visor-Bereich bestuecken |
| **Pausen einlegen** | Helm regelmaessig abnehmen | Alle 30-45 Min, besonders bei warmer Umgebung |

### Fazit Waerme

Fuer einen typischen Halo-Helm mit 10-20 LEDs bei 50% Helligkeit in Einzelfarbe (Amber/Gruen) ist die **Waerme durch LEDs vernachlaessigbar** - sie produzieren weniger als 1 Watt Waerme. Das Hauptproblem ist die Koerperwaerme des Traegers und mangelnde Belueftung, nicht die LEDs selbst. Luefter sind wichtiger fuer den Komfort als fuer LED-Kuehlung.

---

## 6. Haeufige LED-Ausfaelle auf Conventions

### Ausfallursachen (sortiert nach Haeufigkeit)

| # | Problem | Ursache | Haeufigkeit |
| --- | --- | --- | --- |
| 1 | **Akku leer** | Zu klein dimensioniert, vergessen zu laden | Sehr haeufig |
| 2 | **Lockere Steckverbindung** | Erschuetterungen beim Laufen, Anfassen | Sehr haeufig |
| 3 | **Kabelbruch** | Wiederholtes Biegen, Zug an Loestellen | Haeufig |
| 4 | **Kalte Loetstelle** | Vibration loest schlechte Loetung | Haeufig |
| 5 | **SD-Karte korrupt** | Pi startet nicht nach Stromunterbrechung | Gelegentlich |
| 6 | **Software-Absturz** | Python-Fehler, Memory Leak nach Stunden | Gelegentlich |
| 7 | **Kurzschluss** | Blosse Draehte beruehren Metallteile/einander | Selten, gefaehrlich |
| 8 | **LED-Strip-Defekt** | Einzelne LEDs sterben, ganze Kette faellt aus | Selten |
| 9 | **Hitze-Shutdown** | Controller ueberhitzt in geschlossenem Helm | Selten |

### Praevention - Checkliste

**Vor der Convention:**
- [ ] Alle Akkus voll laden (am Vorabend)
- [ ] Ersatzakku/Powerbank einpacken
- [ ] Jede LED-Verbindung physisch testen - dran ziehen, wackeln
- [ ] Multimeter-Check: Spannung an jedem Steckverbinder messen
- [ ] 30-Minuten-Tragetest im Kostuem (alle Systeme gleichzeitig an)
- [ ] SD-Karte als Read-Only mounten (verhindert Korruption)

**Bau-Massnahmen:**
- [ ] **Loeten statt Stecken** wo immer moeglich
- [ ] **Heisschrumpfschlauch** auf JEDE Loetstelle
- [ ] **Zugentlastung** an allen Kabel-Austritten (Kabelbinder + Heisskleber)
- [ ] **Konforme Beschichtung** (Conformal Coating) auf Arduino/Pi-Platinen
- [ ] **JST-Stecker** statt DuPont-Verbindungen (rasten ein, fallen nicht raus)
- [ ] **330 Ohm Widerstand** am Data-In des ersten LED-Pixels
- [ ] **1000 uF Elko** an 5V/GND des LED-Strips (Spannungsspitzen beim Einschalten)
- [ ] **74AHCT125 Level Shifter** zwischen Pi (3.3V) und LEDs (5V)

**Auf der Convention:**
- [ ] Elektronik-Notfall-Kit mitnehmen: Powerbank, Reservekabel, Isolierband, kleiner Loetkolben (Batterie-betrieben)
- [ ] Handler soll Ersatzteile tragen
- [ ] Bei Regen: alle Elektronik sofort schuetzen oder abschalten

### Verbindungs-Upgrade-Pfad

| Schlecht | Besser | Am Besten |
| --- | --- | --- |
| DuPont-Stecker | JST-SM-Stecker (einrastend) | Geloetet + Heisschrumpfschlauch |
| Steckbrett (Breadboard) | Perfboard mit Loetung | Custom-PCB oder Klemmen |
| Normaler Draht | Silikon-Litzenkabel (flexibel) | Silikon-Kabel + Zugentlastung + Spiralschlauch |
| Klebeband | Isolierband | Heisschrumpfschlauch + Conformal Coating |

---

## 7. Das "Photo Mode"-Problem

### Das Problem im Detail

LEDs, die in Person gut aussehen, sehen auf Fotos schlecht aus - und umgekehrt:

| Situation | In Person | Auf Kamera |
| --- | --- | --- |
| LEDs bei 100%, helle Halle | Angenehm sichtbar | Komplett ueberbelichtet, weisse Flecken |
| LEDs bei 25%, dunkler Raum | Subtil, stimmungsvoll | Perfektes Glow-Foto |
| LEDs bei 50%, Convention-Halle | Standard-Look | Helle Punkte, aber akzeptabel |
| LED-Effekte (Breathing, Chase) | Lebendig, dynamisch | Banding-Streifen bei kurzem Shutter |
| EL Wire bei 100% | Kaum sichtbar in heller Halle | Gleichmaessiger, neonartiger Glow |

### PWM-Banding auf Fotos

**Problem:** PWM-gedimmte LEDs schalten schnell ein und aus. Wenn die Kamera-Verschlusszeit mit dem PWM-Zyklus interferiert, entstehen dunkle Streifen im Bild.

**Technische Details:**
- Standard-Arduino `analogWrite`: 490 Hz PWM - erzeugt sichtbare Streifen bei den meisten Kameras
- WS2812B/NeoPixel internes PWM: ~500 Hz (~2 ms pro Zyklus) - Banding moeglich bei 1/500s oder kuerzerer Belichtung
- **Sichere Frequenz fuer Fotografie:** > 25.000 Hz (25 kHz)
- NeoPixel-Library nutzt eigenes Timing und ist bei statischen Farben weitgehend foto-sicher
- **Problem tritt hauptsaechlich auf bei:** sich aendernden Farben/Helligkeiten waehrend der Belichtung

**Banding-Loesung:**
- Bei statischem Leuchten (konstante Farbe, konstante Helligkeit): Kein Banding
- Bei Effekten (Breathing, Chase): Effekt-Geschwindigkeit verlangsamen oder fuer Fotos pausieren
- Fotografen bitten, laengere Belichtungszeiten zu nutzen (1/60s oder laenger)

### Loesung: Brightness-Preset-System mit Taster

Einen physischen Button am Helm einbauen, der zwischen vordefinierten Modi wechselt:

```
Mode 1: Convention  - 50% Helligkeit, statisch oder langsames Breathing
Mode 2: Foto Hell   - 100% Helligkeit, statisch (fuer helle Umgebung)
Mode 3: Foto Dunkel  - 25% Helligkeit, statisch (fuer dunkle Fotoshootings)
Mode 4: Effekte     - Breathing/Boot-Up/Chase bei 70%
Mode 5: Aus         - Alles aus (Spar-Modus)
```

**Arduino-Implementierung:** Siehe `Code/HelmetControl/MainControlCode.ino` fuer das bestehende Setup. Ein Taster an einem digitalen Pin, der bei jedem Druck den Modus hochzaehlt.

### Empfehlungen fuer Fotografen

Wenn ein Fotograf ein Foto mit LED-Helm macht:

| Kamera-Einstellung | Empfohlener Wert | Grund |
| --- | --- | --- |
| **Modus** | Manuell (M) | Auto macht LEDs zu hell/dunkel |
| **ISO** | 100-400 | Niedriger = weniger LED-Ueberbelichtung |
| **Verschlusszeit** | 1/60 - 1/125 | Lang genug fuer PWM, kurz genug fuer Schaerfe |
| **Blende** | f/4 - f/5.6 | Balance zwischen Schaerfe und Lichtmenge |
| **Weissabgleich** | Tageslicht oder Manuell | AUTO verfaelscht LED-Farben massiv |
| **HDR** | Ja, wenn moeglich | Kombination: dunkles Bild (LED-Farben) + helles Bild (Details) |
| **RAW** | Ja | Nachtraegliche Korrektur moeglich |
| **ND-Filter** | Optional, bei extremer LED-Helligkeit | Reduziert Gesamtlicht zum Sensor |

**HDR-Technik fuer LED-Props:**
Zwei Belichtungen kombinieren:
1. Sehr dunkel (Platine/Helm kaum sichtbar, LED-Farben perfekt)
2. Normal belichtet (Details sichtbar, LEDs ueberbelichtet)
In der Nachbearbeitung zusammenfuehren fuer "brillante LEDs mit sichtbaren Details"

### Praxis-Workflow auf Conventions

1. **Convention-Floor:** LEDs auf 50% static oder langsames Breathing, sieht gut in Person aus
2. **Foto-Request in heller Halle:** Button druecken auf "Foto Hell" (100% static), Fotograf nimmt Bild auf, zurueck auf Convention-Modus
3. **Geplantes Fotoshooting (dunkel):** LEDs auf 25% static, Fotograf nutzt Stativ, ISO 100, f/4, Langzeitbelichtung
4. **Video:** LEDs auf statisch (kein Effekt-Wechsel), um Banding/Flicker zu vermeiden

---

## Quellen und weiterfuehrende Links

### Community-Foren
- [405th - Halo Costume and Prop Maker Community](https://www.405th.com/forums/)
- [RPF - Replica Prop Forum](https://www.therpf.com/forums/)
- [Adafruit Forums - Cosplay](https://forums.adafruit.com/)

### Produkte und Haendler
- [BTF-LIGHTING FCOB WS2812B COB Strip (Amazon)](https://www.amazon.com/BTF-LIGHTING-Individual-Addressable-Flexible-Controller/dp/B0CNXKSWD7)
- [SuperLightingLED WS2812B COB 320 chips/m](https://www.superlightingled.com/newest-ws2812b-320-chipsm-addressable-rgb-cob-led-light-dc5v-dream-color-flexible-cob-led-strips-1m328ft-per-roll-p-3723.html)
- [Henry's Helmet Fans](https://henryshelmetfans.com/)
- [Green Stuff World LED Foam](https://www.greenstuffworld.com/en/570-led-foam)
- [Ellumiglow - EL Wire und LED fuer Cosplay](https://ellumiglow.com/pages/best-lighting-for-cosplay-costumes)

### Technische Referenzen
- [Hackaday LED Diffusion Experiments](https://hackaday.io/project/20121-i-love-lamp/log/59085-led-diffusion-experiments-some-results)
- [COB WS2812B Strip Review (The Crucible)](https://crucible.hubbe.net/t/review-of-240led-m-rgb-cob-ws2812b-strips/4797)
- [Evil Mad Scientist - Photographing LEDs](https://www.evilmadscientist.com/2009/photographing-leds/)
- [Waveform Lighting - Flicker Free LED Dimming](https://www.waveformlighting.com/film-photography/an-introduction-to-flicker-free-led-strip-dimming)
- [TI Technical Article - PWM Dimming](https://www.ti.com/lit/ta/ssztay6/ssztay6.pdf)
- [Photo-Spectrum - PWM Banding](https://www.photo-spectrum.info/pages/illumination/PWM-banding-readout.html)
- [Cosplay 3D Print - LED Integration Guide](https://cosplay3dprint.com/3d-printed-cosplay-helmets-safe-led-integration-guide-tips-techniques/)
- [The Star Forge - LED Guide for Cosplay](https://thestarforge.org/led-guide-for-cosplay-props-and-armor/)

### Anleitungen
- [405th - Dual Layer Visor Tutorial](https://www.405th.com/forums/threads/dual-layer-visor-mini-tutorial.1073/)
- [405th - Visor Tutorial](https://www.405th.com/forums/threads/visor-tutorial.29341/)
- [Instructables - LED Space Helmet](https://www.instructables.com/LED-Space-Helmet/)
- [SparkFun - Getting Started with EL Wire](https://learn.sparkfun.com/tutorials/getting-started-with-electroluminescent-el-wire/all)
