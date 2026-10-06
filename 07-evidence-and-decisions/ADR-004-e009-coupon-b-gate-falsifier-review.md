---
status: active
builds-on: [E-009, E-006, E-007, E-008, DES-003, Q-005, Q-011]
---

# Falsifier review: E-009 Coupon-B regional-coupling gate

## Verdict

**UNRESOLVED — not ready as a reproducible engineering gate.** This is not a
hardware rejection. No physical test, FEA, material test, or measured stiffness
exists. DES-003's 0.10 mm untouched-neighbour claim remains unqualified.

## Acceptance-criteria review

The protocol covers the required 5×5, 10×10, and 20×20 cases, update direction,
neighbour peak/residual motion, and eventual pass conditions. The `coupon_b_gate.py`
check reproduces the existing calculated sensitivity: at 5% assumed coupling,
required stiffness is 26.16 / 58.86 / 124.26 N/mm for 5×5 / 10×10 / 20×20.
These are calculations from assumed coupling and a design-calculated 3.27 N load,
not evidence of performance.

## Reproducibility failures

The gate cannot yet be repeated independently because it does not freeze:

- the actual update trajectory, speed, acceleration, dwell, and settle interval;
- the representative miniature mass, contact geometry, load application, or
  whether the 3.27 N load is static throughout the update;
- sensor type, axis convention, resolution, bandwidth/sample rate, calibration,
  reference datum, uncertainty, zero-drift treatment, and synchronization;
- fixture support stiffness, preload, seam/contact condition, and the exact
  10×10/20×20 extent and boundary orientation;
- repeat count, baseline/control runs, acceptance treatment for uncertainty,
  and a non-circular rule for selecting the “worst” orientation.

“Rate sufficient,” “normal trajectory,” and “defined settle interval” are
unresolved placeholders, not reproducible controls. Without them, a reported
0.10 mm result cannot distinguish neighbour motion from fixture motion, sensor
noise, transient aliasing, or residual drift.

## Cheapest credible falsification path

Before full regional sweeps, CTO should authorize one instrumented quasi-static
5×5 boundary case using the existing coupon fixture: record fixture/reference
motion with the update disabled, apply the specified loaded-neighbour mass, and
repeat the update with a calibrated vertical and lateral displacement logger.
Freeze and record trajectory, sensor bandwidth/calibration, support condition,
load/mass, settle time, and at least three repeats in the run sheet. A single
repeat exceeding 0.10 mm peak or residual after subtracting the disabled-update
baseline falsifies the 5×5 case; a clean result only removes that low-cost risk
and does not qualify 10×10 or 20×20.

## Handoff

CTO follow-up: convert the omissions above into a controlled run sheet and
instrumentation definition, then execute the existing E-009 sequence when
physical testing is authorized. Do not promote DES-003 or infer full-scale
stiffness from the sensitivity script. Reassess all three sizes after measured
coupling, support compliance, trajectory, peak motion, and residual error exist.
