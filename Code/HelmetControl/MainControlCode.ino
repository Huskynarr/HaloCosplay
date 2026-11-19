/*
 * Helm-LED Basis-Controller (I2C-Slave 0x08)
 *
 * Versteht dasselbe Protokoll wie HelmetMultiEffects.ino, setzt aber nur
 * die Helligkeit um:
 *   [0x01, wert]  Visor-Helligkeit 0-255
 *   [wert]        altes Ein-Byte-Protokoll = Helligkeit
 * Andere Kommandos (Luefter 0x02, Effekt 0x03, Farbe 0x04) werden ignoriert,
 * statt das Kommando-Byte als Helligkeit zu deuten.
 */
#include <Wire.h>

const uint8_t LED_PIN = 6;
volatile uint8_t brightness = 0;

void onReceive(int bytes) {
  if (bytes == 1) {
    brightness = Wire.read();
  } else if (bytes >= 2) {
    uint8_t cmd = Wire.read();
    uint8_t val = Wire.read();
    if (cmd == 0x01) brightness = val;
  }
  while (Wire.available()) Wire.read();  // ueberzaehlige Bytes verwerfen
}

void setup() {
  Wire.begin(0x08);  // I2C address
  Wire.onReceive(onReceive);
  // Interne 5V-Pull-Ups an SDA/SCL abschalten (Pi-GPIOs vertragen nur 3.3V)
  digitalWrite(SDA, LOW);
  digitalWrite(SCL, LOW);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  analogWrite(LED_PIN, brightness);
  delay(10);
}
