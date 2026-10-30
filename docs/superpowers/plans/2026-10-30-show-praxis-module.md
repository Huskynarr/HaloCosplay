# Show + Praxis-Module Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Drei Module: Shield-Hit-Effekt und Handler-Alert autark auf dem Ruestungs-Arduino, Trink-Erinnerung auf dem Helm-Pi (Ansage + HUD-Banner).

**Architecture:** Touch-Sensoren und Alarm-Taster laufen komplett im `MultiEffects.ino` (kein Pi noetig). Die Trink-Erinnerung ist ein Timer-Thread in `voice_control.py`, der ueber `hud_state.merge()` ein Flag in `hud_state.json` setzt; `hud_display.py` zeigt dazu ein blinkendes Banner.

**Tech Stack:** Arduino (Adafruit_NeoPixel, tone()), Python 3 (threading, hud_state-Modul), PIL-Selftests, arduino-cli, GitHub-CI.

**Spec:** `docs/superpowers/specs/2026-10-30-show-praxis-module-design.md`

## Global Constraints

- ASCII-only in allen `.md`/`.py`/`.ino`-Dateien: ae/oe/ue statt Umlaute, ss statt sz (CI prueft das).
- Dokumentation und Kommentare auf Deutsch.
- Keine neuen pip-Dependencies; Arduino bleibt bei `Adafruit_NeoPixel` (kein MP3-Modul, nur `tone()`).
- Konventionelle Commits, Betreff auf Deutsch, ASCII.
- CI-Befehle, die am Ende gruen sein muessen: `python3 -m compileall -q Code/`, `python3 voice_control.py --selftest`, `python3 hud_display.py --selftest /tmp/hud.png`, `arduino-cli compile --fqbn arduino:avr:nano` pro Sketch.

---

### Task 1: Shield-Hit + Handler-Alert im Ruestungs-Arduino

**Files:**
- Modify: `Code/ArmorControl/MultiEffects.ino` (komplette Neufassung unten)

**Interfaces:**
- Consumes: vorhandene `strip`/`setAll()`/`bootSequence()`-Struktur des Sketches.
- Produces: `checkTouches()`, `shieldHitEffect(bool depleted)`, `checkAlertButton()`, `alertEffect()`, `setAllColor(uint8_t r, uint8_t g, uint8_t b, uint8_t br)`; Pins: Touch D4/D6/D7/D8, Buzzer D9, Alert-Taster D3. Spaeltere Tasks aendern diese Datei nicht.

- [ ] **Step 1: Sketch ersetzen**

`Code/ArmorControl/MultiEffects.ino` komplett durch diese Fassung ersetzen:

