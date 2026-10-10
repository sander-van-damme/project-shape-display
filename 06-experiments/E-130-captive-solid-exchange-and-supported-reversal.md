---
status: complete
builds-on: [E-129, E-126, A-024]
---

# Captive solid exchange preserves contact but does not ground the moving support

**Stop the tested level translating pallet and circular pocket carrier.** Both
admit a sphere-contact path between two grounded states; neither has passive
quasistatic equilibrium after input removal at a finite intermediate pose within
the stated friction bounds. The rotary version relocates the missing arrest to
its carrier. The translating version needs a new linear restraint. Both also
collide with an unchanged upstream stack when copied at pitch along their feed
lane. These are embodiment counterexamples, not rejection of compression-length
storage, every escapement, or every captive conveyor.

Input main `0aad89e`. Reproduce (Python standard library):

```
python3 tools/curated-experiment-checks/E-130/exchange.py
```

Evidence: finite rigid sphere/seat/pad coordinates, bidirectional necessary-path
checks and relaxed static Coulomb force bounds. **No completed pocket assembly,
CAD qualification, dynamics, process distribution or physical measurement.** The
counterexample stops admission before detailing pocket opening/recirculation.
Granting favorable pocket constraints makes a failure stronger, not a successful
path into a constructed machine. This is one bounded probe, not a full schedule/BOM.

## Materially different transactions and control

| Topology | Proposed selection, motion, retention and load path | Verification / missing recovery |
|---|---|---|
| Translating captive pallet | Dock a selected horizontal feed lane; drive an incoming ball beneath the old stack on a guided pallet. Sphere contact raises the old stack continuously. Grounded seat tips carry the old ball initially and the new ball finally; count stores height. | Measure follower height and prove grounded seating before undocking. Midstroke rollback has no qualified catch; a false seat indication releases the loaded pallet. |
| Circular pocket carrier | A selected radius-4-mm carrier moves an incoming ball upward around a fixed axis, lifting the old stack into the next count. Same grounded endpoint seats, rotary pocket load path in transit. | Carrier phase alone cannot prove stack contact or seating. Independent height/seat evidence and rotary arrest would be needed after loss of input. |
| Linked-feed control | Fixed selected feed wheel assembles guided compression length from interlocking links; output count/length is continuous. | The assembled column does not ground its input wheel. Retain E-126's arrest/readback and ≥128k-link obligations. |

The first is a constraint inversion: the incoming ball itself is the lifting
wedge, eliminating a separately lifted fork in the proposed path. The second
recombines circular transport with the same grounded compression seats. Neither
uses E-126's four stopped shuttle strokes **in its proposed loaded path**; neither
has a completed replenishment/reset cycle. This is new finite evidence for two
feed/support topologies, not two new physical principles. No landscape saturation
claim or novelty count follows.

