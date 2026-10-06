# DES-004 independent falsification audit

Evidence class is stated per claim. No physical testing was performed. This
audit is an independent check of the decision-driving bounds, not a production
CAD approval.

## Verdict

**CONDITIONALLY VIABLE as a successor concept; NO-GO for detailed production
CAD until the corrected timing, readback, load/isolation, and fit gates below
are closed.** The nominal arithmetic does not falsify the concept, but the
current document overstates cost and hardware evidence and treats several
unbounded interfaces as if they were inherited from DES-003.

## Claim/evidence/verdict table

| Claim | Evidence actually available | Independent verdict | Falsifier / required correction |
|---|---|---|---|
| Full map remains below 30 s | Calculated from `five_level_successor_bound.py`; 2/4/5 ms per detent are assumptions. DES-003's 1% retry allowance is also an assumption. | **Conditional** | With the stated equation, `T = 13.5612 + 3.2d` s for detent time `d` in ms, so the exact limit is `d < 5.137125 ms`. At 5.0 ms, margin is only 0.4388 s; at 5% misses the inherited retry term is 6.736 s and the 5.0 ms total is 34.9500 s. Measure worst-case loaded four-detent time and miss rate; do not inherit the binary-latch bound without proof. |
| Existing eight-head hardware/cost is retained, approximately $0 purchased delta | Sourced-class DES-003 BOM prices shared hardware; DES-004 has no BOM and excludes 6,400 rotor/follower interfaces from practical cost. | **Not established** | State only “no new bought actuator identified.” Price/record rotor and follower print mass, print time, support removal, assembly, shafts/axles, wear surfaces, and spares before claiming cost parity. |
| Five-stop rotor can carry 3.27 N at 0/10/20/30/40 mm | Inferred from the intended mechanism; no DES-004 dimensions, contact radii, shaft diameter, bearing span, or stress calculation. | **Unresolved** | A load path cannot be checked from the state list. CAD-derived contact pressure, shaft bending, tooth/cam stress, and creep margins are required at the smallest stop land and worst eccentricity. |
| Fixed-standoff coded vane gives reliable readback | Architectural proposal only; no vane geometry, code contrast, aperture, tolerance stack, or optical model in DES-004. | **Unresolved** | The reader must resolve all five codes at the worst rotor phase and neighboring loaded cells. A common-height target removes height variation but does not prove contrast or phase registration. |
| Regional updates isolate unchanged cells | Inferred from “change only target rotors”; DES-003's zero rigid-body motion model does not include this rotor's writer torque, shaft friction, or frame compliance. | **Unresolved** | Measure adjacent displacement while writing the worst loaded target and after repeated cycles. The product criterion requires unchanged regions remain supported; no numerical disturbance limit is currently defined, so report the measurement and its fixture/load state. |
| Printed mechanism is manufacturable at 5.08 mm pitch | CAD/geometry statement only; rotor diameter, axle clearance, vane gap, and tolerance stack are absent. Fabrication criteria explicitly say finished-part accuracy is unqualified. | **Unresolved** | Run a final-process clearance matrix with actual nozzle/layer/orientation and inspect all five stops, return clearance, and reader target registration. “Fits the print bed” is not a fit qualification. |
| 1,000-cycle coupon is the cheapest decisive qualification | Inferred test proposal; it samples gross function, not field-level reliability. | **Reject as a qualification gate; retain only as a smoke test** | For a 99% full-map yield with 6,400 independent cells, the existing DES-003 model implies per-cell error below `1.570e-6`. Zero failures in 1,000 trials has a one-sided 95% upper event-rate bound of about `3.0e-3`, roughly 1,900× looser. It cannot substantiate product reliability. |

## Independent calculations

The script's nominal timing values reproduce exactly when its assumptions are
used. The independent expansion is:

```text
traverse = 5.08 ms/cell
write = 800 cells/head * (max(5.08, 4d) + 1 ms) + 1 s
total = write + 5.864 + (3.0 + 0.05 + 1.5) + 1.3472
      = 13.5612 + 3.2d seconds, when d >= 1.27 ms
```

Thus the 2, 4, and 5 ms rows are arithmetic passes, not evidence that a rotor
can meet them. The 5.2 ms assertion correctly fails: it gives 30.2012 s. The
5% miss stress case is not in the DES-004 script and breaks the margin even at
5.0 ms. Also, the inherited 5.864 s verification and 1.3472 s retry values
describe DES-003's reader and binary writer assumptions; they are not yet
shown for a five-code rotor/vane interface.

The 99% map-yield calculation is a reliability model, not a measurement:
`q <= 1 - 0.99**(1/6400) = 1.570e-6`. It is useful as a scale check only. A
coupon result must not be labelled qualification until its confidence bound,
load spectrum, stop distribution, and wear state are specified.

## Ranked failure modes

1. **Timing cliff:** loaded detent time above 5.137 ms, or a miss rate above
   the inherited 1%, consumes the entire 30 s margin.
2. **Unreadable code:** vane contrast/phase or neighbor reflection produces a
   wrong five-state read; readback then gives false confidence.
3. **Load and wear:** 6,400 rotor/follower contact pairs and axles can creep,
   polish, jam, or lose return force; no stress or life evidence exists.
4. **Regional disturbance:** writer torque and frame compliance can move
   adjacent loaded cells despite no global reset.
5. **Cost/assembly growth:** 6,400 multi-part rotors, axles, and vane features
   may dominate assembly and service burden even if purchased actuators are
   unchanged.

## Cheapest bounded next experiment

Replace the proposed single loaded rotor/1,000-cycle test as the decision gate
with one final-pitch **5x5 loaded read/write coupon** using the intended writer,
five-stop rotor, fixed reader target, and representative neighbor load. Cycle
the center and boundary rotors through a balanced sequence containing all 20
directed stop changes for at least 10,000 transitions, while logging:

- p95 and maximum loaded detent time, including settle; reject the concept if
  the measured worst-case four-step equivalent exceeds 5.0 ms per detent or if
  the resulting full-map bound is not below 30 s;
- every commanded versus read five-state code; any undetected wrong code is a
  hard reject for readback;
- adjacent displacement during the worst target write and after the sequence;
- return force/torque and stop repeatability before and after cycling;
- dimensional clearance and vane registration at the actual print process.

This is a **falsification/smoke gate**, not full life qualification: 10,000
transitions still cannot establish the `1.570e-6` per-cell reliability model.
If it passes, the next justified step is a staged life test with a stated
confidence target; if it fails any hard gate, stop CAD investment.

