---
status: active
builds-on: [ADR-006, Q-010, E-018, E-019, E-020, E-021, E-022, E-023, E-024, E-025, E-026, E-027, E-044, E-045]
---

# E-049: A-011 five-by-five coupon acceptance protocol

## Purpose and evidence boundary

This packet freezes the smallest build-and-measure test for the five A-011
boundary claims named by ADR-006: simultaneous four-plane engagement, reseat
registration, exact readback with wrong-plane/blocked rejection,
actuator/reader compatibility, and loaded-neighbour isolation. It is the
physical handoff for E-018, not a new architecture or full-scale reliability
test.

The result can enable one of three decisions: proceed to detailed fabrication
and measurement of the boundary, modify A-011 and repeat the gate, or reject
A-011 for the `<30 s` arbitrary-map mode. A pass is evidence only for this
coupon, fixture, material lot, reader set, actuator set, and sample; it does
not prove production yield, longer media life, full-scale stiffness, or
complete-display reliability. Do not repair a critical failure in analysis by
serial writing, prepared masks, or an unverified reader substitution.

Mark every statement as sourced/inherited, calculation/CAD, as-built record,
or physical result. Nominal values never count as as-built or physical data.

## Controlled coupon and as-built definition

Build one coupon assembly at the E-018 final pitch. Four planes are installed
and independently written as P0 (lowest) through P3 (highest); a fifth
identical plane is a service replacement and is not silently substituted
during a run. Use one frame and four rigid dummy neighbours, all present for
the isolation test.

| Feature | Nominal controlled value | What must be measured before cycling |
|---|---:|---|
| Frame outside / thickness | 40 x 40 x 3.00 mm | X/Y/Z size, flatness, burrs and clamp datum |
| Active array | 5 x 5 cells at 5.08 mm pitch; 25.40 mm centre span | every cell centre relative to the frame datum |
| Plane carrier | 34 x 34 x 0.80 mm, four installed + one spare | thickness, flatness, aperture and tab coordinates |
| Plane separation | 1.20 mm gap; 2.00 mm writer-port centre pitch | actual inter-plane and port spacing |
| Apertures | 25 square 3.00 x 3.00 mm windows per plane | all 100 installed aperture edges/centres and blockage |
| Fiducials | two Ø2.00 mm holes at (-15,-15), (15,15) mm | diameter, centre coordinates and unobstructed visibility |
| Positive datum/clamp | north 2 x 6 mm witness; south 32 x 2.5 mm clamp land | datum contact, clamp preload, repeatable seating |
| Writer interface | four 4 x 1 x 0.8 mm tongues; 1.00 mm nominal insertion; 0.20 mm parked clearance | insertion, X/Z alignment, parked clearance and collision clearance per port |
| Reader target | frame-fixed 3 x 3 mm centre window; lower face 2.00 mm above upper carrier | optical axis at centre/four corners, Z working distance and cable clearance |
| Neighbours | rigid N/E/S/W carriers on 5.08 mm pitch, no writer ports | before-state, datum, edge clearance and displacement reference |

The drawing source is `E-018.../cad/four_plane_mask_coupon.scad`; the schema
source is `E-018.../analysis/coupon_protocol.py`. Run `--check` before
fabrication. It establishes only nominal geometry, schema, map allocation,
and CAD overlap/clearance—not as-built or physical performance.

### Fixture and load path

The fixture is a rigid base with a fixed north datum, south clamp with preload
indication, four labelled writer guides, frame-fixed reader mount, and four
neighbour seats. The reader is not the registration datum. Channels must be
independently parkable and jointly engageable without moving the frame. Give
clamp, datum, guides, and reader mount permanent IDs.

For every cycle seat north datum, apply south clamp, verify fiducials, install
P0..P3, dummies, and reader. A reseat releases only clamp and planes and
repeats the datum check under the predeclared cleaning rule. Do not adjust the
reader to make a failed reseat pass.

## Instrumentation and preflight

Record instrument ID, calibration due date, resolution and uncertainty for:

1. A calibrated vision/CMM microscope for aperture/fiducial/port coordinates
   and transformed residuals (report uncertainty in mm).
2. A force gauge or load cell in the writer contact line, measuring each
   channel's breakaway, engaged, return and hard-stop force at 1.00 mm tab
   insertion; sample all four channels independently and all four together.
3. A current/voltage logger at the driver supply and a thermocouple on each
   driver/actuator body. Capture the simultaneous pulse, return pulse, pulse
   width, peak and settled current, and temperature before/after the defined
   block.
