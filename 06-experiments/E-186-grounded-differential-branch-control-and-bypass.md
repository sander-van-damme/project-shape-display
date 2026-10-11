---
status: complete
builds-on: [E-185, E-082, E-137, E-156, E-142, M-008]
---

# Differential power sharing needs branch grounding and an idle path

**Reject a common input brake as sole retention and paired working outputs as independently parkable continuous-bus channels.** A dedicated idle rotor escapes the latter contradiction, but replaces the input clutch with two grounded friction interfaces and controlled handover. Retain it only as a conditional comparator; no complete machine, cost advantage or hardware acceptance follows.

Input main `42d8bd6`; LAB-305. Reproduce with Python 3 + NumPy:

```
OPENBLAS_NUM_THREADS=1 python3 tools/curated-experiment-checks/E-186/branches.py
```

Evidence: ideal gear constraints, signed lumped dynamics, deterministic uncertainty boxes and schedule calculations; self-review. No generated gear/brake CAD, contact qualification, calibrated manufacturing distribution or measurements. JSON is disposable.

## Mechanisms and novelty scope

Search axis: automotive differential/planetary power splitting, then inversion of the second working output into an **unloaded bypass rotor**. This adds a repository comparison, not a claim of invention or landscape saturation. E-082 already has physically disengaging row keys; E-137 requires internal power cuts; E-156 separates a slipping belt only after contact opens. Their source equations were inspected. None supplies free branch braking. M-008 remains the clutch-bus control. E-142's finite brake closure/rebound and elastic escape remain unresolved here.

