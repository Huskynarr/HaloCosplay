// bench_core.h - Pruefstandlogik fuer EINEN Antrieb (Nachweisstufen P1 und P2)
//
// Hardwarefrei, auf dem Host getestet (Tests/Firmware/bench_test.cpp). Nur fuer
// den fest eingespannten Antrieb ohne Person. Kein Ersatz fuer den Not-Aus in
// der Motorleitung.
#ifndef BENCH_CORE_H
#define BENCH_CORE_H

#include <stdint.h>
#include <stdlib.h>

namespace bench {

struct Bench {
  float limitNm = 2.0f;        // Arbeitsgrenze am Pruefstand
  float slewNmPerS = 5.0f;     // Anstiegsbegrenzung
  uint32_t holdMs = 5000;      // Totmann: ohne neues Kommando geht das Sollmoment auf null
  uint32_t periodMs = 10;

  // Zeile von der seriellen Schnittstelle:
  //   t <Nm>  Sollmoment setzen (wird auf +/- limitNm begrenzt), startet die Haltezeit neu
  //   z       Sollmoment null
  //   s       keine CAN-Kommandos mehr senden (Verhalten des Antriebs beobachten)
  //   r       wieder senden; beginnt mit Moment null
  // Rueckgabe false: Zeile nicht verstanden, nichts geaendert.
  bool command(const char *line, uint32_t nowMs) {
    while (*line == ' ') line++;
    char c = *line;
    const char *rest = line + 1;
    if (c == 't') {
      char *end = nullptr;
      float value = strtof(rest, &end);
      if (end == rest) return false;
      while (*end == ' ' || *end == '\r' || *end == '\n') end++;
      if (*end != 0 || value != value) return false;
      target_ = value > limitNm ? limitNm : (value < -limitNm ? -limitNm : value);
      lastCommandMs_ = nowMs;
      return true;
    }
    while (*rest == ' ' || *rest == '\r' || *rest == '\n') rest++;
    if (*rest != 0) return false;
    if (c == 'z') { target_ = 0; return true; }
    if (c == 's') { sending_ = false; target_ = 0; output_ = 0; return true; }
    if (c == 'r') { sending_ = true; target_ = 0; output_ = 0; return true; }
    return false;
  }

  void setEstop(bool active) { estop_ = active; }

  void onFeedback(uint32_t nowMs) {
    if (frames_ > 0) lastIntervalMs_ = nowMs - lastFeedbackMs_;
    lastFeedbackMs_ = nowMs;
    frames_++;
  }

  // Einmal je Takt. Not-Aus und abgelaufene Haltezeit setzen das Moment sofort auf null.
  void update(uint32_t nowMs) {
    if (estop_) { target_ = 0; output_ = 0; return; }
    if (target_ != 0 && nowMs - lastCommandMs_ >= holdMs) { target_ = 0; output_ = 0; timedOut_ = true; return; }
    float step = slewNmPerS * (float)periodMs / 1000.0f;
    if (output_ < target_) output_ = output_ + step > target_ ? target_ : output_ + step;
    else if (output_ > target_) output_ = output_ - step < target_ ? target_ : output_ - step;
  }

  float torqueNm() const { return sending_ ? output_ : 0.0f; }
  float targetNm() const { return target_; }
  bool sending() const { return sending_; }
  bool estop() const { return estop_; }
  bool timedOut() const { return timedOut_; }
  void clearTimedOut() { timedOut_ = false; }
  uint32_t frames() const { return frames_; }
  uint32_t lastIntervalMs() const { return lastIntervalMs_; }
  // Zeit seit der letzten Rueckmeldung; ohne jede Rueckmeldung der groesste Wert.
  uint32_t feedbackAgeMs(uint32_t nowMs) const { return frames_ ? nowMs - lastFeedbackMs_ : 0xFFFFFFFFu; }

 private:
  float target_ = 0, output_ = 0;
  uint32_t lastCommandMs_ = 0, lastFeedbackMs_ = 0, lastIntervalMs_ = 0, frames_ = 0;
  bool sending_ = true, estop_ = false, timedOut_ = false;
};

}  // namespace bench

#endif
