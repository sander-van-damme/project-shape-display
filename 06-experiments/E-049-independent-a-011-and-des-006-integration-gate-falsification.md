---
status: complete
builds-on: [ADR-006, ADR-008, Q-010, Q-011, DES-006, E-017, E-028, E-029, E-030, E-041, E-043, E-045, E-047]
---

# E-049: independent falsification of A-011 and DES-006 integration gates

## Scope and reviewed baseline

This is an independent document/arithmetic falsification report for the
baseline at commit `ce8135eb4f1b1cb138bdf71edd6092f7ac9c1db8` (2026-10-07).
It does not edit or supersede ADR-006, ADR-008, Q-010, Q-011, or DES-006.
No physical test, supplier quote, FEA, or production measurement was
performed.

The decision-driving claims tested were:

1. A-011's reusable parallel four-plane generator is the best complete
   boundary for arbitrary-map updates under the 30 s full-field target.
2. DES-006 can be integrated after the current global rail/shaft stiffness
   screen.

The claims matter because the first controls the architecture and procurement
boundary, while the second could release a full-scale load path whose datum
motion affects every cell. A falsifier is either a complete arbitrary-map
implementation that meets the target with a materially different boundary,
or failure of the four-plane/timing/registration/readback assumptions. For
DES-006, any requirement-compliant load case above the motion limit, or any
omitted interface motion not bounded by the drawing, falsifies integration.

## Verdict

**A-011: conditionally survives this falsification as the leading analytical
boundary, but the “best” and hardware-ready claims are not established.** The
boundary comparison is logically stronger than prepared masks, cassette-only
storage, or buffering for unseen arbitrary maps, and serial writing fails the
stated 30 s calculation. However, the 20.18 s result is not a measured
execution bound and depends on simultaneous four-plane engagement, inherited
head rate, local/transport assumptions, and unverified reader/actuator
compatibility. Continue only as a held candidate; modify the claim to
“leading conditional boundary” and do not integrate or procure it.

**DES-006: reject the current stiffness-screen integration gate.** The
independent arithmetic reproduces the nominal component equations but the
combined 100 N case fails `<0.10 mm` before positive seam/bearing/stop
compliance is added. The service case also fails once the credited 0.09 mm
alignment allowance is included. This is a calculated integration rejection,
not a claim that a redesigned or requirement-changed load path is impossible.

## Evidence classes and independent checks

| Claim/input | Independent result | Evidence class |
|---|---:|---|
| `6400/(8*71)` | 11.2676 s | calculation from inherited rate assumption |
| A-011 full-field total | `11.2676 + 0.05 + 1.50 + 5.864 + 0.50 + 1.00 = 20.1816 s`; margin 9.8184 s | calculation; not hardware timing |
| Four-plane serial fallback | `4*6400/71 = 360.5634 s` | calculation; supports rejection only under the stated rate/target |
| One serial five-state code | `6400/71 = 90.1408 s` | calculation; same scope limitation |
| 25 mm rail, 406.4 mm span, 100 N | 0.062258 mm | calculation using simply-supported beam assumption |
| 8 mm shaft, 80×6.54 Nmm | 0.066932 mm at 10 mm radius | calculation using torsion-only assumption |
| 100 N rail + shaft | 0.129190 mm | calculation; already fails `<0.10 mm` |
| 100 N rail + shaft + 0.09 mm stack | 0.219190 mm | conservative additive calculation; not measurement |
| 3.27 N service rail + shaft | 0.068968 mm | calculation from DES-006 assumptions |
| service plus 0.09 mm stack | 0.158968 mm | conservative additive calculation; fails `<0.10 mm` |

I recomputed these with the stated equations, independently of the committed
checker: `I=25*25^3/12`, `delta=P L^3/(48 E I)`, `J=pi*8^4/32`, and
`delta=T L/(J G)*10 mm`. The calculation reproduces the source values to
rounding. The result is therefore not a script-consistency concern; it is a
failure of the stated combined screen.

## A-011 falsification pressure

The product-boundary conclusion is narrower than “A-011 is the best design.”
E-017 rejects prepared masks and buffered media as complete arbitrary-map
generators because an unseen map still needs a generator. That is a valid
boundary argument under the stated semantics, but it does not compare all
possible rewritable media or writer architectures, nor does it prove lowest
cost, yield, service life, or observability.

