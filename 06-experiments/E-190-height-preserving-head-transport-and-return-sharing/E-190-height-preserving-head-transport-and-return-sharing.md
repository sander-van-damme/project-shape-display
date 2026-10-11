---
status: complete
builds-on: [E-123, E-125, E-185, E-188]
---

# Paired returns save vertical work only if the high carriage can leave its row

**Stop the tested paired-carriage machine with a shared clearance lift. Retain
height-preserving transport as a conditional packaging opportunity, not a machine
survivor.** Opposite carriages can share empty return, but one finishes 40 mm high.
The existing shoe intersects an unchanged neighbor during row indexing. Paying
for a 44-mm bank clearance excursion removes the motor-count advantage in all
nine tested motion/transfer scenarios. An unbuilt retracting head could escape;
no geometry, motor capability, priced assembly or physical qualification passes.

Input main `a791ec4`. Reproduce with Python standard library:

```
python3 tools/curated-experiment-checks/E-190/transport.py
```

Evidence: deterministic state replay, finite solid collision, exact scheduling
and analytical kinematic maxima; self-review only. All motion, error, transfer
and cost allocations are labelled engineering scenarios. No sourced process
priors, stochastic samples, measured reliability or purchased-price claim.

## Changed transport and complete causal obligations

The independent search axis is **reuse of the head's endpoint and empty return**,
by analogy with alternating production carriages. Corpus checks covered E-084/
E-087 circulating command carriers, E-099 shared-lift grouping, E-123/E-125 direct
capture, E-156 asynchronous writing and E-188 common-cam completion. These are
recombinations; no new energy or retention principle, patent novelty or search
saturation is claimed. A retained command carrier is not a load-moving head.

| Arrangement | Addressing, motion, support and recovery |
|---|---|
| Home-return direct control | 80 independent vertical setters per bank scan rows on common y transport. Acquire old height, capture/unload ground stop, move, reseat/prove, withdraw and return below feet before indexing. Head drive carries moving load; 6,400 ground stops hold idle columns. Failed proof retains capture. |
| Height-preserving direct | Same private drive and ground stops; retract the entire head into a passing corridor and retain its previous height while indexing, then approach the next old height. A real retracting capture/drive package and withdrawal observation are additional obligations. |
| Opposed pair | One reversible motor/transmission enforces zA=q and zB=40−q at two adjacent rows. Independent lateral capture and resident-stop operations connect either carriage only between its own old and target positions. Pause q at every capture/release event; an idle carriage moves without its column. Complete q: 0→40→0. A common y axis advances two rows. One carriage ends high, so either a genuine passing corridor or a bank z clearance axis is essential. |
| Fixed-datum rotary control | E-185 avoids translating-head return by leaving a screw or indexer at every cell. It still owes resident precision, thrust support, docking, coast/arrest and output proof; its motor-limited results remain distinct from this kinematic screen. |

The opposed pair has **two private capture paths and two ground-stop interfaces
per motor**, not one magically independent common-cam follower. A pinion/belt
inverter can impose the scalar constraint; its finite routing, bearings, backlash
and brake are not generated. Pause to prove capture before unlocking; prove
seating before withdrawing. Every successful paired transition is replayed, but
these prescribed gates are not implemented hardware. The pair cannot inherit
E-125's failed cup or E-189's unqualified arrest as a solved component.
The timing control also grants private capture/stop gates per direct head; only
row indexing is common. Reusing E-123's common insertion axis would impose
additional within-row barriers. Neither model resolves preload/unloading motion
at a loaded stop: required relief stroke, overtravel and actuation must be built
and timed within or beyond the transfer slots. In particular, q=0/40 is not a
proved loaded handoff just because the height coordinate is reachable.

## A real collision and the alternate corridor requirement

Use an actual 4×.6×1.2-mm solid from E-123's side web, initially x=±2,
y=[−2.25,−1.65], z=[0,1.2]. Withdraw .965 mm then index backward 5.08 mm at
unchanged height. At y translation −3.08 mm this solid overlaps a neighboring
2×2.8×1.2-mm foot centred at y=−5.08 by **1.440 mm³**. The foot uses E-124's
narrower x dimension, making this witness more favorable than the original foot.
Equal neighbor/finished heights are legal. This is a continuous-route collision
witness at nominal dimensions, not a failed bounding box or a tolerance guess.
Returning below every foot was doing necessary work in E-123.

