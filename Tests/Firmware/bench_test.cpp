// Host-Tests fuer Code/ExoControl/LegAssist/bench_core.h (kein Hardwaretest).
#include "bench_core.h"
#include "check.h"

#include <math.h>

using namespace bench;

static bool near(float a, float b) { return fabsf(a - b) < 1e-4f; }

int main() {
  TEST("Kommandos");
  {
    Bench b;
    CHECK(b.command("t 1.5", 0) && near(b.targetNm(), 1.5f));
    CHECK(b.command("t -0.5\r\n", 0) && near(b.targetNm(), -0.5f));
    CHECK(b.command("  t 9", 0) && near(b.targetNm(), 2.0f));      // Arbeitsgrenze
    CHECK(b.command("t -9", 0) && near(b.targetNm(), -2.0f));
    CHECK(!b.command("t", 0) && !b.command("t abc", 0) && !b.command("t 1 2", 0) && !b.command("t nan", 0));
    CHECK(near(b.targetNm(), -2.0f));                                // Unverstandenes aendert nichts
    CHECK(!b.command("x", 0) && !b.command("", 0) && !b.command("zz", 0));
    CHECK(b.command("z", 0) && b.targetNm() == 0);
  }

  TEST("Anstiegsbegrenzung");
  {
    Bench b;
    b.command("t 1", 0);
    b.update(10);
    CHECK(near(b.torqueNm(), 0.05f));                                // 5 Nm/s * 10 ms
    for (uint32_t t = 20; t <= 300; t += 10) b.update(t);
    CHECK(near(b.torqueNm(), 1.0f));                                 // kein Ueberschwingen
    b.command("z", 300);
    b.update(310);
    CHECK(near(b.torqueNm(), 0.95f));                                // auch abwaerts begrenzt
  }

  TEST("Totmann-Haltezeit");
  {
    Bench b;
    b.command("t 1", 1000);
    for (uint32_t t = 1010; t < 6000; t += 10) b.update(t);
    CHECK(near(b.torqueNm(), 1.0f) && !b.timedOut());
    b.update(6000);
    CHECK(b.torqueNm() == 0 && b.targetNm() == 0 && b.timedOut());   // sofort null, nicht ausgeblendet
    b.command("t 1", 6000);                                          // neues Kommando startet neu
    b.update(6010);
    CHECK(b.torqueNm() > 0);
  }

  TEST("Not-Aus");
  {
    Bench b;
    b.command("t 2", 0);
    for (uint32_t t = 10; t <= 500; t += 10) b.update(t);
    CHECK(near(b.torqueNm(), 2.0f));
    b.setEstop(true);
    b.update(510);
    CHECK(b.torqueNm() == 0 && b.targetNm() == 0);
    b.setEstop(false);
    b.update(520);
    CHECK(b.torqueNm() == 0);                                        // bleibt null bis zum naechsten Kommando
  }

  TEST("Senden anhalten");
  {
    Bench b;
    b.command("t 1", 0);
    for (uint32_t t = 10; t <= 300; t += 10) b.update(t);
    CHECK(b.command("s", 300) && !b.sending() && b.torqueNm() == 0);
    b.command("t 1", 310);
    for (uint32_t t = 320; t <= 600; t += 10) b.update(t);
    CHECK(b.torqueNm() == 0);                                        // angehalten: nach aussen null
    CHECK(b.command("r", 600) && b.sending() && b.torqueNm() == 0);  // Wiederaufnahme beginnt bei null
  }

  TEST("Rueckmeldungsstatistik");
  {
    Bench b;
    CHECK(b.frames() == 0 && b.feedbackAgeMs(50) == 0xFFFFFFFFu);
    b.onFeedback(100);
    b.onFeedback(102);
    CHECK(b.frames() == 2 && b.lastIntervalMs() == 2 && b.feedbackAgeMs(110) == 8);
  }

  return check_result();
}
