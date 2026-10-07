---
status: active
builds-on: [E-009, E-006, E-007, E-008, E-010, E-012, DES-003, DES-005, Q-005, Q-011]
---

# Falsifier review: E-009 Coupon-B regional-coupling gate

## Verdict

**DES-005 as currently defined: REJECTED for this gate; hardware isolation
performance remains UNRESOLVED.** The rejection is analytical and applies to
the proposed coupon/gate pairing, not to the rotary mechanism itself. No
physical test, FEA, material test, or measured stiffness exists.

The smallest decisive failure is a boundary/load-station mismatch. E-009
requires a 30 mm diameter × 2 mm centre plinth carrying the 3.27 N service
load. DES-005's executable CAD instead provides a 3.00 mm diameter rotor at
the centre station (and no plinth, retainer, support fixture, writer, or
load-transfer part in the assembly). A 30 mm miniature base therefore spans
the surrounding 5.08 mm cells and may contact the frame or adjacent rotors.
Applying the load directly to the 3 mm rotor is a different contact geometry
and does not reproduce the E-009 loaded-neighbour condition. The current
artifact consequently cannot produce a valid 0.10 mm regional-isolation
result for DES-005.

## Evidence ledger and gate disposition

| Input | Evidence class | What it establishes | What it does not establish |
|---|---|---|---|
| E-009 | protocol and calculated acceptance rule | 0.10 mm peak and residual screen; reference correction, repeats, uncertainty treatment, and invalid-run rules | Any measured motion, stiffness, support compliance, or hardware performance |
| E-010 | calculation from assumed coupling and design load | Sensitivity of required stiffness to region size and assumed coupling | A bounded coupling/stiffness pair for DES-003 or DES-005 |
| E-012 / DES-005 | CAD and tolerance calculation | Rotor, vane, pocket, web, and axle/bore envelope values under stated assumptions | Load station, retention, writer reaction, support stiffness, displacement transfer, or physical fit |
| Physical evidence | none available | — | All hardware regional-isolation performance |

The disposition is therefore split deliberately:

- **DES-005 regional-isolation gate: REJECTED for the current artifact.** Its
  centre station and load path do not reproduce the E-009 loaded-neighbour
  condition, so no valid 0.10 mm result can be claimed from it.
- **Q-005 hardware question: OPEN / UNRESOLVED.** The rejection is not a
  measured failure of the rotary mechanism and does not qualify or disqualify
  regional isolation after a corrected coupon is built.

This ADR is the canonical current disposition. E-009 remains a physical-test
protocol, not a claimed result; E-010 remains a sensitivity calculation, not
hardware evidence.

## Acceptance-criteria review

The protocol covers the required 5×5, 10×10, and 20×20 cases, update direction,
neighbour peak/residual motion, and eventual pass conditions. The `coupon_b_gate.py`
check reproduces the existing calculated sensitivity: at 5% assumed coupling,
required stiffness is 26.16 / 58.86 / 124.26 N/mm for 5×5 / 10×10 / 20×20.
These are calculations from assumed coupling and a design-calculated 3.27 N load,
not evidence of performance.

DES-005-specific geometry checks do not repair this failure. E-012's nominal
and assumed-tolerance checks establish only pocket/vane/axle envelope values;
they do not establish a load cap, rotor axial retention, writer reaction path,
frame/support stiffness, or displacement transfer. The 0.68 mm nominal web and
approximately 0.055 mm assumed worst-case vane/pocket margin are geometry
outputs, not regional-coupling evidence. In particular, the 0.055 mm margin is
smaller than the E-009 motion limit and cannot be treated as isolation margin.

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

CTO follow-up: revise the coupon drawing to freeze the centre load cap/contact
footprint, rotor retention/support points, writer force/trajectory/reaction
path, and reference-corrected displacement method; then execute the existing
E-009 sequence when physical testing is authorized. Do not promote DES-003 or
infer full-scale stiffness from the sensitivity script. Reassess all three sizes after measured
coupling, support compliance, trajectory, peak motion, and residual error exist.

## DES-005 disposition and smallest reproducible check

Run the following from the repository root:

```text
python3 08-integrated-designs/DES-004-five-level-rotary-verified-successor/analysis/des004_rotor_coupon_fit_gate.py
python3 08-integrated-designs/DES-003-reliability-first/analysis/coupon_b_gate.py
```

The first command can only report the E-012 analytical geometry envelope; the
second can only report the E-009 sensitivity table. Neither command contains a
DES-005 load cap, writer reaction, support compliance, or coupling model. The
gate therefore fails closed: do not label DES-005 as passing regional isolation
until a revised coupon drawing freezes (1) a non-interfering centre load cap
and contact footprint, (2) rotor axial retention and support points, (3) the
rotary writer force/trajectory and reaction path, and (4) a calibrated
reference-corrected displacement method with the E-009 0.10 mm threshold.

Rollback/integration note: this review changes only the durable ADR verdict
and its DES-005 input link. It does not alter the DES-005 CAD or the E-009
protocol. A future revised coupon must supersede this verdict with a new
evidence object or an explicit update to this ADR that preserves this failure
record.
