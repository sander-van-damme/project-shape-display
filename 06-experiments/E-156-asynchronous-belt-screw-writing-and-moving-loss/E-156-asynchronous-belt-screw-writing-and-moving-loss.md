---
status: complete
builds-on: [E-132, E-150, E-155, E-148, E-109, E-147]
---

# A slipping writer separates source inertia only after contact opens

**Stop the tested belt/rotating-nut embodiment at its fast operating point and the
priced motor-selector implementation of its coast-contained schedule.** Continuous
thread engagement avoids a released sole support, but does not arrest the rotor.
Relative slip dissipates; synchronized belt motion does not. No complete survivor,
selected machine, printing or purchase. This is a scoped failure, not a ban on screws.

Input `d4708bc`. Reproduce: `python3 tools/curated-experiment-checks/E-156/screen.py`.
Python standard library; disposable JSON. Evidence: signed analytical mechanics,
exact piecewise contact intervals, two-rotor elastic solution, finite axial envelopes,
and deterministic manufacturing/cost scenarios. Self-review only; no meshed threads,
assembly CAD, process prior, transient controller, measured performance or life claim.

## Changed coupling and explicit hardware obligations

A guided antirotating **translating screw** joins each column; a fixed-height rotating
nut carries load through continuously engaged flanks and grounded thrust/radial
bearings. The column guide reacts thread torque. A nut collar contacts a shared
reversible belt. A travelling H-head bank independently engages idlers in two signed
passes; actual top sensing must determine withdrawal, coast correction and proof.
Unchanged sites remain unselected. One shared motor still owes H contact commands.

Selector: grounded normal slide, rolling idler, backdrivable motor/pinion/rack pushing
inward and grounded compression spring returning outward. Belt torque reacts through
idler/slide and nut bearings to frame. Return must backdrive the motor; drag, gear
inertia, decay and jams remain **unqualified**, not an assumed cheap clutch.
Section assumptions: gap g=.25 mm, stroke y=.50 mm, contact stiffness 40 N/mm, return
5 N/mm, belt tension 2 N/side, support half-span a=5.08 mm:
`N=40 max(y−g,0)`; `Fcommand=N+5y+4y/sqrt(a²+y²)` (mm/N units).
Nominal N=10 N needs **12.892 N command** before slide friction/acceleration. Nine
g=.10/.25/.40, y=.40/.50/.60-mm corners give **0–20 N contact, 2.31–23.47 N command**.
At W=10 N, thread μ=.3 and belt μ=.15, steady raising requires **12.697 N contact**:
nominal selection fails. This is a compliant section model, not wrapped belt/assembly CAD.

A 1-g slide with only its spring returns .50→.25 mm in .4683 ms; real contact/belt
forces assist, actuator drag/decay may oppose. No guaranteed opening deadline.
Stored return energy is .625 mJ, not deleted. Stuck contact needs independent source
cut/readback. Coil or mask substitutes owe their own force, return and command paths.

E-132's long spinning core and crossed writer elbow are replaced by a short rotating
nut and translating screw. E-150 lost its excited support feet; here belt loss leaves
flanks engaged. E-155's stopped positive dogs become asynchronous friction contact.
These are material recombinations of known principles, **not kinetic-arrest passes**.

## Signed energy/contact model

Let positive θ raise z=kθ, k=lead/(2π), mean thread radius r, σ=sign(θdot),
W net downward force, m translating mass and J resident rotary inertia. Square-thread
Coulomb law, while its single loaded flank remains valid:

```
s = k/r;  cσ = r(μ + σs)/(1 − σμs)
Aσ = J + σm k cσ
Aσ θddot = τ − σW cσ
Fflank = W + m k θddot
Qthread_dot = Fflank (cσ − σk) |θdot|
```

Require Aσ>0 and Fflank≥0; zero reaction is only a bias-free diagnostic. Invalid
inertance/contact stops the model, not the physical rotor: no instant jam/arrest is
credited. μk=.01/.02/.05/.3 are **bounds**, not PLA priors. Static μs≥s does not prove
moving arrest. W=.02/1/10 N pairs with m=.002/.05/1 kg without counterbalance;
W=m=0 separately tests a bias-free rotor, not a weightless real column.