A changed **axis-aligned solid retracted package** could follow half-pitch x/y
corridors around 2×2.8-mm feet only if its width/depth fit the two gaps. With
independent ±e centre and face errors, extra relative pose bound d, and .025-mm
screening reserve:

`width ≤ 3.08−4e−d−.025; depth ≤ 2.28−4e−d−.025 mm`.

At e=.05, d=.15, these are **2.705×1.905 mm**; at e=.10 they become
**2.505×1.705 mm**. This is a necessary package contract for that Manhattan
route, not generated folding jaws or a universal impossibility bound. A concave,
rotating or vertically routed assembly needs its own geometry. E-125's
5.002×3.55-mm retained housing cannot inherit this corridor. Drives, wires,
spines, actuation/return parts and withdrawal faults must fit too.

Common rigid translation cancels. Opposing size bias, guide tilt, warp and
spatially correlated drift need not; the bounds may close an entire bank's
corridor coherently. No probability or X1C capability follows. Roughness,
friction, stiffness, anisotropy, creep and wear remain unmodeled because the
existing transport already fails nominally.

## Exact motion/event model and its independent bound

Assume loaded speed/acceleration 300 mm/s and 5,000 mm/s², empty 600 mm/s with
the same acceleration. Rest-to-rest motion is `2√(d/a)` for d≤v²/a and
`d/v+v/a` otherwise. Scale both v and a by .5/1/2 in the sensitivity. These are
unqualified demands, not sourced actuator capability. The fastest acceleration
is 10 m/s²: an unrestrained miniature can lose contact during downward motion;
that scenario has an additional product/contact failure risk. Jerk, compliance,
force/power, guide friction and thermal limits remain outside this bound.

A transfer stop costs s=.02/.05/.10 s; direct service costs two stops plus
home(−4)→old→target→home travel. The 4-mm undershoot is a clearance allocation,
not useful column stroke. Paired events carry capture/release coordinates for
both jobs. Same-phase simultaneous events may share a slot, but the two sides
of the q reversal are charged separately. Each disconnected carriage continues
empty. An unchanged column never acquires its carriage. All 6,561 pairs of
old/new states on 0/5/…/40 mm replay to the requested heights with continuous
ideal support-state coverage. Free input, wrong capture, false ground proof and
jam are outside the successful-state grant; they still require arrest/recovery.

The paired worst case is not a 40-mm stroke. Two intermediate downward jobs
create six separate rest-to-rest legs. At the central motion, continuous worst
jobs are **26⅔→13⅓ mm on both carriages**, giving **.819677335 s/pair** at
s=.05. The 10/5/2-mm grids give .811104210/.817063484/.819279389 s; a 1-mm local
holdout gives .819581666 s. Those searches understate the continuous maximum.

Independent proof: t(d) is concave. With one job per half-cycle there are two
empty flanks x and one loaded middle 40−2x; their maximum has
`x=min(40/3, v_loaded²/a)`. Evaluate both halves and four slots. If both jobs
occupy one half, at most five segments there plus one empty 40-mm return cost
`≤5*t_loaded(8)+t_empty(40)+4s`, below the split-half maximum at all three tested
scales. Thus the continuous bound is attained, not inferred from grid convergence.
Direct's analogous maximum has one endpoint at 40 and the other at
`min(22,v_loaded²/a)−4`: centrally **40→14 mm**, **.554283297 s/site**.
These maxima apply to this rest-at-every-event protocol, not all possible machines.

## Full display, local workload and cost

Each bank has 80 motor branches across x. B banks divide the 80 y rows into
contiguous blocks of at most ceil(80/B). Direct addresses one row per visit;
pairs address two. Count every stopped y index and final y return to start.
Paired q also returns to its initial state. Six seconds/map additionally reserve
preparation, registration, final observation, settling and one bounded retry;
no qualified sensor latency, successful retry or common-fault recovery is earned.

The generated shared-clearance alternative lowers the withdrawn entire paired
bank **44 mm** (40-mm high carriage plus 4-mm clearance), indexes, then raises.
Every visit including final return pays two loaded-limit strokes. The axis's
mass, frame deflection, power and purchased cost are unqualified; assigning it
this speed is favorable. Empty heads must be in their side aisles first, so this
does not grant a global lift/reset of unchanged terrain.

