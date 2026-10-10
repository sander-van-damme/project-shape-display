---
status: complete
builds-on: [E-108, E-105]
---

# Dual poppets fail the sourced return and bought-channel gate

**Stop this dual-bank embodiment and conclude the chamber-side addressing
campaign without a selected machine.** Separate fine and bypass poppets give a
causally explicit three-state circuit, but the tested resident return spring
cannot keep an unselected valve shut over the declared pressure history.
The sourced position-servo route independently costs **$761.60 for 160 servos
alone**. These reject this assembly and procurement route, not hydraulic
principles or all possible cheap actuators. E-108's conditional schedule remains
useful; it is not a machine survivor.

Input main `a9320a0`. Replay:
`python3 tools/curated-experiment-checks/E-109/dual_poppet.py`.
Evidence: finite primitive-solid subset, analytical force/volume accounting,
81 explicit parameter scenarios, supplier specifications/prices and self-review.
No contact dynamics, complete CAD, calibrated manufacturing, measurement or
independent review. The early return/cost contradictions stop further head,
frame, manifold and seal elaboration; no complete finite assembly is claimed.

## Circuit, finite contact and return failure

Each chamber has two parallel source connections: a .6×40-mm fixed restriction
then a normally closed fine poppet; and an unrestricted bypass poppet. Both are
spring closed. A translating two-tip head contacts the fine stem at s=0 and the
bypass at s=.6 mm. Closed/fine/full commands s=0/.35/1 mm produce valve lifts
(0,0)/(.35,0)/(1,.4). Reversal closes bypass before fine. Independent heads select
columns; row withdrawal follows both seats closing and proof. Neighboring
closed chambers must withstand source changes without head contact. Shared
pressure supplies the energy; springs return the valves into grounded seats.
A failed-open stem requires pressure arrest and service, not head withdrawal.

Two axes lie at x=±1.2 mm in a 5.08-mm cell. Each shell has inner/outer radii
.95/1.15 mm; disk radius/thickness .9/.3, port/stem diameters 1.4/.8 mm.
The source plenum and side port retain E-105's intended path but no new flow-law
pass is credited. The finite seat is z=−.4…0, gland −1.8…−1.3, roof 1.5…1.6;
closed stem ends at −6. A dry return collar at −4.4…−4.2 compresses a spring
against the grounded gland underside. Tip radius .6 remains below the gland;
withdrawal of 1 mm clears closed tails. Disk, stem, collar, tip, spring envelope,
seat, gland, roof and shell do not interpenetrate in 101/201 prescribed states.
Radial separation covers asynchronous branch and neighboring-cell states;
axial extrema cover intervals between samples. This nominal subset omits common
head body, guides, seals, fluid channels, full actuator transmission and frame.
It does not establish process clearance or hydraulic isolation.

