---
status: complete
builds-on: [E-086, E-085, E-084, E-083]
---

# Rotary paddles remove the fork flush but retain capture and completion gates

**Retain the stopped rotary paddle as a nominal section; reject its rigid
completion, the independently programmed long ternary paddle, and the tested
coplanar racetrack.** Rotation removes E-086's opposed jaws and parity-row flush.
A stationary setter with one returning carrier separates by bank but pays a
round trip per row word. No complete machine is selected or qualified.

Input main `63b3ca6`. Reproduce:
`python3 tools/curated-experiment-checks/E-087/rotary_carrier.py`.
Standard-library polygons, convex clipping, state replay, interval corners and
analytical force/time accounting. Every new dimension, error, friction,
acceleration, proof slot and cost reserve is an **explicit assumed scenario**,
not a sourced X1C prior or measurement. Two coupling hypotheses and two routes
are examined; refinements are not additional architectures. No distribution,
yield, contact dynamics, FEA or fabrication claim.

## Short paddle: active rotation at a stopped row

The dog retains E-085's x stroke 1.2 mm, width 0.8 mm and z=[0,1] mm. Generate
an actual 3×0.6-mm rectangular paddle in x–z, extruded 1.2 mm in y, pivoting at
(x,z)=(0.6,3) mm. Angle zero points downward. Each column has an independent
rotary data axis; a common bank lift raises pivots by 1.5 mm. Upward 180-degree
bypass remains clear even when that common lift descends.

While raised, rotate from bypass to −35 degrees for set or +35 for reset.
Lower; rotate to −2.873196 degrees for set or its reflection for reset; lift
at that angle; rotate back to bypass; prove clearance and index. Rotary drives
supply work; retained dog endpoints store commands after separation. Independent
column supports and parked output cams remain boundary conditions. Paddle
polygons do not supply axle bearings, drives, limiter, retention or frame.

All six old-state/set/reset/bypass paths and 256 two-by-two old/new maps replay
at 40/80/160 intervals per stage; midstroke dogs are also tested. Polygon
intersections check target and lateral neighbors. Nominal insertion reserve is
only **0.03418 mm**. Row separation is 5.08−1.2=3.88 mm; no parity flush.

Active ±35-degree envelopes have 1.14705-mm x separation. Programming uses
[−35,180] degrees: enclose the left paddle in radius `sqrt(3²+0.3²)` and bound
the neighboring swept sector's distance by `5.08*cos(35°)−0.3`. The resulting
**0.84633-mm** separation proves nominal paddle isolation for independent
programming phases at equal common-lift height. Raised programming's minimum
z is 1.48504 mm, above dogs. Neither bound clears an absent drive/frame.

Bound pivot x shift b, pivot z shift h, full paddle-width error dw and dog-stop
shift t separately by ±e. Common rail/batch errors may realize coherent adverse
corners across a row; no statistical averaging is credited. At terminal theta,
finite edge contact at the dog top gives
`m=b+h*tan(theta)+dw/(2*cos(theta))−t`.
An independent straight-edge equation agrees with polygon clipping.

| e | Worst capture reserve | Terminal mismatch |
|---|---:|---:|
| 0 mm | 0.03418 mm | 0 |
| 0.05 mm | −0.13135 mm | ±0.12754 mm |
| 0.10 mm | −0.29688 mm | ±0.25508 mm |
| 0.20 mm | −0.62794 mm | ±0.51016 mm |

Negative capture reserve means contact during lowering before the rotary stroke;
impact is unqualified. Positive mismatch is hard-stop interference; negative is
incomplete seating. Constant overdrive cannot remove both. Backlash, boss-size
error, tilt, wear, indentation and bending are additional uncertainty. A changed
approach angle can improve insertion, not rigid completion. Stop this rigid
embodiment; require a real force-limited capture/completion joint.

Nominal terminal lifting separates contact. Failed lift leaves **0.222707 mm²**
intersection with a zero dog on the next row: actual per-paddle clearance must
inhibit indexing. Capture energy, recoil, retention under vibration, friction,
jam extraction and complete support geometry remain open.

## Retained paddle: shared vertical energy

A carrier stores −15 degrees set, +15 reset or 180 bypass. A stationary setter
programs those angles; a common downward stroke supplies work. This substitutes
retained angular memory for moving rotary drives. Angular latches/stops and
setter couplings remain required, not free or qualified.

Generate a 6×0.6-mm paddle about x=0.6 mm. Terminal contact gives pivot
z=1.412701 mm. Contact travel is **4.478461 mm** vertically; add 1.5 mm clearance
for **5.978461 mm** lift and raised pivot z=7.391162 mm. Finite sections replay
set/reset from both states, separation and upward bypass. The complete paddle
sweep extends from z=−4.46050 to 13.39866 mm: **17.85916 mm**, before supports.
Space below the dog is granted for this screen, not proved available.

**Independent coplanar setting fails:** a transition between reset and bypass
in [−15,180] degrees intersects a neighboring stored-bypass paddle by
**0.393490 mm²** at about 114 degrees. The witness persists at 80/160/320
subdivisions. At the lowered pivot, programming through zero also intersects
an endpoint dog by 0.100 mm². Elevating the setter clears dogs, not neighboring
paddles. Reject this independent setter. Coordinated temporary neighbor states,
stacked setters or folding blades could reopen it; no general configuration-space
impossibility is claimed.

A sliding wedge against horizontal F gives
`Fvertical/F=(tan(15°)+mu)/(1−mu*tan(15°))`.
With 80 simultaneous 0.3-N dogs and assumed friction mu=0.1/0.4, shared force
is 9.074/17.955 N, excluding guide/pivot friction and inertia. Frictionless
work satisfies `Fvertical*dz=F*dx`. Retention torque, stress and uncertain rigid
completion still require a joint; this calculation is not force acceptance.

