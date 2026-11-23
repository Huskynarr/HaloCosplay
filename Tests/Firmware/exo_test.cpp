// Host-Tests fuer Code/ExoControl/LegAssist/exo_core.h (kein Hardwaretest).
#include "exo_core.h"
#include "check.h"

using namespace exo;

static uint32_t now_ms = 0;

// Liefert frische Rueckmeldungen fuer alle Gelenke und rechnet einen Regeltakt.
static void tick(Controller &c, float hipR, float hipL, float kneeR = 0, float kneeL = 0) {
  now_ms += 10;
  c.onFeedback(HIP_R, hipR, 30, 0, now_ms);
  c.onFeedback(HIP_L, hipL, 30, 0, now_ms);
  c.onFeedback(KNEE_R, kneeR, 30, 0, now_ms);
  c.onFeedback(KNEE_L, kneeL, 30, 0, now_ms);
  c.update(now_ms);
}

// Kniebeugung langsam bis 60 Grad
static float bend(int i) { return i < 200 ? i * 0.3f : 60.0f; }

static Controller ready(bool knees = false) {
  Controller c;
  c.cfg.kneesInstalled = knees;
  c.begin();
  for (int i = 0; i < 5; i++) tick(c, 0, 0);
  c.calibrateZero();
  return c;
}

// Gangmuster: 0,9 Hz, 20 Grad Amplitude, beginnt im Stand (keine Winkelspruenge).
static float hip_angle(float t, float phase) { return 20.0f * sinf(2.0f * 3.14159265f * 0.9f * t + phase); }

