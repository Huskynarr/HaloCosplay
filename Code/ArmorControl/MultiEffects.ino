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
 * Verkabelung:
 *   LED Data -> Pin 5 (ueber 330 Ohm Widerstand)
 *   Taster   -> Pin 2 (gegen GND, interner Pull-Up)
 *   +5V/GND  -> LED Strip Power (1000 uF Elko!)
 *
 * Anpassen: LED_COUNT, LED_PIN, BUTTON_PIN, Farbe (HUE)
 */

#include <Adafruit_NeoPixel.h>

#define LED_PIN     5
#define LED_COUNT   24
#define BUTTON_PIN  2
#define NUM_MODES   5
#define BRIGHTNESS  128   // 50% = guter Convention-Wert (0-255)

// Farbe: Gruen-Cyan (MJOLNIR Tech-Glow)
#define COLOR_R  0
#define COLOR_G  200
#define COLOR_B  60

Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

uint8_t currentMode = 1;  // Start mit Breathing
bool lastButtonState = HIGH;
unsigned long lastDebounce = 0;

void setup() {
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  strip.begin();
  strip.setBrightness(BRIGHTNESS);
  bootSequence();
}

void loop() {
  checkButton();

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
  for (int i = 0; i < LED_COUNT; i++) {
    strip.setPixelColor(i,
      (uint8_t)(COLOR_R * br / 255),
      (uint8_t)(COLOR_G * br / 255),
      (uint8_t)(COLOR_B * br / 255));
  }
  strip.show();
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
  setAll(br);
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

void setAll(uint8_t br) {
  for (int i = 0; i < LED_COUNT; i++) {
    strip.setPixelColor(i,
      (uint8_t)(COLOR_R * br / 255),
      (uint8_t)(COLOR_G * br / 255),
      (uint8_t)(COLOR_B * br / 255));
  }
  strip.show();
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