The 20.1816 s arithmetic has a hidden architectural discontinuity: the 11.27 s
term writes 6,400 cells once, while the four binary planes are assumed to be
written in the same addressed engagement. If the four planes instead require
four passes through the eight head positions, the write term is 45.0704 s;
the total is already 53.9844 s before any extra settling or retry. If the
channels are serialized at one head, the source's 360.56 s result applies.
Thus “parallel writer” is not enough; simultaneous four-plane write yield,
registration, and readback must be demonstrated.

The 9.8184 s timing margin is model slack, not a tolerance margin. It can be
consumed by reader integration delay, plane skew, reseat, retries beyond the
fixed allowance, or full-cassette transport for a regional update. The
regional 0.72/1.72 s values are proportional calculations, not evidence that
the reader or clamp can operate proportionally at that rate. E-028/E-029/E-030
also show that the current coupon contract does not itself prove stop
identity, applied 3.27 N force, optical `reader_margin_mm`, or a valid
10,000-transition record.

The cost comparison has the same boundary: E-045's arithmetic is internally
reproducible, but its totals contain allowances and catalogue observations,
not delivered quotes. Reader reuse, medium life, clamp/fiducial fit, four
channel compatibility, and calibration/fault behavior remain open. A-011 is
therefore **not established as best overall**, only as the leading candidate
within the analyzed classes and assumptions.

## DES-006 falsification pressure

The 100 N screen is not rescued by assigning arbitrarily high seam, support,
bearing, or stop stiffness. Those terms are nonnegative; the rail-plus-shaft
baseline is already 0.129190 mm. A revised displacement requirement of 0.15 mm
would let that baseline pass but would still fail with the credited 0.09 mm
stack (0.219190 mm). Conversely, retaining the `<0.10 mm` requirement would
require changing a load-path input or removing the credited stack by evidence,
not by assuming ideal joints.

Sensitivity exposes the fragility of the component screen: the rail alone is
0.062258 mm at 100 N, 0.093386 mm at 150 N, and 0.124515 mm at 200 N; a 20 mm
rail is 0.151996 mm at 100 N. Those are not assertions of actual loads, but
they show that a nominal component pass has little margin to unresolved load
or section changes. E-041 separately shows the shaft result is highly
diameter-sensitive and omits bending, bearing play, frame coupling, contact,
wear, and creep.

The service load is not a pass either: 3.27 N gives 0.068968 mm before the
0.09 mm credited alignment allowance, or 0.158968 mm after it. The source
disposition is therefore appropriately conditional only for idealized
components; it cannot support DES-006 integration. The unresolved seam and
contact model is not a minor detail because its allowable displacement is
negative for the 100 N combined screen.

## Cheapest credible next falsification

### A-011: smoke/falsification test, not qualification

Use the existing E-018 5×5 coupon with four independently identified plane
channels, two fiducials, loaded N/E/S/W neighbors, adversarial maps, and a
real timing/readback log. The decisive controlled observations are:

- one addressed engagement must write all four planes, with no serialized
  fallback hidden in the controller;
- every one of the 4×25 expected plane cells must read back the commanded map,
  including blocked and wrong-plane rejection;
- reseat registration, writer/reader compatibility, and loaded-neighbor
  displacement must be recorded with as-built geometry and calibration IDs;
- timing must report complete command/contact/settled/read/return events,
  while full-scale throughput is separately tested with the worst-case map.

Reject A-011 for the 30 s mode on any missing plane, wrong/ambiguous read,
unbounded retry, or neighbor violation. Passing a single 5×5 coupon is not
qualification of 6,400 cells or media life; it only closes the cheapest
architecture falsifier and identifies whether full-scale timing remains
credible.

### DES-006: analytical gate followed by a targeted physical check

First freeze the requirement/load case and run a contact/tolerance model with
seam section and preload/friction, support seating, bearing fit/housing/play,
and post/stop gap/contact stiffness. Reject the current integration claim if
the model cannot meet the requirement with nonnegative omitted compliance.
If the load path is retained, the cheapest physical discriminator is a loaded
5×5 seam coupon plus direct bearing-play and post/stop displacement
measurements. Apply the declared force and direction, measure cell-datum
motion and neighboring motion before/after loading, and preserve the
as-built/tolerance state. Acceptance must be a requirement-owned displacement
limit; analytical agreement alone is not hardware validation.

## Final disposition

Continue A-011 only as a **held, conditional architecture candidate** and
modify its decision language so “leading boundary” is not read as “best,
compatible, or ready.” Reject DES-006's current integration gate and return
it for a frozen requirement/load-path/contact model or redesign. No baseline
decision file was modified by this report.
