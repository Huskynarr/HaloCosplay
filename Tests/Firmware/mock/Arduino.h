// Minimal Arduino stand-in for host tests (see ../README.md). Time is virtual:
// delay() advances mock_ms, so blocking effects finish instantly.
#pragma once
#include <cstdint>
#include <cstdlib>
#include <functional>
#include <math.h>

#define HIGH 1
#define LOW 0
#define INPUT 0
#define OUTPUT 1
#define INPUT_PULLUP 2
#define SDA 18
#define SCL 19

typedef bool boolean;
typedef uint8_t byte;

const int MOCK_PINS = 64;
inline unsigned long mock_ms = 0;
inline int mock_input[MOCK_PINS] = {};        // what digitalRead() returns
inline int mock_output[MOCK_PINS] = {};       // last digitalWrite()
inline int mock_pwm[MOCK_PINS] = {};          // last analogWrite(), -1 = never
inline int mock_mode[MOCK_PINS] = {};
inline unsigned mock_tone_count = 0;
inline unsigned mock_last_tone_hz = 0;
inline std::function<void()> mock_on_delay;   // called on every delay(), lets a test change inputs mid-effect
inline uint8_t TCCR1B = 0;

inline void mock_reset_board() {
  mock_ms = 0;
  for (int i = 0; i < MOCK_PINS; i++) { mock_input[i] = LOW; mock_output[i] = LOW; mock_pwm[i] = -1; mock_mode[i] = INPUT; }
  mock_tone_count = 0; mock_last_tone_hz = 0; mock_on_delay = nullptr; TCCR1B = 0;
}

inline unsigned long millis() { return mock_ms; }
inline void delay(unsigned long ms) { mock_ms += ms; if (mock_on_delay) mock_on_delay(); }
inline void pinMode(int pin, int mode) { mock_mode[pin] = mode; }
inline int digitalRead(int pin) { return mock_input[pin]; }
inline void digitalWrite(int pin, int value) { mock_output[pin] = value; }
inline void analogWrite(int pin, int value) { mock_pwm[pin] = value; }
inline void tone(int, unsigned hz, unsigned long = 0) { mock_tone_count++; mock_last_tone_hz = hz; }
inline void noTone(int) {}
inline void noInterrupts() {}
inline void interrupts() {}
inline long map(long x, long in_min, long in_max, long out_min, long out_max) {
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
inline long random(long low, long high) {
  static unsigned long state = 12345;
  state = state * 1103515245UL + 12345UL;
  return low + (long)((state >> 16) % (unsigned long)(high - low));
}
inline long random(long high) { return random(0, high); }
