# Design: Show + Praxis-Mix (Shield-Hit, Handler-Alert, Trink-Erinnerung)

> Datum: 2026-10-30
> Status: vom Nutzer genehmigt (Architektur: Arduino-autark + Pi-Duo)
> Umfang: 2 Module auf dem Ruestungs-Arduino, 1 Modul auf dem Helm-Pi

## Ziel

Drei kleine Module mit maximalem Con-Nutzen:

1. **Shield-Hit-Effekt:** Beruehrung der Ruestung loest Schild-Treffer-Effekt aus
   (Interaktion mit Publikum, besonders Kindern)
2. **Handler-Alert:** versteckter Taster laesst die ganze Ruestung rot blinken,
   damit die Begleitperson den Traeger in der Menschenmenge findet
3. **Trink-Erinnerung:** der Helm-Pi erinnert alle 45 min ans Trinken
   (Dehydrierung ist das reale Gesundheitsproblem im geschlossenen Helm)

## Architektur-Entscheidung

**Arduino-autark + Pi-Duo:** Shield-Hit und Handler-Alert laufen vollstaendig auf
dem Ruestungs-Arduino (LEDs + Piezo-Buzzer, eigener Taster). Die Trink-Erinnerung
laeuft auf dem Helm-Pi (Sprachansage + HUD-Banner). Begruendung: Show und
Sicherheit funktionieren auch, wenn der Pi abstuerzt oder ausgeschaltet ist -
gleiche Philosophie wie `Elektronik-Sprachsteuerung.md` (der Pi drueckt nur
Taster, ersetzt aber keine Sicherheitslogik).

## Modul 1: Shield-Hit-Effekt (ArmorControl/MultiEffects.ino)

### Hardware

| Teil | Pin | Hinweis |
| --- | --- | --- |
| TP223 Brustbein | D4 | unter dem Foam, ~1-2 mm unter der Oberflaeche |
| TP223 Rueckenplatte | D6 | |
| TP223 Schulter links | D7 | |
| TP223 Schulter rechts | D8 | |
| Passiver Piezo-Buzzer | D9 | Square-Wave via tone(), kein MP3-Modul |

- TP223-Ausgang ist HIGH bei Beruehrung, Modul entprellt selbst (Ausgang bleibt
  einige 100 ms HIGH) - Polling alle 20 ms reicht, keine Interrupts noetig.
- Empfindlichkeit per Poti auf dem Modul justieren; Ziel: Anstossen durch
  Kleidung loest NICHT aus, fester Tipp schon.
- Kostengesamt: 4x TP223 + Buzzer ca. 8-10 EUR.

### Reaktion

- **Treffer:** 2x cyan-weisser Blitz aller LEDs (je 120 ms an, 80 ms aus) +
  Zap-Sound: zwei fallende Toene (1800 Hz -> 900 Hz, je 60 ms).
- **Eskalation:** 3 Treffer innerhalb 10 s -> "Schild leer": rotes Flackern
  1,5 s (4 Hz) + tiefer Ton (300 Hz, 400 ms). Danach Zaehler-Reset.
- Treffer-Richtung wird NICHT unterschieden (alle 4 Sensoren loesen dieselbe
  Reaktion aus - bewusst einfach gehalten).
- Effekt blockiert den normalen Modus-Zyklus nicht: nach der Sequenz laeuft der
  vorherige LED-Modus weiter.

### Aenderungen im Code

- `MultiEffects.ino`: 4 Touch-Eingaenge (INPUT), Buzzer-Ausgang, Treffer-Zaehler
  mit Zeitfenster, zwei neue Effekt-Sequenzen (hit, depleted). Bestehende
  5 Modi und Button-Logik unveraendert.

## Modul 2: Handler-Alert (ArmorControl/MultiEffects.ino)

### Hardware

- Versteckter Taster an D3 (INPUT_PULLUP): Handgelenk-Manschette oder Unterseite
  der Brustplatte - vom Traeger selbst erreichbar, fuer Aussen unsichtbar.

### Reaktion