int main() {
  TEST("CAN-Rahmen nach Handbuch");
  {
    uint8_t b[8];
    packTorque(b, RANGE_AK80_9, 0.0f);
    CHECK(b[0] == 0 && b[1] == 0 && b[2] == 0);          // Kp = Kd = 0
    CHECK(b[3] == 0x7F && b[4] == 0xFF);                 // Position 0 -> Mitte
    CHECK(b[5] == 0x7F && b[6] == 0xF7 && b[7] == 0xFF); // Geschwindigkeit 0, Moment 0
    packTorque(b, RANGE_AK80_9, 25.0f);
    CHECK((b[6] & 0x0F) == 0x0F && b[7] == 0xFF);
    packTorque(b, RANGE_AK80_9, -99.0f);                 // ausserhalb: auf -tMax begrenzt
    CHECK((b[6] & 0x0F) == 0x00 && b[7] == 0x00);
    packMit(b, RANGE_AK80_9, 0, 0, 500.0f, 5.0f, 0);
    CHECK(b[0] == 0xFF && (b[1] >> 4) >= 0xE && (b[1] & 0xF) == 0xF && b[2] >= 0xFE);  // Rundung wie im Handbuch
    CHECK(mitCommandId(3) == 0x803);
    const uint8_t rx[8] = {0xFF, 0x38, 0, 0, 0, 0, 41, 6};  // -200 -> -20,0 Grad
    Feedback f = parseFeedback(rx);
    CHECK(fabsf(f.positionDeg + 20.0f) < 0.01f && f.tempC == 41 && f.error == 6);
  }

  TEST("Ohne Rueckmeldung und ohne Nullpunkt kein Moment");
  {
    Controller c;
    c.begin();
    now_ms += 10;
    c.update(now_ms);
    CHECK(c.state() == STATE_BOOT);
    CHECK(!c.setLevel(1));
    for (int i = 0; i < 5; i++) tick(c, 12, -7);
    CHECK(c.state() == STATE_STANDBY);
    CHECK(!c.setLevel(1));                 // nicht kalibriert
    CHECK(c.calibrateZero());
    CHECK(fabsf(c.angleDeg(HIP_R)) < 0.01f);
    CHECK(c.setLevel(1) && c.state() == STATE_ASSIST);
    CHECK(!c.setLevel(4));
  }

  TEST("Gehen: positive Leistung an beiden Hueften, Grenze und Anstieg eingehalten");
  {
    Controller c = ready();
    c.setLevel(2);
    float powerR = 0, powerL = 0, peak = 0, maxStep = 0, lastR = 0, prevR = 0, prevL = 0;
    for (int i = 0; i < 1000; i++) {
      float t = i * 0.01f;
      float qR = hip_angle(t, 0), qL = hip_angle(t, 3.14159265f);
      if (i == 0) { prevR = qR; prevL = qL; }
      tick(c, qR, qL);
      if (i > 400) {
        powerR += c.torqueNm(HIP_R) * (qR - prevR);
        powerL += c.torqueNm(HIP_L) * (qL - prevL);
        if (fabsf(c.torqueNm(HIP_R)) > peak) peak = fabsf(c.torqueNm(HIP_R));
      }
      float step = fabsf(c.torqueNm(HIP_R) - lastR);
      if (step > maxStep) maxStep = step;
      lastR = c.torqueNm(HIP_R);
      prevR = qR; prevL = qL;
    }
    CHECK(c.state() == STATE_ASSIST);
    CHECK(powerR > 0 && powerL > 0);
    CHECK(peak > 1.0f && peak <= c.torqueLimit() + 1e-4f);
    CHECK(maxStep <= c.cfg.slewNmPerS * 0.01f + 1e-4f);
    CHECK(c.torqueNm(KNEE_R) == 0 && c.torqueNm(KNEE_L) == 0);   // keine Knie verbaut
  }

  TEST("Einblenden: direkt nach dem Einschalten noch kein volles Moment");
  {
    Controller c = ready();
    c.setLevel(3);
    float early = 0;
    for (int i = 0; i < 40; i++) {
      tick(c, hip_angle(i * 0.01f, 0), hip_angle(i * 0.01f, 3.14159265f));
      if (fabsf(c.torqueNm(HIP_R)) > early) early = fabsf(c.torqueNm(HIP_R));
    }
    CHECK(early < 1.0f);
  }

  TEST("Stillstand in Schrittstellung: Moment klingt ab");
  {
    Controller c = ready();
    c.setLevel(3);
    for (int i = 0; i < 600; i++) tick(c, hip_angle(i * 0.01f, 0), hip_angle(i * 0.01f, 3.14159265f));
    float holdR = hip_angle(5.99f, 0), holdL = hip_angle(5.99f, 3.14159265f);
    CHECK(fabsf(holdR - holdL) > 15.0f);
    for (int i = 0; i < 400; i++) tick(c, holdR, holdL);
    CHECK(fabsf(c.torqueNm(HIP_R)) < 0.05f && fabsf(c.torqueNm(HIP_L)) < 0.05f);
    CHECK(c.state() == STATE_ASSIST);
  }

  TEST("Arbeitsgrenze wird auf die feste Obergrenze gekappt");
  {
    Controller c = ready();
    c.cfg.torqueLimitNm = 50.0f;
    c.cfg.hipGainNm[3] = 200.0f;
    c.setLevel(3);
    float peak = 0;
    for (int i = 0; i < 800; i++) {
      tick(c, hip_angle(i * 0.01f, 0), hip_angle(i * 0.01f, 3.14159265f));
      if (fabsf(c.torqueNm(HIP_L)) > peak) peak = fabsf(c.torqueNm(HIP_L));
    }
    CHECK(peak > 8.0f && peak <= ABS_TORQUE_LIMIT_NM + 1e-4f);
  }

  TEST("Stufe 0 nimmt das Moment mit begrenzter Rate zurueck");
  {
    Controller c = ready();
    c.setLevel(3);
    int i = 0;
    for (; i < 700 || (fabsf(c.torqueNm(HIP_R)) < 1.0f && i < 2000); i++)
      tick(c, hip_angle(i * 0.01f, 0), hip_angle(i * 0.01f, 3.14159265f));
    float before = fabsf(c.torqueNm(HIP_R));
    c.setLevel(0);
    tick(c, hip_angle(i * 0.01f, 0), hip_angle(i * 0.01f, 3.14159265f));
    CHECK(c.state() == STATE_STANDBY);
    CHECK(fabsf(c.torqueNm(HIP_R)) < before && fabsf(c.torqueNm(HIP_R)) >= before - 0.2f - 1e-4f);
    for (int k = 0; k < 100; k++) tick(c, 0, 0);
    CHECK(c.torqueNm(HIP_R) == 0 && c.torqueNm(HIP_L) == 0);
  }

  TEST("Stoerungen schalten sofort momentenfrei und bleiben gespeichert");
  {
    // Rueckmeldung bleibt aus
    Controller c = ready();
    c.setLevel(2);
    for (int i = 0; i < 700; i++) tick(c, hip_angle(i * 0.01f, 0), hip_angle(i * 0.01f, 3.14159265f));
    CHECK(fabsf(c.torqueNm(HIP_R)) + fabsf(c.torqueNm(HIP_L)) > 0.1f);
    for (int i = 0; i < 6; i++) {
      now_ms += 10;
      c.onFeedback(HIP_R, hip_angle(6.99f, 0), 30, 0, now_ms);   // linke Huefte meldet sich nicht mehr
      c.update(now_ms);
    }
    CHECK(c.state() == STATE_FAULT && c.fault() == FAULT_FEEDBACK_TIMEOUT);
    CHECK(c.torqueNm(HIP_R) == 0 && c.torqueNm(HIP_L) == 0);
    for (int i = 0; i < 50; i++) tick(c, 0, 0);
    CHECK(c.state() == STATE_FAULT);           // heilt nicht von selbst
    CHECK(!c.setLevel(1));
    CHECK(c.clearFault());
    for (int i = 0; i < 3; i++) tick(c, 0, 0);
    CHECK(c.state() == STATE_STANDBY && c.level() == 0 && c.torqueNm(HIP_R) == 0);

    // Fehlercode des Antriebs
    Controller m = ready();
    m.setLevel(1);
    now_ms += 10;
    m.onFeedback(HIP_R, 0, 30, 7, now_ms);
    m.onFeedback(HIP_L, 0, 30, 0, now_ms);
    m.update(now_ms);
    CHECK(m.fault() == FAULT_MOTOR_ERROR);

    // Treibertemperatur
    Controller h = ready();
    now_ms += 10;
    h.onFeedback(HIP_R, 0, 30, 0, now_ms);
    h.onFeedback(HIP_L, 0, 71, 0, now_ms);
    h.update(now_ms);
    CHECK(h.fault() == FAULT_OVERTEMP);

    // Not-Aus, Quittieren erst nach Freigabe
    Controller e = ready();
    e.setLevel(1);
    e.setEstop(true);
    tick(e, 0, 0);
    CHECK(e.fault() == FAULT_ESTOP && !e.clearFault());
    e.setEstop(false);
    CHECK(e.clearFault());

    // Unplausibel schnelle Bewegung
    Controller s = ready();
    s.setLevel(1);
    tick(s, 0, 0);
    tick(s, 30, 0);
    tick(s, 60, 0);
    CHECK(s.fault() == FAULT_OVERSPEED);

    // Winkel ausserhalb des Bewegungsbereichs
    Controller r = ready();
    for (int i = 0; i < 400; i++) tick(r, 0, -i * 0.1f);
    CHECK(r.fault() == FAULT_RANGE);

    // Regeltakt haengt
    Controller o = ready();
    o.setLevel(1);
    tick(o, 0, 0);
    now_ms += 200;
    o.onFeedback(HIP_R, 0, 30, 0, now_ms);
    o.onFeedback(HIP_L, 0, 30, 0, now_ms);
    o.update(now_ms);
    CHECK(o.fault() == FAULT_LOOP_OVERRUN);
  }

  TEST("Randzone: kein Moment in Richtung Anschlag");
  {
    Controller c = ready();
    c.cfg.hipMaxDeg = 30.0f;
    c.cfg.hipMinDeg = -30.0f;
    c.setLevel(3);
    bool pushed_out = false;
    for (int i = 0; i < 1500; i++) {
      float t = i * 0.01f;
      float qR = 28.0f * sinf(2.0f * 3.14159265f * 0.9f * t), qL = -qR;
      tick(c, qR, qL);
      float room = c.torqueNm(HIP_R) > 0 ? 30.0f - qR : qR + 30.0f;
      if (fabsf(c.torqueNm(HIP_R)) > c.torqueLimit() * room / 10.0f + 1e-3f) pushed_out = true;
    }
    CHECK(!pushed_out && c.state() == STATE_ASSIST);
  }

  TEST("Knie: Streckmoment nur verbaut, freigegeben und bei belastetem Fuss");
  {
    Controller off = ready(true);
    off.setLevel(3);
    off.setFootLoaded(true, true);
    for (int i = 0; i < 400; i++) tick(off, 0, 0, bend(i), bend(i));
    CHECK(off.torqueNm(KNEE_R) == 0 && off.torqueNm(KNEE_L) == 0);   // kneeAssist aus

    Controller c = ready(true);
    c.cfg.kneeAssist = true;
    c.setLevel(3);
    c.setFootLoaded(true, false);
    for (int i = 0; i < 400; i++) tick(c, 0, 0, bend(i), bend(i));
    CHECK(c.torqueNm(KNEE_R) < -1.0f && c.torqueNm(KNEE_R) >= -c.torqueLimit());
    CHECK(c.torqueNm(KNEE_L) == 0);                                   // Schwungbein frei
    c.setFootLoaded(false, false);
    for (int i = 0; i < 100; i++) tick(c, 0, 0, 60, 60);
    CHECK(c.torqueNm(KNEE_R) == 0);

    Controller k = ready(true);                                       // Knie ohne Rueckmeldung
    for (int i = 0; i < 6; i++) {
      now_ms += 10;
      k.onFeedback(HIP_R, 0, 30, 0, now_ms);
      k.onFeedback(HIP_L, 0, 30, 0, now_ms);
      k.onFeedback(KNEE_R, 0, 30, 0, now_ms);
      k.update(now_ms);
    }
    CHECK(k.fault() == FAULT_FEEDBACK_TIMEOUT);
  }

  return check_result();
}
