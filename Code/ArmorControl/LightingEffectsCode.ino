#include <Adafruit_NeoPixel.h>

#define LED_PIN 5
#define LED_COUNT 24

Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  strip.begin();
  strip.show();
}

void loop() {
  // Simple chase effect
  for (int i = 0; i < LED_COUNT; i++) {
    strip.clear();
    strip.setPixelColor(i, strip.Color(0, 150, 0));
    strip.show();
    delay(40);
  }
}