```cpp
/*
 * Multi-Effekt LED Controller fuer MJOLNIR Armor
 *
 * Unterstuetzte Effekte (per Taster umschaltbar):
 *   0 = Static Glow (konstant)
 *   1 = Breathing (sinusfoermig)
 *   2 = Heartbeat (doppelpuls)
 *   3 = Chase (Lauflicht)
 *   4 = Idle Flicker (subtile Variation)
 *
 * Show + Praxis (Spec: docs/superpowers/specs/2026-10-30-show-praxis-module-design.md):
 *   Shield-Hit:    4x TP223 kapazitive Sensoren unter dem Foam. Beruehrung ->
 *                  2x cyan-weisser Blitz + Zap-Ton. 3 Treffer in 10 s ->
 *                  "Schild leer": rotes Flackern + tiefer Ton.
 *   Handler-Alert: Taster an D3 >= 1 s halten -> alle LEDs rot, 2 Hz, Piep-
 *                  Muster. Nochmal >= 1 s halten -> aus. Autark ohne Pi.
 *
 * Verkabelung:
 *   LED Data     -> Pin 5 (ueber 330 Ohm Widerstand)
 *   Modus-Taster -> Pin 2 (gegen GND, interner Pull-Up)
 *   TP223        -> Pins 4 (Brust), 6 (Ruecken), 7 (Schulter L), 8 (Schulter R)
 *                   Ausgang HIGH bei Beruehrung; nicht angeschlossene Sensoren
 *                   brauchen 10 kOhm Pulldown, sonst zufaellige Treffer
 *   Alert-Taster -> Pin 3 (gegen GND, interner Pull-Up)
 *   Buzzer       -> Pin 9 (passiver Piezo, Plus-Seite, ueber 100 Ohm)
 *   +5V/GND      -> LED Strip Power (1000 uF Elko!)
 *
 * Anpassen: LED_COUNT, LED_PIN, BUTTON_PIN, Farbe (HUE)
 */

#include <Adafruit_NeoPixel.h>

#define LED_PIN     5
#define LED_COUNT   24
#define BUTTON_PIN  2
#define ALERT_PIN   3
#define BUZZER_PIN  9
#define NUM_MODES   5
#define BRIGHTNESS  128   // 50% = guter Convention-Wert (0-255)

// Farbe: Gruen-Cyan (MJOLNIR Tech-Glow)
#define COLOR_R  0
#define COLOR_G  200
#define COLOR_B  60

// TP223-Sensoren: Brust, Ruecken, Schulter links, Schulter rechts
const uint8_t TOUCH_PINS[4] = {4, 6, 7, 8};
const unsigned long HIT_WINDOW_MS = 10000;  // 3 Treffer in 10 s = Schild leer
const unsigned long ALERT_HOLD_MS = 1000;   // 1 s halten schaltet den Alarm

Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

uint8_t currentMode = 1;  // Start mit Breathing
bool lastButtonState = HIGH;
unsigned long lastDebounce = 0;

uint8_t hitCount = 0;
unsigned long hitWindowStart = 0;

bool alertActive = false;
bool alertBtnPrev = HIGH;
unsigned long alertHoldStart = 0;
bool alertHoldDone = false;
unsigned long alertLastBeep = 0;

void setup() {
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(ALERT_PIN, INPUT_PULLUP);
  for (uint8_t i = 0; i < 4; i++) {
    pinMode(TOUCH_PINS[i], INPUT);
  }
  pinMode(BUZZER_PIN, OUTPUT);
  strip.begin();
  strip.setBrightness(BRIGHTNESS);
  bootSequence();
}

void loop() {
  checkButton();
  checkAlertButton();
  if (alertActive) {
    alertEffect();
    return;                 // Alarm hat Vorrang, Treffer werden ignoriert
  }
  checkTouches();
  switch (currentMode) {
    case 0: staticGlow(); break;
    case 1: breathing();  break;
    case 2: heartbeat();  break;
    case 3: chase();      break;
    case 4: idleFlicker(); break;
  }
}

// --- Effekte ---

void staticGlow() {
  for (int i = 0; i < LED_COUNT; i++) {
    strip.setPixelColor(i, COLOR_R, COLOR_G, COLOR_B);
  }
  strip.show();
  delay(50);
}

void breathing() {
  float val = (sin(millis() / 1500.0) + 1.0) * 0.5;
  uint8_t br = (uint8_t)(val * 255);
  setAllColor(COLOR_R, COLOR_G, COLOR_B, br);
  delay(10);
}

// Doppelpuls als millis()-Envelope: blockiert nicht, Taster bleibt reaktiv
void heartbeat() {
  uint16_t t = millis() % 1130;
  uint8_t br;
  if      (t <  80) br = map(t,   0,  80,   0, 200);
  else if (t < 200) br = map(t,  80, 200, 200,   0);
  else if (t < 300) br = 0;
  else if (t < 380) br = map(t, 300, 380,   0, 255);
  else if (t < 530) br = map(t, 380, 530, 255,   0);
  else              br = 0;
  setAllColor(COLOR_R, COLOR_G, COLOR_B, br);
  delay(10);
}

void chase() {
  static int pos = 0;
  strip.clear();
  strip.setPixelColor(pos, COLOR_R, COLOR_G, COLOR_B);
  // Nachleuchten (Tail)
  for (int t = 1; t <= 3; t++) {
    int tailPos = (pos - t + LED_COUNT) % LED_COUNT;
    uint8_t fade = 255 / (t + 1);
    strip.setPixelColor(tailPos,
      (uint8_t)(COLOR_R * fade / 255),
      (uint8_t)(COLOR_G * fade / 255),
      (uint8_t)(COLOR_B * fade / 255));
  }
  strip.show();
  pos = (pos + 1) % LED_COUNT;
  delay(40);
}

void idleFlicker() {
  for (int i = 0; i < LED_COUNT; i++) {
    uint8_t flicker = random(230, 256);
    strip.setPixelColor(i,
      (uint8_t)(COLOR_R * flicker / 255),
      (uint8_t)(COLOR_G * flicker / 255),
      (uint8_t)(COLOR_B * flicker / 255));
  }
  strip.show();
  delay(50);
}

// --- Show + Praxis ---

void checkTouches() {
  for (uint8_t i = 0; i < 4; i++) {
    if (digitalRead(TOUCH_PINS[i]) == HIGH) {
      unsigned long now = millis();
      if (hitCount == 0 || now - hitWindowStart > HIT_WINDOW_MS) {
        hitCount = 0;
        hitWindowStart = now;
      }
      hitCount++;
      shieldHitEffect(hitCount >= 3);
      return;               // ein Treffer pro Durchlauf reicht
    }
  }
}

// Zap: 2x cyan-weisser Blitz + zwei fallende Toene. Bei depleted stattdessen
// rotes Flackern + tiefer Ton ("Schild leer"). Blockiert wie bootSequence -
// akzeptabel, weil der Effekt Sekunden-Dauer hat und danach der Modus weiterlaeuft.
void shieldHitEffect(bool depleted) {
  if (depleted) {
    hitCount = 0;
    for (uint8_t f = 0; f < 6; f++) {
      setAllColor(255, 0, 0, 255);
      tone(BUZZER_PIN, 300, 100);
      delay(125);
      setAllColor(0, 0, 0, 0);
      delay(125);
    }
    tone(BUZZER_PIN, 300, 400);
    delay(400);
  } else {
    for (uint8_t b = 0; b < 2; b++) {
      setAllColor(180, 255, 255, 255);
      delay(120);
      setAllColor(0, 0, 0, 0);
      delay(80);
    }
    tone(BUZZER_PIN, 1800, 60);
    delay(60);
    tone(BUZZER_PIN, 900, 60);
    delay(60);
  }
}

// 1 s halten schaltet den Alarm um (Schutz vor versehentlichem Ausloesen).
void checkAlertButton() {
  bool reading = digitalRead(ALERT_PIN);
  if (reading == LOW) {
    if (alertBtnPrev == HIGH) {
      alertHoldStart = millis();
      alertHoldDone = false;
    }
    if (!alertHoldDone && millis() - alertHoldStart >= ALERT_HOLD_MS) {
      alertHoldDone = true;
      alertActive = !alertActive;
      strip.clear();
      strip.show();
      tone(BUZZER_PIN, alertActive ? 1400 : 900, 150);
    }
  }
  alertBtnPrev = reading;
}

// Nicht-blockierend: 2 Hz rotes Blinken + 2 Piep-Toene pro Sekunde.
void alertEffect() {
  setAllColor(255, 0, 0, (millis() % 500) < 250 ? 255 : 0);
  if (millis() - alertLastBeep >= 500) {
    alertLastBeep = millis();
    tone(BUZZER_PIN, 1200, 90);
  }
}

// --- Boot Sequence ---

void bootSequence() {
  // Sweep von links nach rechts
  for (int i = 0; i < LED_COUNT; i++) {
    strip.setPixelColor(i, COLOR_R, COLOR_G, COLOR_B);
    strip.show();
    delay(60);
  }
  // Dreifaches Aufblitzen
  for (int b = 0; b < 3; b++) {
    strip.setBrightness(255);
    strip.show();
    delay(80);
    strip.setBrightness(BRIGHTNESS);
    strip.show();
    delay(80);
  }
}

// --- Hilfsfunktionen ---

void setAllColor(uint8_t r, uint8_t g, uint8_t b, uint8_t br) {
  for (int i = 0; i < LED_COUNT; i++) {
    strip.setPixelColor(i,
      (uint8_t)(r * br / 255),
      (uint8_t)(g * br / 255),
      (uint8_t)(b * br / 255));
  }
  strip.show();
}

void setAll(uint8_t br) {
  setAllColor(COLOR_R, COLOR_G, COLOR_B, br);
}

void checkButton() {
  bool reading = digitalRead(BUTTON_PIN);
  if (reading == LOW && lastButtonState == HIGH && millis() - lastDebounce > 200) {
    currentMode = (currentMode + 1) % NUM_MODES;
    lastDebounce = millis();
    strip.clear();
    strip.show();
  }
  lastButtonState = reading;
}
```

