---
status: superseded
builds-on: [E-006, E-007, E-008, DES-003, Q-005]
---

Research disposition: retained historical protocol/geometry evidence. ADR-009 supersedes its former next-task prescriptions. Reuse is conditional on a new decision-relevant mechanism/model; this record does not require fabrication or continued repair of the old family.

# E-009: Coupon-B stiffness and regional-coupling protocol

## Purpose and scope

This is a bounded, pre-physical-test protocol for deciding whether the
`DES-003` baseline can satisfy the proposed **0.10 mm peak motion of an
untouched loaded neighbour** during 5×5, 10×10, and 20×20 regional updates,
without A-004 couplers. It does not redesign DES-003 and does not repeat the
E-006 sensitivity calculation.

Evidence in this record is either calculated or CAD-derived. No print,
purchase, material test, FEA, or physical validation has been performed.

## Frozen 5×5 screening run sheet (pre-physical-test definition)

This section freezes the cheapest credible physical screen for review by the
future test owner. It is a paper procedure and contains no measurement result.
The existing `a1_coupon_b_5x5.scad` is the fixture definition: 40 × 40 × 3.0
mm base, 5.08 mm pitch, 25 sockets, and a centre-cell miniature plinth. The
centre cell is the untouched loaded-neighbour station; the surrounding cells
are the available update region. This is therefore a 5×5 coupon boundary case,
not evidence that all 25 cells are updated simultaneously.

### Run identification and controlled inputs

The test owner fills one row per run before motion is enabled:

```text
run_id, date, operator, fixture_revision, coupon_serial, cell_serials
orientation_id, update_direction, controller_firmware, logger_file
miniature_id, miniature_mass_g, applied_service_load_N, contact_description
support_description, sensor_serials, calibration_due_dates, ambient_note
```

The following are frozen controls or explicitly labeled assumptions:

| Item | Frozen definition | Evidence class |
|---|---|---|
| Cell pitch and coupon | 5.08 mm pitch; 40 × 40 × 3.0 mm CAD coupon; centre plinth 30 mm diameter × 2 mm | CAD-derived |
| Service load | 3.27 N design-calculated load, applied vertically through the centre of the plinth; record actual deadweight/load-cell result separately | calculated input; physical value unresolved |
| Miniature | Representative 28–35 mm-base figure seated concentrically on the plinth; mass and base/contact geometry recorded before each run | sourced from CAD description; actual item unresolved |
| Support | Coupon hard-seated on the same three-point or four-point support fixture for every run; support count, pad material, preload and seam condition recorded | proposed control; stiffness unresolved |
| Update region | Centre station excluded from the command; use the same selected surrounding-cell boundary for all repeats | proposed control |
| Direction | Run both commanded update directions; define direction in fixture X/Y coordinates, not operator viewpoint | proposed control |
| Motion command | Normalized stroke 0 → 100% → 0%: 0.25 s ramp, 0.50 s high-state dwell, 0.25 s return; 2.0 s post-return settle before the residual sample | assumed screening waveform; DES-003 compatibility unresolved |

If the actuator cannot reproduce the assumed waveform, stop before collecting
the gate result and replace the row with the actual encoder trajectory and a
new reviewable run-sheet revision. Do not silently substitute “normal
trajectory”. Record commanded and measured position/time if an encoder is
available; otherwise trajectory remains unresolved and the result is only a
setup check.

### Instrumentation minimum and reference frame

Use the least instrumentation that can separate coupon motion from support or
frame motion:

1. One calibrated displacement channel normal to the coupon (`Z_N`) aimed at
   the loaded centre station.
2. One calibrated lateral displacement channel in fixture X (`X_N`) aimed at
   the same station or a rigidly attached target that preserves the X line of
   action.
3. One vertical reference channel (`Z_R`) aimed at a rigid datum attached to
   the support frame, plus one lateral reference channel (`X_R`) on that datum.
4. A command/encoder time channel (`CMD`) or a logger trigger shared by all
   channels. A load-cell channel (`F`) is preferred; if unavailable, calibrated
   deadweights and a scale reading are mandatory setup records.

