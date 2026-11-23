// exo_core.h - Regel- und Sicherheitslogik des Eigenbau-Beinantriebs E01
//
// Hardwarefrei: keine Arduino- oder CAN-Aufrufe. LegAssist.ino bindet diese
// Datei ein, Tests/Firmware/exo_test.cpp prueft sie auf dem Host.
// Entwicklungsstand, an keiner Hardware erprobt. Anleitung und Nachweisfolge:
// Documentation/Guides/Exoskelett-Eigenbau.md
//
// Vorzeichen: Winkel und Moment sind bei Beugung (Flexion) positiv, fuer
// Huefte und Knie gleich. Ein negatives Moment streckt das Gelenk.
#pragma once
#include <math.h>
#include <stdint.h>

namespace exo {

const float DEG2RAD = 0.01745329252f;
// Obergrenze fuer das Arbeitsmoment, unabhaengig von der Konfiguration.
// Projektentscheidung (Nennmoment AK80-9), keine medizinisch hergeleitete Grenze.
const float ABS_TORQUE_LIMIT_NM = 9.0f;
const uint8_t LEVEL_COUNT = 4;       // Stufe 0 = mitlaufen ohne Moment
const uint8_t DELAY_BUFFER = 64;

enum Joint : uint8_t { HIP_R = 0, HIP_L = 1, KNEE_R = 2, KNEE_L = 3, JOINT_COUNT = 4 };
enum State : uint8_t { STATE_BOOT, STATE_STANDBY, STATE_ASSIST, STATE_FAULT };
enum Fault : uint8_t {
  FAULT_NONE, FAULT_FEEDBACK_TIMEOUT, FAULT_MOTOR_ERROR, FAULT_OVERTEMP,
  FAULT_OVERSPEED, FAULT_RANGE, FAULT_ESTOP, FAULT_LOOP_OVERRUN
};

struct Config {
  bool kneesInstalled = false;   // false: nur Hueftantriebe (Stufe H), true: vier Antriebe
  bool kneeAssist = false;       // Kniemoment nur mit Fersensensor und eigenem Nachweis
  uint16_t periodMs = 10;        // fester Regeltakt; update() muss in diesem Takt laufen
  float torqueLimitNm = 3.0f;    // Arbeitsgrenze, wird auf ABS_TORQUE_LIMIT_NM gekappt
  float hipGainNm[LEVEL_COUNT] = {0.0f, 3.0f, 6.0f, 9.0f};  // Verstaerkung je Stufe
  float delayS = 0.25f;          // Verzoegerung der Rueckfuehrung
  float filterS = 0.03f;         // Glaettung des Winkelsignals
  float gateOffPerS = 0.3f;      // unterhalb: keine Gehbewegung erkannt, kein Moment
  float gateOnPerS = 1.0f;       // oberhalb: volle Verstaerkung
  float gateTimeS = 0.4f;
  float kneeSpringNm = 4.0f;     // Streckmoment bei 90 Grad Kniebeugung und belastetem Fuss
  float slewNmPerS = 20.0f;      // maximale Momentenaenderung
  float rampInS = 2.0f;          // Einblenden nach dem Einschalten der Unterstuetzung
  float hipMinDeg = -25.0f, hipMaxDeg = 100.0f;
  float kneeMinDeg = -2.0f, kneeMaxDeg = 110.0f;
  float softZoneDeg = 10.0f;     // Moment in Richtung Anschlag laeuft hier auf null aus
  float rangeMarginDeg = 8.0f;   // weiter ausserhalb: Stoerung
  float maxSpeedDegS = 500.0f;
  uint32_t feedbackTimeoutMs = 50;
  int8_t maxDriverTempC = 70;
};

struct JointData {
  float rawDeg = 0, offsetDeg = 0, angleDeg = 0, speedDegS = 0, torqueNm = 0;
  uint32_t lastMs = 0;
  int8_t tempC = 0;
  uint8_t error = 0;
  bool seen = false;
};

class Controller {
 public:
  Config cfg;

  void begin() {
    for (uint8_t i = 0; i < JOINT_COUNT; i++) j_[i] = JointData();
    state_ = STATE_BOOT;
    fault_ = FAULT_NONE;
    level_ = 0;
    calibrated_ = estop_ = started_ = false;
    footLoaded_[0] = footLoaded_[1] = false;
    resetAssist();
  }