## Return routes and regional isolation

The circulating reference joins working/return runs with radius 6-mm turns in
y–z. Model a **solid rectangular carrier bar** 1.2 mm longitudinally by 3.6 mm
vertically, rotating with the path tangent. This is actual declared material,
not an empty clearance box. It is smaller than the long-paddle assembly;
clearing it would not clear that assembly, bearings or track.

Facing bank turns one pitch apart share (y,z)=(2.54,0.564156) mm. Rotated bars
intersect by **1.877303 mm²**. An active turn also intersects a parked neighboring
bottom-run bar by **1.52813 mm²**, defeating regional operation. Bar span is
`(n−1)*5.08+2*hypot(7.8,0.6)` mm: **61.3661 mm** for ten rows in a 50.8-mm
bank pitch. Reject this coplanar route; noncircular/staggered/external returns
require changed geometry. Synchronized full scans do not prove local isolation.

A single **rectangular ferry** avoids shared turns: set above row zero;
translate raised to row j; lower/write/lift; return raised to the setter;
reset/read for the next word. Centers stay within the bank's first/last rows.
Two 1.2-mm-deep bars retain **3.28 mm** longitudinal gap under opposing ±0.20-mm
rail offsets and full-depth errors. This separates bars and constant-y paddles,
not unspecified rails/drives/setters. Multiple carriers need a new occupancy
and passing model. A stopped head uses the same corridor but scans either way;
the ferry revisits its fixed setter every row. Buffering cannot erase preparation
or E-084's sustained setting-rate bound. Output cams stay parked until full-mask
and withdrawal proof; unchanged-column vibration/displacement is not simulated.

## Full/local budgets

Use E-083's 43 masks including final clear, n=80/B rows per parallel bank and
six-second assumed allowance elsewhere. With rest-to-rest `t(s)=2*sqrt(s/a)`
(s in metres), stopped motion is
`6+43*(2*n*t(1.5 mm)+(n−1)*t(5.08 mm))`;
ferry motion is `6+43*sum_j(2*t(j*5.08 mm)+2*t(5.978461 mm))`.
These grant zero data-setting/readback/settling time: **conditional motion
bounds**, not physical deadline passes. No force feasibility or speed cap.

The stopped serial scenario additionally executes rotary legs 215, 32.126804
and 182.873196 degrees per row at assumed 10,000 rad/s², plus 4 ms endpoint/
clearance proof. Every row ends upward in this protocol. A faster itinerary
needs its own transition/fault replay; no settling measurement supports 4 ms.

| B / a (m/s²) | Stopped motion | Stopped serial | Ferry before setting/proof | Residual/channel |
|---|---:|---:|---:|---:|
| 8 / 20 | 33.231 s | 73.415 s | 88.660 s | <$0.3811 |
| 8 / 100 | 18.178 s | 58.361 s | 42.967 s | <$0.3811 |
| 16 / 20 | 18.930 s | 39.022 s | 37.717 s | <$0.1905 |
| 16 / 100 | 11.783 s | 31.874 s | 20.184 s | <$0.1905 |
| 20 / 20 | 16.070 s | 32.143 s | 29.261 s | <$0.1524 |
| 20 / 100 | 10.503 s | 26.577 s | 16.403 s | <$0.1524 |

Fourteen bank/acceleration scenarios run. Bought allowances count 80B data/setter
axes, B lifts and B transports with $250 elsewhere and strict <$500 total.
Complete drives/transmissions/control must fit; no prices are invented. Carrier
latches/setter readers add burden. E-083's 16-bank 27.410-s and E-086's eight-bank
29.090-s scenarios retain their own joint/route failures; none proves dominance.

Allocate the 5×5 patch's 35 writes as seven visits per row: ferry motion is
**5.163 s** near its setter versus **8.293 s** in rows 5–9 at a=20; at a=100,
2.309 versus 3.709 s. Setting, support work, verification and recovery remain
additional. Equal changed area does not imply equal local update time.

Both keep 6,400 dog/retention sites and persistent supports. Stopped heads add
80B paddles/pivots/couplings; ferries add 80B retained paddles/latches and setter
interfaces, return guidance and registration. Extra carriers multiply interfaces.
Removing E-083's bars/6,400 keys requires successful missing joints/drives.
Print/time, axles, assembly, wear, wiring/power, repairs and BOM remain unresolved.
At least 275,200 dog-state and 275,200 paddle-clearance decisions occur, plus
support/setter observations. No measured false-accept bound or independent-read
credit exists; a union bound only becomes quantitative with defensible inputs.
Persistent faults hold output cams parked under retained support. The 20-bank
fast scenario's 3.423-s margin must include settling/retry; one mask replay alone
costs about 0.479 s in that itinerary before support actions.

## Decision and verification

Stop the rigid rotary drive, independent long-paddle setter and coplanar loop.
Retain the short section as a nominal comparator that escapes fork topology
failures. Next require **finite force-limited rotary completion and positive
return**, including pivot/guide solids, capture during lowering, stopped-dog
torque, withdrawal/recoil and bypass scheduling. Retire it if bounded errors/
loads and complete-channel allowance cannot coexist. Carrier work needs changed
setter/turn geometry before richer simulation. No print, purchase or new agent.

Self-review: analytic clipping controls, rotated area at 361 angles, independent
edge support at 301 angles, exact interval corners, path refinements and positive
collision witnesses. Continuous nominal clearance bounds supplement sampling;
no sampled absence alone certifies a path. Zero travel, square-root motion
scaling and frictionless work are checked. No dynamic or mesh convergence claim
is made because no such solver ran. This verifies calculations, not hardware.
