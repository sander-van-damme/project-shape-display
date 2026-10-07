---
status: active
builds-on: [DES-004, DES-005, ADR-007, E-016, E-014, E-012]
---

# E-028: DES-004 loaded rotor/readback falsification coupon

## Purpose and boundary

This document defines the smallest final-pitch article and run record that can
falsify the highest-risk DES-004/DES-005 assumptions before production CAD or
procurement: loaded five-stop motion and return, writer engagement, fixed-
standoff reader discrimination, neighbour isolation, and timing evidence.
It is a fabrication/protocol definition only. No coupon has been printed,
assembled, measured, or cycled; therefore this experiment contains no physical
validation or hardware-performance result.

The article is a 5 x 5 witness frame, not a production module. It exercises
the centre cell and four edge/corner cells under the same pitch and frame
interfaces. The later 10,000-transition sequence is a smoke/falsification
gate, not life qualification, wear qualification, production-yield evidence,
or a claim that the 10,000-transition project target is met.

## Reproducible article definition

Use the existing source CAD without changing DES-004/DES-005 defaults:

`08-integrated-designs/DES-004-five-level-rotary-verified-successor/cad/des004_rotor_coupon_5x5.scad`

The CAD-derived geometry and interfaces are:

| Item | Frozen value | Evidence class |
|---|---:|---|
| Array | 5 x 5 cells, 5.08 mm pitch, 25.40 mm active span | CAD-derived |
| Frame | 40.00 x 40.00 x 3.00 mm | CAD-derived |
| Rotor | 3.00 mm diameter x 3.00 mm thick; 1.40 mm bore | CAD-derived |
| Axle | nominal 1.00 mm diameter x 10.00 mm candidate pin | interface input; actual part unresolved |
| Pocket | 2.20 mm radius | CAD/tolerance-screen repair |
| Code vane | 0.45 x 1.20 mm integral vane; five hard stops at 0/10/20/30/40 mm equivalent levels and 22.5 degree stop increments | CAD-derived from DES-004/DES-005 |
| Writer | blunt 0.80 x 1.00 mm tongue into 1.20 x 1.40 mm rotor pocket | CAD-derived |
| Reader | fixed head with 0.70 x 1.00 mm aperture at 1.80 mm nominal standoff | CAD-derived; registration unresolved |
| Load | 3.27 N applied at the centre rotor service-load station | DES-004 design input; fixture implementation unresolved |
| Witness cells | centre (C3), four corners (A1/A5/E1/E5), and their untouched nearest neighbours | test-layout definition |

The fabricator shall produce one functional orientation (frame flat on XY,
rotor bore axis Z) and one adverse witness set using the E-016 orientation
definition. Label every frame, rotor, writer, reader target, pin, and witness
position before assembly. Do not substitute a different pitch, pocket radius,
pin, reader standoff, or writer tongue without recording a new configuration
ID and rejecting comparison with this coupon baseline.

The CAD/tolerance screen reports 0.70 mm nominal pocket-to-rotor radial
allowance, approximately 0.055 mm assumed worst-case vane/frame margin, and
0.30 mm assumed worst-case axle/bore diametral clearance. These are calculated
or tolerance-derived assumptions, not process capability or measurements.

## Instruments and identities

The operator must assign stable IDs in the result record before any attempt:

| Identity | Required record |
|---|---|
| `process_id` | printer, nozzle, layer height, line width, material/filament lot, slicer version and profile hash, XY and elephant-foot compensation, orientation, operator |
| `article_id` | frame/rotor/writer/reader/axle serials, CAD revision/hash, configuration ID |
| `load_instrument_id` | calibrated force gauge or fixture ID, calibration date, applied force trace/file, target 3.27 N |
| `motion_instrument_id` | displacement instrument/camera ID, resolution, frame rate, calibration reference, coordinate convention |
| `timing_instrument_id` | controller/logger ID, timestamp clock and sampling rate; command, writer-contact, stop, reader and return event channels |
| `reader_instrument_id` | reader head/electronics ID, illumination/threshold configuration, raw read log path |
| `dimension_instrument_id` | pin gauge/micrometer/CMM ID, resolution and calibration date |

