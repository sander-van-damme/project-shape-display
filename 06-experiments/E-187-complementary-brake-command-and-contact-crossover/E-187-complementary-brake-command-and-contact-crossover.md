---
status: complete
builds-on: [E-186, E-142, E-082, M-008, E-163]
---

# One command can cross between friction contacts, but does not make control cheap

**Retain compliant overlapping contacts as a conditional transfer, and stop promoting
the differential on command-count savings.** The same scalar command controls a
friction clutch/ground brake with almost identical tangential dynamics. A rigid
break-before-make shuttle instead has an unsupported interval. The compliant example
needs substantial spring work and an unbuilt endpoint damper; neither architecture
earns a complete machine, cost, outage or reliability pass.

Input main `7e61db6`; LAB-307. Reproduce with Python 3 standard library:

```
python3 tools/curated-experiment-checks/E-187/transfer.py
```

Evidence: finite **axial sections**, analytical interval bounds, signed lumped
simulations and schedule allocations; self-review. Every numerical mechanical input
is an explicitly chosen scenario, not a sourced process distribution. No complete CAD,
calibrated X1C capability, sourced command actuator, physical measurement or independent
validation. JSON is disposable.

## Causal combinations and source check

All alternatives spatially address banked heads, capture before releasing a resident
stop, move 40 mm, reseat/prove and retain capture after failed proof. All owe 6,400
guides/stops with return/readback. Unchanged cells stay parked; disturbance is unqualified.

| Combination | Command and moving load path | Remaining liabilities |
|---|---|---|
| Rigid opposite-face shuttle | One axial command selects grounded work brake or idle brake/input clutch, with positive clearance between engagements. | Both off in crossover: loaded output is free. Interference instead of clearance jams rigid faces; simultaneous positive grounding stalls a moving bus. |
| Differential with compliant overlap | One crosshead decreases spring force on the work brake while increasing force on the idle brake. Both stationary pads react torque to frame; slipping idle brake transfers bus power through the differential to the rack. | Two pad springs, return spring, guides, gears/idle rotor and command actuator. Static grounding of both rotors is incompatible with a moving carrier; at least one friction face must slip. |
| Friction clutch plus ground brake | Same command releases output-to-ground friction and presses input-to-output friction. Slip accelerates output, then clutch sticks; return releases clutch and grounds output. | Two friction interfaces and springs, axial reaction through keyed rotating armature/thrust bearing, return and command. Unlike E-082's positive keys, engagement can slip. |
| Independent direct motor control | Motor directly sets the captured output, with separate output arrest/parked stops. | E-185 motor/control inventory remains; eliminates this shared-power crossover but does not solve retention or proof. |

E-186/M-008 recombination, without novelty/saturation claims. Sources checked 2026-10-11:

- [Miki Pulley operating principles](https://www2.mikipulley.co.jp/EN/Products/ElectoromagneticClutchesAndBrakes/about.html)
  distinguishes powered friction engagement from spring-applied braking. Retrieved
  search text; direct open failed. Only the causal topology is used.
- [Warner CB service manual P-2026-WE](https://www.warnerelectric.com/-/media/Project/Altramotion/shared/files/Literature/brand/warner-electric/service-manuals/p-2026-we.pdf),
  pp. 3–7, supplies a distinct self-energizing clutch/brake comparator: one stop collar,
  separate clutch/brake springs, anti-backup/anti-overrun hardware, and adjusted
  overtravel. It does not establish arbitrary reversible miniature operation. No
  catalog dimensions, torque or tolerances are transferred to our printed mechanism.

E-163 forbids a free capstan tail reaction; E-142 supplies the contact-rebound/control-cost
comparison. Neither failed embodiment is reopened.

## Finite contact and signed transfer

Let command q run from 0 (work held) to S (drive). At separate axial stations, the
1-mm-thick work rotor occupies [-1,0] mm and its 1-mm follower lies to the right;
the idle/input rotor occupies [0,1] mm and its follower lies to the left. Work face
position is `max(0,q−aw)`; idle face is `min(0,q−ad)`. Each follower stops at its rotor
and compresses a **separate spring**, rather than penetrating rigid material:

```
Nw = kw max(aw−q,0); Nd = kd max(q−ad,0)
Bw = mu R Nw; Bd = mu R Nd
U(q) = F0 q + kr q²/2 + kw max(aw−q,0)²/2 + kd max(q−ad,0)²/2
```

A grounded crosshead carries both spring seats and a preloaded return spring. The
oppositely facing pad springs oppose on it; an endpoint takes residual axial reaction.
Spring chambers need the calculated compression travel; free length, stress, bearings,
antirotation and radial housing are unbuilt. No packing/strength pass at 5.08-mm pitch.

If aw<ad, the interval (aw,ad) has neither contact. aw=ad has zero capacity at one
point and no error margin. For aw>ad, minimum combined capacity is exactly
`mu R min(kw,kd)(aw−ad)` when both thresholds lie inside the stroke. No positive
clutch can use this overlap while both connected members have different velocities.

With progress sign s=+1 raising/−1 lowering, output angular speed u, source-imposed
maximum Omega, L=sWr, and 0<u<Omega:

```
J u_dot = Bd−Bw−L
J = Jw+Jidle (differential); J = Jw (friction clutch)
```

At u=0 and u=Omega static friction may react either sign. The solver minimizes
the implicit step's quadratic inertia term plus `Bw|u|+Bd|u−Omega|`; it handles
sticking, reversal and overrun instead of clipping velocities by fiat. For both
load signs, `Bw+Bd>Wr` throughout crossover prevents escape from [0,Omega] under
an **ideal four-quadrant source maintaining speed**. It does not keep the head stationary
through transfer. The model permits intended acceleration/deceleration and dissipates
`Bw|u|+Bd|Omega−u|` as heat. Setting Jidle=0 makes the two reduced laws identical.
Stationary differential pads could still simplify a real actuator relative to a
rotating clutch armature; that unbuilt advantage is not erased by the comparison.

A neutral-gap witness at W=1 N, r=2 mm, vertical mass max(.002,W/9.81) kg,
Jw=m r²+1e−8 and Jidle=1e−8 kg m² drops **.00468/.11689/1.87026 mm** from rest
in 1/5/20 ms, even with carrier speed maintained. This is a gap counterexample, not an accepted outage drop.

## Command work, manufacturing bounds and finite return

Example: S=1.4, aw=1.1, ad=.3 mm; kw=kd=20 N/mm; mu=.1; R=3 mm;
return preload F0=40 N, kr=2 N/mm; guide drag 1 N; crosshead mass .01 kg.
Endpoint pad force is 22 N, minimum total friction torque .0048 N m, endpoint
torque .0066 N m. Required W r is .002 N m at 1 N. Off-state clearances are .3 mm; spring compression reaches 1.1 mm.

Quasistatic opening force is `F0+kr q+Nd−Nw+Fguide`: peak **65.8 N**.
Opening work is `U(S)−U(0)+Fguide S = .05936 J`. Mechanical advantage trades
force for stroke; it cannot remove this work. There is no free latch: a powered
actuator must keep q=S, or a separate release/return mechanism must be constructed.
Return with command force zero follows `m q_ddot=Nw−Nd−F0−kr q+Fguide`
while q decreases. Minimum nominal return margin is 17 N at q=0.

Enumerate 128 endpoint scenarios at each threshold error e: aw/ad independently
±e, kw/kd independently ×.8/1.2, mu=.1/.3, R×.9/1.1, return preload/stiffness
together ×.8/1.2. Guide drag is fixed at its stipulated 1-N bound. Coherent pad,
material, radius, frame and spring shifts are present; no independent-cell averaging
or probability is used. Counts pass only capacity, positive clearance and monotone
return conditions, not strength, dynamic settling or hardware qualification.

| Threshold bound | Passing corners at 1 N | Minimum torque sum | Minimum return margin | Maximum static command / opening work |
|---|---:|---:|---:|---:|
| e=0 | 128/128 | .003456 N m | 4.6 N | 78.76 N / .075792 J |
| e=.10 mm | 128/128 | .002592 N m | 2.2 N | 81.16 N / .080232 J |
| e=.20 mm | 106/128 | .001728 N m | −.2 N | 83.56 N / .084752 J |

At 10 N only 2/128 of the e=.10-mm scenarios satisfy these conditions. Load cases
are sensitivity scenarios, not newly adopted requirements. At .10 mm the static
capacity floor corresponds to 1.296 N at the rack; no dynamic margin is implied.
Threshold bounds stand in for assembly registration, surface thickness, layer offsets
and warp; creep/wear can shift both contact onset and spring force. Actual hole shrink,
roughness-dependent static/kinetic friction, spring anisotropy, fatigue, thermal drift
and guide binding remain uncalibrated. A guide jam defeats the assumed return bound.

A 20-section generator sweeps S=1/1.4/2/3/5 mm and k=5/10/20/40 N/mm, keeping
.3-mm nominal endpoint clearances and sizing return preload against the adverse work
spring plus guide drag with 10% margin. Thirteen satisfy every .10-mm-box corner at
1 N. The smallest worst-case command force among these is **54.37 N** at S=3 mm,
k=5 N/mm; its worst-case work is .11191 J. Minimum worst-case work is .08187 J
at 1.4 mm/20 N/mm with 82.33 N peak. These are finite-grid outcomes, not global optima,
purchase specifications or evidence that any spring fits.

## Local stopping is conditional on endpoint dissipation

For powered start, prescribe a finite 5-ms cubic command
`q=S(3z²−2z³)`, z=t/5 ms, then hold S. Its calculated force includes crosshead
inertia; an actuator has not been demonstrated. For stop, release from q=S at rest
and integrate the return. Assume massless quasi-static pad followers and an **inelastic
q=0 stop**. At 1 N and .1 m/s:

| Transfer | Differential time / output travel | Friction clutch time / output travel |
|---|---:|---:|
| Raise start | 8.174 ms / .23523 mm | 8.066 ms / .22992 mm |
| Lower start | 5.534 ms / .13275 mm | 5.476 ms / .13006 mm |
| Raise stop | 3.034 ms / .17878 mm | 2.976 ms / .17587 mm |
| Lower stop | 5.258 ms / .29306 mm | 5.148 ms / .28763 mm |

Crosshead first reaches its stop in .706 ms, **before the output stops**. Replacing
its mass with .005/.020 kg changes nominal differential lower-stop travel to
.27523/.31827 mm. These are local command-loss traces with bus speed maintained,
not total power-loss simulations. E-186's source inertia/mode failures still apply;
E-142's downstream elastic escape remains unmodeled here.

The stop is a consequential grant. Independent return-energy calculation gives
**.05656 J** kinetic energy and **3.363 m/s** command speed immediately before impact.
After an impact with restitution e_stop=0/.3/.6/1, an energy bound gives rebound
q=0/.23574/.70169/1.35714 mm including guide work. The elastic case completely
reopens the work pad (aw=1.1 mm). These restitution values are alternatives, not
measured probabilities. A damper/controlled deceleration must absorb this energy;
declaring spring return or first contact does not supply it. No full-power-loss,
stuck-source, endpoint-rebound or settled-hold acceptance follows.

## Full display consequence and disposition

Use E-186's explicitly allocated four full-stroke passes per bank: empty approach,
loaded up, loaded down, empty return; empty total weight .01962 N. Compute finite
start/stop above at each speed, cruise through the remainder of 40 mm, add .10 s/bank
for capture/release/proof and 6 s/map for preparation/indexing/source ramps/readback/
settling/retry. `T=6+ceil(6400/H)*tbank<30`. This is a **full-stroke schedule scenario**;
short-move command trajectories, proof reliability and the overheads are not validated.
Do not call it achieved arbitrary-map throughput or an optimized schedule.

| v | Differential H / T | Friction clutch H / T | Channel allowance with $250 shared, free sites |
|---|---:|---:|---:|
| .1 m/s | 493 / 28.358 s | 493 / 28.352 s | <$0.507 |
| .2 m/s | 256 / 29.191 s | 256 / 29.172 s | <$0.977 |
| .3 m/s | 183 / 29.404 s | 183 / 29.366 s | <$1.366 |

At 183 heads, $.02 purchased/site reduces channel allowance to **<$0.667** under
the $500 ceiling. These are residual allowances, not quotes; no return spring,
actuator, damper, pad, bearing, wire, sensor or power supply has a free BOM entry.
E-185's 82 independent heads use a different motion schedule and remain a control,
not an intrinsic ranking against all shared-speed designs.

Four openings for every one of 6,400 cells cost **1,519.616 J/map** of command work
in this scenario, before loaded motion (at least 256 J for a 1-N full raise), brake
heat and losses. In the unregenerated inelastic-stop model this energy is spent each
cycle. Over 30 s that is >50.65 W mean mechanical command power. At 183 simultaneously
commanded heads, each 5-ms opening averages **2.173 kW** mechanical input across the
bank. Staggering, energy recovery or a precharged shared source could reduce supply
peaks, but changes the controller/mechanism and must retain independent selection and
charged reset time. Slower control cannot keep the displayed timing without recalculation.

Replication: 6,400 parked support/guide/proof paths; per head two friction interfaces,
two pad springs, return, command guide/actuator, damper and capture. Differential adds
gearing; clutch adds rotating thrust support. Frame load, drift, bus sag and jams are
correlated. Height readback cannot prove torque capacity; retain capture through proof
and stop the module after failed recovery. False acceptance, disturbance, assembly,
wear life and print scrap are unquantified.

**Decision:** stop a rigid neutral shuttle as continuous support, and stop treating a
one-command differential as inherently cheaper than a one-command friction clutch.
Keep both compliant combinations only as conditional references. Do not detail gears,
purchase actuators or print: the decisive next opportunity is reducing command work
while preserving signed control, not fine-tuning these pad dimensions.

Reopen with source-energized control (e.g. wrap-spring collar) or shared spring-energy
recovery: account for both directions, collar/tail reaction, loss, reset and cost.
Cross-check E-163/E-129/E-140 failures. Stop if it hides another full-force actuator
or free lock; return to broader discovery. No print, purchase or CEO boundary.

Checks: generated axial sections satisfy gap/normal complementarity over 1,001 points;
piecewise-affine extrema independently prove the continuous section and torque bounds.
All 128 corner capacities reconstruct the analytical minimum; work quadrature matches
potential difference within 1e−10 J. Free motion, static friction and signed middle-slip
limits pass; Jidle=0 exactly matches clutch traces. At 8/4/2-µs steps nominal lower-stop
travel is .292165/.292765/.293064 mm; normal-coordinate preimpact energy residual
.4646/.2332/.1168 mJ decreases against .05656 J impact energy. This verifies the reduced integration only; omitted follower inertia/rebound,
friction-law uncertainty and elastic load paths dominate its timestep error.