The reported neighbour motion is the synchronized difference
`dZ = Z_N - Z_R` and `dX = X_N - X_R`, after each channel's zero correction.
The reference datum must not be attached to the moving coupon. Sensor axes are
positive away from the fixture in Z and positive along marked fixture X; mount
photos and a dimensioned datum sketch belong with the run file.

Minimum logger settings are 1 kS/s per analogue displacement/load channel and
at least 16-bit conversion. These are proposed alias-control settings, not
sensor performance claims. The test owner may use a faster logger but may not
down-sample before peak extraction. Record anti-alias filter type and corner
frequency; it must be at or below one-half the sample rate and documented with
the data. `CMD` and all analogue channels must share a trigger or have a
measured time offset.

Before each run, record calibration certificate, range, resolution, stated
expanded uncertainty and calibration date for every channel. Perform a zero
check with no update motion, then a two-point or manufacturer-approved
traceable check over the expected displacement range. The provisional data
quality targets are channel resolution ≤0.01 mm and expanded uncertainty
`U95 ≤0.02 mm`; these are acceptance-screen assumptions, not sourced sensor
specifications. If either target is not met, retain the data but mark the gate
unresolved rather than declaring pass/fail.

### Controlled sequence

1. Inspect the coupon, cells, plinth, supports, wiring and sensor targets;
   photograph the setup. Reject the setup for visible crack, loose cell,
   sensor saturation, cable contact, or an unrecorded support contact.
2. Install the specified miniature and apply the 3.27 N service load. Confirm
   contact is concentric and does not touch the fixture or sensor target.
   Record mass, load application height, contact diameter and any preload.
3. With update commands disabled, collect 5.0 s of `Z_N`, `X_N`, `Z_R`, `X_R`
   and `F` (or the deadweight setup). This is the disabled-update baseline.
4. Execute one commanded direction using the frozen waveform. Capture from
   1.0 s before command start through 5.0 s after return. Do not touch the
   fixture or reload between baseline and update.
5. Wait until the 2.0 s settle interval has elapsed, then leave the load in
   place and collect the final residual window. The settled value is the mean
   over the final 0.5 s; if drift is visible, report its slope and mark the
   residual unresolved.
6. Repeat steps 3–5 three times in the same orientation and direction. Then
   repeat the three-run set in the opposite direction. Re-zero only between
   run sets and record the zero change; do not hide drift by re-zeroing each
   trace.
7. For the first pass, test the four rotations of the coupon/support datum
   (0°, 90°, 180°, 270°) using one repeat per rotation. Select the worst
   orientation by the largest baseline-subtracted `max(|dZ|, |dX|)` across
   that scout set, before collecting its three-repeat set. This is a fixed
   selection rule, not a choice made after seeing the final repeats.

### Reduction, baseline and uncertainty rules

For each update trace, subtract the time-aligned disabled-update baseline and
the rigid-datum reference channel. Report separately:

```text
d_peak = max over update window of max(abs(dZ), abs(dX))
d_residual = max(abs(mean_final(dZ)), abs(mean_final(dX)))
baseline_drift = slope of each reference-corrected baseline channel
```

Use the same filtering and peak window for every run; publish the raw trace,
filtered trace, command trace, baseline trace, and exact reduction settings.
Do not average away a peak. For each run, attach the instrument uncertainty
to the reported displacement; a conservative screening interval is
`reported value ± U95_combined`, where `U95_combined` is calculated from the
calibration uncertainty and baseline/reference repeatability. The formula and
component values must be recorded by the test owner; no value is invented here.

The proposed Q-005 gate is met only when every required run has
`d_peak ≤ 0.10 mm` and `d_residual ≤ 0.10 mm`, no tip-over, stall or fracture
occurs, and the upper uncertainty bound does not cross 0.10 mm. If the upper
bound crosses the limit, disposition is **unresolved**, not a pass. Any run
with a missing channel, saturated channel, timing ambiguity, baseline drift,
unknown contact, or unverified trajectory is **invalid/setup failure** and is
repeated after correction; it is not removed from the sample set.

### Stop conditions and dispositions

