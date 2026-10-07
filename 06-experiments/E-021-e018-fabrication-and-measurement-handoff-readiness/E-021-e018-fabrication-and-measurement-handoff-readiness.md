---
status: complete
builds-on: [E-018, E-019, E-020, ADR-006]
---

# E-021: E-018 fabrication and measurement handoff readiness

## Review boundary

This is an analytical repository review of the repaired E-018 four-plane
coupon. Python and OpenSCAD results are calculations/CAD checks only; no
physical validation, supplier fact, or product-adoption claim is made.

## Result

**Ready for a future fabricator's measurement handoff, subject to physical
preflight gates.** The handoff preserves the 5 x 5 map, 5.08 mm pitch, 40 mm
frame, four plane identities, diagonal fiducials, positive datum, repaired
writer/reader geometry, and adversarial-cycle intent.

The protocol now requires a complete 4 x 25-bit readback and exact comparison
after every cycle, eliminating the stale unchanged-cell false pass. It records
the fiducial transform and maximum residual over all active apertures, freezes
reader calibration and ambiguous/reject handling, allocates exactly 125 cycles
to each of eight cases, and requires auditable neighbour, wear, and as-built
port records. `coupon_protocol.py --check` makes the 28-field schema and exact
1,000-cycle allocation deterministic.

## Physical acceptance gates

Before cycling, freeze fixture-specific port limits, reader calibration,
measurement uncertainty, wear cadence/trend rule, and exact-state comparison.
Measure each port's insertion, alignment, and parked clearance; reject
out-of-limit hardware. During cycling, require zero wrong/ambiguous states,
maximum transformed active-aperture residual ≤0.20 mm after reseat, no
neighbour state change, signed neighbour displacement ≤0.20 mm, and no
mechanical damage or increasing miss trend. These are unresolved physical
gates, not analytical results.

## Cheapest falsifier and remaining risks

Deliberately corrupt one unchanged cell, change another cell, and require the
complete four-plane readback to reject the state across the fixed cases and a
small reseat sample. Remaining risks are medium construction, actuator
force/stroke, cross-plane coupling, reader margin, clamp preload, process
spread, wear, and achievable post-reseat registration/park clearance.