4. The reader acquisition path with raw signal, calibrated value, ambient
   level, sample timestamp, calibration ID, threshold, class and reject code.
5. A displacement microscope/LVDT or equivalent fixed-datum gauge for each
   neighbour's signed X/Y motion before and after an active write.

Before cycle 1, freeze calibration ID, threshold `0.85`, ambient window,
sample/settle schedule, fixture limits, cleaning rule, wear cadence, and
comparison software revision. Verify every port and reader centre/corner
overlay. Missing calibration/uncertainty, an out-of-limit port, or obstructed
fiducial is a preflight reject.

## Sample and run plan

The physical sample is **one fully instrumented 5 x 5 coupon**, four installed
planes, four writer channels, one reader, and four loaded dummy neighbours.
The minimum run is 1,000 commanded cycles, using the exact
E-018 repeating order of eight named maps, 125 occurrences per map:
`all_zero`, `all_four`, `checkerboard`, `single_corner`, `single_centre`,
`plane_complements`, `cross_neighbour`, and `walking_one`.

Cycles 10, 20, ..., 1000 are the 100 deterministic reseat events. Cycles 11,
21, ..., 991 are the 100 deterministic loaded-neighbour events. A neighbour
event is a local write with dummies installed and displacement measured;
dummies remain installed for all cycles. The first 100 cycles remain in the
sample and cannot be discarded after observation.

Before cycling, exercise each channel separately for 10 engage/park commands,
then exercise all four channels simultaneously for 10 commands. These 50
commands are compatibility preflight, not substitutes for the 1,000-cycle
sample. At cycles 1, 10, 20, ..., 1000, and after every reseat, perform a
complete four-plane readback and fiducial survey. Every ordinary cycle also
performs complete 4 x 25 readback; changed-cell-only logging is not allowed.

At start, midpoint, end, and each 100-cycle block inspect planes, tabs,
apertures, guides, clamp contacts, and neighbour seats for crack, tear, burr,
permanent set, blockage, delamination, force increase, and retry/miss trend.
The spare plane may be installed only after a stopped run and creates a new
sample; it cannot erase the failed installed-plane evidence.

## Frozen acceptance gates

All limits are coupon-level engineering gates, not sourced standards. A
single critical violation fails the corresponding claim and stops the run.

### G1 — parallel four-plane engagement and actuator compatibility

* All four labelled channels acknowledge engagement and park in all 10
  individual and 10 simultaneous preflight commands, with zero plane swap,
  tongue collision, missed stroke, or uncommanded contact.
* At 1.00 mm tab insertion, measured available engagement force is at least
  `2.0 x` the measured worst-case breakaway force of that channel, and
  measured return force is at least `1.25 x` the measured worst-case return
  requirement. These ratios are calculated from future force readings; no
  catalogue force is credited.
* Four-channel simultaneous peak current is within the installed driver and
  supply ratings with at least 20% current margin; no driver or actuator
  exceeds a 20 °C rise above the pre-pulse stabilized temperature during the
  preflight block. Record the actual ratings and temperatures; if the chosen
  hardware has a stricter limit, the stricter limit governs.
* Every command reaches its positive engaged/parked stop without relying on
  friction to define state. No actuator, tab or guide has visible damage or
  permanent set at the end of the run.

### G2 — reseat registration

After every one of the 100 reseats, transform the post-reseat survey from the
two fiducials and report all 100 installed aperture residuals (four planes x
25 cells). The maximum transformed active-aperture residual must be ≤0.20 mm,
with measurement uncertainty reported separately. Both fiducials must be
detected, and the positive datum/clamp must be seated without a new shim or
operator-selected alignment. One missing residual or a changed transform ID
invalidates that reseat record.

### G3 — exact readback and wrong-plane/blocked rejection

For every cycle, compare all 100 returned bits against the commanded P0..P3
maps. Acceptance requires zero unexplained bit misses, stale bits, plane
identity swaps, wrong-plane accepts, or ambiguous/missing accepts. The reader
threshold remains exactly `0.85` under the frozen calibration ID; confidence
is supporting data and cannot override exact-state comparison.

Include at least one deliberately blocked-aperture control, one deliberately
mis-seated/wrong-plane control, and one stale/corrupted unchanged-cell control
in the preflight and at the midpoint. Each must return `reject` or
`ambiguous`, never the expected valid state. Controls are not counted as
successful map cycles. A run with a control accepted as valid stops
immediately and fails G3.

### G4 — loaded-neighbour isolation