At belt speed u and collar radius R, slip is `u−Rθdot`; sliding force on the rotor
is `f=μb N sign(slip)`, torque Rf, and belt reaction is −f. For H identical engaged
cells and belt/source effective translational mass Mb:

```
Mb udot = −Hf                  (source torque cut, no source brake)
Qbelt_dot = H f (u − Rθdot) >= 0
E = H[.5(J+m k²)θdot² + Wkθ] + .5 Mb u²
Edot = −Qthread_dot_total − Qbelt_dot
```

Mb includes belt/pulleys/reflected motor inertia; .02/.2/2 kg are scenario bounds.
Stick solves u=Rθdot and |f|≤μbN: **Mb R²/H** adds to each rotor's J with **zero slip
heat**. This symmetric witness rejects universal isolation; heterogeneous banks remain
unsolved. Four exact initial slip intervals cover each rotor/belt sign combination,
ending at first zero slip/rotor speed. Two hit the single-flank limit; valid intervals
balance signed source, gravity, rotor and heat work to <3e−17 J.

## Finite inventory and moving-loss result

Nominal mean diameter 3 mm, lead .15 mm; nut annulus length 4 mm, inner radius
r−lead/4, outer r+.7 mm; 1-mm collar to R=r+1 mm. A solid thread-region annulus
conservatively overcounts voids; bearings/gears are excluded. Assumed density
1250 kg/m³ gives **.05857 g**, J=**2.15769e−10 kg m²**. Bare 5-mm rotors leave .08 mm
at 5.08-mm pitch, so bearings/idlers/frame require unbuilt tiers/routing. 4.6-mm tops
leave .48-mm gaps. The .075-mm axial tooth width is unqualified on stage-02 nozzles.

Translating screw [h−50,h+4] mm fully overlaps fixed nut [−5,−1] at h=0…40. From h=20,
**25 mm** either way loses full overlap and **29 mm** loses all overlap. Flank strength,
backlash, thrust faces and helical contact geometry are unbuilt. Large coast distances
below extend the ideal thread to diagnose failure, **not physical travel after disengagement**.

Instant belt separation, 100 mm/s, nominal lightweight rotor:

| W / m | μk | Downward hypothetical coast | Upward hypothetical coast |
|---|---:|---:|---:|
| .02 N / .002 kg | .01 | Accelerates downward | 58.62 mm |
| same | .02 | **368.41 mm** | **42.43 mm** |
| same | .05 | 43.73 mm | 23.33 mm |
| same | .30 | 4.83 mm | 5.25 mm |
| 1 N / .05 kg | .02 | 7.13 mm | 1.09 mm |
| 10 N / 1 kg | .02 | .238 mm, **31.02-N flank reaction** | .584 mm |

The favorable heavy-load stop is not a strength pass. High-friction/heavy-mass
lowering corners with Aσ≤0 are model-limit results, not proof of better arrest.
At zero generalized bias and separated contact, nonzero J coasts indefinitely in
this ideal model. Bearing drag could change this only with a defensible lower bound.

Retained contact after cut worsens light-load μ=.02 coast. Mb=.02 kg, H=80/320 gives
**3,039.92/1,036.29 mm** hypothetical downward travel versus 368.41 separated. Stick
needs only 43.1/31.6 µN/cell within the tested 2-N capacity. Mb=.2 kg, H=80 gives
27,083 mm. This is common-mode energy, not relative slip. Constant source speed during
1/3/10-ms opening delay adds .10/.30/1.00 mm before coast; a stuck powered contact can
continue until travel runs out. A grounded jam brakes only with valid contact/friction;
tear/tension loss exposes local coast. Global cut does not delete source kinetic energy.

## Elasticity and coherent manufacturing bounds