Blank, unknown, or `unresolved` identity is not evidence and rejects the
corresponding gate. Raw traces and photographs/video, when generated, remain
beside the signed result CSV using the `article_id` and attempt number.

## Run sheet

1. **Pre-fit baseline.** At 20 +/- 3 C after at least 30 minutes, measure
   frame pitch/flatness, each pocket, rotor OD, bore, vane envelope, writer
   tongue/pocket, reader aperture, and reader target location at three clock
   positions (0, 120, 240 degrees). Record mean/min/max/range and all
   instrument IDs. Measure unloaded rotor-to-frame and rotor-to-neighbour
   clearances before assembly.
2. **Unloaded directed motion.** For each of the five witness rotors, command
   every directed transition `0->1->2->3->4->3->2->1->0`, then repeat the
   reverse and wrap-directed sequences `0->4->0`. Make 10 complete sequences
   per rotor. Record command, stop reached, return-to-stop, contact/binding,
   peak actuation force/torque if available, and command-to-stable-stop time.
3. **Writer engagement.** At every stop and for both approach directions,
   make 30 writer insert/withdraw attempts on C3 and one adverse witness rotor.
   Record engagement depth, contact, missed actuation, peak force, and timing.
4. **Loaded motion/isolation.** Apply 3.27 N at C3 with the force instrument
   active. Repeat the directed and reverse sequences in step 2 for 10
   sequences. Synchronize C3 displacement, each nearest untouched-neighbour
   displacement, force, writer contact, stop event, and return event. Repeat
   with the four edge/corner witness cells unloaded but mechanically coupled.
5. **Fixed-standoff readback.** Lock the reader at 1.80 mm standoff. At each
   stop, collect 30 reads per witness rotor, including both travel directions
   and after the loaded sequence. Retain raw code/confidence and the declared
   reader threshold; do not count an absent or manually inferred code.
6. **10,000-transition smoke run.** Use all 25 cells in a deterministic,
   balanced directed schedule: for transition index `k`, address cell
   `(k mod 25)` and command `state = (k mod 5)`; on the next pass use
   `state = (4 - (k mod 5))`, with the schedule repeated until exactly
   10,000 transitions are completed. Include a directed transition counter,
   command state, writer event, settled stop, reader code, retry count, and
   timestamp for every transition. Apply 3.27 N at C3 for the first and last
   100 transitions and for the loaded directed subset in step 4; do not
   pretend the load was applied to every cell unless the fixture records it.
7. **Post-fit inspection.** Repeat step 1 with the same instruments and
   positions. Photograph/retain any wear, debris, cracking, witness contact,
   deformation, or changed reader registration. Preserve failed parts and raw
   logs; do not repair or reprint before recording the failed condition.

## Machine-checkable result contract and gates

The existing E-016 checker is the result-contract implementation. This
experiment does not change it: use its required metadata, row identities,
attempt counts, clock positions, stop/load evidence, actual dimensions, and
summary consistency checks. A result CSV or signed equivalent must contain
the following observable fields for each gate. A missing field or missing raw
evidence is a rejection/unresolved result, never a pass.