| Motion scale / transfer slot | Direct motors; seconds | Pair with free corridor | Pair with 44-mm clearance |
|---|---:|---:|---:|
| .5 / .02 s | 240; 28.344 | 160; 28.653 | 320; 24.372 |
| .5 / .05 s | 240; 29.964 | 240; 23.524 | 320; 25.572 |
| .5 / .10 s | 320; 25.755 | 240; 26.324 | 320; 27.572 |
| 1 / .02 s | 160; 28.708 | 160; 22.148 | 240; 23.094 |
| 1 / .05 s | 240; 22.963 | 160; 24.548 | 240; 24.774 |
| 1 / .10 s | 240; 25.663 | 160; 28.548 | 240; 27.574 |
| 2 / .02 s | 160; 22.454 | 80; 29.664 | 160; 23.189 |
| 2 / .05 s | 160; 24.854 | 160; 20.256 | 160; 25.589 |
| 2 / .10 s | 160; 28.854 | 160; 24.256 | 160; 29.589 |

These are minimum tested integer bank counts for the declared schedules, not
hardware deadline passes. Partial final pairs conservatively pay full service.
E-185's 82-head control grants different addressing and motor-limited profiles;
this table does not correct or inherit that result.

Height-preserving direct uses a max-plus dynamic program over previous target
and next old/new height; exact brute force agrees for one/two/three jobs. At
central settings the nine-height worst 80-site vertical itinerary is **37.860 s**.
That single-lane DP alone is insufficient for a bank: different columns can set
successive row barriers and final reset time. An independent bound for n rows is
`2*t_empty(44)+(n−1)*t_empty(40)+n*(t_loaded(40)+2s)`. Two columns attain it:
repeat 40→0 in one and 0→40 in the other. This bounds continuous old/new heights
for the stated serial-acquisition protocol, not just the nine-level alphabet.
With two banks, row motion and reserve it is **28.038 s / 160 motors**, before
building or timing the new retraction route. Repeated 0→40 still needs a 40-mm
empty return between jobs; free routing removes only the home undershoot there. Over 80 rows,
vertical time changes 43.001→37.843 s. Alternating 0→40/40→0 changes
43.001→23.580 s; repeated 20→25 changes 36.330→18.347 s. Bypass has real
workload value, but no universal elimination of empty travel.

A five-row 20→25 patch needs three paired visits (one mate inactive): **2.175 s
vertical service** before clearance/indexing, addressing, proof and the global
allowance. This is not a regional deadline; starting location matters. Untargeted
columns remain on their stops in the state model; vibration and displacement
through the common frame have no bound here.

At $250 shared reserve/free sites, <$500 leaves **<$1.0417 per motor branch at
240 motors**, or <$1.5625 at 160. A paired branch must buy two carriages, local
capture/stop control, inverse transmission, arrest, observation and wiring within
its allowance; shared y/z hardware also needs real cost allocation. $.02 bought
per cell consumes another $128. There is no sourced BOM or accepted affordability.
The central clearance design has 480 carriages versus direct's 240, plus three
bank z axes and the same 6,400 ground supports. One 10-s resident assembly action
still totals 17.8 h. No ungenerated print mass, time, scrap or lifetime is claimed.

At least capture, final ground support and withdrawal must be proved at each
changed site (19,200 opportunities for a full map). Top height alone cannot prove
retracted jaws. Without a defensible false-accept bound, observation gets no
reliability credit; common registration bias or a stuck bank axis can affect many
cells. Persistent failed proof holds the last support and stops that bank; the
six-second allowance is not a promise to repair arbitrary faults.

## Decision and next discriminator

Stop optimizing the clearance-lift pair: it buys no motor reduction in the tested
scenarios and duplicates carriages. Stop deleting direct return by assumption.
Keep the opposed-pair state model and collision witness as negative/conditional
knowledge; neither rejects all inverse transmissions or parallel setters.

The next useful question is **whether capture can change topology to fit a real
passing corridor without adding costly independent actuators**: e.g. separately
withdraw a load-bearing blade into an aisle while a broad grounded drive remains
below the feet, versus a wholly folding moving gripper. First generate all
material/drive/return paths and replay withdrawal plus two-row indexing. Reopen
paired transport only after that route and finite added time exist; stop the route
if it merely assumes a disconnected blade or restores a full 40-mm reset. Compare
its complete cost/time to direct and fixed-datum controls before detailed arrest
work. No print, purchase, approval gate or preferred architecture follows.

Self-review: analytic trapezoid integrals/limits; 6,561 paired state cases;
independent DP brute force; interval collision witness; coherent error/pose
bounds; grid/local refinement checked against attained continuous maxima; strict
integer timing and all reset/return operations. These checks validate the stated
models, not manufactured contact, motors or hardware.
