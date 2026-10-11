---
status: complete
builds-on: [E-188, E-187, E-140]
---

# Finite wrap contact retains low command force but not an earned brake

**Keep two-end wrap control as a conditional component lead, without promoting a
machine.** The finite rod retains small opening forces in the tested sliding states.
Initial torque changes disposition with friction and correlated radius error; moving
the opening tang does not monotonically eliminate contact. Stop actuator sizing from
capstan gain or uniform expansion. Broaden architecture exploration before detailing
another coil. No purchase, printing or physical qualification is justified here.

Input main `a66e00f`; LAB-311. Reproduce with Python 3, numpy 1.26.4 and scipy 1.14.1:

```
python3 tools/curated-experiment-checks/E-189/check.py
python3 tools/curated-experiment-checks/E-189/check.py --full
```

JSON is disposable. Evidence: **nonlinear planar rod/contact simulation and analytical
bounds; self-review**. No calibrated friction/process prior, full helical assembly,
static loaded-release transient, stability proof, physical measurement or independent
validation. This is a distinct contact question following E-188, not a new mechanism.

## Mechanism and finite model

[WO2024011096A1](https://patents.google.com/patent/WO2024011096A1/en), checked
2026-10-11, discloses exchanging the load-bearing tang on reversal and separating
the ends for release. The following guided-end boundary conditions are **our trial
embodiment**, not a reconstruction or rejection of that patent's hardware.

A three-turn spring surrounds a mandrel. Its two ends run on circular radial guides
at hub radius + wire radius + .05 mm. One tang is seated angularly and its director
clamped to the local tangent; the opposite end is angularly free for initial engagement,
then displaced to open the spring. Reversal exchanges ends and slip direction. A
moment-free seated-end alternative tests the clamp assumption. Real tang bends,
blocks, bearings, linkages, seats, command actuator and finite return are unbuilt.

Nominal **assumptions**: 3-mm hub radius, .05-mm radial interference, .3-mm round wire,
E=200 GPa, isotropic Poisson ratio .3, shear stiffness `(6/7)GA`, friction .1.
Natural centerline radius Rf=3.10 mm; material length L=6πRf. These wire-like inputs
are not a material selection or spring-steel allowable. Stage-02 PLA printing may
make guides/hubs; it does not qualify these wire properties or their interfaces.

Each element has constant extension, shear and material curvature. Endpoint
positions/directors determine its **exact circular arc** through the rotation
exponential (`sinc(Δψ/2)`), rather than straight chords or imposed uniform expansion:

```
Ue = h/2 [EA ε² + (6/7)GA γ² + EI (Δψ/h − 1/Rf)²]
gap_j >= 0; N_j >= 0; gap_j N_j = 0
F_t,j = sign(slip) mu N_j;  torque = sign(slip) mu R_hub sum(N_j)
```

The circular wire's eccentric contact couple `−(d/2) F_t` is included, so hub torque
is not incorrectly calculated at the wire centerline. A contact active set and
banded Newton solver enforce equilibrium; complex-step derivatives use local element
support. Failed roots are **indeterminate**, not mechanical rejections. The method
finds a continued equilibrium branch, without proving uniqueness or dynamic stability.

All contacts are at impending/ongoing slip in one imposed direction. Thus the model
computes sliding torque and tang reaction while the mandrel slips relative to a
quasi-stationary spring. It does **not** solve the unknown stick/peel history of a
loaded static brake, engagement from free rotation, friction reversal during opening,
or power-loss return. No actuator may be sized from these reactions alone.

The model is planar: successive turns occupy the same projection. Axial pitch,
helical torsion, interturn contact and real tang transitions are omitted. Actual
element arcs are checked against the mandrel between nodes, not merely at endpoints;
this is finite contact geometry, not full CAD or a packing/printability pass.

## Nominal opening and signed reaction

Let q be extra opening referenced to Rf after the angularly free end equilibrates.
The actual end-guide arc is `q × 3.20/3.10`; reported force below is conjugate to
that actual arc. Results use 240 elements, mu=.1:

| q / actual arc, mm | Sliding torque, N mm | Opening force, N | Elastic energy, mJ |
|---|---:|---:|---:|
| 0 / 0 | 1.5340 | 0 | .08118 |
| .10 / .1032 | .37738 | .10410 | .08515 |
| .30 / .3097 | .07310 | .15337 | .11130 |
| .60 / .6194 | .06090 | .19279 | .16206 |
| 1.00 / 1.0323 | .06904 | .23929 | .24687 |
| 2.50 / 2.5806 | .11662 | .40719 | .72470 |

Most distributed contact peels away, but localized contact persists. After q=.6 mm,
additional opening increases residual drag; an imposed increasing uniform radius
would miss this. **Full clearance is not achieved in this displacement range.** That
does not by itself forbid a low-drag clutch: a wear/heat budget and repeatable return
would be needed. No model demonstrates release at every possible larger displacement.
The bending-stress diagnostic reaches 1.015 GPa at q=2.5; yield, fatigue, tang
concentration and life are unqualified. Stored-energy change is not total command or
source work: frictional work and the rotating mandrel's energy are separate terms.

At 120 elements, reversing the slip and exchanging the seated end reproduces torque
of opposite sign and the same opening reaction. Reversing slip while retaining the
same seat gives only **.3383 N mm** initial magnitude, versus **1.5331 N mm** with
the proper end. The second seat is a real reaction-path obligation, not a free sign
change. Removing the director clamp gives 1.5784 N mm initially and .1602 N mm at
q=2.5: the residual contact is not solely an artifact of that rotational clamp.

## Variability versus uncertainty

These are **bounded competing scenarios**, not distributions or yield samples.
With otherwise nominal geometry, initial sliding torque at mu=.05/.10/.125/.15/
.175/.20 is **.4830/1.5331/2.4646/3.8522/5.9232/9.0165 N mm** (120 elements).
Continuation in mu resolves the high-friction branch; an unsuccessful cold start
must not be called a self-locking failure. There is no measured prior choosing a mu.

The continued mu=.2 branch also releases with small force: at q=.10/.30 mm,
torque is **2.2113/.16584 N mm** and actual tang force **.1040/.1614 N**.
Thus a branch with adequate initial torque can retain the command advantage; this
is stronger evidence than the under-capacity nominal example alone. It still slides,
dissipates source work and has residual contact, rather than demonstrating static
loaded release or passive power-loss recovery.

Under the separate 1-N load / 2-mm pinion scenario, required torque is 2 N mm.
The nominal .1 case falls short even before finite engagement; .125 crosses this
necessary sliding-capacity condition. It is **not** an arrest or holding acceptance.
E-140's need for a grounded dissipative rotor, and E-188's finite engagement/coast
obligations, remain. A coasting drive clutch cannot serve as that ground path.

To expose the consequence, **grant** instantaneous engagement and a grounded rotor
maintaining the calculated initial torque throughout a stop. Reuse E-188's downward
.3-m/s, 1-N gravity load and 1e−8-kg-m² shaft inertia through a 2-mm pinion. With
`m_eff=1/9.81+J/r²`, `B=tau/r`, stopping distance is `m_eff v²/[2(B−1 N)]` when
B>1 N. The .1 friction case has no finite stop in this imposed model; .125/.20 give
**20.23/1.340 mm**. Brake heat equals initial kinetic energy plus gravitational work.
These are conditional post-engagement calculations, not hardware outage bounds:
return delay, rotor compliance, changing spring pressure and rebound are omitted.
Merely crossing the static torque requirement leaves very little arrest margin.

Apply ±.10-mm bounds independently to hub radius and natural inner radius, including
coherent and opposing shifts. Keep nominal interference .05 mm; mu=.1:

| Hub / natural-radius errors, mm | Actual interference, mm | Initial torque, N mm | q=2.5 torque, N mm |
|---|---:|---:|---:|
| −.10 / −.10 | .05 | 1.6285 | .1244 |
| −.10 / +.10 | −.15 | 0 | .0671 |
| +.10 / −.10 | .25 | 6.5663 | .2598 |
| +.10 / +.10 | .05 | 1.4459 | .1096 |

The loose corner has .05-mm minimum initial clearance and no acquired engagement.
Its imposed end motion later creates localized contact: opening command is not a
universal monotone clearance coordinate. The tight corner reaches a **2.177-GPa**
elastic bending diagnostic at q=2.5; the constitutive assumption may fail there.
Large-deformation, material and contact uncertainty dominate any apparent advantage.

Radius bounds represent hub shrink/bias and purchased-coil variation; they are not
measured X1C capability. Common print/material batches can move all heads toward the
same corner. No independent-cell averaging, yield, force percentile or board-reliability
claim follows. Ovality, roughness, wear, creep, guide misalignment and correlation
between friction and dimensions are unresolved. Corner runs at 120 elements have up
to .000752-mm inter-node penetration, so their late-opening drag is a coarser screen.

## Numerical evidence and disposition

Nominal 60/120/240-element initial torques are **1.53414/1.53311/1.53404 N mm**;
q=.6 torques are **.06144/.06111/.06090 N mm**. Across the six reported opening
states, 120→240 changes torque by at most about .5% and command force by about .2%.
At 240 elements the worst exact-arc mandrel penetration is **.000029 mm**; the solver
does not disguise nodal complementarity as perfect continuous contact. This numerical
error is much smaller than the manufacturing bounds, without bounding omitted physics.

Checks: analytic energy gradient versus complex step; rigid translation/rotation
objectivity; independently known circular pure bending and straight-element limits;
zero friction; signed seat exchange; nodal complementarity; global angular balance
including section couples; exact arc endpoint closure; mesh and contact-gap refinement.
No independent hardware/model validation is claimed.

Discarded displacement-element models exposed two distinct numerical failures:
linearized uncoiling introduced false strain, while reduced integration undercounted
interpolant energy and fully integrated low-order fields locked. The latter gave
false full clearance on coarse meshes. Their source is archived in checkpoint
`87fe40b` (`contact.py` and `nonlinear.py` in the E-189 experiment workspace);
the retained exact-arc formulation avoids those interpolation errors. Do not resurrect
coarse clearance or force estimates from those trials as engineering evidence.

**Portfolio decision:** low command effort survives as a reason to retain wrap
control; reliable engagement, loaded release, finite return and grounded arrest do
not. Direct motor plus explicit ground brake remains the simpler control architecture.
E-187's pad has much larger command effort but a different modeled capacity margin;
neither has qualified hardware. Do not rank machines by one force number.

No full-display obligation is removed: 6,400 parked supports/proof paths, and per-head
wire spring, hub, two seats, guides/linkage, actuator/return, bearings, dissipative
rotor and capture/readback remain. Under E-188's particular four-pass schedule, even
instantaneous transitions require 173 heads and <$1.445 purchased/head with $250
reserved and free sites. This contact calculation supplies neither that BOM nor
completion timing, local disturbance, readback reliability or recovery.

Next attention shifts to a materially different addressing/transport architecture
axis rather than further coil sizing. Reopen this component with a concrete 3D tang/
hub geometry and stick/slip return model that retains its advantage under fit/friction
bounds and a finite grounded energy sink. The entire wrap principle is not rejected;
no print request or CEO-owned boundary is created.
