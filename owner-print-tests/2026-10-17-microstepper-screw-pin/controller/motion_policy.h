#pragma once
#include <stdint.h>
#include <math.h>

// 20 full steps/rev is a provisional motor parameter: verify on the bare motor.
constexpr int FULL_STEPS = 20;
constexpr int MICROSTEPS = 8;
constexpr int STEPS_PER_REV = FULL_STEPS * MICROSTEPS;
constexpr int PIN_LIMIT = STEPS_PER_REV / 2; // +/-1.5 mm from manual centre
constexpr float MAX_RPM = 120.0f;
inline bool planMove(bool pinMode, int32_t position, float revs, int32_t &steps) {
  if (!isfinite(revs) || fabs(revs) > 1.0f) return false;
  steps = lroundf(revs * STEPS_PER_REV);
  if (steps == 0) return false;
  int32_t next = position + steps;
  return !pinMode || (next >= -PIN_LIMIT && next <= PIN_LIMIT);
}
