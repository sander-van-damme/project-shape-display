---
status: complete
builds-on: [E-151, E-131, E-148]
---

# Smooth plastic forming cannot retain 10 N across the inherited section bounds

**Stop the smooth two-lobe former as a robust 0/1/10-N embodiment over E-151's
uncertainty box.** A finite admissible feed direction gives a **history-independent
5.8-N reaction ceiling** at the thin/weak corner. It has no parked equilibrium or
downward arrest at 10 N, even with perfect rigid lateral guidance and zero friction.
This is stronger than E-151's 5.435-N mean-loss calculation. The nominal 12.5-N ceiling
neither fails 10 N nor establishes holding. These loads remain scenarios, not product
requirements; **do not reject plastic memory generally or claim a selected machine**.

Input main `8411e9f`; reproduce `python3 tools/curated-experiment-checks/E-152/former.py`
(Python standard library, ~4 s; emitted JSON is disposable). Evidence: analytical
counterexample, generated finite wall/strip coordinates and constitutive quadrature;
self-review. **No contact-force solution, time integration, parked-state simulation,
FEA, calibrated manufacturing prior, physical measurement or independent review.**
The task's cheaper-necessary-bound stop applies: do not spend the remaining probe on
force-feasible contact reconstruction or writer/material optimization of this box.

## Finite geometry and the released coordinate

Use arclength s through one grounded former, with straight tails outside [0,L]:

```
L = 2*pi*R*alpha
kappa(s) = sin(2*pi*s/L)/R
 theta(s) = alpha*(1-cos(2*pi*s/L))
 r'(s) = (sin(theta), cos(theta))            in x,z; vertical at both ends
 n(s) = (cos(theta), -sin(theta))
```

Nominal R=3 mm, alpha=.25 rad, strip b=3 mm wide in y and t=.25 mm thick.
The positive and negative curvature lobes return the tangent to vertical;
they do not return x to zero. Length **4.71239 mm**, exit offset **1.14772 mm**,
rise **4.49483 mm**. Generate strip faces `r±t*n/2` and stationary wall faces at
the same offsets. Each wall is a **unilateral** no-penetration constraint, with
nonnegative normal reaction and zero friction; paired zero-clearance walls are an
ideal limiting channel, not an X1C fit or a solved feasible reaction field.
Assumed .5-mm wall bodies give a **2.39772 × 4.0-mm x/y envelope**. Wall strength,
mounting, manufacture and capture hardware are unbuilt.

A continuous strip has length 80+L mm: input straight length 80−q and vertical
output length q, 0≤q≤40 mm. Both straights receive grounded lateral guidance;
the top follows the output at the exit x. Signed feed moves material coordinate
u to s=u+q, raising/lowering the top without moving the former. Input removal means
**zero axial head traction**, not removing the permanent lateral guides. No end
seat is available inside the 40-mm range. The bound even permits arbitrary end
moments compatible with lateral guidance: it does not silently give axial arrest.
Free-end stress compatibility would restrict this favorable stress set further.

The material velocity at an offset eta is `(1−eta*kappa)*r'(s)*qdot`.
Its dot product with each wall normal is zero for either sign of feed. Thus normal
contacts cannot supply generalized feed work. With t/(2R)<1 and max theta<pi/2,
all offsets are regular and z-monotone: no cusp or self-intersection. This checks
actual generated wall geometry and an admissible transition, **not contact pressure,
wall strength or equilibrium**. A required negative single-wall reaction would need
the opposite wall; no tensile adhesive contact is credited.

## Bound all stress histories, not just cyclic heat

The assumed elastic-perfect-plastic law caps total longitudinal stress by sy.
For any section, including residual stress and axial compression,

```
|M| = |integral_A sigma*y dA| <= sy*integral_A |y| dA = sy*b*t²/4 = Mp.
```

A compatible virtual feed dq changes curvature by `kappa'(s)*dq`, with zero axial
extension. The generalized internal reaction is `Q=int M(s)*kappa'(s) ds`; hence

```
|Q| <= Mp * TV(kappa) = 4*Mp/R = sy*b*t²/R = Cmax.
```

This is a **necessary condition**, independent of strain history, reversal, elastic
unloading and whether the material is currently yielding. It does not require that
the maximizing stresses be mechanically attainable. Their inclusion makes the bound
more generous. For downward feed d=−q, external load does W*dd; equilibrium requires
an opposing reaction W. **W>Cmax excludes equilibrium along this path at every phase.**
Plastic heat alone would not give this result. A stationary normal wall supplies no
missing tangential work; adding friction, an axial stop, another curvature reversal,
a moving/preloaded frame or a genuinely different contacted path changes the model.