- [ ] **Step 2: Kompilieren**

```bash
cd /home/ss2299/Projekte/HaloCosplay
arduino-cli compile --fqbn arduino:avr:nano Code/ArmorControl
```

Falls der AVR-Core fehlt: `arduino-cli core update-index && arduino-cli core install arduino:avr`, dann erneut.
Erwartet: `Sketch uses ... bytes ...` ohne Fehler.

- [ ] **Step 3: Commit**

```bash
git add Code/ArmorControl/MultiEffects.ino
git commit -m "feat(armor): Shield-Hit-Effekt und Handler-Alert autark"
```

---

### Task 2: Trink-Erinnerung in voice_control.py (TDD)

**Files:**
- Modify: `Code/HelmetControl/voice_control.py`
- Modify: `Code/HelmetControl/voice_config.example.json`

**Interfaces:**
- Consumes: `hud_state.merge(path, updates=None, remove=())` (existiert), `Recorder`/`run_selftest()` der Datei.
- Produces: `HydrationTimer(cfg, out, interval_min=None)` mit `done()`, `snooze(minutes=10)`, `set_enabled(on)`, `stop`; `Commander` ruuf `out.hydration(action)` mit `action in {"done","snooze","off","on"}`; `Helmet.hydration(action)`; Config-Key `hydration_interval_min` (Default 45).

