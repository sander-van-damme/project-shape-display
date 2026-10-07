---
status: active
builds-on: [E-022, E-018, DES-003]
---

# E-023: mask-generator drawing-level sourcing and compatibility screen

This active record screens the E-018 drawing boundary against catalogue and
fabrication-route observations. It is not a quote, CAD release, procurement
commitment, or physical validation. E-040 is the quote-ready arithmetic
handoff; E-044 is the current A-011 sourcing screen; E-043 and E-045 retain
the independent boundary and sourcing audits.

## Controlled interface

The E-018 interface is the authority: 40 x 40 x 3.00 mm frame, independent
34 x 34 x 0.80 mm carriers, 5.08 mm pitch, 3 x 3 mm apertures, two 2 mm
fiducials at diagonal 15 mm offsets, four 1 x 0.8 mm writer tabs on 2 mm
pitch, and a frame-fixed reader target nominally 2 mm above the upper carrier.
These are CAD/interface requirements, not measured capability.

## Candidate route and gate summary

| Item | Screen result | Required closure evidence |
|---|---|---|
| Deburred 304 stainless reusable planes | Preferred rigid baseline; HOLD | Exact thickness, flatness, aperture/fiducial/tab tolerances, burr/kerf, life, cleanability, MOQ, lead time, and delivered price |
| Photo-etched spring stainless | Coupon candidate only; HOLD | Carrier, springback, writer-contact, taper, and life evidence |
| PET/polyimide film | Rejected as first reusable baseline | Separate cost-down experiment after metal evidence |
| Local clamp, hard datum, and fiducials | RFQ candidate; HOLD | Dimensioned parts, preload/stop, tolerance stack, reseat and loaded-neighbour clearance |
| Four writer actuators | HOLD | Exact body/mount, usable travel, force at 1 mm engagement, return, stop, duty/thermal, life, and driver compatibility |
| Eight DES-003 reader heads | Reuse not accepted; HOLD | XY overlay, Z/collision section, optical isolation, cable/pinout, timing, and calibration/fault trace |

The inherited reader path is **$0 incremental only if** every E-018 overlay,
optical, cabling, timing, and calibration gate closes. A fallback reader stack
is an alternative cost path, not additive to reader reuse. The candidate 5 V
actuator arithmetic (`5 V / 6 ohm = 0.833 A`) is calculation only; it does
not establish force, return, life, thermal margin, or fit.

## Disposition and traceability

**304 SS plane and standard clamp route: GO to RFQ, HOLD for compatibility.
Exact writer actuator route: HOLD. Reader reuse: REJECT for acceptance now;
retain HOLDs.** No candidate is promoted to procurement or integration.

The smallest closing action is a controlled E-018 drawing overlay for one
reader/head and one exact actuator, followed by expansion to all eight heads
and four channels only if the first overlay closes. Preserve the distinction
between sourced catalogue observations, estimates, CAD-derived arithmetic, and
physical measurements; none of the latter exists here.