  bool installed(uint8_t j) const { return j < KNEE_R || (j < JOINT_COUNT && cfg.kneesInstalled); }

  // Rueckmeldung eines Antriebs: Abtriebswinkel in Grad (Rohwert), Treibertemperatur, Fehlercode.
  void onFeedback(uint8_t j, float rawDeg, int8_t tempC, uint8_t error, uint32_t nowMs) {
    if (j >= JOINT_COUNT) return;
    JointData &d = j_[j];
    if (d.seen && nowMs != d.lastMs) {
      float speed = (rawDeg - d.rawDeg) * 1000.0f / (float)(nowMs - d.lastMs);
      d.speedDegS = 0.5f * d.speedDegS + 0.5f * speed;
    }
    d.rawDeg = rawDeg;
    d.angleDeg = rawDeg - d.offsetDeg;
    d.tempC = tempC;
    d.error = error;
    d.lastMs = nowMs;
    d.seen = true;
  }

  void setEstop(bool active) { estop_ = active; }
  void setFootLoaded(bool right, bool left) { footLoaded_[0] = right; footLoaded_[1] = left; }

  // Nullpunkt im aufrechten Stand uebernehmen. Nur im Bereitschaftszustand.
  bool calibrateZero() {
    if (state_ != STATE_STANDBY) return false;
    for (uint8_t i = 0; i < JOINT_COUNT; i++) {
      if (!installed(i)) continue;
      j_[i].offsetDeg = j_[i].rawDeg;
      j_[i].angleDeg = 0;
    }
    calibrated_ = true;
    return true;
  }

  // Stufe 0 schaltet die Unterstuetzung ab, 1..3 schalten sie ein (nur kalibriert).
  bool setLevel(uint8_t level) {
    if (level >= LEVEL_COUNT) return false;
    if (state_ != STATE_STANDBY && state_ != STATE_ASSIST) return false;
    if (level == 0) {
      level_ = 0;
      state_ = STATE_STANDBY;
      return true;
    }
    if (!calibrated_) return false;
    if (state_ == STATE_STANDBY) resetAssist();
    level_ = level;
    state_ = STATE_ASSIST;
    return true;
  }

  // Stoerung quittieren: nur ohne Not-Aus; danach Bereitschaft mit Stufe 0.
  bool clearFault() {
    if (state_ != STATE_FAULT || estop_) return false;
    for (uint8_t i = 0; i < JOINT_COUNT; i++) j_[i].seen = false;
    fault_ = FAULT_NONE;
    level_ = 0;
    state_ = STATE_BOOT;
    return true;
  }

  // Einmal je Regeltakt aufrufen. Danach torqueNm() an die Antriebe senden.
  void update(uint32_t nowMs) {
    float dt = started_ ? (float)(nowMs - lastUpdateMs_) / 1000.0f : 0.0f;
    lastUpdateMs_ = nowMs;
    started_ = true;

    if (state_ == STATE_FAULT) return zeroAll();
    if (estop_) return trip(FAULT_ESTOP);

    if (state_ == STATE_BOOT) {
      zeroAll();
      for (uint8_t i = 0; i < JOINT_COUNT; i++)
        if (installed(i) && !j_[i].seen) return;
      state_ = STATE_STANDBY;
      return;
    }

    for (uint8_t i = 0; i < JOINT_COUNT; i++) {
      if (!installed(i)) continue;
      const JointData &d = j_[i];
      if (nowMs - d.lastMs > cfg.feedbackTimeoutMs) return trip(FAULT_FEEDBACK_TIMEOUT);
      if (d.error != 0) return trip(FAULT_MOTOR_ERROR);
      if (d.tempC > cfg.maxDriverTempC) return trip(FAULT_OVERTEMP);
      if (!calibrated_) continue;
      if (fabsf(d.speedDegS) > cfg.maxSpeedDegS) return trip(FAULT_OVERSPEED);
      if (d.angleDeg < minDeg(i) - cfg.rangeMarginDeg || d.angleDeg > maxDeg(i) + cfg.rangeMarginDeg)
        return trip(FAULT_RANGE);
    }

    float target[JOINT_COUNT] = {0, 0, 0, 0};
    if (state_ == STATE_ASSIST) {
      if (dt <= 0.0f) return;
      if (dt > 5.0f * cfg.periodMs / 1000.0f) return trip(FAULT_LOOP_OVERRUN);
      computeTargets(dt, target);
    }

    float limit = torqueLimit();
    float step = cfg.slewNmPerS * dt;
    for (uint8_t i = 0; i < JOINT_COUNT; i++) {
      if (!installed(i)) { j_[i].torqueNm = 0; continue; }
      float want = clampf(target[i], -limit, limit);
      float out = j_[i].torqueNm + clampf(want - j_[i].torqueNm, -step, step);
      j_[i].torqueNm = capNearLimit(i, out, limit);
    }
  }

