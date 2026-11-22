#pragma once
#include "Arduino.h"
#include <vector>

class TwoWire {
 public:
  void begin(int address = 0) { address_ = address; }
  void onReceive(void (*callback)(int)) { callback_ = callback; }
  int available() { return (int)(buffer_.size() - position_); }
  int read() { return available() ? buffer_[position_++] : -1; }
  // Test side: deliver one I2C write transaction to the sketch.
  void mock_receive(std::vector<uint8_t> bytes) {
    buffer_ = bytes; position_ = 0;
    if (callback_) callback_((int)bytes.size());
  }
  int mock_address() const { return address_; }
 private:
  int address_ = 0;
  void (*callback_)(int) = nullptr;
  std::vector<uint8_t> buffer_;
  size_t position_ = 0;
};
inline TwoWire Wire;