| Gate | Observable field(s) | Attempts | Acceptance threshold | Rejection rule |
|---|---|---:|---|---|
| pre/post clearance | `actual_dimensions_mm`, `clearance_pre_mm`, `clearance_post_mm` and three-clock summaries | 3 positions before + 3 after per inspected interface | every measured diametral clearance >= 0.10 mm; post-minus-pre change <= 0.05 mm provisional screen | any missing clock, clearance below threshold, or unaccounted change |
| five-stop motion/return | `stop_results`, `loaded_3p27N_result`, reached/returned flags, binding/contact | 10 complete directed sequences per witness rotor unloaded; 10 loaded C3 sequences; 5 witness rotors | 100% of commanded stops reached and returned, no binding or rotor/frame/neighbour contact | one missed stop, failed return, binding, contact, or absent force trace |
| writer engagement | `writer_engagements`, depth/force/timing per attempt | 30 attempts at each of 5 stops x 2 approach directions x 2 articles | 300/300 attempts engage and withdraw without binding; clearance >= 0.20 mm in both axes | any miss, bind, uninstrumented attempt, or below-clearance result |
| reader discrimination | `reader_reads`, raw code/confidence, `reader_margin_mm` | 30 reads per stop x 5 stops x 2 directions x 5 witness rotors = 1,500 | 1,500/1,500 correct codes; reader margin >= 0.20 mm at fixed standoff | wrong/missing code, margin below threshold, or manual-only read |
| neighbour isolation | `neighbour_displacement_peak_mm`, `neighbour_displacement_residual_mm` | every loaded directed transition in 10 C3 sequences plus 10 sequences at each edge/corner witness | peak and residual untouched-neighbour displacement <= 0.10 mm | any value > 0.10 mm, lost synchronization, or absent displacement trace |
| timing | `t_command`, `t_writer_contact`, `t_stop_stable`, `t_reader_valid`, `t_return_stable` | every directed transition in steps 2, 4 and 6 | every event has monotonic timestamps and complete event chain; report p50/p95/max, no performance pass threshold until DES-004 timing is frozen | missing event, non-monotonic timestamps, clock mismatch, or inferred timing |
| 10,000 smoke | `transition_index`, commanded/settled/read states, retry and error fields | exactly 10,000 transitions; no silent omissions | 10,000/10,000 records; zero missed stop, wrong read, unbounded retry, neighbour violation, or unclassified event | count mismatch, any unclassified failure, or missing raw log |
| post-fit condition | post dimensions, damage/contact/debris fields and evidence references | one complete post inspection per article | no new contact/damage and all post gates above remain passing | any damage, new contact, or unmeasured post condition |

`retry_count` is recorded, not hidden. A retry may be diagnostically useful,
but it does not convert a missed stop or wrong read into a zero-error smoke
pass. The 10,000-transition gate is a falsifier: one failure rejects the
coupon configuration for further design use until diagnosed.

## Evidence classification, risks, and rollback

Calculated/CAD-derived claims are the geometry table and the reproduced
nominal/tolerance values above. Protocol thresholds are provisional engineering
acceptance assumptions inherited from E-012/E-016/E-014, not sourced standards.
The run outputs, if later created, will be physical measurements only when the
listed instrument IDs and raw evidence exist. Timing, friction, return force,
reader optical margin, writer force, process spread, creep, and neighbour
coupling are unresolved until that run occurs. Analytical or synthetic checker
tests cannot close any physical gate.

If any gate fails, retain the failed record and parts, mark the configuration
rejected, and do not alter DES-004/DES-005. Rollback/integration is a document
and configuration decision: revert only a future coupon configuration or
experiment result, leaving the baseline CAD and candidate status unchanged.
No production CAD, procurement, architecture promotion, or life claim follows
from this package.

## Handoff

The next owner is the nominated fabricator/operator or Design Engineer for the
physical coupon run. They must reproduce the frozen CAD, assign the instrument
and article identities, execute the run sheet, preserve failed evidence,
populate the E-016-compatible result contract, and update Q-009 plus the
DES-004/DES-005 disposition. This package is complete as an analytical and
measurement protocol; physical validation remains open.

## Reproduction checks

From repository root:

```sh
python3 tools/fdm-critical-fit-calibration/fit_calibration_matrix.py --plan
python3 08-integrated-designs/DES-004-five-level-rotary-verified-successor/analysis/des004_rotor_coupon_fit_gate.py
python3 -m unittest discover -s tools/fdm-critical-fit-calibration -p 'test_*.py'
./repo check
```

The plan/CAD commands are geometry/calculation checks. The unit tests use
synthetic contract fixtures only. None of these commands prints, measures, or
validates hardware.
