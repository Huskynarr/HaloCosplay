/*
 * Helm LED + Luefter Controller
 *
 * Funktionen:
 *   - Visor-LEDs mit Effekt-Umschaltung (Taster)
 *   - I2C Slave (Adresse 0x08) fuer Pi-Kommandos
 *   - Luefter-PWM Steuerung
 *
 * Verkabelung:
 *   Visor LEDs Data -> Pin 6 (ueber 330 Ohm)
 *   Taster          -> Pin 2 (gegen GND, Pull-Up intern)
 *   Luefter PWM     -> Pin 9
 *   I2C SDA         -> A4
 *   I2C SCL         -> A5
 *
 * I2C Kommandos vom Pi:
 *   Byte 0: Kommando-Typ
 *     0x01 = Visor Helligkeit (Byte 1 = 0-255)
 *     0x02 = Luefter Speed (Byte 1 = 0-255)
 *     0x03 = Effekt waehlen (Byte 1 = 0-4)
 */

#include <Wire.h>
#include <Adafruit_NeoPixel.h>

#define VISOR_PIN    6
#define VISOR_COUNT  10
#define BUTTON_PIN   2
#define FAN_PIN      9
#define I2C_ADDR     0x08
#define NUM_MODES    5

// Visor-Farbe: Warm-Gold/Amber
#define VIS_R  255
#define VIS_G  180
#define VIS_B  20

Adafruit_NeoPixel visor(VISOR_COUNT, VISOR_PIN, NEO_GRB + NEO_KHZ800);

volatile uint8_t visorBrightness = 128;
volatile uint8_t fanSpeed = 180;
volatile uint8_t currentMode = 1;

bool lastButtonState = HIGH;
unsigned long lastDebounce = 0;

void onReceive(int numBytes) {
  if (numBytes < 2) {
    // Altes Protokoll: einzelnes Byte = Helligkeit
    if (numBytes == 1) {
      visorBrightness = Wire.read();
    }
    return;
  }
  uint8_t cmd = Wire.read();
  uint8_t val = Wire.read();
  switch (cmd) {
    case 0x01: visorBrightness = val; break;
    case 0x02: fanSpeed = val; break;
    case 0x03: if (val < NUM_MODES) currentMode = val; break;
  }
}

void setup() {
  Wire.begin(I2C_ADDR);
  Wire.onReceive(onReceive);

  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(FAN_PIN, OUTPUT);

  visor.begin();
  visor.setBrightness(visorBrightness);
  bootSequence();
}

void loop() {
  checkButton();
  analogWrite(FAN_PIN, fanSpeed);
  visor.setBrightness(visorBrightness);

  switch (currentMode) {
    case 0: staticGlow(); break;
    case 1: breathing();  break;
    case 2: heartbeat();  break;
    case 3: chase();      break;
    case 4: idleFlicker(); break;
  }
}

// --- Effekte (Visor) ---

void staticGlow() {
  for (int i = 0; i < VISOR_COUNT; i++) {
    visor.setPixelColor(i, VIS_R, VIS_G, VIS_B);
  }
  visor.show();
  delay(50);
}

void breathing() {
  float val = (sin(millis() / 1500.0) + 1.0) * 0.5;
  uint8_t br = (uint8_t)(val * 255);
  for (int i = 0; i < VISOR_COUNT; i++) {
    visor.setPixelColor(i,
      (uint8_t)(VIS_R * br / 255),
      (uint8_t)(VIS_G * br / 255),
      (uint8_t)(VIS_B * br / 255));
  }
  visor.show();
  delay(10);
}

void heartbeat() {
  pulse(200, 80); pulse(0, 120); delay(100);
  pulse(255, 80); pulse(0, 150); delay(600);
}

void pulse(uint8_t target, uint16_t dur) {
  uint8_t start = visor.getPixelColor(0) >> 8;
  for (uint16_t t = 0; t < dur; t += 10) {
    uint8_t br = start + (int16_t)(target - start) * t / dur;
    setVisor(br);
    delay(10);
  }
}

void chase() {
  static int pos = 0;
  visor.clear();
  visor.setPixelColor(pos, VIS_R, VIS_G, VIS_B);
  int tail = (pos - 1 + VISOR_COUNT) % VISOR_COUNT;
  visor.setPixelColor(tail, VIS_R / 3, VIS_G / 3, VIS_B / 3);
  visor.show();
  pos = (pos + 1) % VISOR_COUNT;
  delay(80);
}

void idleFlicker() {
  for (int i = 0; i < VISOR_COUNT; i++) {
    uint8_t f = random(230, 256);
    visor.setPixelColor(i,
      (uint8_t)(VIS_R * f / 255),
      (uint8_t)(VIS_G * f / 255),
      (uint8_t)(VIS_B * f / 255));
  }
  visor.show();
  delay(50);
}

// --- Boot Sequence ---

void bootSequence() {
  for (int i = 0; i < VISOR_COUNT; i++) {
    visor.setPixelColor(i, VIS_R, VIS_G, VIS_B);
    visor.show();
    delay(100);
  }
  for (int b = 0; b < 3; b++) {
    visor.setBrightness(255);
    visor.show(); delay(80);
    visor.setBrightness(visorBrightness);
    visor.show(); delay(80);
  }
}

// --- Hilfe ---

void setVisor(uint8_t br) {
  for (int i = 0; i < VISOR_COUNT; i++) {
    visor.setPixelColor(i,
      (uint8_t)(VIS_R * br / 255),
      (uint8_t)(VIS_G * br / 255),
      (uint8_t)(VIS_B * br / 255));
  }
  visor.show();
}

void checkButton() {
  bool reading = digitalRead(BUTTON_PIN);
  if (reading == LOW && lastButtonState == HIGH && millis() - lastDebounce > 200) {
    currentMode = (currentMode + 1) % NUM_MODES;
    lastDebounce = millis();
  }
  lastButtonState = reading;
}