  float torqueNm(uint8_t j) const { return j < JOINT_COUNT ? j_[j].torqueNm : 0.0f; }
  float angleDeg(uint8_t j) const { return j < JOINT_COUNT ? j_[j].angleDeg : 0.0f; }
  float torqueLimit() const { return clampf(cfg.torqueLimitNm, 0.0f, ABS_TORQUE_LIMIT_NM); }
  State state() const { return state_; }
  Fault fault() const { return fault_; }
  uint8_t level() const { return level_; }
  bool calibrated() const { return calibrated_; }

  static float clampf(float v, float lo, float hi) { return v < lo ? lo : (v > hi ? hi : v); }

 private:
  JointData j_[JOINT_COUNT];
  State state_ = STATE_BOOT;
  Fault fault_ = FAULT_NONE;
  uint8_t level_ = 0;
  bool calibrated_ = false, estop_ = false, started_ = false;
  bool footLoaded_[2] = {false, false};
  uint32_t lastUpdateMs_ = 0;
  float ring_[DELAY_BUFFER];
  uint8_t head_ = 0;
  float filtered_ = 0, envelope_ = 0, ramp_ = 0;
  bool filterPrimed_ = false;

  float minDeg(uint8_t j) const { return j < KNEE_R ? cfg.hipMinDeg : cfg.kneeMinDeg; }
  float maxDeg(uint8_t j) const { return j < KNEE_R ? cfg.hipMaxDeg : cfg.kneeMaxDeg; }

  void zeroAll() {
    for (uint8_t i = 0; i < JOINT_COUNT; i++) j_[i].torqueNm = 0;
  }

  void trip(Fault f) {
    fault_ = f;
    state_ = STATE_FAULT;
    level_ = 0;
    zeroAll();
  }

  void resetAssist() {
    for (uint8_t i = 0; i < DELAY_BUFFER; i++) ring_[i] = 0;
    head_ = 0;
    filtered_ = envelope_ = ramp_ = 0;
    filterPrimed_ = false;
  }

  // Verzoegerte Rueckfuehrung der Hueftwinkeldifferenz (siehe Guide, Abschnitt 6).
  void computeTargets(float dt, float *target) {
    float y = sinf(j_[HIP_R].angleDeg * DEG2RAD) - sinf(j_[HIP_L].angleDeg * DEG2RAD);
    if (!filterPrimed_) { filtered_ = y; filterPrimed_ = true; }
    float before = filtered_;
    filtered_ += dt / (cfg.filterS + dt) * (y - filtered_);
    float rate = fabsf(filtered_ - before) / dt;
    envelope_ += dt / (cfg.gateTimeS + dt) * (rate - envelope_);
    float gate = clampf((envelope_ - cfg.gateOffPerS) / (cfg.gateOnPerS - cfg.gateOffPerS), 0.0f, 1.0f);

    int samples = (int)(cfg.delayS * 1000.0f / cfg.periodMs + 0.5f);
    if (samples < 1) samples = 1;
    if (samples > DELAY_BUFFER - 1) samples = DELAY_BUFFER - 1;
    ring_[head_] = filtered_;
    float delayed = ring_[(head_ + DELAY_BUFFER - samples) % DELAY_BUFFER];
    head_ = (head_ + 1) % DELAY_BUFFER;

    ramp_ = clampf(ramp_ + dt / cfg.rampInS, 0.0f, 1.0f);
    float hip = cfg.hipGainNm[level_] * gate * ramp_ * delayed;
    target[HIP_R] = -hip;
    target[HIP_L] = hip;

    if (cfg.kneesInstalled && cfg.kneeAssist) {
      float share = ramp_ * (float)level_ / (float)(LEVEL_COUNT - 1);
      for (uint8_t side = 0; side < 2; side++) {
        float bend = j_[KNEE_R + side].angleDeg;
        if (footLoaded_[side] && bend > 0.0f)
          target[KNEE_R + side] = -cfg.kneeSpringNm * share * sinf(clampf(bend, 0.0f, 90.0f) * DEG2RAD);
      }
    }
  }

