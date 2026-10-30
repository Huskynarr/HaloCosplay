# Elektronik: Show- und Praxis-Module (Shield-Hit, Handler-Alert, Trink-Erinnerung)

> **Level:** [A] Anfaenger | [F] Fortgeschritten  |  **Varianten:** V2/V3 (optional)
> **Voraussetzungen:** Ruestungs-LEDs laufen (`MultiEffects.ino`), Sprachsteuerung
> installiert (`Elektronik-Sprachsteuerung.md`), Strombudget gerechnet
> (`Elektronik-Strombudget.md`).

Drei kleine Module mit grossem Con-Nutzen: Beruehrungseffekt fuer das Publikum,
Alarm fuer die Begleitperson, Trink-Erinnerung fuer den Trager. Shield-Hit und
Handler-Alert laufen autark auf dem Ruestungs-Arduino - ohne Pi, ohne Helm.

## 1. Shield-Hit-Effekt (Ruestungs-Arduino)

### Hardware

| Teil | Preis ca. | Pin | Hinweis |
| --- | --- | --- | --- |
| 4x TP223 kapazitiv | 6-8 EUR | D4 Brust, D6 Ruecken, D7 Schulter L, D8 Schulter R | Empfindlichkeit per Poti |
| Passiver Piezo-Buzzer | 1-2 EUR | D9 (ueber 100 Ohm) | Square-Wave, kein MP3 |

- TP223 unter dem Foam platzieren, ca. 1-2 mm unter der Oberflaeche, auf
  sauberer, fester Flaeche (nicht auf losem Schaumstoff - sonst Dauertrigger).
- Justage: Anstossen durch Kleidung loest NICHT aus, fester Tipp schon.
- Nicht angeschlossene Sensoren brauchen 10 kOhm Pulldown, sonst zufaellige
  Treffer.

### Reaktion

- Treffer: 2x cyan-weisser Blitz + Zap-Ton (zwei fallende Toene).
- 3 Treffer in 10 s: "Schild leer" - rotes Flackern 1,5 s + tiefer Ton, dann
  Reset. Kinder tippen gern mehrfach - genau dafuer ist die Eskalation da.

## 2. Handler-Alert (Ruestungs-Arduino)

- Versteckter Taster an D3 (INPUT_PULLUP): Handgelenk-Manschette oder
  Unterseite der Brustplatte. Selbst erreichbar, fuer Aussen unsichtbar.
- 1 s halten = Alarm an: alle LEDs 100 % rot, 2 Hz blinkend, 2 Piep-Toene/s.
  Nochmal 1 s halten = aus.
- Das 1-s-Halten ist Absicht: im Menschenstrom wird ein Taster gedrueckt.
- Autark: funktioniert ohne Pi und ohne Helm, aus der FX-Stromschiene
  (`Elektronik-Strombudget.md`, Schiene 2).

## 3. Trink-Erinnerung (Helm-Pi)

Dehydrierung ist das reale Gesundheitsproblem im geschlossenen Helm. Der Pi
erinnert deshalb alle 45 min:

- Ansage "Hydration erforderlich" auf den inneren Lautsprechern + Piepton
- Blinkendes Banner "TRINKEN!" auf dem HUD, solange nicht bestaetigt
- Sprachbefehle: "wasser" (getrunken, Timer neu), "spaeter" (10 min Snooze),
  "trinken aus" / "trinken an" (Session-Weise deaktivieren)
- Intervall: `hydration_interval_min` in `voice_config.json` (Default 45)

Der Timer schreibt das Flag `hydration_due` in die `hud_state.json` (ueber
`hud_state.merge()`, ueberschreibt also keine anderen Module). Faellt der Pi
aus, faellt nur die Erinnerung aus - die Ruestung bleibt voll funktionsfaehig.

## 4. Testreihenfolge

1. Selftests: `voice_control.py --selftest` und `hud_display.py --selftest /tmp/hud.png`
2. Arduino kompilieren: `arduino-cli compile --fqbn arduino:avr:nano Code/ArmorControl`
3. Bench: TP223-Empfindlichkeit justieren, Buzzer-Lautstaerke, 1-s-Halten des Alarms
4. In der Ruestung: Treffer durch den Foam, Alarm von aussen sichtbar?
5. Ausfalltest: Pi ausschalten - Shield-Hit und Alert muessen weiterlaufen

## 5. Grenzen

- Keine Treffer-Richtung (alle 4 Sensoren loesen dieselbe Reaktion aus)
- Keine Sound-Dateien, nur Square-Wave-Toene
- Trink-Erinnerung ist Komfort, kein Sicherheitsfeature

## Verwandte Guides

- Ruestungs-LEDs: `Code/ArmorControl/MultiEffects.ino`, [LED-Effekte.md](LED-Effekte.md)
- Sprachbefehle: [Elektronik-Sprachsteuerung.md](Elektronik-Sprachsteuerung.md)
- Sicherheit: [Sicherheit.md](Sicherheit.md)
