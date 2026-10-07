---
status: complete
builds-on: [E-031, A-010, A-011, E-018, E-028, E-029, E-030, DES-004, DES-005]
---

# E-032: E-031-G1 common A-010/A-011 5x5 cartridge coupon

## Purpose and evidence boundary

This package freezes the smallest common analytical/CAD article and record
contract that can later compare A-010's axle-free translating gate with
A-011's reusable four-plane mask boundary. It is a geometry and protocol
definition only. No article has been fabricated, assembled, measured, cycled,
or read. Analytical checks below cannot establish hardware performance or
select either mechanism.

The common article tests the shared boundary: final-pitch 5x5 registration,
five-state reach/return, writer access, reader event chain, loaded-neighbour
isolation, and reseat residual. The mechanism insert is the only variable:

* **A-010 insert:** one laminated translating gate cartridge, one writer
  tongue, five hard stops, and representative follower/load shoulder.
* **A-011 insert:** four independently writable binary planes in the same
  registered envelope, with four parallel writer channels. A-011 must not be
  represented by serial plane writes or by a prepared-mask substitute.

The frame, fiducials, positive datum, reader target, witness positions,
nominal pitch, event names, limits, and result fields are common. Any changed
dimension or event definition creates a new configuration ID and is not
comparable with this baseline.

## Frozen coupon envelope and datums

Coordinates are in millimetres. The XY origin is the active-field centre; Z is
normal to the frame, positive toward the reader. Cell columns A..E increase
in +X and rows 1..5 increase in +Y. Cell centre `(col,row)` is
`((index(col)-2)*5.08, (index(row)-2)*5.08)`. The five centre-to-centre
span is 20.32; the 25.40 mm value is the five-pitch active envelope retained
from the source coupon records.

| Interface item | Baseline value | Evidence class / note |
|---|---:|---|
| active array | 5 x 5 cells | E-031 contract |
| final pitch / centre span / active envelope | 5.08 / 20.32 / 25.40 | inherited project reference; envelope is five pitch bins |
| frame outside / thickness | 40.00 x 40.00 / 3.00 | DES-005/E-018 CAD envelope |
| fiducials F1/F2 | Ø2.00 holes at (-15,-15), (15,15) | E-018 CAD definition |
| positive seating datum D+ | north rail witness, 2.00 x 6.00 | E-018 interface; exact fixture contact unresolved |
| opposing clamp land | south land, 32.00 x 2.50 | E-018 interface; preload unresolved |
| reader target R0 | centre cell, 3.00 x 3.00 window | frame-fixed, nominal Z standoff 2.00 |
| writer datum W0 | common west-side channel datum at x=-10.16 | A-011 plane-tab reference; A-010 tongue alignment input |
| loaded witnesses | C3 target; A1, A5, E1, E5 adverse targets; each nearest N/E/S/W neighbour | test layout |
| mechanism keep-out | active frame, datum lands, fiducials, reader target and witness coordinates unchanged | comparison rule |

F1 and F2 define the 2-D reseat transform. D+ is the positive XY seating
datum; the south land supplies the opposing clamp reaction. The reader head is
not a datum. The writer fixture references W0 and its mechanism-specific
engagement datum. Z reference is the frame upper face; the A-010 follower
shoulder and A-011 plane stack must each provide their own declared Z datum.

### Mechanism-specific interface envelope

The envelope is deliberately a contract, not an invented process capability.
The following are nominal analytical inputs inherited from the source evidence;
actual stack heights, force paths, material properties, clearances, and reader
technology remain unresolved.

| Insert | Required common interface | Mechanism-specific analytical input |
|---|---|---|
| A-010 | one labelled writer port at W0; aperture at every cell; follower passes the reader target | five hard-stop states `S0..S4`, slider captured by flat guides, load shoulder bypasses gate; writer tongue envelope and stroke are to be dimensioned in the insert CAD |
| A-011 | four labelled ports `P0..P3` at W0, 2.00 mm centre pitch; full 4x25-bit readback | 4 x 1 x 0.8 tongue envelope, 1.00 mm nominal tab overlap, 0.20 mm parked clearance, 1.20 mm plane separation from E-018; all are CAD inputs, not fit results |

The A-010 and A-011 inserts may share the frame and reader fixture in
separate runs; they need not be co-assembled. The common package therefore
discriminates mechanism behaviour without silently asserting that one reader
can serve both technologies. Reader compatibility and sensor accuracy are
unresolved inputs and must be declared in the future configuration record.

## State, transition, and event nomenclature

The state record uses `S0..S4`, where the numeric ordering is the commanded
five-level order, not a claim of height, optical code, or force. A transition
is counted only when `previous_settled_state != commanded_state`; repeated
commands are `noop` and are recorded separately. For A-011, `S0..S4` are the
decoded five-level combinations across P0..P3; the exact binary encoding must
be frozen before a run and recorded as `state_code_map_id`.

Every state-changing action must contain the following monotonic event chain
from one declared clock: `commanded`, `writer_contact`, `stop_or_write_settled`,
`reader_valid`, `return_stable`. For A-011, `stop_or_write_settled` means all
four plane acknowledgements and clamp release/settle; there is no serial
recovery path. For A-010 it means the selected hard stop is reached after the
writer unload/move/re-seat sequence. Missing or inferred events reject the
record; timestamps are evidence only when clock identity and sampling details
are present.

## Analytical dimensional and tolerance checks

`analysis/common_coupon_check.py --check` is the reproducible calculation
source. It verifies the coordinate span, fiducial placement outside the active
field, datum/reader/writer keep-outs, A-011 port spacing, and the acceptance
inequalities below. It does not model friction, compliance, load transfer,
optics, fabrication spread, wear, or actuation timing.

