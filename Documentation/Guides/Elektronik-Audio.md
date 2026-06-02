# Elektronik: Audio und Voice Changer

Optionale Audio-Erweiterung fuer den Helm — Stimmverstaerker, Lautsprecher und Voice Changer.

## Option A: Einfacher Stimmverstaerker (kein Pitch-Shift)

Plug-and-Play Loesungen ohne Bastelarbeit:

- **COSVOX Cosplay Sound & Voice Amplifier** (~50-60 EUR) — speziell fuer Cosplay-Helme, Guertel-montierbar, hohe Lautstaerke
- **VoiceBooster MR1506** (~40 EUR) — portabler PA-Verstaerker, beliebt in der Cosplay-Community

## Option B: Arduino Voice Changer (Pitch Shifting)

### Komponenten

| Teil | Preis ca. |
| --- | --- |
| Adafruit MAX4466 Elektret-Mikrofon-Verstaerker | 7 EUR |
| Arduino Uno oder Leonardo | 10-15 EUR |
| Adafruit Audio FX Sound Board (oder Wave Shield) | 20-25 EUR |
| PAM8403 Class-D Verstaerker (2x3W) | 2-3 EUR |
| 40 mm Lautsprecher (3W, 4 oder 8 Ohm) | 3-5 EUR |

### Wichtige Verkabelungshinweise

- **AC-Koppelkondensator** (10-47 uF Elko) zwischen MAX4466 Ausgang und PAM8403 Eingang — PFLICHT! Der MAX4466 hat einen DC-Offset, der den PAM8403 ohne Kopplung beschaedigt
- PAM8403 Links und Rechts Ausgaenge NIEMALS zusammenschliessen (verbrennt den IC)
- Lautsprecher VOR dem Einschalten anschliessen
- Mikrofon mit kleinem Ballon umwickeln gegen Atem-Pops (alter Audio-Trick)

### Schaltplan

```
MAX4466 OUT --[47uF Elko]--+-- PAM8403 L-IN
                            |
                           GND

PAM8403 L-OUT+ ---- Speaker +
PAM8403 L-OUT- ---- Speaker -

5V ---+--- MAX4466 VCC
      +--- PAM8403 VCC
      +--- Arduino VCC

GND --+--- MAX4466 GND
      +--- PAM8403 GND
      +--- Arduino GND
```

## Option C: Raspberry Pi Software Voice Changer

- **sox** oder **pyo** Python Library fuer Echtzeit-Pitch-Shifting auf dem Pi Zero 2 W
- USB-Soundkarte noetig (Pi Zero hat keinen Audio-Ausgang): ~5 EUR fuer USB Audio Adapter
- Mehr CPU-Last, aber flexiblere Effekte
- Kann auf dem gleichen Pi wie das HUD laufen

## Lautsprecher-Platzierung

- Lautsprecher nach vorne gerichtet im Kinn-/Kieferbereich montieren
- Kleines Gehaeuse oder Schallwand fuer bessere Basswiedergabe
- Schallaustritt durch vorhandene Oeffnungen oder gebohrte Loecher im Helm

## Stromverbrauch

| Komponente | Strom |
| --- | --- |
| MAX4466 Mikrofon | < 0.01 A |
| PAM8403 Verstaerker (aktiv) | 0.05-0.15 A |
| Arduino (fuer Processing) | 0.02-0.04 A |
| USB-Soundkarte (Pi) | 0.02-0.05 A |