For each of the 100 neighbour events, log N/E/S/W separately against one fixed
fixture datum, including before/after state and signed X/Y displacement. Each
neighbour must remain in its known state, with absolute displacement ≤0.20 mm
per local write. Any state change, lost support, contact, or displacement over
the limit fails G4 and stops the run. This is a coupon disturbance gate, not a
full-display miniature-load claim.

### G5 — wear and run integrity

There must be zero unexplained channel/cell misses in the accepted 1,000-cycle
sample, no crack/tear/permanent set/blocked aperture, and no monotonic upward
trend in force, retries, ambiguous reads, or missed acknowledgements across
the predeclared 100-cycle inspection blocks. A run is invalid (not a pass) if
any cycle lacks its command, four-plane readback, fiducial/residual record,
reader result, neighbour observation when tagged, or wear/as-built reference.

The `<30.0 s` arbitrary-map criterion remains a separate system requirement.
Timestamp write, settle, readback, registration, retry, and control handling
for comparison with the inherited 20.18 s analytical bound. A coupon timing
pass is not an 80 x 80 demonstration; missing timing prevents a conclusion.

## Stop conditions and disposition

Stop immediately on actuator collision, plane swap, blocked/wrong-plane
accept, missing/ambiguous valid-state accept, fiducial loss, residual >0.20
mm after reseat, neighbour state change or displacement >0.20 mm, rating or
thermal violation, permanent damage, or two unexplained consecutive misses.
Preserve the stopped state and raw data; do not resume to reach 1,000 cycles.

Stop at the next inspection boundary for a single noncritical upward trend
in force, retries, or ambiguity, and have the test owner apply the frozen
trend rule. If the trend rule was not frozen before cycling, the entire run
is invalid rather than judged after the fact.

The result is **pass for coupon-level A-011 boundary evidence** only when G1–G5
and all preflight controls pass, all 1,000 cycles are valid, and the report
contains complete raw data plus as-built geometry. Otherwise report the first
failed gate(s), cycle ID, stop reason, and whether the failure is attributable
to fixture, medium, actuator, reader, registration, or neighbour loading.
Do not call an incomplete run a pass or average away a critical failure.

## Frozen data schema and handoff

Store one machine-readable row per command in CSV or JSONL, keyed by
`coupon_id, assembly_id, plane_set_id, cycle_id, command_id`. Each row must
contain: `map_case`; four 25-bit commanded maps; four complete 25-bit
readbacks; per-plane ack/fault/retry; pulse start/width, engage/park times;
current/voltage and temperature IDs; `reader_calibration_id`, threshold,
raw/calibrated signal, class, confidence and reject code; two-fiducial
transform ID and X/Y errors; 100 residual records with plane/row/column,
nominal coordinates and residual; reseat and neighbour tags; N/E/S/W
before/after states and signed X/Y displacement; `wear_inspection_id`;
`as_built_port_measurement_id`; instrument IDs; operator/environment; and
software revision.

The summary must include, without replacing raw data: maximum residual per
reseat, all force/current/thermal extrema, count of each fault/retry/reject,
all control outcomes, neighbour extrema by side, inspection findings, cycle
completion count, and an explicit G1–G5 disposition. Missing fields are
invalid evidence. The E-018 `coupon_protocol.py --check` remains the
schema/allocation sanity check; extend the run logger only in a future
measurement workspace and do not commit fabricated example measurements.

## Reproducibility and unresolved boundary

Before hardware, run from the repository root:

```sh
python3 06-experiments/E-018-four-plane-mask-generator-coupon-package/analysis/coupon_protocol.py --check
openscad --export-format binstl -o /dev/null -D 'part="assembly"' 06-experiments/E-018-four-plane-mask-generator-coupon-package/cad/four_plane_mask_coupon.scad
./repo check
```

These commands verify the inherited nominal geometry and protocol invariants
only. They do not measure force, current, optical discrimination, wear,
registration, or neighbour motion. The medium construction, actuator exact
part, linkage/stop stack, reader optical margin, fixture preload, fabrication
spread, and service replacement behavior remain unresolved until physical
records exist. Detailed procurement remains gated on this evidence and the
separate sourcing conditions in E-044/E-045.

## Disposition

**E-049 is an active, frozen test packet with no physical result.** It
consolidates E-018's controlled geometry and 1,000-cycle allocation with the
falsifiers identified by E-020/E-021, the reader/actuator boundaries in
E-024/E-027, and the procurement/compatibility cautions in E-044/E-045. It
does not modify ADR-006, Q-010, A-011, or the current DES-003/DES-004 baseline.
