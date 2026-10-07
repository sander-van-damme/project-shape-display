---
status: active
builds-on: [E-034, A-010, A-011]
---

# Decision

Reject the claimed five-state A-010 load-path/integration gate. Accept only
the represented centered S2 section as nominal CAD evidence. Do not treat
E-034 as closing state reach, indexed stop identity, or load separation.

# Evidence

LAB-118 independently reproduced the nominal checker, OpenSCAD export, and
`./repo check` (104 objects). Its committed E-034 report identifies that the
SCAD renders every slider at `state=2`, has one centered 1.60 mm stop bore per
cell, and does not model five-stop geometry or lateral follower motion. For a
fixed 1.20 mm follower in the 3.00 mm square aperture, full-clearance centre
offset is calculated as 0.90 mm; the claimed S0/S4 offset is ±1.60 mm, leaving
a calculated 0.70 mm shortfall. This is analytical/CAD evidence only.

Writer, datum, service/removal, fabrication, force, wear, timing, isolation,
reader, and E-032 measurement gates remain unresolved. No physical or
procurement claim follows from this decision.

# Reopening condition

ADR-009 retires the current A-010 implementation. E-039 retains the bounded repair's geometry contradiction. A materially redefined mechanism must model every state, actual guide/actuator envelopes, indexed height stops and a continuous support path before a new comparison can be credible. No further repair, coupon or integration task follows automatically from this historical rejection.