The checks are:

1. **Envelope:** active envelope 25.40 < frame outside 40.00; the two
   fiducials are outside the active field and do not overlap the 3 x 3 mm
   reader target.
2. **Reseat:** after fitting a rigid 2-D transform from measured F1/F2, the
   maximum transformed aperture/fiducial residual must be `<= 0.20 mm`.
   This is a future measurement field; nominal CAD coincidence is not a pass.
3. **Writer:** measured two-axis clearance at every engaged and parked
   interface must be `>= 0.20 mm`; a single nominal clearance does not close
   the gate. A-011's 1.00 mm tab overlap and 0.20 mm parked clearance are
   geometry assertions only.
4. **Isolation:** target peak and residual displacement of every named loaded
   or unloaded adjacent witness must each be `<= 0.10 mm`, relative to a fixed
   witness datum. This is stricter than E-018's earlier 0.20 mm neighbour
   screen because E-031-G1 is the controlling contract.
5. **Load separation:** a section/FBD must show the A-010 follower load
   closing through shoulder/stop/frame surfaces, never through a gate face.
   The A-011 clamp/media load path must likewise be labelled; no force value
   or material strength is assumed here.
6. **Timing:** report p50/p95/max for each event interval and preserve the
   complete chain. The 9 ms per-cell A-010 screen and E-017 parallel-write
   requirement are analytical bounds/architecture constraints, not measured
   pass results.

No tolerance stack is promoted to process capability. Dimensional tolerances,
flatness, layer orientation, friction coefficient, detent force, clamp
preload, applied load, reader threshold/accuracy, and actuator timing must be
filled as unresolved or sourced/calibrated inputs before physical work.

## Planned run and falsifier

The future owner shall freeze `configuration_id`, CAD revision/hash, insert
identity, process/material metadata, instrument IDs, reader calibration and
threshold, initial five-state map, clock identity, and uncertainty budget
before the first change. The minimum sequence is:

1. Record as-built frame, fiducial, datum, reader, writer, guide, aperture,
   and witness dimensions with three-clock or three-position summaries where
   applicable.
2. Seat against D+, clamp the south land, read F1/F2, and record the frame-
   fixed reader target before and after every planned reseat.
3. At C3 and each corner witness, command `S0->S1->S2->S3->S4->S3->S2->S1->S0`,
   reverse it, then test `S0<->S4`; record reach, return, binding/contact,
   writer clearance, load-path evidence, reader code/confidence, and all
   named events. The corner cases exercise adverse registration and neighbours.
4. Apply the declared representative load only if the fixture and force trace
   identify its actual value and tolerance. Record target and nearest
   neighbours synchronously; do not claim loaded evidence without that trace.
5. Execute exactly 1,000 state-changing transitions using a frozen schedule
   that alternates extreme states, single-cell neighbour updates, corner/C3
   targets, and reseat-tagged intervals. Count no-ops separately. Retain every
   row and raw event/read trace; retries remain visible and do not erase a
   failure.

The coupon is rejected for this configuration on one missed state, failed
return, gate/media load transfer, writer clearance shortfall, reseat residual
over 0.20 mm, any adjacent-witness displacement over 0.10 mm, wrong/ambiguous
reader result, incomplete event chain, or any missing raw evidence. This is a
planned falsifier, not life qualification or a product reliability claim.

## Reduction and record template

The future signed result must include these fields; blank or `unresolved` is
not a pass:

```text
configuration_id, cad_revision_hash, insert_type, article_id, process_id,
fixture_id, datum_id, fiducial_ids, reader_id, reader_calibration_id,
reader_threshold, state_code_map_id, clock_id, instrument_ids,
transition_index, target_cell, previous_settled_state, commanded_state,
event_commanded_ns, event_writer_contact_ns, event_stop_or_write_settled_ns,
event_reader_valid_ns, event_return_stable_ns, retry_count, raw_trace_ref,
fiducial_transform_id, fiducial_residual_max_mm, writer_clearance_x_mm,
writer_clearance_y_mm, target_displacement_peak_mm,
target_displacement_residual_mm, adjacent_witness_id,
adjacent_displacement_peak_mm, adjacent_displacement_residual_mm,
applied_load_N, applied_load_tolerance_N, reader_code, reader_confidence,
reader_margin_definition, outcome, failure_code
```

Reduction reports count exactly 1,000 state-changing rows, separately count
no-ops and retries, verify event timestamp monotonicity, report max/p50/p95
for residuals and event intervals, and preserve failed rows. A-011 additionally
records all four plane commands/acknowledgements and a complete 4x25-bit
readback; A-010 records hard-stop identity and follower load-path evidence.

## Handoff and unresolved questions

The bounded handoff is to a future physical-test owner. They must produce or
reference the two mechanism-specific insert CADs, freeze the missing material,
force, reader, calibration, and process inputs, and run the record contract.
They must not treat this document or its script as physical validation, and
must return raw traces and failed parts/evidence with the configuration ID.

Unresolved: exact A-010 slider/aperture/guide stack and writer stroke; exact
A-011 medium and clamp; common reader optical/electrical compatibility;
fixture datum stiffness and preload; process capability and tolerance
distributions; load magnitude and instrument; state-code encoding; and whether
the nominal 0.20/0.10 mm screens are physically achievable. The mechanism
decision remains conditional on later evidence.

## Reproduction checks

From repository root:

```sh
python3 06-experiments/E-032-e-031-g1-common-a-010-a-011-5x5-cartridge-coupon-package/analysis/common_coupon_check.py --check
./repo check
git diff --check
```

These checks are calculations/schema-independent geometry assertions only; no
hardware, reader, timing, durability, or physical performance is validated.
