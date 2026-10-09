---
status: complete
builds-on: [E-084, E-077, E-083]
---

# Finite flying cams require a different completion joint and real return time

**Reject the generated rigid endpoint cams as robust command writers.** Moving
opposed blades to separate longitudinal stations solves their changeover
collision and provides nominal set/reset/bypass paths, but cannot positively
complete uncertain dog strokes without overdriving a hard stop. Their finite
footprints, empty return and failed-withdrawal stopping distance also remove the
apparent low-bank-count advantage of E-084. Retain the generated geometry and
failure witnesses; no whole mechanism or product is accepted.

Input main `57734bd`. Reproduce with
`python3 tools/curated-experiment-checks/E-085/flying_cam.py`.
Optional `--svg PATH` exports the actual two-station polygons. Standard-library
polygon clipping, extruded-section reasoning, deterministic state replay and
analytical timing. **Every new dimension, error, acceleration and proof time is
an explicitly assumed scenario**, not an X1C prior, contact simulation, sourced
material property, yield, physical measurement or fabrication release.

## Generated solids and transitions

The output dog slides in x between 0 and d=1.2 mm. Its command boss is a
rectangle 0.8 mm wide in x, h=0.6/1.0 mm in y and occupies z=[0,1] mm.
An independently captive vertical slide carries each cam blade, with active
z=[0.2,0.8] and raised z=[1.4,2.0]; nominal lift is 1.2 mm. Lower guides must
remain below the blade. Their complete frame, retention, bearings, transmission
and pullback strength are **not** synthesized. Dog endpoint retention and
independently retained column supports are boundary conditions.

Generate twelve sections: ramp L=2/3/4 mm, boss h above, entrance wall
w=0.6/0.8 mm. For 0≤s≤L, define
`f(s)=-0.2+(1.2+0.2+o)*cycloid(s/L)` mm, followed by a 0.4-mm terminal dwell;
o is terminal overtravel, nominally zero. The filled set blade lies between
x=`-0.4-0.2-w` and `f(s)-0.4`; the reset blade is its reflection about x=d/2.
The source generates the actual polygons rather than treating f as a point
follower trajectory. A finite boss contacts the furthest edge over its occupied
y band; a hard-stop-constrained dog intersecting the solid is a failure.

Two placements were examined:

- **Opposed slides at one longitudinal station:** their terminal dwells overlap
  in x by d−0.8=0.4 mm. Parking one slide above the other does not solve
  changeover: the upper slide crosses the parked lower solid on descent. A
  0.4×0.4×0.6=**0.096 mm³** collision witness is reconstructed by polygon
  clipping. Reject these two z-only slides; lateral escape or rotation changes
  the mechanism. Both raised at the same height also collide.
- **Set and reset stations separated by one pitch (5.08 mm):** their solids
  have disjoint y extents. Set only changed target-one dogs; the following
  station resets changed target-zero dogs. Both gates bypass unchanged dogs.
  Unknown old endpoints can be written by set/reset rather than bypass.
  Translation supplies lateral work through the selected cam face; the gate
  drive supplies insertion/withdrawal, and local retention stores the result.
  Output cams remain parked until both stations have flushed the mask, all
  blades have withdrawn and actual dog endpoints have been read.

Nominal L=3,h=0.6,w=0.6 paths cover six old-state/command pairs, intermediate
old position, contact, terminal dwell and release. All 256 two-by-two old/new
binary maps compose these paths correctly, conditional on isolated rows and
retention. All twelve sections are replayed against both states of both lateral
neighbors. Ten have nominal longitudinal isolation under the envelope-gated
protocol; L=4,h=1 variants overlap neighboring rows (sampled solid-intersection
witness 0.224 mm²). L=4,h=0.6 has only 0.08-mm nominal free corridor and loses
it with ±0.10-mm longitudinal registration per head/row. These are generator
results, not twelve distinct architectures or manufacturing samples.

