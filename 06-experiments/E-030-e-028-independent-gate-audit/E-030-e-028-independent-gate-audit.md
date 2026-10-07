---
status: active
builds-on: [E-028, DES-004, DES-005, E-016, E-014, E-012]
---
---
status: complete
builds-on: [E-028, DES-004, DES-005, E-016, E-014, E-012]
---

# E-030: independent audit of the E-028 gate

## Verdict

**Bounded rejection of the machine-checkable gate contract; analytical
readiness remains conditional.** The CAD and tolerance claims are reproducible
calculations only. No physical coupon, measurement, or hardware validation was
performed. E-028 is not independently accepted as a machine-checkable
physical result contract until the corrections below are retained and a
dedicated E-028 result checker or equivalent signed schema enforces them.

## Accepted evidence

- The DES-004 CAD gate runs successfully. It reports nominal vane/frame
  clearance 0.1046 mm, assumed worst-case clearance 0.0546 mm, nominal
  axle/bore diametral clearance 0.40 mm, and assumed worst-case 0.30 mm.
  These are CAD/tolerance-derived values, not process capability.
- The E-016 contract tests pass (8 tests), including the 42-row synthetic
  fixture. That fixture is not a measurement result.
- E-012, E-016, DES-004, and DES-005 consistently keep fit, load, readback,
  wear, and coupling performance unresolved pending physical evidence.

## Rejected or corrected findings

### F-1 — writer denominator was arithmetically false (corrected)

E-028 originally stated `300/300`, while its own run sheet required 30
attempts × 5 stops × 2 directions × 2 articles = **600** attempts. The E-016
checker is not a remedy: it checks separate writer rows as `30/30` and does not
parse E-028 records. E-028 now states 600/600 and requires article/stop
identity. A result claiming 300 attempts is rejected.

### F-2 — E-016 is not an E-028 machine checker (unresolved contract gap)

The named E-016 checker validates 42 calibration rows, not E-028's loaded
motion, neighbour displacement, timing event chain, 1,500 reader reads, or
10,000-transition log. It also has no schema for actual applied force, force
tolerance, two-axis writer clearance, reader calibration/threshold, or raw
trace references. Passing E-016 tests therefore cannot be used as an E-028
gate pass. The next physical result must use a dedicated checker or a signed
record whose schema enforces every E-028 row identity and count.

### F-3 — reader margin is not operationally defined (unresolved)

E-028 requires `reader_margin_mm >= 0.20`, but does not define whether this is
an aperture-to-target geometric margin, a calibrated optical separation, or a
confidence-derived quantity. A raw code/confidence and fixed standoff do not
make the margin reproducible. E-028 now requires the declaration, calibration
reference, and calculation; until then reader acceptance is unresolved. This
matches the E-014/E-026 warning that nominal standoff arithmetic is not optical
evidence.

### F-4 — force trace identity did not bind the applied load (unresolved)

The 3.27 N value is a DES-004 design input, not a measurement. An instrument
ID and trace path alone do not require the trace to contain the applied force,
sampling/calibration validity, or an allowed force band. E-028 now explicitly
rejects a result lacking the measured force and tolerance. The force remains
unresolved until physical evidence exists.

### F-5 — “10,000 transitions” was under-specified (corrected condition)

The schedule named commanded states but did not define the initial state or
whether repeated commands count as transitions. A command equal to the prior
settled state is an action but not a state transition. E-028 now requires
previous settled state, freezes initial state and schedule, counts no-ops
separately, and requires exactly 10,000 state-changing transition records.

### F-6 — writer clearance observable was incomplete (corrected condition)

The acceptance rule required clearance in both axes, but the result contract
listed no measured two-axis writer-clearance fields. E-028 now requires those
measurements for every writer attempt/article configuration. A single scalar
or nominal CAD value cannot close this gate.

## Remaining risks

The 0.10 mm neighbour threshold, 0.20 mm writer/reader margins, 3.27 N load,
and zero-error 10,000-transition criterion remain provisional engineering
assumptions, not sourced standards. Timing has completeness/monotonicity
requirements but no performance threshold, so it cannot close the DES-004
30-second analytical claim. Process spread, axle/pin fit, detent torque,
reader optical behaviour, creep, wear, and fixture registration remain
unresolved. No design promotion, procurement, or hardware-validation claim is
justified by this audit.

## Reproduction

The CAD gate and E-016 synthetic contract tests were run on 2026-10-07 and
passed. `./repo check` remains required after this document is committed;
pre-existing structural failures must remain distinguished from E-028
evidence.