Split J equally into nut θ and rim φ with torsional spring K; retain steady pre-cut
twist δ0=σWcσ/K and both velocities. After separation:
`Aσ θddot=K(φ−θ)−σWcσ`, `Jrim φddot=−K(φ−θ)`.
The exact sinusoidal relative solution plus mean deceleration accounts for `.5Kδ²`;
all analytic velocity extrema bracket first zero, refined with 16/32/48 bisections.
W=.02, μ=.02, v=20 mm/s, K=1e−5/1e−4/1e−3 N m/rad give downward first-zero travel
**14.7366 mm**, raising **1.6971–1.6984 mm**. The rim still moves (up to 4.52 rad/s),
so this is **not settled arrest**. Equation/energy residuals <1e−18 J; no numerical
damping. Axial compliance, backlash, tooth bending and post-zero contact switches
remain unmodeled and receive no stabilizing credit.

144 coherent corners cross r=1.45/1.50/1.55 mm, lead=.10/.15/.20 mm, density=1000/1300,
extra J=0/one nominal rotor, μ=.01/.02/.05/.3 at W=.02, 100 mm/s. 48 lack downward
arrest; 96 valid hypothetical stops span **2.65–847.32 mm**, 53 exceeding 40 mm. These
are **not probabilities/yield**. Common lead/friction bias can defeat whole banks:
nominal slope .01592 is below .02; .20-mm lead/r=1.45 mm gives .02195 and overhauls.

Unselected margin `.25−3e` accounts for adverse rotor growth, registration and belt
intrusion each e: .175/.100/−.050 mm at e=.025/.05/.10. The last gives **2 N unintended
normal** in the section law; at μb=.15 that is .75 mN m drive torque versus .002 mN m
static raising threshold at W=.02, μs=.05. No regional-isolation pass. Layer/hole/first-
layer bias, warp, roughness, anisotropy, interlayer weakness, creep, fatigue and wear
can change gaps, friction and stiffness. No X1C prior or independent-cell averaging.

## Full display: speed, heat, command cost and comparison

| Mean thread diameter / lead | Turns per 40 mm | rpm at 100 mm/s | Belt speed | Light-load μ=.02 down coast |
|---|---:|---:|---:|---:|
| 3 / .15 mm | 266.7 | 40,000 | 10.47 m/s | 368.4 mm |
| 6 / .30 mm | 133.3 | 20,000 | 8.38 m/s | 536.4 mm |
| 12 / .50 mm | 80 | 12,000 | 8.80 m/s | 687.1 mm |
| 3 / .50 mm | 80 | 12,000 | 3.14 m/s | Overhauls |

Increasing lead avoids turns at the expense of kinetic hold; scaling up the nut adds
inertia. This is not exhaustive. Rim balance,
critical speed, bearings and thread wear at these speeds are unqualified.

Raising heat is `6400*(Wc_up/k−W)*.04`: nominal W=1 N gives **322/805/4,850 J/map**
at μ=.02/.05/.3; W=10 gives **3,219/8,051/48,499 J**. At 10 N, μ=.3, H=320 and
100 mm/s, source mechanical power is **6.38 kW**. Uniform 10%-slip speed fraction adds
**5,673 J/map**, before bearing/belt/electrical losses. Lowering dissipates gravity plus
supplied work when kinetically self-locking. No temperature/duty limit is established:
these are heat-management obligations, not a universal thermal rejection.

Ideal arbitrary-map protocol uses one raising and one lowering pass per group, with
independent contact termination; unchanged cells stay unselected. Exhaustive 625
two-cell old/new maps verify only state reach, **not sensed or physically isolated
termination**. With .10 s/group for acquisition, directional reversal, local proof
and withdrawal, plus 6 s/map for preparation, transport/registration, final read,
settling and one bounded retry:
`T=6+ceil(6400/H)*(.08/v+.10)`.
Those are optimistic allocations; no earned readback or settling deadline.

| Constant v, mm/s | Required H for <30 s | Complete channel ceiling, $250 shared/free sites |
|---:|---:|---:|
| 25 | 915 | $.273 |
| 50 | 458 | $.546 |
| 100 | 247 | $1.012 |
| 200 | 137 | $1.825 |
| 300 | 99 | $2.525 |

