#pragma once
#include "Arduino.h"
#include <vector>

#define NEO_GRB 0
#define NEO_KHZ800 0

struct MockPixel { uint8_t r, g, b; };

class Adafruit_NeoPixel {
 public:
  Adafruit_NeoPixel(int count, int pin, int = 0) : pin_(pin), pixels_(count, MockPixel{0, 0, 0}), shown_(count, MockPixel{0, 0, 0}) {}
  void begin() {}
  void setBrightness(uint8_t value) { brightness = value; }
  void setPixelColor(int index, uint8_t r, uint8_t g, uint8_t b) {
    if (index >= 0 && index < (int)pixels_.size()) pixels_[index] = MockPixel{r, g, b}; else out_of_range++;
  }
  void clear() { for (auto &pixel : pixels_) pixel = MockPixel{0, 0, 0}; }
  void show() { shown_ = pixels_; shown_brightness = brightness; show_count++; }
  int numPixels() const { return (int)pixels_.size(); }
  // Test side: state as of the last show().
  const MockPixel &shown(int index) const { return shown_[index]; }
  bool all_shown(uint8_t r, uint8_t g, uint8_t b) const {
    for (const auto &pixel : shown_) if (pixel.r != r || pixel.g != g || pixel.b != b) return false;
    return true;
  }
  uint8_t brightness = 255, shown_brightness = 255;
  unsigned show_count = 0, out_of_range = 0;
 private:
  int pin_;
  std::vector<MockPixel> pixels_, shown_;
};
