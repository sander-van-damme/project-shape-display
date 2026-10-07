---
status: open
builds-on: [A-013, Q-009, Q-011]
---

# Can row programming retain positive support within cost and timing limits?

Determine whether an independently addressed rack/pawl head can acquire arbitrary initial heights, unload, release, reposition, relatch and verify at final pitch without disturbing non-targets. Compare 80 independent linear channels against a common elevator with independently disengageable grippers; the latter must explicitly implement capture at different initial heights, isolation, lowering and reset. Address-bit counts do not establish that mechanism.

Next discriminator: generated contact geometry and complete channel BOM for those two alternatives, including actuators, release channels, grippers, readers, links and recovery. With $250 shared hardware reserve, the $500 ceiling permits $3.125 per 80-head channel or $1.5625 per 160-head channel before any cell purchases. These are budget envelopes, not supplier prices. Reject channels exceeding the envelope or lacking continuous support; do not further optimize their nominal timing.

Bound common alignment error and per-cell fit separately. Required overlap and pitch compete; changing to staggered wider internal supports is allowed by stage 02 and should be compared with a single-plane latch. A viable route needs a complete <30 s schedule and a bounded load/support model; absence of a robust survivor does not justify printing. Calibrate only if an actual remaining fit/friction parameter changes selection after cost and geometry survive.