The section moment/work method is consistent with [MIT 2.080J, Problem 12-5,
PDF pp.14–15](https://ocw.mit.edu/courses/2-080j-structural-mechanics-fall-2013/d822a94a5e00663ee03a4909086181bb_MIT2_080JF13_ProbSet_10_Sol.pdf).
The transport inequality above is derived here; that source supplies neither this
machine nor material properties. Accessed 2026-10-11.

| Assumed section | E MPa / sy MPa / b,t,R mm | E-151 stabilized loss N | New instantaneous ceiling N |
|---|---|---:|---:|
| Nominal metal-like | 200000 / 200 / 3,.25,3 | 11.9072 | **12.5** |
| Thin/weak coherent corner | 160000 / 160 / 2.9,.20,3.2 | 5.43474 | **5.8** |
| Entire 32-corner box | E-151 combinations | 5.435–23.030 | **5.8–23.9143** |

No named alloy, strain-life curve or hardening law is qualified. Weak t/(2R)=3.125%
and nominal 4.167% are large cyclic bending strains; the thin-rod model is not a
material qualification. Strain hardening or rate strength could change sy: a weak
section would need ≥275.862 MPa effective cap, or t≥.262613 mm at sy=160 MPa,
merely to stop this inequality rejecting 10 N. Equality has no holding margin.

## Elastic inventory and free-input cuts

Elastic control: a homogeneous straight-reference strip fully occupying the fixed
front has `U=EI*L/(4R²)`, independent of q. Nominal U=**102.265 N mm**. The front has
zero generalized elastic force: W=0 is neutral, W=1/10 N has no interior equilibrium,
and nonzero input-cut velocity at W=0 persists in this ideal feed coordinate.
Large stored bending energy does not establish a length-dependent barrier.

For the plastic law, the entire strip's elastic inventory obeys
`Ue<=sy²/(2E)*b*t*(80+L)`: **6.35343 N mm nominal**, **3.94523 N mm weak**.
These are upper bounds, not computed parked inventories. Residual straight-tail
energy matters: a virgin nominal section passage gives work **11.83372 N**,
heat **11.76210 N**, exit-minus-entry elastic energy **.071946 N** at finest
quadrature. Stabilized entry/exit history instead gives nearly zero inventory
change and the E-151 loss. Neither can be assigned as a static brake.

For rigid guidance and assumed constant generalized mass m, the free-feed dynamics
obey `dK/dd=W−resistance>=W−Cmax`. This is an analytical inequality, not a time-step
simulation. At the weak 10-N corner acceleration is always downward, including
immediately after releasing a previously raising or parked writer. For downward
initial speeds 0/.1 m/s, m=1.1 kg and cut heights 5/20/40 mm:

| Cut height | Minimum kinetic energy at bottom, initially stationary | Initially .1 m/s downward |
|---|---:|---:|
| 5 mm | 21 N mm | 26.5 N mm |
| 20 mm | 84 N mm | 89.5 N mm |
| 40 mm | 168 N mm | 173.5 N mm |

All remain positive: **no turning point before the bottom**, while the smooth path
remains constrained. Bottom impact is not successful height arrest. Initially
.1 m/s **upward**, the same bound makes it turn within **1.30952 mm**, then fall;
from the 40-mm endpoint it may meet the upper limit first, so no free-travel result
is assigned through that collision. Endpoint impact/recovery is unmodeled.

The code checks 27 combinations of height, W=0/1/10 N and signed velocity
−.1/0/+.1 m/s; masses .02/.12/1.1 kg are scenarios. The stress bound covers every
raising/reversing/lowering history without inventing representative frozen states.
**Weak 0/1-N cuts and all nominal plastic cuts remain unresolved**, not passes.
The inequality already includes elastic release: do not add the inventory cap as
another stopping reservoir. Coupled transverse/frame vibrations require a richer
model only if a revised embodiment clears the necessary bound.

## Buckling, manufacturing bounds and an unchanged neighbor

Without the granted continuous lateral guidance, Euler buckling of a 40-mm weak
straight strip gives **1.9081 N pinned / 7.6325 N ideally fixed at both ends**;
even the fixed-end control is below 10 N. Nominal values are 4.8191/19.2766 N.
Weak pinned unsupported spans need to be below **17.4728 mm** for a 10-N elastic
Euler threshold. This is an ideal upper screening calculation: residual curvature,
plastic zones, imperfections and end compliance are not stability qualifications.
See [Roylance, beam buckling and strain energy](https://eng.libretexts.org/Bookshelves/Mechanical_Engineering/Mechanics_of_Materials_(Roylance)/04:_Bending/4.02:_Stresses_in_Beams),
accessed 2026-10-11. Lateral bracing removes that escape but not the feed mode above.

Bound scenarios, **not distributions or calibrated X1C priors**:

- Coherent weak material/thickness across a bank; R=2.8–3.2 mm and alpha=.2–.3.
  The feed cap remains **5.8–6.6286 N**. Granting an additional 20% total curvature
  variation still caps it at **7.9543 N**. A radius bound alone cannot bound layer
  stair roughness or extra curvature extrema: TV is an explicit separate assumption.
- Generate neighboring identical cartridges at 5.08-mm centers, keep the neighbor's
  q fixed and bound differential pose error by .2 mm. Largest tested x envelope is
  2.94265 mm; minimum x/y body clearances **1.93735/.98 mm**; 4.8-mm top clearance
  **.08 mm**. Common rigid translation cancels in these clearances. This finite pair
  is geometrically separated, not a routed full-board capture/reader/repair design.
- A rigid frame gives zero neighbor motion by construction. Assumed cross-compliance
  0/.001/.01 mm/N yields 0/.01/.1 mm neighbor motion for a 10-N reaction change.
  No allowable disturbance or compliance prior is inferred. Geometry separation
  does not prove unchanged-region support or vibration isolation.

Finite clearance, warp, hole/slot shrinkage, first-layer swell, layer quantization,
assembly alignment and wear can open contacts or introduce different paths. The
zero-clearance channel is not a production fit. Finite-gap jamming, roughness friction
or a new geometric well could hold where this smooth path fails, but would require
explicit geometry/contact evidence; they are not a free repair. PLA wall creep,
anisotropy/interlayer failure and fatigue can remove guidance. Material hardening,
Bauschinger effect, damage and rate dependence remain model uncertainty. No sampled
yield or board-failure probability follows from the 32 coherent corners.

## Checks, machine comparison and decision

Self-review reconstructs the cap by maximizing over an unrestricted bounded fiber
stress field `sigma=sy*sign(y*kappa')`, independently of constitutive history.
64/256/1024 spatial intervals give weak cap **5.795341/5.799709/5.799982 N**, versus
exact 5.8. Geometry normal-feed dot products are below 6e−17; analytic monotonicity
and offset bounds cover between samples. Fiber/path refinements 32/64, 64/256,
128/1024 reproduce stabilized heat **11.9000/11.90654/11.90654 N**, versus exact
11.9072. Stabilized work−heat−inventory residual magnitude falls
**.020423→.001232→.0000749 N**; virgin residual .108741→.004766→.000332 N.
Reverse stabilized passage agrees, elastic cycle work is below 3e−14 N, and the
section moments stay below Mp. These validate the reduced calculation, not actual
contact force feasibility or settled arrest. There is no time integrator to converge.

The nominal former fits one pair's internal footprint; dense routing is **not** the
rejection. A complete display still owes 6,400 strips, formers, grounded guides,
tops at 5.08 mm, 40-mm usable travel, bilateral capture, observation and supported
recovery. Continuous guide faces replace E-151's illustrative four-station count;
they introduce distributed sliding/wear rather than eliminating repeated contacts.
E-151's .1-m/s writer schedule still needs **137 heads without empty return / 247
with it** for strict <30 s, under its unearned .1-s local and 6-s preparation/proof/
retry/settling assumptions. Joint purchases must satisfy
`6400*c_cell + H*c_head + c_shared < $500` (ideal <$200, acceptable $200–400).
With $250 elsewhere and H=137, even free cells allow <$1.825/head; free heads allow
<$.039063/site. No priced BOM, timing, repair or readback pass. A cut proof that drops
a weak cell cannot establish supported handback; no perfect reader or free return.

E-131 screw retention instead depends on lead/friction and still owes speed/routing;
E-148 field-jaw control has a grounded return path but still owes field decay, kinetic
arrest and fit. Both remain conditional controls, not preferred machines. E-150
feet/bridge stays stopped. Plastic forming's different material physics is real;
this result excludes robust retention across the inherited section box, **not
its entire principle**. Nominal and lower-load cases are unresolved, so no cyclic
material sourcing, richer writer optimization, printing or purchase is earned.

Reopen only with a revised load/material/geometry envelope whose necessary cap
exceeds the relevant load, followed by a feasible finite contact state and cut-path
arrest. Merely increasing the mean-loss calculation is insufficient. Additional
curvature, qualified hardening or explicit axial geometry could change the answer;
all carry new inventory/strain/contact consequences. The next useful search axis is
**geometric barriers that survive free feed**, compared against these controls,
not another smooth-strip section sweep. No CEO authority boundary arose.