The [MathWorks differential model](https://www.mathworks.com/help/sdl/ref/differential.html) explicitly retains counter-rotation with the driveshaft locked. Its [planetary model](https://www.mathworks.com/help/sdl/ref/planetarygear.html) supplies the analogous three-port gear constraint. Accessed 2026-10-11. These support ideal topology only; their default inertias, friction and efficiencies are not transferred to X1C parts.

All heads below address guided 5.08-mm tops spatially, capture a column before releasing its resident ground stop, move up/down through 40 mm, restore/prove that stop and withdraw. Resident stops, release/return, guide support and direct height/loaded-seat readback remain necessary. Failed proof retains capture and inhibits travel; a commanded brake state is not support proof.

| Combination | Selection and motion | Retention/load reaction; verification/recovery obligations |
|---|---|---|
| Two working outputs | One shared carrier drives a pair of rack heads; brake the other output to move one. | Each output needs a ground brake or resident seat. Input brake alone permits counter-motion. Parking both stalls its carrier; independent completion on a rigid continuously moving bus is impossible. Stop the bus, add carrier disconnection or change topology. |
| Work + idle rotor | Carrier on common reversible bus; work shaft drives captured rack, other shaft is an unloaded rotor. Ground idle rotor to drive work; ground work to idle the bus. Exchange friction brakes to accelerate/decelerate independently. | Work brake grounds the captured column during idle; idle-brake reaction enables motion. Count both friction faces, return/control, rotor/gear bearings and common source sink/arrest. Read actual height and support before release. Neither spring closure nor source braking is built. |
| Dog-clutch bus | Shared shaft connects to rack head through selectable positive dogs. | Separate ground brake/seat holds disconnected head. Teeth must synchronize/unload before engagement/disconnection; a rigid dog alone cannot deliver the asynchronous friction schedule below. Source cut still leaves coupled inertia. E-082's command keys are not this loaded power clutch. |
| Independent direct setter | E-185 bidirectional motor/profile per reusable head. | Avoids shared-source inertia, retains capture, resident stops, output arrest and readback. E-185 base schedule needs 82 heads; no hardware/BOM pass. |

Internal mechanisms may be larger than top pitch, but tiers, transport, bearings, wire routing and X1C modules remain unbuilt. No 5.08-mm gearbox packaging claim.

## Grounding test and a source-lock counterexample

For equal side gears, `w+d=2c` for work, second output and carrier angular velocities. Virtual work gives equal side reaction torque and twice that reaction at the carrier. Grounding c leaves `(w,d)=(u,-u)` free. Grounding either side plus c removes that mode; grounding both sides forces c=0. Planetary weights `a*w+(1-a)*d=c`, a=.25/.5/.75, change ratios but preserve the same rank defect. All eight grounding combinations are enumerated.

A binary differential tree with N leaves has N output degrees of freedom before constraining its source and N−1 afterwards. Numerical rank checks at N=2…64 agree with induction: each added split adds one independent difference coordinate. Sole root arrest therefore leaves **6,399** free coordinates at 6,400 leaves. This is a constraint count, not a universal actuator lower bound; mechanically ganged brakes and resident stops can supply constraints. With all but one leaf fixed in a balanced N-leaf tree, that leaf runs at N times root speed. Redistribution is not independent velocity control.

Finite witness: carrier **already stationary and grounded**, two output pinions r=2 mm, unequal downward loads 1/.02 N, translated masses `max(.002,W/9.81)` kg and 1e−8 kg m² rotary inertia each. Both branch brakes open, initially at rest:

`(J1+J2)*w_ddot=−(W1−W2)*r`, `d_ddot=−w_ddot`.

At 1/5/20 ms the 1-N column drops **.00450/.1124/1.7986 mm** while its neighbor rises by the same amount. Signed potential loss equals kinetic gain. Equal loads remove acceleration but supply no restoring stiffness and do not stop an existing counter-rotation. These are explicit load/inertia bounds, not service requirements, observed displacement or acceptance limits.

## Idle-rotor handover: finite time, signed work

Let positive progress follow the commanded direction s=+1 raising/−1 lowering. Carrier speed is held at `v/(2r)` by an ideal four-quadrant source; work speed u ranges 0…v/r and idle speed is v/r−u. Let `L=s*W*r`, `Jw=max(.002,W/9.81)*r²+1e−8`, and idle inertia Jd. Sliding work/idle brake torques Bw/Bd oppose their positive progress velocities:

```
(Jw+Jd)*u_dot = −L−Bw+Bd
lambda = Jw*u_dot+L+Bw
carrier_torque = 2*lambda
source_work = change(kinetic) + L*work_angle
              + Bw*work_angle + Bd*idle_angle
```

For start use Bw=0, Bd=B; for stop use Bw=B, Bd=0. A held brake can react either torque sign at zero velocity. Both travel directions require **B>W*r** for this protocol. Brake capacity is not actuator command force and neither is free.

At W=1 N, r=2 mm, Jd=1e−8 kg m², B=.003 N m, v=.1 m/s:

| Transition | Time | Work travel | Brake heat |
|---|---:|---:|---:|
| Raise start / lower stop | 21.387 ms | 1.0694 mm | 1.6041 mJ |
| Lower start / raise stop | 4.277 ms | .2139 mm | .3208 mJ |

An instantaneous positive dog cannot substitute for either moving brake contact. Both ideal brakes fully grounded at nonzero c are incompatible; releasing both leaves motion load-dependent. Actual contact overlap, backlash, delay and source compliance must determine the transition, not an assigned perfect switch.

Short moves need not reach source-imposed maximum speed: exchange brakes before idle speed reaches zero. Constant accelerations give triangular/trapezoidal profiles. All 441 old/new combinations of 21 heights at 2-mm spacing pass the **ideal** finite-move calculation at each v=.1/.2/.3 m/s. At a .3-m/s bus setting, a 2-mm raise instead peaks at .12484 m/s and takes 32.040 ms. Independent stopping grants arbitrary maps only while the common source maintains speed and brake commands are independently realized. There is no sensed contact/geometry pass.

216 deterministic transitions cross W=.02/1/10 N, Jd=1e−8/1e−6/1e−5 kg m², B=.003/.01/.03 N m, v=.1/.3 m/s, both signs and start/stop. **24 have no desired transition** (insufficient brake torque); 192 are finite, eight requiring >40 mm in a single full-speed transition, maximum 234.40 mm. Slower/triangular motion can repair a distance failure at a timing cost. Counts describe this box, not yield or rejection of every ratio/brake design.

A separate three-axis mass/constraint solve reconstructs the reduced acceleration and source reaction. Signed energy identities close to 1e−9 J; 8/32/128-step midpoint integrations reproduce exact constant-acceleration travel. This verifies equations, not real contact dynamics; midpoint is exact here, so it cannot establish contact timestep convergence.

## Outage and manufacturing sensitivity

Idle-rotor diversion separates idle operation from work, **not** a universal source-energy cut. During drive its idle brake is held. If all engaged heads descend together after power cut, common carrier inertia reflects as `Jsource/(4H)` into each work coordinate. Until the work brake closes, gravity accelerates them; after closure at torque B, deceleration is `(B−W*r)/(Jw+Jsource/(4H))`. A symmetric witness suffices to disprove guaranteed isolation; heterogeneous banks and failed brakes remain unmodeled.

For the preceding 1-N, .1-m/s, .003-N-m case:

| Source inertia referred per head | First stop with 1-ms delay | With 20-ms delay |
|---|---:|---:|
| 1e−8 kg m² | 1.383 mm | 12.680 mm |
| 1e−6 kg m² | 3.849 mm | 11.237 mm |
| 1e−4 kg m² | 251.344 mm | 257.068 mm |

Larger inertia reduces acceleration during delay but increases kinetic energy; ordering depends on delay. Values beyond travel extrapolate the rigid law to expose failure, not predict post-crash motion. Closure is an imposed torque step; E-142 shows why nominal touch does not establish sustained braking. Static hold afterwards also needs adequate friction, structure and intact load path. Simultaneous brake closure can arrest the whole bus, with unmodeled peak shaft/gear/frame loads.

Illustrative brake box: single face, friction μ=.1/.3, effective radius 3/6 mm with a coherent −10% radius bound, normal force 1/5 N. Capacities span **.00027–.0081 N m**; only 3/8 corners exceed the 1-N requirement .002 N m, none exceed the 10-N requirement .020 N m. This is not a calibrated friction or tolerance prior. Shared material/temperature, radius bias and spring relaxation can defeat whole banks; independent-cell averaging is inappropriate. At μ=.1 and minimum radius 2.7 mm, B=.003 needs 11.11 N normal force before release friction or dynamics.

Shrinkage, holes, wall/layer quantization, first-layer distortion, warp, gear backlash, alignment, surface friction, anisotropy, creep, fatigue and wear are not characterized. No manufacturing yield, brake life, print time or scrap claim is warranted. More stiffness can reduce deflection but does not remove the free differential mode.

## Complete-board bounds and disposition

Illustrative bank protocol starts heads at zero: empty approach upward to old heights, loaded raising pass, loaded lowering pass, empty return downward after seating. Empty motion includes a 2-g carriage and its .01962-N weight; loaded W denotes total downward force. Each pass permits independent start/stop via the granted brakes. A full 40-mm trapezoid takes `.04/v+(t_start+t_stop)/2`. Add .10 s/bank for capture/release/local proof, and 6 s/map for digital preparation, transport/registration, source ramps/reversal, final read, settling and one bounded retry:

`T=6+ceil(6400/H)*(.10+sum(four_pass_times)) <30`.

These are unvalidated allocations, not accomplished update times or an optimum scheduler. Brake command preparation is charged to those allocations, not outside the boundary. Shared motor acceleration, observation latency and fault recovery can exceed them. Shorter moves fit inside the ideal full-pass envelope; unchanged cells stay on resident seats, though shared-frame disturbance is unquantified.

| v (m/s) | Minimum H for this schedule | T (s) | Complete channel allowance, $250 shared/free sites | With $.02/site purchases |
|---|---:|---:|---:|---:|
| .1 | 493 | 28.446 | <$0.507 | <$0.247 |
| .2 | 256 | 29.830 | <$0.977 | <$0.477 |
| .3 | 194 | 29.533 | <$1.289 | <$0.629 |

All limits derive from `Cshared+H*Cchannel+6400*Csite<500`; they are **not prices**. At the $400 band subtract $100/H from each allowance. A $250 reserve cannot meet the ideal <$200 band. Source, sink, brake commands, gear supports, wiring, sensing, capture and arrest must all fit an actual BOM. Two brake interfaces need not mean two actuators: a complementary linkage may share one command, but needs finite geometry, return and loss behavior. No cheap actuator is supplied by this model.

Ideal concurrent loaded mechanical power at those H/v combinations is 49.3/51.2/58.2 W for W=1 N, before brake/gear/idle losses and source ramps. Full upward work is at least 256 J at 1 N, 2,560 J at 10 N; lowering needs an energy destination. The assumed source speed is not a selected motor. E-185's independently optimized 82-head schedule and these fixed-bus four-pass schedules are **not an intrinsic ranking**; shared speed optimization/regrouping can change counts.

Replication remains 6,400 guides/stops and their release/proof paths, plus H reusable captures/rack outputs, H differential assemblies and idle rotors, **2H ground friction interfaces**, controls/returns and bearing supports. A 10-s repeated resident assembly step alone is 17.8 h. Dog-clutch control needs H coupling and H grounding interfaces, synchronization and return; direct control needs H motors plus arrest. Printed parts do not erase fit, wear or assembly. Source sag, stuck brakes and bus jams are correlated failures. A shared input encoder cannot detect counter-motion or prove top height; readback false acceptance and recovery reliability remain unmeasured.

Stop paired-working-output continuous-bus independence and source-brake-only retention claims. Do not start detailed differential gearing or printing from these counts. The bypass rotor is a real changed topology, but has no demonstrated cost or arrest advantage over clutch/brake control. Reopen promotion only with a finite affordable complementary brake command, signed load-support continuity and bounded source-loss travel; retain the direct control.

Next useful discriminator: **compare one-command complementary ground/bypass brakes with one-command clutch/ground switching**, reusing E-142 closure and E-082 positive-key failures as controls. First inspect finite return/overlap and command work, then cost/time; stop before detailed CAD if it merely substitutes a catalog motor per costly selector or hides an unsupported crossover. This is conditional function-combination probing, not a preferred machine or another claim of broad novelty. No print, purchase, approval wait or CEO boundary.
