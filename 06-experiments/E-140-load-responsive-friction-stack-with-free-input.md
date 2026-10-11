---
status: complete
builds-on: [E-139, E-129, E-132]
---

# Load-responsive friction permits controlled descent, but does not guarantee free-input arrest

**Retain the Weston principle as a conditional transfer brake; stop this unpreloaded
head as a complete arrest solution.** Unlike E-129's released rollers, its loaded
lowering branch has a grounded, dissipative reaction. The compliant model
arrests both free shafts in favorable cases. Low load,
inertia, adverse friction and stack opening produce stroke-end failures. This
neither rejects all Weston brakes nor accepts an outage drop or complete machine.

Input main `754bb3d`. Reproduce with Python 3 and NumPy:

```
OPENBLAS_NUM_THREADS=1 python3 tools/curated-experiment-checks/E-140/brake.py
```

Evidence: sourced operating principles, signed analytical mechanics, deterministic
hybrid simulation and bounds. No assembly CAD, qualified friction/process prior,
physical measurements or independent review. Generated JSON is disposable.

## Source reconstruction and actual torque path

Sources accessed 2026-10-11:

- [US3399867A](https://patents.google.com/patent/US3399867A/en), description/Figs.1–3:
  input disc 29 screws relative to output-fixed disc 43; both grip ratchet 37.
  Pawl 36 returns ratchet torque to the casing through its supported pivot.
  Spring 40 loads the **pawl's frictional operating joint**, not the brake stack.
  Output reversal moves the pawl into engagement; that motion is not instantaneous.
- [Thern's operating description, pp.1–2](https://thern.com/wp-content/uploads/2023/09/Weston_Brake_Operation1.pdf):
  input tightening raises, output load tightens during holding, reverse input
  loosens the stack for lowering with the pawl holding. This is topology evidence.
- [Harrington Accolift](https://harringtonhoists.com/accolift-electric-chain-hoists/accolift-low-headroom-hoists)
  pairs load and motor brakes. [Its Wright description](https://www.harringtonhoists.com/wire-rope-hoists/acco-wright-work-rated-wire-rope-hoists)
  separately attributes load holding/control to the mechanical brake and rapid
  stopping to the motor brake. Pairing alone does **not** prove standalone failure.
- [US5937990A](https://patents.google.com/patent/US5937990A/en), background:
  axial feedback friction and transverse misalignment can cause chatter. Its
  additional guidance/damping are not included here.

Explicit embodiment: a right-hand male screw on the output shaft; an axially
floating input nut/disc outboard of the output flange; one freely rotating
ratchet annulus between them, with a friction interface on each side. Viewed
from the nut toward the flange, define clockwise tightening/raising as positive.
Input advancing relative to output closes the stack; output rotating in lowering
direction relative to input also closes it. This handedness is our assumption;
US3399867A does not specify it.

Shaft bearings/frame support output force; the screw/flange close axial clamp
force internally. During lowering, ratchet teeth → seated pawl → grounded pivot
carry torque, and both disc interfaces dissipate energy. No motor holding, detent,
bearing drag, stack-return spring or preload is
credited. Relative screw advance compresses the elastic stack.

## Signed branches, not a release flag

Let theta_i/theta_o increase in raising direction; output height is r*theta_o.
Use SI units, load torque L=F*r, lead coefficient a=lead/(2*pi), signed axial
compression x=a*(theta_i−theta_o)−g and N=k*max(x,0). Negative x is a real gap.
The model retains both shaft inertias and **sets input motor torque to zero**
after loss. For square threads with pitch tangent s=a/r_t:

```
h_plus  = r_t*(s+mu_t)/(1−s*mu_t)   # relative tightening
h_minus = r_t*(s−mu_t)/(1+s*mu_t)   # relative opening
thread torque t = h_plus*N or h_minus*N while sliding
                 [h_minus*N,h_plus*N] while relatively stuck
b = mu_disc*R_eff                 # each interface, uniform-pressure annulus
J_i*omega_i_dot = T_i − t + f_i
J_o*omega_o_dot =       t + f_o − L
```

For negative shaft velocity, f_i=f_o=+b*N. At rest each f is in [−b*N,+b*N].
Ratchet reaction must be one-sided: f_i+f_o>=0; this is checked.

Steady descending shafts have equal negative speed and constant compression.
For a permitted thread torque t=h*N, `N=L/(h+b)` and
`T_i=(h−b)*N`. If **b>h_plus**, input torque must actively drive lowering;
removing it decelerates the input on either thread branch while contact remains.
Output overrun increases N, providing feedback instead of an unsupported released
roller. This sufficient sign is not an arrest theorem. Steady heat is
`2*b*N*abs(omega)`; input work is included.

| State | Established behavior and limitation |
|---|---|
| Hold at 12/34 mm, F=.2/1/10 N | With nominal coefficients, choose N=L/(h_plus+b), t=h_plus*N, f_i=t, f_o=b*N. Both shafts can be free and static. No height-specific force assumption. |
| Raise | Tightening builds clamp; ratchet turns in its permitted direction and the discs can rotate together. Total steady input torque is L, ignoring bearing/pawl losses. Clutch capacity and pawl overrun must exist; no qualified full raising transient is claimed. |
| Loaded lower | Grounded ratchet, both friction faces sliding, continuously positive N in the nominal simulated trace. Input actively lowers; no fixed input is used for arrest. |
| Reverse raise→lower | Pawl swing/tooth take-up precedes grounded braking. A 24–60-tooth scenario at r=2 mm gives up to .524–.209 mm equivalent tooth pitch, **plus** unknown pawl swing/compliance; not a measured catch distance. |
| Lower→raise | Input tightens and drives the stack into ratchet overrun. Breakaway, pawl release and alignment are unresolved. |
| Input loss | Simulation below starts with the pawl seated during lowering. It does not grant instantaneous engagement after raising or while a dock is open. |

Even an intact co-rotating stack has raising inertia. In the ideal locked-stack,
massless-ratchet limit, gravity-only upward coast is
`r*(J_i+J_o)*omega^2/(2*L)`: **1.5 mm at 1 N; 75 mm at .02 N** for the baseline.
This is an admissible energy bound/example, not a simulated reversal; at low load
it exceeds remaining travel. Pawl engagement and impacts need separate treatment.

## Free-input transient and independent checks

Labelled design bounds, not process distributions: output r=2 mm;
thread r_t=2 mm, lead=.5 mm; annulus radii 2.5/5 mm (R_eff=3.888889 mm);
k=100 N/mm; J_i=1e−6 and J_o=2e−7 kg m²; 100 mm/s downward start.
J_o may include a 1-g translator plus 1.96e−7 kg m² shaft/transmission inertia.
Applied constant loads .02/.2/1/10 N are independent service-force scenarios,
not masses silently substituted without their inertia. A real carried load needs
its own reflected mass. Nominal mu_disc=.1, mu_t=.02; static=kinetic is an explicit
Coulomb simplification. Axial moving mass, backlash and material damping are omitted.

With nominal coefficients, h_plus=.119673 mm versus b=.388889 mm.
Start on a valid steady lowering branch at minimum compression, then set T_i=0.
Enumerate sliding/sticking modes at both discs and thread with unilateral stack
contact using backward Euler; reject ambiguous solutions/unsupported directions.
Solve static torque intervals and check rest on a further free-input step.

At dt=.1 ms, each case is run from **both 12 and 34 mm**:

| Load | Calculated drop/time until both shafts stop | Finite-stroke result |
|---:|---:|---|
| .02 N | reaches 12 mm in .1243 s / 34 mm in .3822 s, still moving | no arrest before stroke end; no impact extrapolation |
| .2 N | 8.936 mm / .1737 s | arrests in both starting-height scenarios |
| 1 N | 2.281 mm / .0385 s | arrests; clamp increases 3.933→4.854 N |
| 10 N | .913 mm / .0134 s | arrests; clamp increases 39.327→42.042 N |

These drops are **not accepted outage limits**. At 1 N, varying initial steady
thread reaction across its sticking interval changes drop to 1.835–2.281 mm.
Other baseline values fixed: disc mu=.05/.3 gives 4.735/1.391 mm;
thread mu=.1 gives 6.634 mm. Disc mu=.02 or thread mu=.3 causes accelerating
co-rotation and stroke-end failure. J_i=1e−5 also reaches the 12-mm endpoint;
J_i=1e−7 stops in .906 mm. k=10/1000 N/mm gives 4.143/1.855 mm.

Self-review: halving dt=.2/.1/.05 ms gives nominal drop
**2.274947/2.281163/2.284297 mm**. Numerical dissipation falls
8.243/4.137/2.072 microjoules versus ~3.74 mJ physical friction work.
Every step checks kinetic + elastic energy + load work against thread/disc heat
and the explicitly accumulated implicit-step dissipation (residual <1e−8 J).
An independent analytic first sliding segment, with harmonic compression,
halves velocity error .05048/.02503/.01246 rad/s at 5 ms.
A separate exact co-accelerating witness at mu_disc=.02, mu_t=0 has
N=12.681 N and acceleration **−22.822 rad/s²**, agreeing with the solver.
Frictionless-thread and ballistic limits are checked. This verifies equations,
not manufactured geometry, thermal stability, wear or chatter.

## Opening, uncertainty and correlated failures

Opening is not instantly repaired by a load-responsive brake. Grant a seated
pawl but zero compression, output initially at rest, input coasting at −50 rad/s,
and axial gap g. Until re-contact, input stays free while output acceleration is
−L/J_o. Exact first re-contact time and drop are:

```
alpha=L/J_o
t=(50+sqrt(50^2+2*alpha*g/a))/alpha
fall=.5*r*alpha*t^2
```

At g=.1 mm, first re-contact requires **54.912/9.351/4.676 mm** for
F=.02/.2/1 N. Even g=0 with those unequal velocities opens immediately and needs
50/5/1 mm to catch again. The .02-N case cannot re-contact within the entire
40-mm product travel. At .2 N, the simulation contacts but still reaches the
12-mm endpoint moving; at 1 N it arrests after 9.529 mm. These initial states bound
reversal/over-release faults, **not demonstrated
reachable from nominal lowering**, which never opens. Excluding them requires
a proved controller/mechanical invariant; no automatic return is granted.
Gap-case refinement at .2/.1/.05 ms: 9.474/9.529/9.557 mm; numerical loss
180/91/46 microjoules. This is model convergence, not real-contact accuracy.

64 deterministic force/disc/thread scenarios give 36 with the sufficient
`b>h_plus` sign; the fraction is not yield. Coherent low disc friction represents
shared material/contamination; coherent high thread friction can defeat feedback.
Cross ±.05-mm lead, thread radius and annulus-radius errors (16 corners per
mu=.02/.1) with mu_t=.02. Nominal high/low disc-friction sign dispositions remain
unchanged. This is **not an X1C tolerance prior**. Uniform-wear
pressure would give R_eff=3.75 mm; actual patch contact could move the reaction
within [2.5,5] mm. Neither pressure nor stiffness is calibrated.

Hole shrinkage, layer stepping, roughness, face warp, assembly tilt and axial
float affect g/k/friction together. First-layer defects, anisotropic strength,
interlayer weakness, creep, fatigue and wear are unqualified; pad relaxation can
change the initial clamp. Do not average these over 6,400 independent cells or
infer board reliability. The scalar stack has no finite tooth/flank/face collision
model; further geometry is required before a brake design can be admitted.

## Full-machine comparison and disposition

| Family | New conclusion relative to controls | Remaining machine burden |
|---|---|---|
| Load-responsive stack | Real supported sliding-descent branch and conditional free-input arrest; lower heat than heavy permanent drag | Screw fit, two friction faces, ratchet/pawl and its return/operating joint, bearings/thrust support, axial retention, wear adjustment; low-load/reversal envelope unresolved |
| E-129 roller | Nominal hold but released overhauling branch lacks resisting torque | Return/re-wedge dynamics, precision races and release contacts; present result does not repair it |
| E-132 permanent drag | Contact always present; adverse friction/preload corners still accelerate | Large preload/reactions, drive force, heat and dense capture/routing failures |

Resident brakes repeat precision at 6,400 sites; H reusable heads still need
**6,400 guided outputs and service supports**. Addressing selects/captures one supported
column, takes load, releases its parked support, traverses 40 mm, restores/proves
support, and only then leaves. That causal architecture is incomplete: capture,
keeper retention, arbitrary-height routing, actual top/support readback and bounded
recovery are unbuilt. E-132's neighbor collision is not repaired by changing its
brake. The 10-mm discs require remote/tiered routing beneath 5.08-mm tops;
40-mm travel remains fixed.

Optimistic all-site full-stroke schedule at 100 mm/s: `.4 s` motion + `.05 s`
capture/proof per site, plus `6 s` map preparation, registration, final proof,
bounded retry and settling. This gives `T=6+ceil(6400/H)*.45`: **42 s at 80 heads;
minimum 121 heads for <30 s**. Including .4-s empty return gives **74 s / 229 heads**.
With a hypothetical $250 shared reserve and free cells, the $500 ceiling leaves
approximately **$2.066/$1.092 per head**, respectively. Before heads it permits
<$.039063 per cell. These are budget bounds, not prices or a BOM pass.
At 1 N nominal steady descent, heat is .15294 W/head, including .05294 W motor
input; a 40-mm descent dissipates .06117 J/site (~391.5 J/board). At 10 N multiply
by ten. This improves E-132 high-drag heat without settling cost, assembly or
cooling. All-raising 1-N work remains at least 256 J.

Input encoding cannot prove output seating or intact capture. Read actual height
and support before releasing; failed proof must retain capture and arrest. Reader
bias/false acceptance are unquantified. Timing reserves do not prove completion
or isolation of unchanged miniatures.

**Decision:** do not print, purchase, optimize a complete display or add a hidden
motor brake. Keep the supported descent principle; retire this unpreloaded head under the tested load/inertia bounds as a general
arrest answer. Reopening requires
an explicit low-load energy sink or enforceable speed/compression envelope,
finite reversal/capture geometry, and local recovery. Nonzero drop alone is not
the rejection; demonstrated stroke-end escape and missing phases are.

**Next discriminator:** broaden to head-scale energy sinks that remain effective
at low load: spring-applied braking (complete closure/force-rise dynamics, extending
E-128 rather than repeating its contact-gap observation), fluid meter-out with a
normally closed holding valve, and centrifugal speed limiting plus explicit static
retention. Compare against this stack and permanent drag. First screen the complete
selection/motion/retention/recovery paths, low-load inertia and full-board cost/time;
These are search axes, not novelty or acceptance claims.
