---
status: complete
builds-on: [E-174, E-173, E-172, E-090, E-131, A-022]
---

# Preloading changes the error law; distributed stops spend the gain on access

**Stop the tested V-key and vertical-stop packages.** Preloaded V-keys replace
clearance drift with form/attitude sensitivity and keeper force; their spring
roof obstructs the neighboring pad. Vertically distributed binary stops remove
narrow Y memory but hit the neighboring moving pickup. Even granting repaired
access, split writers restore the separate-control channel count with more locks
and slower updates. Unloaded screw stops duplicate a friction-sensitive control.
These findings reject embodiments/boundaries, not the underlying principles.

Input main `5fd6150`, E-174; LAB-285. Reproduce:
`python3 tools/curated-experiment-checks/E-175/selectors.py`.
Standard library; imports unchanged E-173/E-172 schedule functions. Evidence:
finite rigid sections/boxes, static force balance, affine error bounds and
conditional schedules. Self-review only; **no assembled loaded trajectory**, CAD,
calibrated process distribution, physical measurement, priced BOM or reliability
qualification. Reproducible JSON is discarded. No printing/purchases justified.

## Search move and duplicate check

| Combination | Complete causal route; unbuilt functions are tested below |
|---|---|
| V-key | Selected deck unloads column; lift/translate/spring-seat lane key. Two stations resist moment, X walls bound translation; read lane/height, retain deck on disagreement. |
| Vertical stops | One foot, five binary grounded stops at 0…40.4 mm. Lift, rewrite one-hot target, descend onto sole active stop, clear pickup. Read all stops/height/support; missing capture retains deck. |
| Screw stop | Lift clear, reusable rotary head adjusts resident screw/nut support, descend. Friction retains length; thrust frame carries load. Read length/support; brake airborne bank. |

Three search moves: fixture preloading; transpose lanes into vertical stations;
separate unloaded preparation from loaded support. Only the middle combination
is new here. Unlike A-022's serial telescoping bit sum, one of five **parallel
grounded** stops carries load. E-090's one-hot decoder grants permission, not
support. Screws duplicate E-131/A-007. E-098/E-172 remain single-dog/rack controls.