- [ ] **Step 1: Fehlschlagende Selftest-Faelle ergaenzen**

In `run_selftest()` die `cases`-Liste um vier Eintraege erweitern (vor `("blablub", ...)`):

```python
        ("wasser", ("hydration", "done")),
        ("spaeter", ("hydration", "snooze")),
        ("trinken aus", ("hydration", "off")),
        ("trinken an", ("hydration", "on")),
```

Direkt vor `run_selftest()` diese Funktion einfuegen:

```python
def test_hydration_timer():
    """Timer mit verkuerztem Intervall: Ansage + Flag, done() raeumt auf."""
    state = os.path.join(tempfile.gettempdir(), "hydration_selftest.json")
    if os.path.exists(state):
        os.remove(state)
    rec = Recorder()
    timer = HydrationTimer({"state_path": state}, rec, interval_min=0.01)  # 0,6 s
    time.sleep(0.9)
    ok_announce = ("say", "Hydration erforderlich.") in rec.calls
    ok_flag = hud_state.load(state).get("hydration_due") is True
    timer.done()
    ok_cleared = "hydration_due" not in hud_state.load(state)
    timer.stop.set()
    failed = sum(not x for x in (ok_announce, ok_flag, ok_cleared))
    print(f"  [{'ok' if failed == 0 else 'FEHLER'}] Hydration-Timer: "
          f"Ansage={ok_announce} Flag={ok_flag} done()={ok_cleared}")
    return failed
```

In `run_selftest()` vor dem `missing = ...`-Absatz einfuegen:

```python
    failed += test_hydration_timer()
```

- [ ] **Step 2: Fehlschlag verifizieren**

```bash
cd Code/HelmetControl && python3 voice_control.py --selftest
```

Erwartet: `NameError: name 'HydrationTimer' is not defined` bzw. FEHLER-Zeilen fuer die vier Befehle.

- [ ] **Step 3: Implementierung**

3a) In `DEFAULTS` (nach `"announce_pause_s": 12,`) einfuegen:

```python
    "hydration_interval_min": 45,
```

3b) `WORDS` erweitern (Liste neu sortiert, 3 neue Woerter):

```python
WORDS = ["visier", "ruestung", "licht", "weiter", "nebel", "boost", "schub", "show",
         "alarm", "stopp", "ruhe", "heller", "dunkler", "aus", "an", "luefter", "voll",
         "leise", "normal", "staerker", "schwaecher", "scanner", "stimme", "status",
         "wasser", "trinken", "spaeter"]
```

3c) `SPOKEN` um einen Eintrag erweitern:

```python
SPOKEN = {"ruestung": "r\u00fcstung", "luefter": "l\u00fcfter", "staerker": "st\u00e4rker",
          "schwaecher": "schw\u00e4cher", "gruen": "gr\u00fcn", "weiss": "wei\u00df",
          "tuerkis": "t\u00fcrkis", "spaeter": "sp\u00e4ter"}
```

3d) In `Commander.handle()` diesen Zweig VOR `elif w & {"ruestung", "licht"}:` einfuegen:

```python
        elif w & {"wasser", "trinken", "spaeter"}:
            if "aus" in w:
                out.hydration("off")
            elif "an" in w:
                out.hydration("on")
            elif "spaeter" in w:
                out.hydration("snooze")
            else:
                out.hydration("done")
            out.beep("ok")
```

3e) Neue Sektion nach der `Commander`-Klasse (vor `# ============================== Hardware ==============================`):

```python
# ============================== Hydration ==============================

class HydrationTimer:
    """Erinnert alle N Minuten ans Trinken: Ansage innen + HUD-Banner.

    Das HUD-Flag (hydration_due) geht ueber hud_state.merge() in die
    hud_state.json - hud_display.py zeigt solange ein blinkendes Banner.
    Faellt der Pi aus, faellt nur die Erinnerung aus - kein Sicherheitsmodul.
    """

    def __init__(self, cfg, out, interval_min=None):
        # interval_min nur fuer den Selftest; Produktion floort auf 60 s
        if interval_min is None:
            self.interval = max(60.0, float(cfg.get("hydration_interval_min", 45)) * 60.0)
        else:
            self.interval = max(0.0, float(interval_min)) * 60.0
        self.snooze_s = 0.0
        self.state_path = cfg["state_path"]
        self.out = out
        self.enabled = True
        self.wake = threading.Event()
        self.stop = threading.Event()
        threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self):
        while not self.stop.is_set():
            wait = self.snooze_s or self.interval
            self.snooze_s = 0.0
            self.wake.clear()
            if self.stop.wait(wait):
                return
            if self.wake.is_set() or not self.enabled:
                continue        # neu gestartet (getrunken/snooze) oder deaktiviert
            hud_state.merge(self.state_path, {"hydration_due": True})
            self.out.say("Hydration erforderlich.")
            self.out.beep("ok")

    def done(self):
        """Getrunken: Flag weg, Timer voll neu starten."""
        hud_state.merge(self.state_path, remove=("hydration_due",))
        self.wake.set()

    def snooze(self, minutes=10):
        """Flag weg, naechste Erinnerung erst in `minutes` Minuten."""
        self.snooze_s = minutes * 60.0
        hud_state.merge(self.state_path, remove=("hydration_due",))
        self.wake.set()

    def set_enabled(self, on):
        self.enabled = bool(on)
        hud_state.merge(self.state_path, remove=("hydration_due",))
        self.wake.set()
```

3f) In `Helmet.__init__()` nach `self.commander = Commander(self)` einfuegen:

```python
        self.hydration = self._try("Hydration-Timer", lambda: HydrationTimer(cfg, self))
```

3g) In `Helmet` diese Methode einfuegen (nach `set_scanner`):

```python
    def hydration(self, action):
        if self.hydration is None:
            self.say("Trink-Erinnerung nicht aktiv.")
            return
        if action == "done":
            self.hydration.done()
            self.say("Hydration protokolliert.")
        elif action == "snooze":
            self.hydration.snooze(10)
            self.say("Erinnerung in 10 Minuten.")
        elif action == "off":
            self.hydration.set_enabled(False)
            self.say("Trink-Erinnerung aus.")
        elif action == "on":
            self.hydration.set_enabled(True)
            self.say("Trink-Erinnerung an.")
```

- [ ] **Step 4: Selftest grueneufen verifizieren**

```bash
cd Code/HelmetControl && python3 voice_control.py --selftest
```

Erwartet: alle `[ok]`-Zeilen inkl. der 4 neuen Befehle und der Hydration-Timer-Zeile, Abschluss `Selftest ok - Vokabular: 41 Woerter` (38 + 3 neue).

- [ ] **Step 5: Beispiel-Konfiguration**

In `Code/HelmetControl/voice_config.example.json` nach `"announce_pause_s": 12` einfuegen:

```json
  ,
  "hydration_interval_min": 45
```