Stop motion immediately for miniature tip-over, cell ejection, hinge stall,
fracture, unexpected contact, sensor saturation, support slip, or a command
trajectory outside the frozen envelope. Preserve the raw data and photograph
the state. The physical-test owner records whether the disposition is
`damage`, `instrument/setup`, `trajectory`, `load/contact`, or `support` and
whether the coupon is safe to reuse. A stop is not a pass or a falsification
until the failure mechanism is reviewed.

The 5×5 screen is **falsified** only by a valid required run exceeding the
motion gate after baseline/reference correction, or by a repeatable physical
failure intrinsic to the tested DES-003 configuration. It is **passed for
screening only** when all valid required runs meet the gate with uncertainty
and controls intact. It remains **unresolved** when physical support
stiffness, actual load, contact, trajectory, timing, or uncertainty cannot be
verified. This screen neither qualifies DES-003 nor predicts the larger cases.

### Extension and handoff

After the 5×5 screen, extend the same coordinate frame, sensor/reference
definition, load/contact definition, waveform record, baseline subtraction and
uncertainty rules to 10×10 and 20×20. Record the actual tiled/extended coupon
extent and support layout; do not infer it from the 40 mm CAD tile. The future
physical-test owner must receive this run sheet, the CAD revision, calibration
records, setup sketch/photos, raw and reduced traces, stop/failure log, and a
list of unresolved items. The present record authorizes no physical test and
contains no measured result.

## Variables and calculations

For each run, report:

- `d_peak_mm`: maximum absolute neighbour displacement during the update;
- `d_residual_mm`: displacement after the defined settle interval;
- `F_service_N = 3.27` (design-calculated input);
- `n_boundary = 4 × (side − 1)` for the square updated region;
- `alpha_eff = F_transferred / (F_service × n_boundary)` when transferred
  force is available from an instrumented trace;
- `k_eff_N_per_mm = F_transferred / d_peak_mm` when the displacement is
  non-zero and the force path is identified.

The cheapest pre-test screening bound uses the E-006 sensitivity assumption
`alpha_assumed` per boundary cell:

```text
F_equiv = F_service × n_boundary × alpha_assumed
k_required = F_equiv / 0.10 mm
alpha_max(k) = k × 0.10 mm / (F_service × n_boundary)
```

These are calculated sensitivities, not measured properties. The reproducible
check is:

```text
python3 08-integrated-designs/DES-003-reliability-first/analysis/coupon_b_gate.py
```

It prints the 1%, 5%, and 10% sensitivity rows and the maximum allowable
coupling at candidate stiffnesses 10, 32.7, and 50 N/mm. Candidate stiffness
values are deliberately labels for sensitivity only.

## Pre-test decision gate

The analytical check alone cannot promote DES-003. Before any physical work,
use these dispositions:

- **Reject/falsify regional claim:** a justified CAD/FEA model or later trace
  predicts `d_peak_mm > 0.10` mm for any required size, or requires an
  explicitly bounded stiffness/coupling combination that the design cannot
  provide.
- **Promote to physical coupon test:** all three cases have a reproducible,
  geometry/material-justified bound with `d_peak_mm ≤ 0.10` mm, and the model
  includes support compliance, actuator trajectory, contact/clearance, and
  worst boundary orientation. This is only promotion to a test; it is not
  product qualification.
- **Leave unresolved:** any stiffness, coupling, support condition, load path,
  or trajectory is assumed or omitted; or any required case is not modelled.

For eventual coupon evidence, pass requires both `d_peak_mm ≤ 0.10 mm` and
`|d_residual_mm| ≤ 0.10 mm` for every required run, with no miniature tip-over,
hinge stall, or fracture. A single failed required run fails that regional
case. These are proposed test gates derived from Q-005, not established
product limits.

## Current calculated disposition

The existing E-006 model gives, at 5% assumed coupling, required stiffness of
26.16, 58.86, and 124.26 N/mm for 5×5, 10×10, and 20×20 respectively. At 10%
it gives 52.32, 117.72, and 248.52 N/mm. Therefore the present evidence is
**NOT FALSIFIED, OPEN, and not qualified**. It is insufficient to promote
DES-003: effective coupling, support stiffness, trajectory, and residual
motion remain unresolved. Under ADR-009 this is retained historical evidence. Further work should establish the decision-relevant load cases and computational bounds before selecting any physical calibration.
