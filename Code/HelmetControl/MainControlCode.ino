#include <Wire.h>

const uint8_t LED_PIN = 6;
volatile uint8_t brightness = 0;

void onReceive(int bytes) {
  if (bytes > 0) {
    brightness = Wire.read();
  }
}

void setup() {
  Wire.begin(0x08);  // I2C address
  Wire.onReceive(onReceive);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  analogWrite(LED_PIN, brightness);
  delay(10);
}
