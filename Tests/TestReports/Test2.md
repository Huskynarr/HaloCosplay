# Test 2 - Elektronik und Dauertest

## Ziel

- Alle elektronischen Systeme im eingebauten Zustand pruefen
- Laufzeit unter realistischen Bedingungen messen
- Temperatur und Komfort mit laufender Elektronik bewerten

## Aufbau

- Volle Ruestung mit aller Elektronik angezogen
- Alle Systeme eingeschaltet (HUD, LEDs, Luefter, Audio)
- Batterien voll geladen
- Timer starten bei Einschalten
- Thermometer im Helm (optional)

## Pruefpunkte

### Elektronik-Funktion

- [ ] HUD Display zeigt korrektes Bild
- [ ] HUD ist lesbar (Position, Helligkeit, Fokus)
- [ ] Helm-Luefter laufen (Luftstrom spuerbar)
- [ ] Visor beschlaegt nicht (nach 10 Min)
- [ ] Visor-LEDs leuchten
- [ ] Brust-LEDs leuchten
- [ ] Weitere LED-Zonen leuchten
- [ ] Audio funktioniert (wenn vorhanden)
- [ ] Stimme ist verstaendlich durch den Helm

### Laufzeittest

| Zeitpunkt | HUD | LEDs | Luefter | Audio | Batterie-Status | Temperatur Helm |
| --- | --- | --- | --- | --- | --- | --- |
| Start (0 Min) | | | | | 100% | |
| 30 Min | | | | | | |
| 60 Min | | | | | | |
| 120 Min | | | | | | |
| 180 Min | | | | | | |
| 240 Min | | | | | | |

### Bewegungstest mit Elektronik

- [ ] Gehen: Kabel bleiben verbunden, nichts lockert sich
- [ ] Setzen: kein Kabelzug, kein Stecker-Disconnect
- [ ] Helm aufsetzen/abnehmen: Quick-Disconnect funktioniert sauber
- [ ] Kopf drehen/nicken: OLED bleibt im Sichtfeld

### Komfort mit Elektronik

- [ ] Luefter-Geraeush stoerend? (0-10 Skala)
- [ ] Helm-Temperatur ertraeglich?
- [ ] Sichtfeld durch OLED eingeschraenkt?
- [ ] Kabel stoeren bei Bewegung?

## Ergebnis

| Messung | Wert |
| --- | --- |
| Gesamt-Laufzeit bis erster Ausfall | Min |
| Gesamt-Laufzeit bis Batterie leer | Min |
| Max Helm-Temperatur | C |
| Komfort-Score (1-10) | |

## Probleme

| Problem | Schwere | Loesung |
| --- | --- | --- |
| | | |

## Naechste Schritte

- [ ] Identifizierte Probleme beheben
- [ ] Falls Laufzeit < 6h: Batterie-Upgrade planen
- [ ] Falls Temperatur > 35 C: Luefter-Upgrade oder mehr Oeffnungen
- [ ] Convention-Ready Check (siehe Checklisten)