  // Moment, das zum Anschlag hin wirkt, laeuft in der Randzone linear auf null aus.
  float capNearLimit(uint8_t j, float torque, float limit) const {
    float room = torque > 0 ? maxDeg(j) - j_[j].angleDeg : j_[j].angleDeg - minDeg(j);
    float allowed = limit * clampf(room / cfg.softZoneDeg, 0.0f, 1.0f);
    return clampf(torque, -allowed, allowed);
  }
};

// --- CAN-Rahmen der CubeMars-AK-Antriebe, Treiber V3, Kraftregelung (MIT) ---
// Nach "V3 Drive Software User Manual" V1.0.1, Abschnitt 2.2 und 2.3.1.
// Am eigenen Antrieb pruefen: aeltere Treiber nutzen ein anderes Rahmenformat.

struct MitRange { float pMax, vMax, tMax, kpMax, kdMax; };
const MitRange RANGE_AK80_9 = {12.56f, 65.0f, 25.0f, 500.0f, 5.0f};
const MitRange RANGE_AK60_6 = {12.56f, 60.0f, 12.0f, 500.0f, 5.0f};

const uint32_t CAN_MODE_MIT = 8;        // Kommando: (8 << 8) | Antriebs-ID, Extended Frame
const uint32_t CAN_FEEDBACK = 0x29;     // Rueckmeldung: (0x29 << 8) | Antriebs-ID

inline uint32_t mitCommandId(uint8_t driveId) { return (CAN_MODE_MIT << 8) | driveId; }

inline uint32_t floatToUint(float x, float lo, float hi, uint8_t bits) {
  if (x < lo) x = lo;
  if (x > hi) x = hi;
  return (uint32_t)((x - lo) * ((float)((1u << bits) - 1u) / (hi - lo)));
}

inline void packMit(uint8_t *out, const MitRange &r, float posRad, float velRadS, float kp, float kd, float torqueNm) {
  uint32_t p = floatToUint(posRad, -r.pMax, r.pMax, 16);
  uint32_t v = floatToUint(velRadS, -r.vMax, r.vMax, 12);
  uint32_t kpInt = floatToUint(kp, 0, r.kpMax, 12);
  uint32_t kdInt = floatToUint(kd, 0, r.kdMax, 12);
  uint32_t t = floatToUint(torqueNm, -r.tMax, r.tMax, 12);
  out[0] = (uint8_t)(kpInt >> 4);
  out[1] = (uint8_t)(((kpInt & 0xF) << 4) | (kdInt >> 8));
  out[2] = (uint8_t)(kdInt & 0xFF);
  out[3] = (uint8_t)(p >> 8);
  out[4] = (uint8_t)(p & 0xFF);
  out[5] = (uint8_t)(v >> 4);
  out[6] = (uint8_t)(((v & 0xF) << 4) | (t >> 8));
  out[7] = (uint8_t)(t & 0xFF);
}

// Nur Moment, ohne Lage- und Geschwindigkeitsregler: der Antrieb bleibt nachgiebig.
inline void packTorque(uint8_t *out, const MitRange &r, float torqueNm) {
  packMit(out, r, 0.0f, 0.0f, 0.0f, 0.0f, torqueNm);
}

struct Feedback { float positionDeg; int8_t tempC; uint8_t error; };

inline Feedback parseFeedback(const uint8_t *d) {
  Feedback f;
  f.positionDeg = (float)(int16_t)((uint16_t)d[0] << 8 | d[1]) * 0.1f;
  f.tempC = (int8_t)d[6];
  f.error = d[7];
  return f;
}

}  // namespace exo