For L=3,h=0.6, polygon corner checks show the gate can traverse its entire z
stroke throughout the reserved inter-row corridor without touching either boss,
also under the stated
±0.10-mm x/y/width scenarios. Nominal raised z clearance is 0.4 mm, reduced to
0.2 mm by opposing ±0.10-mm blade/boss z shifts. Boss-height variation, blade
bending, tilt and actual slide packaging can consume that remaining margin.
A stuck-down set blade actually takes the next bypassed zero to one in replay;
controller command or carriage position is not proof of individual withdrawal.

## Rigid completion conflict and capture impact

Let blade lateral shift b, retained-stop shift t and full boss-width error dw
independently lie in ±e. Direct polygon contact at the terminal dwell gives the
set-side endpoint mismatch
`m=o+b−t+dw/2`. Positive m is solid hard-stop interference; negative m is
undertravel without a demonstrated completion detent. Reflection gives the
same interval for reset. The eight corners produce `m∈[o−2.5e,o+2.5e]`.
Positive completion requires o≥2.5e; no rigid overdrive requires o≤−2.5e.
For e=0.05/0.10/0.20 mm the incompatible requirements are respectively
±0.125/0.250/0.500 mm. At e=0 the nominal joint passes; injected 0.1-mm
overtravel produces actual polygon interference in both directions.

These are competing uncertainty bounds, not distributions. A whole head shift
against a whole printed dog batch can realize the adverse corners coherently;
6,400 cells do not average them away. Perfectly matched b=t cancels that term,
but width error still leaves ±e/2. Calibration can reduce residual uncertainty;
it does not make a nonzero rigid completion interval disappear. A finite spring
cartridge, force-limited follower, proved snapping retention or individually
measured/adapted stroke could change the result. None is supplied by this model.
The 0.2-mm entrance lead gap is itself smaller than 2.5e at e=0.10: the adverse
corner can strike the leading face before the smooth cam ramp begins.

Even nominal capture is not E-084's rest-to-rest cycloid. The dog starts moving
when f reaches its old endpoint, inside the lead-in. For L=3 and old=0 this
occurs at s/L=0.295541, with slope 0.598385. At E-084's four-bank boundary
speed 0.182033 m/s the ideal constrained dog velocity jumps from zero to
**0.108926 m/s**. This rigid kinematic discontinuity requires impact/compliance
analysis; it is not a finite force or an achieved speed. Stop tuning nominal
cycloid acceleration as if it bounded this capture event.

## Finite switching, return and fault timing

A conservative controller changes a blade only outside the entire boss/blade
y envelope. With independent head/row y errors ±e, the free corridor is
`G=p−(L+0.4+h)−4e`. Each end needs a 2e reserve for the unmeasured head/row
phase difference. A common head offset cancels from physical pitch but not from
an open-loop switching schedule. This is a sufficient scheduling rule, not a proof
that every shorter contact-aware scheduler is impossible. With e=0.10,
L=3,h=0.6, G=0.68 mm: at B=4 it gives only **3.736 ms**, versus **15.492 ms**
for a 1.2-mm rest-to-rest gate stroke at 20 m/s², plus assumed 1-ms proof.
Each independently lifted pair uses **160B gate channels**, not E-084's
hypothetical 80B ternary channels. Consecutive identical gate states need no
transition, but arbitrary alternating row commands do. Interleaved lanes sharing
this row trajectory still have to clear each intervening row; Q times the word
period is not an extraction allowance without an alternative route.

For the adverse 43-mask, 3,440-row workload, n=80/B rows per bank. Start and
finish outside the full two-station head envelope. Each forward pass covers
`D=n*p+L+0.4+h+4e` mm. The unidirectional profiles require 43 forward scans
and 42 empty returns (none after final clear). Reversing an engaged profile
encounters its terminal face first; no bidirectional writing is credited.
Use equal forward/return speed v and transport acceleration A=20 m/s², with
rest at every endpoint. Per-leg time is D/v+v/A when trapezoidal, otherwise
2√(D/A), with metres throughout. Add E-083's **assumed six seconds** for all
other work; its sufficiency is still unproved.

