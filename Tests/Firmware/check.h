#pragma once
#include <cstdio>
inline int check_failures = 0, check_total = 0;
#define CHECK(condition) do { check_total++; if (!(condition)) { check_failures++; \
  std::printf("  FEHLER %s:%d: %s\n", __FILE__, __LINE__, #condition); } } while (0)
#define TEST(name) std::printf("- %s\n", name)
inline int check_result() {
  std::printf("%d Pruefungen, %d fehlgeschlagen\n", check_total, check_failures);
  return check_failures ? 1 : 0;
}