(= Zeile `"hydration_interval_min": 45` mit fuehrendem Komma korrekt einreihen; Datei bleibt gueltiges JSON.)

- [ ] **Step 6: Syntax + Commit**

```bash
cd /home/ss2299/Projekte/HaloCosplay
python3 -m compileall -q Code/ && echo OK
git add Code/HelmetControl/voice_control.py Code/HelmetControl/voice_config.example.json
git commit -m "feat(voice): Trink-Erinnerung mit HUD-Flag"
```

---

### Task 3: HUD-Banner in hud_display.py (TDD)

**Files:**
- Modify: `Code/HelmetControl/hud_display.py`
- Modify: `Code/HelmetControl/hud_state.example.json`

**Interfaces:**
- Consumes: `hydration_due`-Flag in `hud_state.json` (Task 2 schreibt es).
- Produces: `read_state()` liefert optional `state["hydration_due"] = True`; `draw_hydration_banner(draw, t)`; Selftest rendert Frame `_2`.

- [ ] **Step 1: Fehlschlagenden Selftest-Frame ergaenzen**

In `run_selftest()` nach der Frame-Schleife einfuegen:

```python
    state_h = read_state(CONFIG, 0.0)
    state_h["hydration_due"] = True
    frame = draw_hud(0.0, battery, state_h, dict(CONFIG, show_battery=True))
    frame.convert("L").save(f"{base}_2{ext}")
    banner = Image.open(f"{base}_2{ext}").convert("L")
    ok_banner = banner.getpixel((10, 30)) == 255   # Outline des Banners
    print(f"  [{'ok' if ok_banner else 'FEHLER'}] Hydration-Banner gerendert")
```

Und die Abschluss-Zeile aendern auf:

```python
    print(f"Selftest-Frames gespeichert: {base}_boot{ext}, {base}_0{ext}, {base}_1{ext}, {base}_2{ext}")
```

Zusaetzlich `failed`-Semantik: den bestehenden `print(...)`-Block so ergaenzen, dass `ok_banner` geprueft wird - konkret: nach dem `print(f"  [{'ok'...}] Hydration-Banner ...")` einfuegen:

```python
    if not ok_banner:
        sys.exit("Selftest fehlgeschlagen: Hydration-Banner fehlt")
```

- [ ] **Step 2: Fehlschlag verifizieren**

```bash
cd Code/HelmetControl && python3 hud_display.py --selftest /tmp/hud.png
```

Erwartet: `Selftest fehlgeschlagen: Hydration-Banner fehlt`

- [ ] **Step 3: Implementierung**

3a) In `read_state()` nach dem Vision-contacts-Block (vor `return state`) einfuegen:

```python
    # Trink-Erinnerung (voice_control.py): Flag -> blinkendes Banner
    if data.get("hydration_due"):
        state["hydration_due"] = True
```

3b) Neue Zeichenfunktion nach `draw_battery()` einfuegen:

```python
def draw_hydration_banner(draw, t):
    """Blinkendes Banner ueber dem HUD, solange hydration_due gesetzt ist."""
    if int(t * 2) % 2 == 0:
        draw.rectangle((10, 30, 118, 46), outline=1, fill=0)
        draw.text((38, 34), "TRINKEN!", fill=1)
```

3c) In `draw_hud()` vor `return image` einfuegen:

```python
    if state.get("hydration_due"):
        draw_hydration_banner(draw, t)
```

3d) Im Modul-Docstring die Feature-Liste um eine Zeile erweitern:

```python
  - hydration reminder banner (blinking, driven by "hydration_due" flag)
```

- [ ] **Step 4: Selftest grueneufen verifizieren**

```bash
cd Code/HelmetControl && python3 hud_display.py --selftest /tmp/hud.png
```

Erwartet: `[ok] Hydration-Banner gerendert`, Frame `/tmp/hud_2.png` existiert.

- [ ] **Step 5: Beispiel-State + Commit**

In `Code/HelmetControl/hud_state.example.json` einfuegen:

```json
  "hydration_due": false,
```

(neue Zeile nach `"heading": 123`; Datei bleibt gueltiges JSON; `false` = kein Banner)

```bash
cd /home/ss2299/Projekte/HaloCosplay
python3 -m compileall -q Code/ && echo OK
git add Code/HelmetControl/hud_display.py Code/HelmetControl/hud_state.example.json
git commit -m "feat(hud): blinkendes Trink-Banner bei hydration_due"
```