The [MIT kinematic-coupling overview](https://pergatory.mit.edu/kinematiccouplings/html/about.html)
provides the fixture analogy: arranged contact normals locate a body. The
[Willoughby thesis, §2.1](https://pergatory.mit.edu/kinematiccouplings/documents/Theses/willoughby_thesis/Chapter_2.htm)
explicitly warns that friction can prevent seating and preload must overcome it.
Accessed 2026-10-11; no transferable PLA priors, patent clearance or global
search-saturation claim.

## Finite V sections and the force needed to keep them seated

Use E-173's nose/rack and transverse .9-mm state pitch. Proposed carriage seats
at Xf=2.2 and Xr=3.5 mm; nose reaches Xn=1.2. At each station a male 90° V has
Y half-width .3 and depth .3, inside a .4-half-width/.4-deep female opening.
Five groove centers span −1.8…1.8. Nominal lands are .1 wide. Extrude each contact
section .4 in X, join by the carriage, and attach grounded combs below it.
Generated vertices verify both flank gaps, **not simultaneous seating of four
imperfect facets on one carriage**. Mismatch may require rocking/compliance.
X end walls would bound translation; play, friction and strength are unqualified.
These plane sections do not certify neighboring comb lands under form errors.

For each flank normal error ±e, the two contact-plane equations give local
lateral error up to `sqrt(2)e`. A common groove-to-rack bias moves both stations;
opposed station errors yaw the nose. Straight-centerline extrapolation gives
`|dq_nose| <= sqrt(2)e [1+2(Xf−Xn)/(Xr−Xf)] = 3.589927e`.
The 16 normal-error corners per e are enumerated. This is an **affine attitude
sensitivity**, not a nonlinear rotated-solid witness or an assembled pass.

For comparison retain E-173's separate four-term edge/datum budget `.4−4e`:
tooth and key-bank registration ±e each, and facing tooth/dog edge ±e each.
The new flank form errors are additional; no datum is counted twice. Coherent
bank registration, common face growth and front/rear differential bias are legal
corners, without independent-cell averaging.

| e mm | Additional nose error mm | Remaining wrong-lane gap mm |
|---:|---:|---:|
| .025 | .08975 | .21025 |
| .050 | .17950 | .02050 |
| .075 | .26924 | −.16924 |
| .100 | .35899 | −.35899 |

A .05 reserve requires e<.046114 in this reduced model; positive gap requires
e<.052701. Neither is measured capability. Negative affine gaps are **not**
actual loaded collision witnesses. Wider remote keys require a real output connection, per E-174.

With downward load F at x and a downward keeper P at Xr, vertical station
reactions are `Rf=F(Xr−x)/(Xr−Xf)`, `Rr=P−F(Xf−x)/(Xr−Xf)`.
These sum to F+P and balance moment. For x=1.2…1.8, nonnegative rear contact
requires P≥.76923F… .30769F. At F=1/x=1.2/P=.8 N, Rf=1.76923,
Rr=.03077 N. Add .1-N transverse nose force at x=1.2: station lateral reactions
are .17692 and −.07692 N. The 45° flank normals `(Ri±Hi)/sqrt(2)` then include
a negative rear reaction. Thus a keeper sufficient for vertical load can still
allow a flank to open under side load. These frictionless conditions identify
contact loss, not its subsequent trajectory. Friction may prevent acquisition or alter later motion.

A proposed bought round-wire compression spring has mean diameter .8 mm,
6 active coils, wire .15 or .20, initial compression .2… .4. Explicit hypothetical
steel shear modulus 60–80 GPa gives `k=Gd^4/(8D^3n)` in N/mm. This torsion model
is uncalibrated and excludes end effects/stress correction/fatigue:

- .15 wire: P=.247… .659 N; insufficient at the adverse 1-N vertical-load corner.
- .20 wire: P=.781…2.083 N; low corner has only .012 N vertical reserve and fails
  the side-load witness. Neither supports the adverse 10-N scenario (P≥7.692 N).
- An .8-mm release would require 1.236…6.25 N and .593…3.333 mJ spring work,
  **if sufficient cavity existed**, before friction and writer losses.

A 1.6-mm installed cavity shrinks to .8 on release, below even the active-coil
solid heights .9/1.2 mm. Minimum cavity is 1.7/2.0 before ends/reserve. Linear
spring work above cannot be credited as an executable release in the short cavity.

Proposed ground spring roof X=3…4.1, Y=±2.3, Z=−2.5…−2 intersects the next
cell's home pickup pad, X=2.88…3.88, Z=−3…−2, by **.44 mm³** in both active
and clear Y states. This exact finite-box collision rejects the stated package
before writer withdrawal. Raising the roof does not supply a clear pad sweep.
Below-frame tension or remote clamps require changed load/energy/access geometry.

At top-of-stroke, E-173's 3.85-mm minimum tooth clearance would permit a nominal
.8-mm key lift, but no acquisition/withdrawal route through the obstructed package
exists. Unchanged cells must keep individual springs/keys seated; a row-wide
release violates isolation. Ideal flat flank area .4×(.3sqrt(2)) gives front
mean normal pressure 7.37 MPa at the adverse 1-N case, before edge concentration;
E-173's nose patch already gives 8.33 MPa. Neither is a material allowable.
Stop this local compression-preloaded embodiment on real access/keeper boundaries.

## Vertical stops: finite isolated cycle, failed neighboring sweep

Column spine X=±.6, Y=±2.3, Z=h−2…h+50; broad foot X=.2…1.8,
Y=±.8, Z=h…h+1.2. Five stops have tops zj=10.1j+error_j and thickness 1.
Their X intervals are 1.2…3.2 active, 2.2…4.2 retracted; Y=±.8. Each needs
a grounded prismatic guide, binary end restraint and an individually released
keeper. Those components are **unbuilt obligations**, not a loaded-guide pass.
Pickup lip/pad retains E-173's sections and 1-mm offset.

Changed columns lift off their old foot/stop onto real overlapping pickup/pad
faces, reach h=44.4, then all five stops are written to the target one-hot word.
All stop sweeps clear beneath the raised foot. Descend to the selected stop;
old=target remains grounded.
All 25 transitions × 32 independent vertical-error patterns (±.05) pass
**7,200 isolated contact poses**; nonsymmetric-error subdivision counts 1/4/16
are 225/345/825. Endpoint/contact separation makes each intervening translation
affine. This checks finite collision and vertical contact availability; ideal
guides still supply eccentric moment, and the deck approach schedule is inherited.
It is not a new loaded trajectory or proof of an assembled five-stop cartridge.

The **neighbor** defeats the apparently good single-column cycle. An unchanged
zero-height cell has its level-4 stop retracted at X=2.2…4.2,
Z=39.4…40.4. The next cell's selected pickup at h=39 has X=3.28…4.88,
Y=±.5, Z=40…40.9. Intersection is **.368 mm³** on an ordinary ascent.
Disjoint Y lanes or below-frame routing could escape; combined guide/keeper/writer
geometry remains unsolved. No manufacturing prior is needed for this collision.

A stale level-4 stop while commanding level 2 captures **20.2 mm too high**.
Lowering .05 beyond first contact produces .048 mm³ overlap. Read all five states
and actual height: firm support can be wrong. Missing targets retain the pickup.

## Full-machine comparison and stopping gate

Same five-height dense arbitrary workload and 80×80 array as E-173/E-172.
Single stacked-stop writer: 80 setting/read channels, row axis, 40.4-mm access-Z
axis and deck drive per bank. Seven scans
(pad-on, five stop planes, pad-off) are charged at .1 s/row including capture,
keeper release/reset, bit proof and withdrawal. Serialize row, Z and deck motion;
include final row/Z home returns. Use v=200 mm/s, a=5,000 mm/s², ten .1-s
pickup/support proofs, 2-s preparation/registration/final settle, one repeated
bit write and one supported short reseat/proof. Common access and .1-s capability
are unqualified. Successful-map allocations only; no machine/persistent-fault pass.

| Banks | V-key optimistic E-173 floor | Vertical stops | Separate support control | Direct heads |
|---:|---:|---:|---:|---:|
| 2 | 41.252 s | 51.401 s | 82.197 s | 36.238 s |
| 4 | 22.919 s | 27.968 s | 42.897 s | 19.469 s |
| 8 | 13.752 s | 16.251 s | 23.247 s | 11.085 s |

The key floor omits newly required access time; E-174's already favorable 1.1475-s
allowance would raise B4 to 24.066. For vertical stops B4, .05/.1/.2-s bit slots
give 20.918/27.968/42.068 s. Slow 80/1,000 motion gives 41.475 s, fast
400/20,000 gives 22.584. B4 only leaves 2.032 s for all omitted work; no free
release mechanism fits that margin by assumption. Initially flat 5×5 patch,
20 changed cells over all 76 row locations, takes 7.336–10.481 s under grants.
Unchanged cells stay grounded in the ideal cycle; the actual neighbor collision
means this embodiment does **not** pass regional isolation.

| Passing central allocation | Complete setter/head bundles | Axes included | Minimum reused read channels |
|---|---:|---|---:|
| V-key B4 shared, including E-174 access axes | 336 | 4 row + 4 deck + 8 access | 320 |
| Vertical stops B4 shared | 332 | 4 row + 4 access-Z + 4 deck | 320 |
| Vertical stops B4 separate pad/stop writers | 656 | 8 row + 4 access-Z + 4 deck | 640 |
| Separate control B8 shared | 656 | 8 row + 8 deck | 640 |
| Direct B4 | 324 | 4 row; head Z inside each of 320 bundles | 320 |

Readers are included functionally inside bundles, **not additional quoted cheap
motors**. Parallel bank pickup/height/load proof, brakes, frame, wiring, power and
controller remain bought/reserve obligations. Splitting writers grants access;
it does not solve the repeated keeper. At $500 ceiling with $250 elsewhere,
mean bundle allowances are .744/.753/.381/.381/.772 dollars respectively, before
local purchases. The stacked version then matches control count, adds four
resident stops/keepers per cell and is slower: **stop on control-equivalent burden
without demonstrated benefit**. No price feasibility is claimed.

Vertical stops require 32,000 grounded slides/retainers plus 6,400 pickup
selectors, versus 6,400 ground + 6,400 pickup for lane/separate controls. Five
$.02 bought keepers/site alone cost **$640**; one $.02 key spring/site costs
$128. Printed locks replace those prices with repeated compliance/assembly risk,
not free performance. A ten-second assembly operation costs 17.8 h per 6,400
repetitions; five such operations 88.9 h. Print mass/time/scrap remain unsliced.
At least 57,600 per-cell observations cover five stop states, pad on/off, pickup
and final support; independent height sensing and writer-clear proof add work.
A common reader bias can accept many wrong states; no false-accept rate is known.

Screw stops do not require lateral state accuracy. But square-thread moving
self-lock with assumed kinetic friction μ=.02/.05/.1 and lead=.8πdμ gives
267.91/107.16/53.58 turns for 40.4 mm at d=3. A .5-s setting slot needs
32,149/12,860/6,430 rpm before acceleration/proof. At d=12 these divide by four;
the wider internal nut is allowed, but requires real multilayer routing. Shared
lift still needs pickups, bank arrest and 6,400 thrust/nut/anti-rotation sets.
This changes unloaded drive torque, not E-131's friction/retention uncertainty;
no renewed screw-family advantage or priced schedule is established.

All shared-lift comparisons still need input-loss arrest of **160/1,600/16,000 N
per B4 bank** for .1/1/10-N loads/site, plus deck mass. Local stops/keys cannot
catch the airborne bank at arbitrary height. No brake is provided here. After a
late wrong-height capture, a short reseat cannot clear a stale stop or rewrite a
loaded key. Keep pads armed, stop on existing support, reacquire selected cells,
then rewrite and prove; persistent obstruction requires supported service. A full
late bank rerun can approach another 27.968 s, yielding roughly **55.94 s** for
the stacked allocation. No <30-s claim covers that case, power loss or jamming.

## Decision and evidence limits

Stop these V-key and vertical-stop embodiments and duplicate screw elaboration;
retain the changed contact law and vertical selection principle. Reopening needs
finite guide/keeper/shared-writer clearance throughout neighboring pickup sweeps,
and a burden advantage over direct/separate controls. Change routing or eliminate
one resident selector; do not extend local key tuning. No machine is selected.

Dimensions, spring modulus and friction are explicit bounds, not X1C/PLA priors.
V features/.1-mm lands are unqualified. Warp, form, layers, hole shrinkage, first
layer, roughness, anisotropy, creep/wear and assembly need a combined budget;
correlated cases cannot average away. Isolated passes establish no yield.
Self-review checks force/moment residuals, contact equations, continuous sweep
separations, neighbor/stale-bit collisions, independent scan-time sum and
empty/local workloads. No dynamics, nonlinear contact or independent validation.