[Lee Spring CID010ZL 03S](https://www.leespring.com/product/compression-spring-cid010zl03s-stainless-steel)
lists 1.3-mm OD, 1.1-mm ID, 5.8-mm free length, 1.15-mm solid height,
.59 N/cm rate, .28-N solid load and ±.51-mm free-length tolerance. The page
rounds rate to .06 N/mm elsewhere; use .059. Installed length 2.4 mm yields
.2006-N preload and .25-mm solid-height clearance after the fine valve's 1-mm
lift. The finite occupied spring annulus is checked; no invented helical CAD
or fatigue rating is asserted. Catalog size is not a qualified printed fit.

For chamber/source gauge pressures pc/ps, closing pressure force is
`pc Aport − ps(Aport−Astem)`. Across the inherited 0….5-MPa history box,
required spring preload exceeds **.518363 N**, or .548363 N with an explicit
.03-N return-drag allowance. Even moving the collar to the maximum preload
compatible with the full stroke allows only **.21535 N**. Demanding sufficient
preload from this spring requires a negative installed length: a finite
coil-bind contradiction, not a missing nominal slot. At pc=.08 MPa, the
nominal unselected valve starts losing seating above ps=.312282 MPa even
without drag. This matters before any selected-head motion.

The 81 deterministic cases combine port/stem diameter errors −.05/0/+.05 mm,
rate −10/0/+10% and free length −.51/0/+.51 mm. Rate and diameter bounds are
uncalibrated scenarios; only length tolerance is supplier data. All closed
return margins remain negative (**−.4813…−.2082 N**, including drag). Common
pressure, batch or assembly error can affect a whole bank; no yield follows.
The .5-MPa history is a conservative inherited design box, not proof every
normal E-108 trajectory reaches that differential. A narrower enforced
pressure history could remove this particular failure, but requires a revised
complete circuit and timing/recovery analysis. It does not fix the priced heads.

## Actuation, swept volume and time cannot be inherited

A replacement return meeting the worst pressure box would require at least
**2.6361 N** total opening force at two valves, before added spring compression,
guide friction or dynamics. A 5-mm effective output arm would need ≥13.18 N·mm;
the actuator body/transmission cannot be inherited from E-105's allocated boxes.
[TowerPro SG92R](https://towerpro.com.tw/product/sg92r-7/) specifies 2.5 kgf·cm
stall torque and .1 s/60° at 4.8 V. Stall torque is not continuous or fast loaded
capability. Its dimensional table and supplier body dimensions differ; neither
is a completed mounting envelope. A 1-mm output rise at 5-mm radius requires
11.537°, nominally **19.228 ms**. Final .35-mm closure takes **6.690 ms** at the
same nominal speed, already exceeding the inherited 2-ms response allocation.

Charging only this nominal coarse/fine/closed motion beyond E-108's two 2-ms
transitions per chunk raises its bound from 23.387 to **25.275 s** (124 worst-case
chunks including recovery). This is diagnostic overhead accounting, **not** an
updated feasible schedule: the old .5-mm error/flow bound no longer applies.
At 225 mm/s, a conservative full-speed-during-closure error allocation becomes
1.555 mm including .05-mm read error. Real tapering flow, controller delay,
loaded speed, proof and pressure transients are unresolved. No 2-ms closure or
loaded speed is credited from a servo dead-band specification.

Stem insertion reduces total connected fluid space by .703717 mm³ over the
two full lifts, equivalent to .224 mm of 2-mm piston travel. The final .35-mm
fine closure releases .175929 mm³, equivalent to .056 mm. These are net swept
volume witnesses, not inevitable final errors: source flow can compensate while
a port is open. Independent integration of the generated fluid/solid cross
sections verifies the stem-area result. A disk-area-times-stroke calculation
would overcount net displacement: each disk remains fully inside the connected
fluid space; its occupied volume does not change as it translates. Local flow
around the disk, restriction pressure loss, gas/wall compliance and piston
friction still determine the transient split. Once seated, rigid solids stop
sweeping, but seal deformation/leakage remains unbounded. Readback must follow
closure; no pressure-dependent closure or reverse-pressure seal pass follows.

## Complete-channel economics and disposition

[Adafruit's SG92R listing](https://www.adafruit.com/product/169) gives $4.76 at
100+ units: 160 units cost $761.60, or $1,011.60 with a **scenario** $250 shared
reserve and free cell parts. Included servo electronics/gearing/arms do not
supply the printed head, transmission, grounded guides, PWM distribution,
frame, reader, pumps, power or plumbing. Nonnegative omitted costs cannot rescue
this route. [The same supplier's bare geared motor](https://www.adafruit.com/product/2941)
is $2.80 at 100+, or $448 before driver, feedback/three-state control and head
parts; $698 with the same shared reserve. It is not an affordable complete
channel. Prices accessed 2026-10-10, excluding freight/tax; they are listed
routes, not market minima, negotiated quotes or proof cheap custom drives
cannot exist. No purchase or supplier contact.

This two-stem embodiment repeats **12,800 stem glands**, **12,800 shutoff seats**,
**12,800 resident springs** and 6,400 piston seals, plus 160 shared heads. E-108's
≥6,400 stem-gland count must not be reused as exact. Even free heads and $250
elsewhere allow only **$.019531 per return spring** if all other cell purchases
are free. No spring quote is established; the current manufacturer page requires
quantity entry, so cached search prices are not treated as a 12,800-piece offer.
Spring winding, printed flexures or pressure-balanced spools would be changed
implementations with lifetime/manufacture/closure burdens, not free repairs.
Nominal packing leaves tiny clearances; no print time or yield is defensible
from this incomplete assembly. No fabrication is decision-relevant now.

The bounded attempt has supplied two independent scoped failures. Stop further
poppet tuning, detailed dry-head frame/return, dependent leakage qualification
and board-reliability elaboration. Preserve E-108's chunking counterexample and
conditional time window. Reopen with a materially changed return/isolation
mechanism **and** a credible complete-channel bought path within joint budgets,
then recompute pressure/volume, closing response and full/local schedules.
Neither a cheaper bare motor nor a narrower assumed pressure box is sufficient
alone. Portfolio disposition belongs in ADR-018.
