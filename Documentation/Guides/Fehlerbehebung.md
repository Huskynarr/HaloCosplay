# Fehlerbehebung

> **Level:** [A] Anfaenger | [F] Fortgeschritten | [P] Profi  ·  **Varianten:** alle

Haeufige Probleme und Loesungen, geordnet nach Kategorie.

## Elektronik

### Display bleibt schwarz

| Pruefschritt | Wie | Erwartet |
| --- | --- | --- |
| I2C-Adresse | `i2cdetect -y 1` | 0x3C oder 0x3D sichtbar |
| Spannung | Multimeter an VCC/GND | 3.3V (NICHT 5V!) |
| Kabel | SDA und SCL vertauschen und testen | Oft falsch angeschlossen |
| Verbindung | Stecker fest? Kabel durchmessen | Durchgang auf allen 4 Leitungen |

Falls `i2cdetect` keine Adresse zeigt: I2C nicht aktiviert (`raspi-config` pruefen) oder Hardware-Defekt.

### Pi startet staendig neu

| Ursache | Diagnose | Loesung |
| --- | --- | --- |
| Unterspannung | `vcgencmd get_throttled` (nicht 0x0) | Dickeres USB-Kabel, staerkere Powerbank (min 2A) |
| USB-Kabel zu duenn/lang | Spannung am Pi messen (muss >4.8V sein) | Kurzes, dickes Kabel (max 30 cm fuer Daten) |
| Defekte SD-Karte | Boot-Schleife, kein SSH | SD-Karte neu flashen, Marken-SD nutzen |
| Zu viel Last | Passiert bei vielen Peripheriegeraeten | Peripherie einzeln testen, Sternverkabelung |

### LEDs flackern

| Ursache | Diagnose | Loesung |
| --- | --- | --- |
| Fehlende gemeinsame Masse | GND von LED-Strip und Arduino/Pi nicht verbunden | ALLE GND zusammenfuehren! |
| Datenleitung zu lang | Signal degradiert ueber >30 cm | Kabel kuerzen, 330 Ohm Widerstand am Data-In |
| Fehlender Kondensator | Spannungsspitzen beim Einschalten | 1000 uF Elko an +5V/GND des Strips |
| Level-Mismatch | Pi 3.3V Signal an 5V LED | 74AHCT125 Level Shifter einsetzen |
| Falscher LED-Typ im Code | WS2812B vs SK6812 | LED-Typ in der Library korrekt setzen |

### Luefter machen Geraeusche

| Ursache | Loesung |
| --- | --- |
| Lose Montage | Fester mit Klett fixieren, Gummi-Unterlegscheibe |
| Unwucht | Anderen Luefter versuchen (Billig-Luefter haben oft Unwucht) |
| Kabelkontakt | Kabel beruehrt Luefterblatt — umverlegen |
| Resonanz mit Helm | Weichen Schaumstoff zwischen Luefter und Helmwand |

### Audio brummt/rauscht

| Ursache | Loesung |
| --- | --- |
| Fehlender AC-Koppelkondensator | 47 uF Elko zwischen MAX4466 Out und PAM8403 In |
| Ground Loop | Alle GND an einem Punkt zusammenfuehren |
| Zu lange Audiokabel | Kabel so kurz wie moeglich |
| Mikrofonposition | Mikrofon weiter vom Luefter entfernt montieren |

## 3D-Druck

### Teile passen nicht zusammen

| Ursache | Loesung |
| --- | --- |
| Thermische Schrumpfung | 0.2-0.3 mm Toleranz auf Passflaechen |
| Unterschiedliche Skalierung | Alle Teile einer Region mit gleichem Faktor drucken |
| Elephant's Foot | First-Layer-Kalibrierung pruefen, Elephant Foot Compensation 0.1-0.15 mm |
| Warping | Brim nutzen (8 mm+), Bauraum geschlossen halten |

**Quick Fix:** Passflaeche mit Dremel/Schleifpapier nacharbeiten, Spalt mit CA-Kleber + Bondo fuellen.

### Layer-Trennung (Delamination)