---

### Task 4: Dokumentation + CI-Gesamtcheck

**Files:**
- Create: `Documentation/Guides/Elektronik-Show-Praxis-Module.md`
- Modify: `Documentation/TODO.md`, `sitemap.xml`, `web/content.js`, `CLAUDE.md`

**Interfaces:**
- Consumes: fertige Tasks 1-3 (Pin-Zuordnung, Befehle, Config-Key).
- Produces: verlinkte Doku; keine Code-Interfaces.

- [ ] **Step 1: Guide anlegen**

`Documentation/Guides/Elektronik-Show-Praxis-Module.md` mit diesem Inhalt anlegen:

```markdown
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
```

- [ ] **Step 2: Querverweise ergaenzen**

`Documentation/TODO.md` - nach der Sprachsteuerung-Zeile in Phase 6 einfuegen:

```markdown
- [ ] Optional: Shield-Hit, Handler-Alert, Trink-Erinnerung (siehe [Elektronik-Show-Praxis-Module.md](Guides/Elektronik-Show-Praxis-Module.md))
```

`sitemap.xml` - nach der Elektronik-Sprachsteuerung-URL einfuegen:

```xml
  <url><loc>https://huskynarr.github.io/HaloCosplay/Documentation/Guides/Elektronik-Show-Praxis-Module.md</loc><priority>0.7</priority></url>
```

`web/content.js` - nach dem Indoor-Navigation-Eintrag einfuegen:

```javascript
        { title: "Show- und Praxis-Module", file: "Documentation/Guides/Elektronik-Show-Praxis-Module.md" },
```

`CLAUDE.md` - in der Repo-Structure-Liste nach der Elektronik-*.md-Zeile einfuegen:

```markdown
- `Documentation/Guides/Elektronik-Show-Praxis-Module.md` - shield-hit touch effect, handler alert, hydration reminder
```

Und in der Arduino-Liste den `MultiEffects.ino`-Eintrag zu:

```markdown
- `Code/ArmorControl/MultiEffects.ino` - **advanced**: 5 LED effects + button switching + boot sequence + shield-hit touch sensors + handler alert
```

- [ ] **Step 3: Gesamtcheck (alle CI-Jobs lokal)**

```bash
cd /home/ss2299/Projekte/HaloCosplay
grep -rlP '[^\x00-\x7F]' --include='*.md' --include='*.ino' --include='*.py' . ; echo "ASCII-exit=$? (1 = OK)"
python3 -m compileall -q Code/ && echo "compileall OK"
cd Code/HelmetControl
python3 hud_display.py --selftest /tmp/hud.png
python3 sensor_bridge.py --selftest --state /tmp/s.json --battery /tmp/b.json
python3 robot_bridge.py --selftest --state /tmp/r.json
python3 vision_bridge.py --selftest --state /tmp/v.json
python3 voice_control.py --selftest
cd ../..
arduino-cli compile --fqbn arduino:avr:nano Code/ArmorControl
```

Erwartet: ASCII-exit=1, alle Selftests ok, Compile erfolgreich.

- [ ] **Step 4: Commit**

```bash
git add Documentation/Guides/Elektronik-Show-Praxis-Module.md Documentation/TODO.md sitemap.xml web/content.js CLAUDE.md
git commit -m "docs(show): Guide fuer Shield-Hit, Alert, Trink-Erinnerung"
```

---

## Selbst-Review (vom Plan-Autor ausgefuehrt)

- **Spec-Abdeckung:** Shield-Hit (Task 1), Handler-Alert (Task 1), Trink-Erinnerung inkl. Banner + Befehle + Config (Tasks 2+3), Fehlerbehandlung/Tests (in den Tasks), Doku (Task 4). Keine Luecken.
- **Platzhalter:** keine TBD/TODO; alle Code-Schritte vollstaendig.
- **Typ-Konsistenz:** `out.hydration(action)` (Task 2 Commander) == `Helmet.hydration(action)`; `HydrationTimer(cfg, out, interval_min=None)` == Selftest-Aufruf; `hydration_due` konsistent in voice_control.py, hud_display.py, hud_state.example.json.
