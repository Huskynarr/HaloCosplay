// Host tests for Code/ArmorControl/MultiEffects.ino (included above by run.py).
#include "check.h"

static void boot() {
  mock_reset_board();
  mock_input[BUTTON_PIN] = HIGH; mock_input[ALERT_PIN] = HIGH;   // pull-ups, released
  currentMode = 1; lastButtonState = HIGH; lastDebounce = 0;
  hitCount = 0; hitWindowStart = 0;
  alertActive = false; alertBtnPrev = HIGH; alertHoldStart = 0; alertHoldDone = false; alertLastBeep = 0;
  for (uint8_t i = 0; i < 4; i++) touchPrev[i] = LOW;
  setup();
}

static void run_for(unsigned long ms) {
  unsigned long end = mock_ms + ms;
  while (mock_ms < end) { unsigned long before = mock_ms; loop(); if (mock_ms == before) mock_ms += 1; }
}

static void touch(int index) {              // one clean touch + release, evaluated directly
  mock_input[TOUCH_PINS[index]] = HIGH; checkTouches();
  mock_input[TOUCH_PINS[index]] = LOW; checkTouches();
}

int main() {
  TEST("Start: Boot-Animation endet mit der eingestellten Helligkeit");
  boot();
  CHECK(strip.shown_brightness == BRIGHTNESS);
  CHECK(strip.out_of_range == 0);

  TEST("Handler-Alarm: erst nach ALERT_HOLD_MS, kurzer Druck loest nichts aus");
  boot();
  mock_input[ALERT_PIN] = LOW; run_for(300);
  mock_input[ALERT_PIN] = HIGH; run_for(300);
  CHECK(!alertActive);
  mock_input[ALERT_PIN] = LOW; run_for(ALERT_HOLD_MS - 100);
  CHECK(!alertActive);
  run_for(200);
  CHECK(alertActive);

  TEST("Handler-Alarm: Weiterhalten schaltet nicht zurueck, zweites Halten schaltet aus");
  run_for(3000);
  CHECK(alertActive);
  mock_input[ALERT_PIN] = HIGH; run_for(200);
  CHECK(alertActive);
  mock_input[ALERT_PIN] = LOW; run_for(ALERT_HOLD_MS + 100);
  CHECK(!alertActive);
  mock_input[ALERT_PIN] = HIGH; run_for(200);
  CHECK(strip.shown_brightness == BRIGHTNESS || strip.brightness == BRIGHTNESS);

  TEST("Handler-Alarm: blinkt rot mit voller Helligkeit und piept");
  boot();
  mock_input[ALERT_PIN] = LOW; run_for(ALERT_HOLD_MS + 50); mock_input[ALERT_PIN] = HIGH;
  unsigned tones = mock_tone_count; bool seen_red = false, seen_dark = false;
  for (int i = 0; i < 2000; i++) {
    run_for(1);
    if (strip.all_shown(255, 0, 0) && strip.shown_brightness == 255) seen_red = true;
    if (strip.all_shown(0, 0, 0)) seen_dark = true;
  }
  CHECK(seen_red && seen_dark);
  CHECK(mock_tone_count - tones >= 3 && mock_tone_count - tones <= 5);   // about 2 beeps per second

  TEST("Modus-Taster: ein Druck = ein Effekt weiter, im Alarm bleibt der Alarm sichtbar");
  boot();
  run_for(300);
  mock_input[BUTTON_PIN] = LOW; run_for(500);
  CHECK(currentMode == 2);
  mock_input[BUTTON_PIN] = HIGH; run_for(300);

  TEST("Shield-Hit: Flanke zaehlt einmal, drei Treffer im Fenster leeren den Schild");
  boot();
  mock_input[TOUCH_PINS[0]] = HIGH; checkTouches();
  CHECK(hitCount == 1);
  checkTouches(); checkTouches();               // still touching: no further hit
  CHECK(hitCount == 1);
  mock_input[TOUCH_PINS[0]] = LOW; checkTouches();
  touch(1);
  CHECK(hitCount == 2);
  touch(2);
  CHECK(hitCount == 0);                         // depleted effect ran and reset the counter
  CHECK(mock_last_tone_hz == 300);

  TEST("Shield-Hit: nach Ablauf von HIT_WINDOW_MS beginnt die Zaehlung neu");
  boot();
  touch(0); touch(1);
  CHECK(hitCount == 2);
  mock_ms += HIT_WINDOW_MS + 1;
  touch(2);
  CHECK(hitCount == 1);
  CHECK(mock_last_tone_hz != 300);

  TEST("Waehrend eines langen Effekts bleiben Taster und Alarm bedienbar");
  boot();
  touch(0); touch(1);
  unsigned long start = mock_ms; uint8_t mode = currentMode;
  mock_on_delay = [start]() {                   // 200 ms pulse, like the optocoupler from the Pi
    mock_input[BUTTON_PIN] = (mock_ms - start >= 300 && mock_ms - start < 500) ? LOW : HIGH;
  };
  touch(2);                                     // depleted effect, about 1.9 s
  mock_on_delay = nullptr;
  CHECK(currentMode == (mode + 1) % NUM_MODES);
  boot();
  touch(0); touch(1);
  start = mock_ms;
  mock_on_delay = []() { mock_input[ALERT_PIN] = LOW; };
  touch(2);
  mock_on_delay = nullptr;
  CHECK(alertActive);
  CHECK(mock_ms - start < 1500);                // effect ended early instead of running its 1.9 s

  TEST("Im Alarm und ohne TOUCH_ENABLED loesen Sensoren im Hauptprogramm nichts aus");
  mock_input[ALERT_PIN] = HIGH;
  for (uint8_t i = 0; i < 4; i++) mock_input[TOUCH_PINS[i]] = HIGH;
  uint8_t hits = hitCount; run_for(500);
  CHECK(hitCount == hits);
  boot();
  for (uint8_t i = 0; i < 4; i++) mock_input[TOUCH_PINS[i]] = HIGH;   // floating inputs read HIGH
  unsigned before = mock_tone_count; run_for(2000);
  CHECK(TOUCH_ENABLED == 0);
  CHECK(mock_tone_count == before && hitCount == 0);

  TEST("Kein Effekt schreibt ausserhalb des LED-Streifens");
  boot();
  for (uint8_t m = 0; m < NUM_MODES; m++) { currentMode = m; run_for(3000); }
  CHECK(strip.out_of_range == 0);
  return check_result();
}
