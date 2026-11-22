// Host tests for Code/HelmetControl/HelmetMultiEffects.ino (included above by run.py).
#include "check.h"

static void boot() {
  mock_reset_board();
  mock_input[BUTTON_PIN] = HIGH;            // pull-up, button released
  visorBrightness = 128; fanSpeed = FAN_DEFAULT; i2cActivity = false; lastI2cMs = 0;
  currentMode = 1; visR = VIS_R; visG = VIS_G; visB = VIS_B;
  lastButtonState = HIGH; lastDebounce = 0;
  setup();
}

static void run_for(unsigned long ms) {
  unsigned long end = mock_ms + ms;
  while (mock_ms < end) loop();
}

int main() {
  TEST("Start: I2C-Adresse, Pull-Ups aus, Luefter laeuft schon waehrend der Boot-Animation");
  boot();
  CHECK(Wire.mock_address() == I2C_ADDR);
  CHECK(mock_output[SDA] == LOW && mock_output[SCL] == LOW);
  CHECK(mock_pwm[FAN_PIN] == FAN_DEFAULT);
  CHECK(mock_ms >= 1000);                   // boot animation ran (blocking, once)
  run_for(100);
  CHECK(mock_pwm[FAN_PIN] == FAN_DEFAULT);

  TEST("0x01 setzt die Helligkeit, einzelnes Byte bleibt als altes Protokoll gueltig");
  boot();
  Wire.mock_receive({0x01, 77}); run_for(50);
  CHECK(visor.shown_brightness == 77);
  Wire.mock_receive({200}); run_for(50);
  CHECK(visor.shown_brightness == 200);

  TEST("0x02: Werte unter FAN_MIN_SPIN werden angehoben, 0 bleibt aus");
  boot();
  Wire.mock_receive({0x02, 40}); run_for(50);
  CHECK(mock_pwm[FAN_PIN] == FAN_MIN_SPIN);
  Wire.mock_receive({0x02, 0}); run_for(50);
  CHECK(mock_pwm[FAN_PIN] == 0);

  TEST("Failsafe: gedrosselter Luefter faellt nach FAN_FAILSAFE_MS ohne Pi auf Standard zurueck");
  boot();
  Wire.mock_receive({0x02, 0}); run_for(FAN_FAILSAFE_MS - 500);
  CHECK(mock_pwm[FAN_PIN] == 0);            // not early
  run_for(1000);
  CHECK(mock_pwm[FAN_PIN] == FAN_DEFAULT);

  TEST("Failsafe: regelmaessige Bestaetigung haelt den Luefter aus");
  boot();
  for (int i = 0; i < 12; i++) { Wire.mock_receive({0x02, 0}); run_for(3000); }
  CHECK(mock_pwm[FAN_PIN] == 0);

  TEST("Failsafe: jedes gueltige Kommando zaehlt als Lebenszeichen, ein unbekanntes nicht");
  boot();
  Wire.mock_receive({0x02, 0}); run_for(6000);
  Wire.mock_receive({0x01, 90}); run_for(6000);
  CHECK(mock_pwm[FAN_PIN] == 0);            // brightness command kept it alive
  boot();
  Wire.mock_receive({0x02, 0}); run_for(6000);
  Wire.mock_receive({0x7F, 1}); run_for(6000);
  CHECK(mock_pwm[FAN_PIN] == FAN_DEFAULT);  // unknown command is no sign of life

  TEST("Failsafe: Werte ab FAN_DEFAULT bleiben ohne Pi bestehen");
  boot();
  Wire.mock_receive({0x02, 255}); run_for(3 * FAN_FAILSAFE_MS);
  CHECK(mock_pwm[FAN_PIN] == 255);

  TEST("0x03: nur gueltige Effekte, 0x04: Farbe nur mit drei Farbbytes");
  boot();
  Wire.mock_receive({0x03, 3}); CHECK(currentMode == 3);
  Wire.mock_receive({0x03, NUM_MODES}); CHECK(currentMode == 3);
  Wire.mock_receive({0x04, 10, 20, 30});
  CHECK(visR == 10 && visG == 20 && visB == 30);
  Wire.mock_receive({0x04, 99});
  CHECK(visR == 10 && visG == 20 && visB == 30);
  Wire.mock_receive({0x03, 0}); run_for(100);  // static glow shows the commanded color
  CHECK(visor.all_shown(10, 20, 30));

  TEST("Ueberzaehlige und leere Uebertragungen stoeren das naechste Kommando nicht");
  boot();
  Wire.mock_receive({0x01, 50, 1, 2, 3, 4, 5});
  CHECK(Wire.available() == 0);
  Wire.mock_receive({});
  Wire.mock_receive({0x01, 60}); run_for(50);
  CHECK(visor.shown_brightness == 60);

  TEST("Taster schaltet genau einen Effekt weiter, Halten und Prellen zaehlen nicht mehrfach");
  boot();
  run_for(300);
  mock_input[BUTTON_PIN] = LOW; run_for(20);
  mock_input[BUTTON_PIN] = HIGH; run_for(20);  // contact bounce inside the 200 ms window
  mock_input[BUTTON_PIN] = LOW; run_for(1000); // then held for a second
  CHECK(currentMode == 2);
  mock_input[BUTTON_PIN] = HIGH; run_for(300);
  for (int i = 0; i < NUM_MODES - 1; i++) {
    mock_input[BUTTON_PIN] = LOW; run_for(300);
    mock_input[BUTTON_PIN] = HIGH; run_for(300);
  }
  CHECK(currentMode == 1);                     // wrapped around once

  TEST("Prellen beim Loslassen nach langem Halten zaehlt nicht als zweiter Druck");
  boot();
  run_for(300);
  mock_input[BUTTON_PIN] = LOW; run_for(1000);
  CHECK(currentMode == 2);
  mock_input[BUTTON_PIN] = HIGH; run_for(10);  // released ...
  mock_input[BUTTON_PIN] = LOW; run_for(10);   // ... contact bounces closed once more
  mock_input[BUTTON_PIN] = HIGH; run_for(500);
  CHECK(currentMode == 2);

  TEST("Ein 200-ms-Puls (Optokoppler vom Pi) zaehlt in jedem Effekt genau einmal, zwei Druecke zweimal");
  boot();
  run_for(300);
  for (int i = 0; i < 2 * NUM_MODES; i++) {
    uint8_t before = currentMode;
    mock_input[BUTTON_PIN] = LOW; run_for(200);
    mock_input[BUTTON_PIN] = HIGH; run_for(400);
    CHECK(currentMode == (before + 1) % NUM_MODES);
  }

  TEST("Kein Effekt schreibt ausserhalb des LED-Streifens oder blockiert laenger als 100 ms");
  boot();
  for (uint8_t mode = 0; mode < NUM_MODES; mode++) {
    Wire.mock_receive({0x03, mode});
    for (int i = 0; i < 400; i++) {
      unsigned long before = mock_ms;
      loop();
      CHECK(mock_ms - before <= 100);
    }
  }
  CHECK(visor.out_of_range == 0);
  return check_result();
}
