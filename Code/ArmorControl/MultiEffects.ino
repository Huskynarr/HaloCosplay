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
 *                   Ausgang HIGH bei Beruehrung. Nur aktiv mit TOUCH_ENABLED 1
 *                   (Standard 0): offene Eingaenge floaten und loesen sonst
 *                   zufaellige Treffer aus. Der AVR hat keine internen
 *                   Pulldowns - jeder nicht bestueckte Sensor-Pin braucht
 *                   10 kOhm nach GND, bevor TOUCH_ENABLED auf 1 gesetzt wird.
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
#define TOUCH_ENABLED 0   // 1 = Shield-Hit-Sensoren auswerten (siehe Verkabelung oben)

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
bool touchPrev[4] = {LOW, LOW, LOW, LOW};

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
#if TOUCH_ENABLED
  checkTouches();
#endif
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

// Flankenerkennung LOW->HIGH: ein langes Beruehren zaehlt nur EINEN Treffer,
// nicht einen pro loop-Durchlauf.
void checkTouches() {
  for (uint8_t i = 0; i < 4; i++) {
    bool reading = digitalRead(TOUCH_PINS[i]);
    if (reading == HIGH && touchPrev[i] == LOW) {   // neue Beruehrung (Flanke)
      unsigned long now = millis();
      if (hitCount == 0 || now - hitWindowStart > HIT_WINDOW_MS) {
        hitCount = 0;
        hitWindowStart = now;
      }
      hitCount++;
      shieldHitEffect(hitCount >= 3);
      touchPrev[i] = reading;
      return;               // ein Treffer pro Durchlauf reicht
    }
    touchPrev[i] = reading;
  }
}

// Wie delay(), fragt aber alle 5 ms Modus- und Alert-Taster ab. So geht ein
// kurzer Tastendruck (z.B. 200 ms Optokoppler-Puls vom Pi) waehrend eines
// laengeren Effekts nicht verloren. Gibt true zurueck, wenn der Alarm aktiv
// ist - der laufende Effekt soll dann sofort enden.
bool waitMs(unsigned long ms) {
  unsigned long start = millis();
  while (millis() - start < ms) {
    checkButton();
    checkAlertButton();
    if (alertActive) return true;
    delay(5);
  }
  return alertActive;
}

// Zap: 2x cyan-weisser Blitz + zwei fallende Toene. Bei depleted stattdessen
// rotes Flackern + tiefer Ton ("Schild leer"). Dauert bis ca. 1,9 s; waitMs()
// haelt Taster und Handler-Alarm waehrenddessen bedienbar.
void shieldHitEffect(bool depleted) {
  if (depleted) {
    hitCount = 0;
    for (uint8_t f = 0; f < 6; f++) {
      setAllColor(255, 0, 0, 255);
      tone(BUZZER_PIN, 300, 100);
      if (waitMs(125)) return;
      setAllColor(0, 0, 0, 0);
      if (waitMs(125)) return;
    }
    tone(BUZZER_PIN, 300, 400);
    waitMs(400);
  } else {
    for (uint8_t b = 0; b < 2; b++) {
      setAllColor(180, 255, 255, 255);
      if (waitMs(120)) return;
      setAllColor(0, 0, 0, 0);
      if (waitMs(80)) return;
    }
    tone(BUZZER_PIN, 1800, 60);
    if (waitMs(60)) return;
    tone(BUZZER_PIN, 900, 60);
    waitMs(60);
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
      strip.setBrightness(alertActive ? 255 : BRIGHTNESS);
      strip.clear();
      strip.show();
      tone(BUZZER_PIN, alertActive ? 1400 : 900, 150);
    }
  }
  alertBtnPrev = reading;
}

// Nicht-blockierend: 2 Hz rotes Blinken + 2 Piep-Toene pro Sekunde.
void alertEffect() {
  bool on = (millis() % 500) < 250;
  strip.setBrightness(on ? 255 : 0);
  setAllColor(255, 0, 0, on ? 255 : 0);
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
    if (waitMs(60)) return;   // Handler-Alarm schon waehrend des Bootens moeglich
  }
  // Dreifaches Aufblitzen
  for (int b = 0; b < 3; b++) {
    strip.setBrightness(255);
    strip.show();
    if (waitMs(80)) return;
    strip.setBrightness(BRIGHTNESS);
    strip.show();
    if (waitMs(80)) return;
  }
}

// --- Hilfsfunktionen ---

void setAllColor(uint8_t r, uint8_t g, uint8_t b, uint8_t br) {
  for (int i = 0; i < LED_COUNT; i++) {
    // uint16_t: 255 * 255 passt nicht in den 16-bit-int des AVR
    strip.setPixelColor(i,
      (uint8_t)((uint16_t)r * br / 255),
      (uint8_t)((uint16_t)g * br / 255),
      (uint8_t)((uint16_t)b * br / 255));
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