Constant speed is **not** coast containment near endpoints. At the light-load μ=.02
corner, instantaneous separation gives `v(h)≤sqrt(2*a_stop*h)` for remaining travel h.
Even granting infinite powered acceleration, its 40-mm descent takes **≥2.4279 s**;
raising analog **≥.8239 s**. The same mixed-group protocol therefore needs **915
channels**, before extra elastic settling or release latency. Full-stroke initial
speed can be at most 32.95 mm/s and must taper. This is a controller/embodiment bound,
not a universal optimum over regrouping, dual-direction sources or extra travel.

Joint purchases: `H*c_channel+6400*c_site+c_shared<500`. At $250 shared, H=915 permits
<$.273/channel with free sites, <$.134 with $.02/site; a $400 cap leaves $150 instead
of $250. The **$2.30 motor comparator alone** gives **$2,354.50** with reserve before
rack/return/driver/read/wiring/power. It is not a force-qualified selector: stop this
priced route even before qualification. At 100 mm/s motors plus reserve are $818.10;
300 mm/s could give $480 buying 100 motors, but needs 120,000 rpm and ~3.3-m ideal
light-load coast. It cannot inherit the contained schedule. Custom selectors remain
unbuilt, not proved impossible.

Controls: independent screws shed shared source energy but retain E-132's inertia/cost
problem; the lightweight nut improves inertia without solving fast coast. E-155's
rigid roller-cam needs 3,200 stopped dog channels; asynchronous belt contact reduces
that count only before coast-safe slowing. E-148's downstream jaw survives upstream
separation but still owes return, excursion and cost; no jaw is added here.

Repetition: 6,400 screws/nuts/collars, thrust/radial supports and antirotation guides;
H idler/slide/return/actuator sets; shared belts/tensioners/source/abort/readers/motion.
One 10-s resident operation means 17.8 assembly hours before fits, calibration or repair.
Actual geometry is needed for print-time/yield; seized-nut access/props remain unbuilt.

Top readback plus post-separation stationarity/support proof is needed; encoder/current
alone does not establish height after slip. Failed proof retains the bank for supported
correction and one bounded retry, but continued coast/nut failure may defeat recovery.
Assumed p=1e−4 false acceptance gives .64 expected misses/map without independence;
no p is measured, and common bias can defeat every read. No hardware/completion claim.

## Decision and next discriminating axis

Stop fast belt/low-lead nuts, retained-belt-as-universal-sink, nominal 10-N selector
at the adverse load/friction corner, and the priced motor-per-selector contained
schedule. Do not fit higher friction, invent a bias spring, retune a cam or add a
relay. Reopening requires changed inertia/kinematics **and** a bounded moving-loss
path, actual selective contact/readback, manufacturable threads and joint cost/time.

Next: **positive-displacement fluid writing through overlapping tube occlusions**,
retaining pressure behind the last pinch while a bank meters packets. Compare resident
roller train, travelling pinch front and E-109 poppets. First test open reservoir paths
and pressure-driven rollback; then tube inventory, reversal/reset, leakage/creep,
regional isolation and volume/time/cost. Preserve E-109 gland/return and E-147 recharge
failures. Stop if this merely renames valves or transfers the same free coordinate.

Primary sources checked 2026-10-11: [Roton backdriving](https://www.roton.com/screw-university/screw-actions/screw-backdriving-efficiency/)
supports the distinction between powered lowering and overhauling; its bronze friction
is not transferred. [Roton speed](https://www.roton.com/screw-university/types-of-screws/power-screws/speed-for-power-screws/)
identifies sliding heat and wear/duty constraints. [Gates drive manual](https://cms.gates.com/~/media/Files/Gates/Industrial/Power%20Transmission/Catalogs/Heavy_Duty_VBelt_Drive_Design_Manual.pdf)
warns that slip heating can change clutch-belt dimensions and engagement; retrieved
indexed text only, no small flat-belt parameters transferred. [Pololu 1117](https://www.pololu.com/product/1117)
lists $2.30 at 100, excluding freight/tax; this is a comparator, not a market floor
or an available/qualified quantity commitment.

Self-review: signed force/rotor and frictionless limits, μ=s threshold, exact belt
stick balance and sliding work conservation, two-rotor equation/energy identities,
analytic event bracketing with three refinements, axial endpoint overlap, 144 coherent
corners and strict integer schedules. No independent validation or fabricated yield.