| Ursache | Loesung |
| --- | --- |
| Zu niedrige Drucktemperatur | +5-10 C auf Hotend |
| Zugluft/offener Bauraum | Tueren schliessen, nicht neben Fenster |
| Zu hohe Druckgeschwindigkeit | Fuer kritische Teile auf 150 mm/s reduzieren |
| Feuchtes Filament | Filament trocknen (60 C, 4-6 Stunden) |

### Support-Narben auf sichtbarer Flaeche

| Loesung |
| --- |
| Druckorientierung aendern (sichtbare Seite aufs Bett oder nach oben) |
| Support Z-Gap auf 0.2 mm erhoehen |
| Support Interface 100% Dichte mit Concentric Pattern |
| Narben nachschleifen + Filler Primer |

## Mechanik / Passform

### Ruestung passt nicht

| Problem | Loesung |
| --- | --- |
| Zu eng (geht nicht ueber Arm/Bein) | Skalierung +3-5%, oder Oeffnung vergroessern (Dremel) |
| Zu weit (rutscht, wackelt) | Mehr Polsterung innen (EVA Foam Spacer), Gummiband |
| Kann nicht sitzen | Oberschenkel-Befestigung lockerer machen, Segmente kuerzer |
| Schultern blockieren Arme | Schulterstueck-Ausschnitt vergroessern |
| Helm zu eng | Polsterung duenner machen, Innenraum nachschleifen |
| Helm zu weit | Dickere Polsterung, Kinnriemen enger |

### Teile fallen ab

| Ursache | Loesung |
| --- | --- |
| Klett zu schwach | Industrial Velcro oder 3M Dual Lock verwenden |
| Magnete zu schwach | Groessere Magnete (12x3 statt 10x3), oder stapeln |
| Magnete falsch gepolt | Raus nehmen, richtig einsetzen, Polaritaet markieren! |
| Gurt zu locker | Kuerzen, Schnalle enger stellen |
| Schweiss loest Kleber | Mechanische Befestigung (Nieten, Schrauben) statt nur Kleber |

## Lackierung

### Farbe blaettert ab

| Ursache | Loesung |
| --- | --- |
| Fehlende/schlechte Grundierung | Richtig grundieren (Filler Primer, anschleifen, Primer, anschleifen) |
| Zu dicke Farbschichten | Mehrere DUENNE Schichten, je 15-20 Min trocknen |
| Nicht durchgetrocknet | Zwischen Schichten mindestens 24h warten |
| Falscher Lack auf Plastik | Lack fuer Kunststoff verwenden (Krylon Fusion, Rust-Oleum 2X) |
| Flex-Bereich (Gelenke) | Flexiblen Klarlack nutzen, oder diese Bereiche nicht dick lackieren |

### Weathering sieht unnatuerlich aus

| Problem | Loesung |
| --- | --- |
| Zu gleichmaessig | Weathering sollte UNGLEICHMAESSIG sein — fokussiere auf Kanten und logische Abnutzungsstellen |
| Zu viel auf einmal | Langsam aufbauen, Schicht fuer Schicht, zwischendurch zuruecktreten und bewerten |
| Falsches Silber | Mattes Silber/Gunmetal nutzen, KEIN glaenzendes Chrome |
| Wash trocknet fleckig | Wash duenner anmischen, schneller abwischen, auf kleinen Bereich konzentrieren |

### Visor beschlaegt

| Loesung |
| --- |
| Luefter pruefen (Intake + Exhaust richtig herum?) |
| Anti-Beschlag-Spray (z.B. fuer Schwimmbrillen) innen auftragen |
| Kleinen Spalt oben/unten am Visor lassen (Luftzirkulation) |
| Bei hoher Luftfeuchtigkeit: mehr Pausen, Helm oefter abnehmen |

**Ausfuehrliche Loesungen** (Cat Crap, Pinlock-Technik, Nasenabweiser, Kinndeflektoren): siehe `Documentation/Guides/Praxis-Tipps-Fortgeschritten.md` Abschnitt 2.

## Weiterfuehrend

- **Fortgeschrittene Praxis-Tipps:** `Documentation/Guides/Praxis-Tipps-Fortgeschritten.md`
- **LED-Visor-Forschung:** `Documentation/Guides/LED-Visor-Forschung.md`