Decision-driving primary control source: [Tsubaki ZCA instruction manual,
ZCA01TSE-3, printed 2022-09-20, printed p.6 / PDF p.10](https://tt-net.tsubakimoto.co.jp/lib/manual/M_ZCA_EN/book/data/all_page.pdf),
accessed 2026-10-10. It explicitly says load can reverse the input and requires a
brake; printed p.1 / PDF p.5 also describes load rotating the input shaft. This
supports retaining the control's arrest obligation, not importing industrial
performance, friction or manufacture to 5.08-mm pitch. The pocket search produced
no source needed for the decisive calculation; these constructions are hypotheses.

## Finite geometry, two heights and the interrupted exchange

Sphere diameter d=4 mm. Stack centerline x=y=0; three or eight original spheres
have centers z=0,4,…, giving retained heights **12 and 32 mm** above the initial
bottom tangent. Follower tops are assumed 4.8-mm squares at 5.08-mm centers.
Two fixed spherical seat tips have radius .25 and centers
`(0, ±1.30, −sqrt(2.25²−1.30²))` mm. Outboard supporting rods extend in ±y;
their closest points to the moving balls are those inner tips. Neither grounded
seat translates or receives a free return spring.

Let φ increase during insertion and decrease during removal. Incoming center b
and old bottom center a are generated from actual sphere tangency:

```
Linear: b = (−d cosφ, 0, 0),                    0 ≤ φ ≤ π/2
Rotary: b = (−R cosφ, 0, R sinφ−R), R=d=4,  π/6 ≤ φ ≤ π/2
a = (0, 0, b_z + sqrt(d²−b_x²)); upper centers = a+(0,0,k d)
```

Thus the attempted cycles are **12→16→12** and **32→36→32 mm**. Both old and
new balls touch the grounded tips at their respective endpoints; throughout the
interior both have positive seat clearance. Their mutual contact remains exact,
but the **only load path then passes through the moving pallet/carrier**. This
explicitly locates old support, new support and the handover gap in ground support;
it does not replace those with Boolean lock states.

At φ=45°, actual radius-.25 rear/bottom pocket pads are tangent to the incoming
sphere and clear the old stack by at least **3.56295 mm**. They can supply positive
horizontal/upward forces at that witness. The model grants captive guidance,
bilateral input and noninterfering remaining pocket walls; a complete pocket,
release lip, axle, inlet and outlet are **not** claimed built. No success depends
on these grants: the generous force model still fails. Input removal sets applied
pallet force/carrier torque to zero, without freezing its coordinate. Captive end
stops bound the proposed path, not its intermediate position. Reverse drive retraces
the same load-bearing contact and the same failure pose; lowering is not an
unloaded return stroke. A down-biased follower is required at light loads; the
load scenarios below include total downward bias. Its actual spring and resistance
to follower sticking remain unbuilt. A feed-return spring toward the inlet worsens
rollback; no unmodeled preload or instantaneous reset is credited.

| Witness | Old-seat clearance | New-seat clearance | Height above original seat |
|---|---:|---:|---:|
| Linear | 2.59262 mm | 1.36421 mm | 2.82843 mm |
| Rotary | 1.47734 mm | .93309 mm | 1.65685 mm |

Those heights are geometric distances along a possible rollback route, **not
predicted arrest distances or an invented allowable-drop criterion**. The linear
start also has zero upward component of the ball contact and an unbounded
frictionless lifting-force limit. Moving the initial support or prelifting changes
that entry geometry; it does not repair the separate 45° counterexample.

## Input-loss counterexamples, including friction

Assume total old-stack downward load W={1,3.27,10} N. These are engineering
scenarios, not a new product load requirement. Grant freely available static
friction coefficients {.05,.1,.3} independently at ball contact, old vertical guide
and pallet horizontal guide. Pallet weight C={0,.2} N aids guide friction. Ignore
sphere moment constraints to enlarge the admissible force set; infeasibility of
this relaxed set also rejects the more constrained assembly. The old guide has
no imposed preload or opposing-wall self-stress; unintended wedging is not credited
as controlled retention.

At 45°, contact force on the old stack has positive components Fx,Fz with
`r=Fx/Fz ≥ ρ = cot(45°+atan μ_contact)`. The upper guide gives
`Fz ≥ W/(1+μ_guide r)`. The grounded pallet guide can resist at most
`μ_pallet(Fz+C)` horizontally. Minimizing over r≥ρ, missing restraint is bounded below by

`(ρ−μ_pallet) W/(1+μ_guide ρ) − μ_pallet C`.

All **162 deterministic corners** require additional restraint; minimum **.14530 N**.
At W=3.27 N, all coefficients .3 and C=.2 N, at least **.61132 N** remains.
The expression increases with force ratio, so this uses the most favorable
contact-cone edge. For equal coefficients and C=0, the relaxed threshold at this
pose is `μ=tan(22.5°)=.414214`; larger friction can change the answer. It is not
sourced for PLA, does not fix entry singularity, and is not permission to assume
self-lock. Captivation prevents losing the ball, not translating the whole pallet.

For the rotary case, include the **actual sphere contact point**, not merely its
center. At 45°, carrier torque from the upper load is

`T = ((R−d/2) Fz + (R+d/2) Fx)/sqrt(2)`.

Grant a plain journal radius {.4,.6} mm with coefficient {.05,.1,.3}; its maximum
resisting torque is bounded by `μ_j r_j (Fx+Fz+C)`. Place carrier weight C at the
pivot to grant friction without adding driving torque; omit incoming-ball weight.
With ball/upper-guide coefficient {.05,.1,.3}, all **108 scenarios** still need
external torque (minimizing the combined torque deficit over r≥ρ): minimum
**2.90991 N·mm**; at W=3.27 N and the largest friction,
journal radius and C, at least **9.59713 N·mm**. A brake, ground pawl or over-center
support changes this topology; a stationary input cannot be assumed after removal.
At zero friction virtual work independently gives `W dz/dφ = W(R+d)/sqrt(2)`.

## Manufacturing, neighbors and repetition

These are **bounds, not X1C distributions**. Common sphere diameter bias ±.05 mm
moves the fixed-seat center height by −.03072/+ .03055 mm. Rotary contact angle
at the witness shifts to 44.2701…45.7031°. Independent common d/R biases ±.05
also preserve positive missing rotary torque. Bore diameter 4.2±.10 versus balls
4±.05 gives only .05-mm minimum diametral running gap; with .3-mm walls the
maximum nominal bounded outside diameter is 4.90 mm, within pitch. These reproduce
E-126's section assumptions, not a demonstrated slotted housing. Center wander,
warping, compliance, layer quantization, contact roughness, guide preload, creep,
wear and assembly distortion remain model uncertainty. No yield or lifetime is
estimated. Friction above the bounds or a preloaded guide is a different retention
assumption requiring evidence. Common geometry/friction errors may affect a whole
bank; no independent-cell averaging is used.

An unchanged transverse stack at y=5.08 retains both grounded tips through the
whole sampled insertion/removal: minimum ball-to-ball clearance **1.08 mm**;
nominal top gap .28 mm. This is rigid geometry, not disturbance/vibration proof.
Copy the same input lane in x and the initial incoming ball **intersects the
unchanged upstream bottom ball** by 2.92000 mm (linear) or 1.42879 mm (rotary).
Therefore an isolated clear two-site section cannot establish 80×80 packing.
Vertical staggering/routing is a changed architecture, not a tiny clearance fix.

Forty-mm reach retains E-126's 11-ball bounded case (43.2946-mm low bound before
compression), ≥70,400 balls across 6,400 cells. Per cell: tube and follower guide,
up to ten stack contacts, two ground tip/ball contacts, follower bias, accessible
storage and count/seat readback. Per active lane: two or more pocket contacts,
captive walls/release interfaces, pallet guide or carrier journal, input coupling,
return/end constraints, and now a missing arrest. Permanent local carriers multiply
these by 6,400; reusable carriers instead require docking/selection and recoverable
handover. Count/reset errors, reader false acceptance, shared support deflection
and common feed jams remain. No complete-map time or cost passes are inferred.

Self-review: 64/256/1024 intervals in each direction at both heights; exact sphere
contacts, seat-tip distances and neighbor distances; reverse trace equality;
contact-point cross product versus rotary torque; zero-friction and equal-friction
threshold limits; virtual-work finite differences (rotary derivative error falls
from 9.43e−7 to 1.12e−10 mm/rad). These are geometry/force checks, not time-step
convergence or independent external validation. No reproducible JSON is retained.

**Decision / reopening:** stop these pocket paths before detailed fabrication,
assembly, timing or BOM. Do not tune roller sizes or resurrect the four-stroke
shuttle. Reopen only with a changed path that supplies grounded support or an
explicit arrest during loaded exchange and clears unchanged upstream sites.
The useful next search axis is a different way to keep load in grounded structure
while changing length: shallow translating compression surfaces or counterbalanced
transfer, compared with the direct-head control. Test geometry and input-loss force
balance before any machine claim. No purchases, printing or review gate is needed.
