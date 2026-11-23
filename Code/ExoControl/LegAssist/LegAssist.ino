// LegAssist.ino - Steuerung des Eigenbau-Beinantriebs X01 (ESP32 + CAN)
//
// ENTWICKLUNGSSTAND, AN KEINER HARDWARE ERPROBT. Nicht am Koerper betreiben,
// bevor die Nachweisfolge in Documentation/Guides/Exoskelett-Eigenbau.md
// (Pruefstand ohne Person zuerst) durchlaufen ist.
//
// Aufbau: 2 Hueftantriebe (Stufe H) oder 4 Antriebe mit Knien (Stufe K),
// CubeMars AK-Serie mit Treiber V3 in Kraftregelung (MIT), CAN 1 Mbit/s.
// Regel- und Sicherheitslogik: exo_core.h (auf dem Host getestet).
//
// Board: ESP32 Dev Module, CAN-Transceiver 3,3 V (z.B. SN65HVD230).
// Der Not-Aus trennt die Motorversorgung in Hardware; dieser Sketch liest
// ihn nur zusaetzlich mit. Software ist keine Sicherheitseinrichtung.

#include "driver/twai.h"
#include "exo_core.h"

// ---------------- Aufbau anpassen ----------------
#define KNEES_INSTALLED 0        // 1 = vier Antriebe (Huefte + Knie)
#define KNEE_ASSIST 0            // 1 erst nach bestandenem Hueft-Nachweis und mit Fersensensoren
#define TORQUE_LIMIT_NM 3.0f     // Arbeitsgrenze; exo_core.h kappt bei 9 Nm
#define MOTOR_RANGE exo::RANGE_AK80_9

#define PIN_CAN_TX 5
#define PIN_CAN_RX 4
#define PIN_BUTTON 25            // gegen GND, interner Pull-Up
#define PIN_ESTOP 26             // Oeffnerkontakt gegen GND: LOW = frei, offen/HIGH = Not-Aus
#define PIN_LED 2
#define PIN_HEEL_R 34            // Fersensensor (FSR-Spannungsteiler), nur fuer KNEE_ASSIST
#define PIN_HEEL_L 35
#define HEEL_THRESHOLD 1500      // ADC-Rohwert 0..4095, am Aufbau einmessen

// CAN-ID und Drehsinn je Gelenk: Huefte R, Huefte L, Knie R, Knie L.
// Drehsinn am Pruefstand bestimmen: positives Moment muss das Gelenk beugen.
const uint8_t DRIVE_ID[exo::JOINT_COUNT] = {1, 2, 3, 4};
const float DRIVE_SIGN[exo::JOINT_COUNT] = {1.0f, -1.0f, 1.0f, -1.0f};
// -------------------------------------------------

#define PERIOD_MS 10
#define DEBOUNCE_MS 50
#define LONG_PRESS_MS 2000

exo::Controller ctrl;
unsigned long nextTick = 0, lastLog = 0, lastEdge = 0, pressedAt = 0;
bool buttonDown = false, longHandled = false, canOk = false;

void sendTorque(uint8_t joint, float torqueNm) {
  twai_message_t msg = {};
  msg.identifier = exo::mitCommandId(DRIVE_ID[joint]);
  msg.extd = 1;
  msg.data_length_code = 8;
  exo::packTorque(msg.data, MOTOR_RANGE, torqueNm * DRIVE_SIGN[joint]);
  twai_transmit(&msg, 0);
}

void readCan(unsigned long now) {
  twai_message_t msg;
  while (twai_receive(&msg, 0) == ESP_OK) {
    if (!msg.extd || msg.rtr || msg.data_length_code != 8) continue;
    if ((msg.identifier >> 8) != exo::CAN_FEEDBACK) continue;
    uint8_t id = msg.identifier & 0xFF;
    for (uint8_t j = 0; j < exo::JOINT_COUNT; j++) {
      if (DRIVE_ID[j] != id) continue;
      exo::Feedback f = exo::parseFeedback(msg.data);
      ctrl.onFeedback(j, f.positionDeg * DRIVE_SIGN[j], f.tempC, f.error, now);
    }
  }
}