A nominal gate/proof speed ceiling is G/(tg+tp). To stop after a failed
withdrawal before the next row envelope, require instead
`v*(tg+tp)+v²/(2A)≤G`, in metres. The full attempted withdrawal time must be
counted before declaring failure. Equality is a zero-margin timing boundary,
not an operating recommendation. This assumes actual per-blade detection and
available deceleration; neither is qualified. False acceptance, fractured
blades and insufficient braking defeat it.

| Ramp / banks / gate acceleration | At gate/proof ceiling, total s | With withdrawal-fault stopping reserve, total s | Gate channels | Residual allowance/channel |
|---|---:|---:|---:|---:|
| 2 mm / 8 / 100 m/s² | 28.642 | **38.321** | 1,280 | <$0.1953 |
| 2 mm / 16 / 20 m/s² | **30.464** | **33.679** | 2,560 | <$0.09766 |
| 2 mm / 16 / 100 m/s² | 18.453 | 23.464 | 2,560 | <$0.09766 |
| 3 mm / 16 / 100 m/s² | **35.897** | **42.370** | 2,560 | <$0.09766 |
| 3 mm / 20 / 100 m/s² | **30.863** | **36.221** | 3,200 | <$0.07813 |

Allowances reserve $250 elsewhere and use the strict $500 purchased ceiling;
they are not prices. The 144 geometry/bank/gate-acceleration scenarios are timing
sensitivities of already rejected rigid joints, **not feasible machine counts**.
Return topology or faster transport can change the itinerary; a real gate,
force limiter and reader must then pass the resulting contact/fault envelope.
No changed mechanism inherits these times automatically.

Compared with E-083's 1,280 data plus 80 row channels and 27.410-s scenario,
the short fast conditional 16-bank case removes 6,400 captive keys/feet but
adds 2,560 accessible lifted blades, gates and their guides. It retains 6,400
command dogs, detents/guides and persistent support outputs, and adds bank
translation, return clearance and readback. There is no complete BOM, mass,
print/assembly time, service package or overall Pareto winner. A reader checking
both 80-blade stations per transaction faces 550,400 blade-state decisions,
plus 275,200 dog decisions before support observations. No measured error bound
or independent-read reliability credit exists. Regional logical bypass is
proved only within the stated isolated nominal section; transmitted disturbance
and column support are not simulated.

## Disposition and next discriminator

Stop same-station z-only opposed changeover and rigid terminal completion for
these generated cams. Retain the separated two-station paths as reproducible
negative/nominal references. A stationary setter plus retained carrier using
the same local rigid joint inherits its endpoint conflict; buffer capacity
cannot fix it or E-084's sustained-word-rate limit. Carrier routing itself has
not been synthesized or rejected. The stopped reusable-head comparator remains
an open comparison, not a qualified alternative.

The next useful result is a **finite compliant completion/withdrawal package or
a materially different single-gate coupling**, compared with a stopped head and
an explicit carrier return path. Its required changed inputs are bounded
capture energy, terminal recoil/force, positive pullback and individual fault
proof, with actual gate and scan footprints. A rotating ternary cartridge may
avoid the vertical-order collision and doubled data channels, but requires its
own swept solid and cannot be accepted from three encoded states. These are
computational reopening conditions; no purchase, print or human approval wait.

Self-review only: polygon clipping is checked against the independent analytic
finite-square support function at 503 positions. Profile refinements of
40/80/160/320 segments give max discrepancies 0.000685/0.000171/0.0000429/
0.0000107 mm (approximately fourfold improvement). Monotone profile bounds and
exact terminal corners supplement sampled sweep witnesses; this is not a
continuous 3D assembly/contact certificate. Nominal maps, mid-stroke capture,
opposite neighbors, changeover collision, overtravel in both directions and a
stuck blade are exercised. Stopping-cap substitution checks dimensions and the
quadratic distance identity. Friction, stress, energy dissipation, wear, spring
life and complete load-support transitions await a changed surviving package.
