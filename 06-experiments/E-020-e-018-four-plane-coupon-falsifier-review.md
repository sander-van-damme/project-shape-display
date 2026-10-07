---
status: complete
builds-on: [E-018, E-017, ADR-006, E-019]
---

# E-020: independent falsifier review of E-018

## Scope and evidence boundary

This is a repository review of the conditional reusable four-plane mask
boundary. The Python result and OpenSCAD export below are calculations/CAD
checks. No physical measurements, sourced performance values, or hardware
validation are present.

## Verification performed

These commands completed successfully:

```sh
python3 06-experiments/E-018-four-plane-mask-generator-coupon-package/analysis/coupon_protocol.py --check
openscad --export-format binstl -o /dev/null -D 'part="assembly"' 06-experiments/E-018-four-plane-mask-generator-coupon-package/cad/four_plane_mask_coupon.scad
./repo check
```

The export reports a pre-existing non-manifold warning. The checks establish
the declared nominal coordinates and protocol allocation only; they do not
establish engagement, actuation, read classification, wear, or neighbour
loading.

## Findings

### F-1 — Critical: unchanged stale cells can produce a false pass

E-018 says each cycle reads “all changed cells” (lines 77–79), while its
acceptance gate is zero cell misses (lines 110–110). E-017 and ADR-006 require
per-cell verification, but the protocol does not require a full 4-plane
post-write map or a validated pre-write baseline. A cell that was previously
wrong and is not in the changed set can remain wrong while every recorded
changed cell passes. The 19-field schema has a 25-bit readback field, but does
not state whether it is a complete post-write map or only changed-cell data
(`analysis/coupon_protocol.py`, lines 11–14).

Smallest repair: for this 5 x 5 coupon, require a complete 4 x 25-bit readback
after every write and compare it with the commanded map; if a changed-cell
optimization is retained, require and archive a complete validated baseline
before the first optimized cycle and after every reseat. A physical falsifier
is one deliberately corrupted unchanged cell followed by a map changing only
another cell; the run must reject it.

### F-2 — High: the active-cell registration gate is not measurable from the schema

The gate requires fiducial *and active-cell* XY error ≤0.20 mm (E-018 lines
110–112), but the required fields contain only `fiducial_error_x_mm` and
`fiducial_error_y_mm` (protocol lines 11–14). Two fiducials can pass after a
rigid transform while carrier skew, pitch error, plane-to-plane offset, or
aperture placement leaves active cells out of tolerance. No per-cell position,
transformed residual, skew, or pitch field is required.

Smallest repair: predefine the fiducial-to-frame transform and record the
maximum residual for every active aperture in every plane, including plane
identity; gate the maximum residual at 0.20 mm. The decisive check is a
coordinate survey after each reseat, not the current two-fiducial scalar log.

### F-3 — High: reader confidence is a movable, undefined pass criterion

E-018 leaves the confidence threshold to be “chosen before testing” (lines
112–113) and lists no calibration set, confidence definition, reject/ambiguous
class, illumination/environment limits, or fixed threshold in the protocol.
`reader_class` plus `reader_confidence` can therefore report an apparently
confident wrong class, or a threshold can be selected after observing data.

Smallest repair: freeze a calibration procedure and threshold before coupon
cycles, with an independent known-state set, an explicit ambiguous/reject
class, and a recorded confusion matrix. Any wrong or ambiguous state in the
accepted run fails; confidence is supporting evidence, not a substitute for
the exact expected 4-plane state.

### F-4 — Medium: the 1,000-cycle allocation permits an easy-case majority

The executable check proves only eight cases × 20 minimum ≤ 1,000 (protocol
line 38). The remaining 840 cycles can be benign repeats, and the text does
not require reseats or loaded-neighbour events to be distributed across the
adversarial cases (E-018 lines 96–99). A zero-miss result can consequently
under-sample the failure modes named by the boundary.

Smallest repair: freeze a deterministic allocation before testing, requiring
each of the eight cases to occur 125 times, with the 100 reseats and 100
loaded-neighbour cycles explicitly tagged and distributed across cases and
planes. This remains a coupon sample, not a life or production-yield proof.

### F-5 — Medium: neighbour-state and wear gates lack auditable observations

The gate requires no neighbour state change and no increasing miss trend
(E-018 lines 114–116), but the required schema has only one displacement scalar
and a free-form `wear_code` (protocol lines 11–14). It does not identify each
neighbour, record before/after state, define displacement direction/reference,
or define inspection cadence and a trend test. “No increasing trend” can thus
be judged after the fact.

Smallest repair: log each N/E/S/W neighbour's before/after state and signed
displacement relative to a fixed datum, plus a predeclared wear inspection
schedule and trend rule. Missing or unscorable observations fail the run.

### F-6 — Medium: nominal CAD overlap is not an as-built fixture gate

The CAD/protocol check asserts exactly 1.00 mm nominal writer overlap and
0.20 mm parked clearance (protocol lines 20–29), while E-018 says actual tongue
dimensions and insertion depth are to be measured (lines 63–65). No tolerance,
measurement uncertainty, minimum engagement, or collision envelope is defined.
The OpenSCAD non-manifold warning also means export success is not a robust
physical interference proof.

Smallest repair: before cycles, measure each port's as-built insertion,
vertical/lateral alignment, and parked clearance against fixed minimums with
measurement uncertainty recorded; reject any port outside those bounds. Keep
this separate from the CAD result.

## Verdict

**Needs bounded repair.** E-018 is an adequate low-cost coupon concept and its
nominal interface checks pass, but it is not adequate as written as a credible
falsifier of the conditional boundary. F-1 and F-2 alone allow a false pass on
the central per-cell verification and registration requirements. These findings
do not invalidate the four-plane coupon boundary; they invalidate the current
acceptance protocol until the bounded repairs are made.

## Highest-value unresolved uncertainty and cheapest falsifier

The highest-value uncertainty is physical four-plane write/read correctness
with a real rewritable medium and actuator stack: E-018 intentionally leaves
the medium, force/stroke, reader technology, and process spread unresolved
(lines 43–48 and 148–151). Nominal CAD cannot bound missed strokes,
cross-plane coupling, stale states, or classification margin.

The cheapest credible falsifier, once physical work is permitted, is the same
5 x 5 coupon with a deliberately corrupted unchanged cell plus a complete
post-write 4-plane readback, repeated across all eight fixed map cases and a
small reseat sample. It directly attacks F-1 and exposes whether the writer,
medium, reader, and registration contract can detect a wrong state. Until
that measurement exists, the architecture remains conditional as stated by
ADR-006; no product-performance conclusion follows from these checks.
