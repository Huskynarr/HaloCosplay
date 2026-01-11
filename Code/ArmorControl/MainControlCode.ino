#include <Adafruit_NeoPixel.h>

#define LED_PIN 5
#define LED_COUNT 24

Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  strip.begin();
  strip.show();
}

void loop() {
  // Simple breathing effect
  for (int b = 0; b <= 255; b += 5) {
    for (int i = 0; i < LED_COUNT; i++) {
      strip.setPixelColor(i, strip.Color(0, b, 0));
    }
    strip.show();
    delay(20);
  }
  for (int b = 255; b >= 0; b -= 5) {
    for (int i = 0; i < LED_COUNT; i++) {
      strip.setPixelColor(i, strip.Color(0, b, 0));
    }
    strip.show();
    delay(20);
  }
}