// Kurz druecken: Stufe 0 -> 1 -> 2 -> 3 -> 0. Zwei Sekunden halten: im Stand
// Nullpunkt setzen, nach einer Stoerung quittieren.
void readButton(unsigned long now) {
  bool down = digitalRead(PIN_BUTTON) == LOW;
  if (down != buttonDown && now - lastEdge > DEBOUNCE_MS) {
    lastEdge = now;
    buttonDown = down;
    if (down) {
      pressedAt = now;
      longHandled = false;
    } else if (!longHandled) {
      ctrl.setLevel((ctrl.level() + 1) % exo::LEVEL_COUNT);
    }
  }
  if (buttonDown && !longHandled && now - pressedAt >= LONG_PRESS_MS) {
    longHandled = true;
    if (ctrl.state() == exo::STATE_FAULT) ctrl.clearFault();
    else ctrl.calibrateZero();
  }
}

void showState(unsigned long now) {
  bool on;
  switch (ctrl.state()) {
    case exo::STATE_ASSIST: on = true; break;
    case exo::STATE_FAULT: on = (now / 100) % 2; break;                          // schnelles Blinken
    case exo::STATE_STANDBY: on = ctrl.calibrated() ? (now / 1000) % 2 : (now % 2000) < 100; break;
    default: on = false;
  }
  digitalWrite(PIN_LED, on ? HIGH : LOW);
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_BUTTON, INPUT_PULLUP);
  pinMode(PIN_ESTOP, INPUT_PULLUP);
  pinMode(PIN_LED, OUTPUT);

  ctrl.cfg.kneesInstalled = KNEES_INSTALLED;
  ctrl.cfg.kneeAssist = KNEE_ASSIST;
  ctrl.cfg.torqueLimitNm = TORQUE_LIMIT_NM;
  ctrl.cfg.periodMs = PERIOD_MS;
  ctrl.begin();

  twai_general_config_t general = TWAI_GENERAL_CONFIG_DEFAULT((gpio_num_t)PIN_CAN_TX, (gpio_num_t)PIN_CAN_RX, TWAI_MODE_NORMAL);
  twai_timing_config_t timing = TWAI_TIMING_CONFIG_1MBITS();
  twai_filter_config_t filter = TWAI_FILTER_CONFIG_ACCEPT_ALL();
  canOk = twai_driver_install(&general, &timing, &filter) == ESP_OK && twai_start() == ESP_OK;
  if (!canOk) Serial.println("{\"error\":\"can_init\"}");
  nextTick = millis();
}

void loop() {
  unsigned long now = millis();
  if ((long)(now - nextTick) < 0) return;
  nextTick += PERIOD_MS;
  if ((long)(now - nextTick) > PERIOD_MS) nextTick = now + PERIOD_MS;   // nach Haenger nicht aufholen

  if (canOk) readCan(now);
  readButton(now);
  ctrl.setEstop(digitalRead(PIN_ESTOP) == HIGH);
#if KNEE_ASSIST
  ctrl.setFootLoaded(analogRead(PIN_HEEL_R) > HEEL_THRESHOLD, analogRead(PIN_HEEL_L) > HEEL_THRESHOLD);
#endif
  ctrl.update(now);

  // Auch in Bereitschaft und Stoerung wird Moment null gesendet: der Antrieb
  // bleibt nachgiebig. Ohne Rueckmeldung (STATE_BOOT) laeuft das genauso.
  if (canOk) {
    for (uint8_t j = 0; j < exo::JOINT_COUNT; j++)
      if (ctrl.installed(j)) sendTorque(j, ctrl.torqueNm(j));
  }

  showState(now);
  if (now - lastLog >= 100) {
    lastLog = now;
    Serial.printf("{\"state\":%u,\"fault\":%u,\"level\":%u,\"hipR\":%.1f,\"hipL\":%.1f,\"tR\":%.2f,\"tL\":%.2f}\n",
                  ctrl.state(), ctrl.fault(), ctrl.level(), ctrl.angleDeg(exo::HIP_R), ctrl.angleDeg(exo::HIP_L),
                  ctrl.torqueNm(exo::HIP_R), ctrl.torqueNm(exo::HIP_L));
  }
}