- **Aktivieren:** Taster >= 1 s halten (Schutz vor versehentlichem Ausloesen im
  Menschenstrom). Alarm: alle LEDs 100 % Helligkeit, rot, 2 Hz blinkend +
  Buzzer-Muster (2 kurze Piep-Toene pro Sekunde).
- **Deaktivieren:** nochmal >= 1 s halten. Danach normaler Modus.
- Der Alarm hat Vorrang vor Shield-Hit-Effekten (Treffer werden waehrend des
  Alarms ignoriert).
- Autark: funktioniert ohne Pi und ohne Helm - eigene LED-Stromversorgung
  (Schiene 2/FX-Bus laut Strombudget).

## Modul 3: Trink-Erinnerung (Pi 5, voice_control.py + hud_display.py)

### Verhalten

- Timer-Thread in `voice_control.py`: alle `hydration_interval_min` (Default 45)
  -> Ansage "Hydration erforderlich" (Piper/espeak, innere Lautsprecher) +
  kurzer Piepton + `hydration_due: true` in `hud_state.json` (via
  `hud_state.merge()`).
- `hud_display.py`: zeigt Banner "TRINKEN" (blinkend, 2 Hz), solange das Flag
  gesetzt ist; Banner hat Vorrang vor dem normalen HUD-Inhalt.
- Sprachbefehle (neu in WORDS/on_command_text):
  - "wasser" -> getrunken: Flag entfernen, Timer neu starten, Bestaetigungston
  - "spaeter" -> Snooze 10 min, Flag entfernen
  - "trinken aus" -> Erinnerung fuer die aktuelle Session deaktivieren,
    per "trinken an" reaktivierbar
- Konfiguration: `hydration_interval_min: 45` in `voice_config.example.json`.

### Aenderungen im Code

- `voice_control.py`: Timer-Thread (stoppt sauber beim Beenden), 3 neue
  Befehle, Ansage-Funktion nutzt vorhandene say()-Infrastruktur.
- `hud_display.py`: Banner-Rendering bei `hydration_due`.
- `hud_state.example.json`: Flag dokumentiert.
- Selftests beider Skripte erweitert (hardwarefrei, laufen in der CI).

## Datenfluss

```
TP223 (4x) --> ArmorControl Arduino --> LEDs + Buzzer        (autark)
Taster D3 --> ArmorControl Arduino --> Alarm an/aus          (autark)
voice_control.py (Timer) --> hud_state.json (hydration_due)
                          --> Ansage innen + Piepton
hud_display.py <-- hud_state.json --> Banner "TRINKEN"
```

## Fehlerbehandlung

- TP223 False-Positives (Feuchtigkeit/Schweiss im Foam): Treffer-Zaehler statt
  Sofort-Eskalation; Schwelle 3 in 10 s macht Einzelausloeser harmlos.
- Pi tot: Shield-Hit und Handler-Alert laufen weiter (autark). Trink-Erinnerung
  faellt aus - akzeptiert, kein Sicherheitsmodul.
- Timer-Thread crasht nicht die Sprachsteuerung: Exceptions im Thread werden
  geloggt, Timer laeuft weiter.

## Tests

1. `arduino-cli compile` fuer `MultiEffects.ino` (CI-Job existiert)
2. `voice_control.py --selftest`: neue Befehle "wasser"/"spaeter"/"trinken aus"
   erzeugt erwartete Aktionen; Timer-Logik mit verkuerztem Intervall getestet
3. `hud_display.py --selftest`: Banner-Frame bei gesetztem Flag erzeugt
4. ASCII-Check + Link-Check (CI)
5. Hardware-Test auf dem Bench: TP223-Empfindlichkeit, Buzzer-Lautstaerke,
   1-s-Halten des Alarms

## Bewusste Grenzen

- Keine Treffer-Richtung, keine Sound-Dateien (nur Square-Wave-Toene)
- Keine Funksynchronisation zwischen Ruestung und Helm (Komplexitaet unwert)
- Trink-Erinnerung ist Komfort, kein Sicherheitsfeature
