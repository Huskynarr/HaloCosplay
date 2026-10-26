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
 *     0x04 = Visor-Farbe (Byte 1-3 = R, G, B) - z.B. per Sprachbefehl
 *
 * Pegel: Der Pi arbeitet mit 3.3V-I2C. Die internen 5V-Pull-Ups des Nano
 * werden in setup() abgeschaltet, die Pull-Ups des Pi (3.3V) reichen.
 */

#include <Wire.h>
#include <Adafruit_NeoPixel.h>

#define VISOR_PIN    6
#define VISOR_COUNT  10   // z.B. 4 bei vier einzelnen Visor-LEDs
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
volatile uint8_t visR = VIS_R;   // per I2C (0x04) aenderbar
volatile uint8_t visG = VIS_G;
volatile uint8_t visB = VIS_B;

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
    case 0x04:
      if (numBytes >= 4) {
        visR = val;
        visG = Wire.read();
        visB = Wire.read();
      }
      break;
  }
  while (Wire.available()) Wire.read();  // ueberzaehlige Bytes verwerfen
}

void setup() {
  Wire.begin(I2C_ADDR);
  Wire.onReceive(onReceive);
  // Interne 5V-Pull-Ups an SDA/SCL abschalten (Pi-GPIOs vertragen nur 3.3V)
  digitalWrite(SDA, LOW);
  digitalWrite(SCL, LOW);

  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(FAN_PIN, OUTPUT);
  // Timer1 ohne Vorteiler: PWM an Pin 9/10 mit ~31 kHz statt 490 Hz
  // (kein hoerbares Pfeifen des Luefters direkt am Ohr)
  TCCR1B = (TCCR1B & 0b11111000) | 0x01;

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
    visor.setPixelColor(i, visR, visG, visB);
  }
  visor.show();
  delay(50);
}

void breathing() {
  float val = (sin(millis() / 1500.0) + 1.0) * 0.5;
  uint8_t br = (uint8_t)(val * 255);
  for (int i = 0; i < VISOR_COUNT; i++) {
    visor.setPixelColor(i,
      (uint8_t)(visR * br / 255),
      (uint8_t)(visG * br / 255),
      (uint8_t)(visB * br / 255));
  }
  visor.show();
  delay(10);
}

// Doppelpuls als millis()-Envelope: blockiert nicht, Taster und I2C bleiben reaktiv
void heartbeat() {
  uint16_t t = millis() % 1130;
  uint8_t br;
  if      (t <  80) br = map(t,   0,  80,   0, 200);
  else if (t < 200) br = map(t,  80, 200, 200,   0);
  else if (t < 300) br = 0;
  else if (t < 380) br = map(t, 300, 380,   0, 255);
  else if (t < 530) br = map(t, 380, 530, 255,   0);
  else              br = 0;
  setVisor(br);
  delay(10);
}

void chase() {
  static int pos = 0;
  visor.clear();
  visor.setPixelColor(pos, visR, visG, visB);
  int tail = (pos - 1 + VISOR_COUNT) % VISOR_COUNT;
  visor.setPixelColor(tail, visR / 3, visG / 3, visB / 3);
  visor.show();
  pos = (pos + 1) % VISOR_COUNT;
  delay(80);
}

void idleFlicker() {
  for (int i = 0; i < VISOR_COUNT; i++) {
    uint8_t f = random(230, 256);
    visor.setPixelColor(i,
      (uint8_t)(visR * f / 255),
      (uint8_t)(visG * f / 255),
      (uint8_t)(visB * f / 255));
  }
  visor.show();
  delay(50);
}

// --- Boot Sequence ---

void bootSequence() {
  for (int i = 0; i < VISOR_COUNT; i++) {
    visor.setPixelColor(i, visR, visG, visB);
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
      (uint8_t)(visR * br / 255),
      (uint8_t)(visG * br / 255),
      (uint8_t)(visB * br / 255));
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
