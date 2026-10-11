---
status: complete
builds-on: [E-159, E-148, E-140]
---

# Finite braid opening needs strand redistribution and supported capture

**Stop the prescribed fixed-crossing braid as a release/regrip solution. Do not
promote the freely sliding path to a force-bearing mechanism.** Finite end anchors
produce simultaneous strand slack and stretch during opening. Allowing material
redistribution repairs that kinematic contradiction, but neither supplies the
crossing forces nor guarantees spring return. One strong corner still returns
in the restricted model; the braid principle is unresolved, not universally
rejected. No machine selection, sourcing, print or purchase is earned.

Input main `01c0ce3`. Replay: `python3 tools/curated-experiment-checks/E-160/braid.py`
(Python with NumPy; tested 1.26.4). Evidence: generated finite strand centerlines,
polyline separation checks, elastic/work bounds, conditional return integration,
and analytical support/access witnesses; self-review only. **This is a prescribed
kinematic path, not a relaxed rod/contact equilibrium or loaded braid simulation.**
All numerical material, tolerance, load and friction values below are explicit
scenario bounds, not X1C/yarn priors or measured performance. Generated JSON is
reproducible and omitted from the repository.

## Construction and what the model can falsify

Sixteen .10-mm circular strands, eight of each hand, surround a rigid 3-mm stalk.
Upper ends are grounded; lower ends terminate in an axially guided collar. A
separate grounded spring pulls the collar downward: nominal P=.10 N, k=20 N/m.
Closed sleeve length is 20 mm; core strand angle is nominally 45°. The stalk must
be at least 60 mm long to retain 20-mm overlap through signed 40-mm motion, before
end fittings/guides. No exposed stalk end may enter the sleeve during motion.

Generate `z=L*t`, `phi=2*pi*j/8 ± Omega*t`, `Omega=L0*tan(theta)/(r+d/2)`.
The central 70% has base centerline radius `r+d/2+q`. Smooth cubic shoulders over
the first/last 15% join fixed 2-mm-radius anchor regions. Alternating radial lifts
`1.25*d*max(±cos(8*Omega*t),0)^2` form explicit over/under paths; half the central
strand path lies on the stalk at q=0. Positive q lifts that entire contact subset:
**partially open does not mean partially supported in this constructed path**.
The round-strand choice is a design hypothesis, not a claim about all flat braids.

For each q solve L by bisection so mean strand length is conserved. The two hands
have slightly different lengths; give each its own initial rest length and include
its changing total elastic strain. Do not silently give one common inextensible
length to both. Fixed-crossing material instead retains each segment's rest length.
Tension-only energy is `sum(EA*s0*max(strain,0)^2/2)`, EA=20 N/strand. Bending uses
`sum(EI*kappa^2*ds/2)`, EI=0/1e-10/1e-9/1e-8 N m², with straight stress-free yarn.
Curvature comes from generated tangent changes. Crimp-set/preformed yarn needs a
different reference curvature; no benefit from it is credited.

The mean-cosine initial prestrain is a nominal inventory estimate, **not** an
assembled preload equilibrium. Prescribed radial shape and axial stationing have
uncomputed constraint reactions. In particular, collision clearance at a crossing
is not a compressive contact reaction. A real unconstrained braid can relax to a
different shape. This limitation prevents accepting any calculated exponential
capacity; it does not erase a failure of this specific imposed path.

Primary context, accessed 2026-10-11:
[Lu et al., 2024, abstract/section excerpts](https://www.sciencedirect.com/science/article/pii/S2352431624000804)
model fixed-end woven tubes by intersection energy and report nonuniform shapes.
The full article was inaccessible (403); no equations or properties are transferred.
[US5505117A](https://patents.google.com/patent/US5505117A/en) intentionally uses
interstrand friction to retain expansion. Thus zero crossover drag is a favorable
alternative, not a sourced default. Neither source qualifies this small assembly.

## Finite geometry and return results

Nominal .15-mm radial clearance needs **1.839-mm collar stroke**, versus E-159's
2.224-mm uniform-helix construction; these are different geometries, not a correction
to that formula. Fixed material develops **+1.38% / −3.45%** segment strain at 384
segments. Negative strain is slack, not compressive yarn strength. Material must
redistribute by approximately **.160 mm** along a strand (range of cumulative
segment length mismatch); simply declaring fixed crossings and uniform tension
is inconsistent. At EA=20 N, the peak local tension inventory is .276 N/strand,
not the intended .1-N total preload. Finite tensile allowables are still absent.

Nominal outer envelope radius is **2.175 mm**; two such envelopes at 5.08-mm pitch
leave **.730 mm**. A proposed 4.6-mm collar OD leaves .480 mm between collars.
Exact polyline segment comparisons check opposite-handed and adjacent same-handed
strands. Open-state minimum crossing surface gap is **20.74 micrometres** at 384
segments, **22.26 micrometres** at 768. This is deliberately separated geometry;
it supplies **no crossing normal-force witness**. Closed stalk chord penetration
is .219 micrometres at 384 segments, a discretization artifact, not granted material
interference. Open stalk clearance converges toward .150 mm. End bonds, guide
walls, spring packaging, head sweep and force-bearing contacts remain unbuilt.

Spring/bending/strand energy gives an approximately **.217-mJ** nominal opening
inventory before dissipation. A .05-N generalized resistance adds **.092 mJ**
opening work. This resistance is defined at the collar and bounds all guide,
crossover and hysteretic losses; it is not a fitted yarn friction coefficient.
Integrate released potential minus resistance work into a 1-g collar's kinetic
energy along the prescribed path. Zero kinetic energy with insufficient drive
sticks. No external motor closes it and no impact/bounce credit is granted.

| Generalized resistance | Nominal full-open return | Cuts at 25/50/75% opening |
|---:|---:|---|
| 0 N | about 5.32 ms | return in restricted model |
| .05 N | about 6.78 ms | return in restricted model |
| .12 N | stops before full closure | all fail full closure |
| .20 N | cannot start from full open | all fail full closure |

Opening/closing cuts with zero initial collar velocity are explicit arrest/restart
bounds. They do not simulate a moving opener, drive detachment, impact or recovery
from a jam. Partial-closing cuts use the same coordinate and inventory; a jammed
opener that remains connected can prevent return regardless of this table.

Coherent scenarios vary the whole neighboring pair's radius/angle/friction/gap/
preload together, not as independent cells:

| Scenario: r mm / angle / mu / gap mm / P N | Stroke mm | Fixed-material peak strain | Material redistribution mm | Return at .12-N resistance |
|---|---:|---:|---:|---|
| weak: 1.6 / 40° / .1 / .30 / .05 | 2.556 | 2.51% | .251 | fails |
| nominal: 1.5 / 45° / .2 / .15 / .10 | 1.839 | 1.38% | .160 | fails |
| strong: 1.4 / 50° / .3 / .05 / .15 | .895 | .527% | .0654 | about 6.44 ms, conditional |

These three corners are not yield estimates. EI variation over the stated bounds
changes nominal restoring force from roughly .093–.137 N; it does not rescue
.12-N drag across the full path. A 4-mm opening stop covers these paths; a closing
stop .20 mm beyond nominal leaves .10/0/−.10 mm reserve after .10/.20/.30-mm
coherent assembly error. If the stop intercepts required extension, spring load
can bypass the sleeve and **zero strand preload is permitted**. Stop adjustment
and take-up cannot be omitted. Local radius/alignment deviations add to shared
bias; the generous nominal envelope clearance does not qualify .05-mm opening.

Hole shrinkage, first layers, layer stepping, warp and guide tilt couple stop
position, sliding resistance and clearance. PLA anisotropy, interlayer weakness,
creep/fatigue alter anchors and returns; yarn finish, bending set, fraying and
spring relaxation alter both hold and reset. None has a calibrated distribution.

## Force, support, capture and the plain-clamp control

Replacing E-159's full length by this 14-mm core gives only **counterfactual force
extrapolations**. With all/half core contact, nominal downward capacities are
.547/.154 N; the strong corner gives 10.48/1.113 N. They are neither measured
forces nor rigorous bounds for this curved, discrete, unequilibrated weave.
No 1-N or 10-N support pass follows. Upward extrapolation remains below preload.

Even with perfect force transfer, the anchor needs P+F and total strand tension
at least `(P+F)/cos(theta)`. At 10 N, P=.1 N and 55°, this is **10.1 N anchor /
17.61 N total strand tension**. Equal sharing among sixteen .10-mm round strands
would require about **140 MPa axial stress**, **5.50% strain** at EA=20 N and
**1.75 MPa mean shear** over each assumed 2-mm-long bonded termination. These are
necessary demands, not allowables; load imbalance, peel, creep and damage worsen
them. A copied high exponential capacity cannot bypass this check.

Sequence must be: physically acquire stalk → prove head carries payload → open
collar → signed motion → remove opener → restore/prove sleeve support → withdraw.
At every q>0 the constructed sleeve loses core contact. Head loss then creates a
real unsupported interval, even at zero payload (inertia persists). Script checks
0/.02/1/10-N applied-force scenarios, effective mass .02 kg, and signed .1 m/s
motion; applied force and inertia are independent bounds, not inconsistent gravity
masses. It grants instant extrapolated friction only after calculated closure.
Nominal 1/10-N cases still cannot hold; favorable zero/low-load coast results are
not acceptable outage limits. Strand recoil, delayed force rise, stored head energy
and bounce can worsen them; no force-result admission relies on those coast values.

An unchanged neighbor stays separately anchored. Ideal independent rigid frames
command zero neighbor motion; shared-frame coupling is not zero: 1/10-N reaction
changes over an assumed 10^4–10^6-N/m transfer stiffness give **.001–1 mm** shift.
This is a compliance sensitivity, not a predicted disturbance. Regional isolation
requires the frame and release head to meet a physical displacement criterion.

A .30-mm side shoe plus .10-mm registration allowance around the 1.5-mm-radius
stalk fits a favorable bare-stalk envelope (1.68-mm gap to its neighbor). It still
has **no bilateral shoulder** on a smooth stalk. A friction shoe restores a returned
clamp and its proof/abort obligations. An end cup needs an undercut or closing
keeper, 40-mm acquisition reach, and a separate stationary collar opener. Passing
the radial envelope is not an accessible, grounded capture mechanism. Stop this
handover rather than grant a hidden brake or assume the drive remains supported.

For a direct returned plain jaw at mu=.2, matching the nominal .154-N extrapolation
needs .771-N normal preload. A .15-mm release stroke stores **.116 mJ** and closes
within **.679 ms** under the same 1-g/.12-N-drag bounds, before rebound. Matching
1/10-N support instead needs **5/50 N** normal preload and **.750/7.500 mJ** opening
work. The braid's low axial preload can reduce opening energy, but adds long collar
travel, directional grip and uncertain crossover return; it has not shown a complete
support advantage. E-148's finite jaw field/remanence/capture limitations and E-140's
low-load free-input/coasting failures remain unchanged.

## Different nonfluid axis and board consequences

A small constraint-inversion screen asked whether **opposed screw torques can cancel
writer load without opening support**. Two retained screw coordinates would encode
`h=a*(theta1−theta2)/2`; an indexed differential head moves them oppositely, grounded
nuts carry compression, a difference lock retains height, output readback proves it,
and failed proof must keep that lock/head supported. With lead .5 mm,
`a=lead/(2*pi)`. Load torques are ±F*a/2. Equal shaft rotations cancel input torque
but give **zero height change**; opposite rotations produce height and add work
`F*40 mm` (0/.8/40/400 mJ at F=0/.02/1/10 N). A fixed 1-N counterweight cancels
only one load; residual work spans −40…360 mJ. Release of the difference lock
restores an unsupported coordinate. Stop “free load cancellation”; genuine energy
storage or positive constraint exchange is required. This is a distinct functional
axis from friction tuning, not a novel complete machine or an E-140 repair.

No causal braid survivor earns detailed sourcing. The E-159 board ledger remains:
6,400 sleeves, upper anchors, collars, returns and guides; 12,800 sleeve-end assemblies
(**204,800 strand-end interfaces** for sixteen strands, not necessarily separate
assembly operations); H bilateral
captures plus H independent local release interfaces, retained drive/support paths,
readers, power and indexing. Nominal strand paths total about 3 km before end tails;
cutting, threading, bond consistency and service access dominate repeated work.

Retain the optimistic complete-map allocation
`T=6+ceil(6400/H)*(.12/v+.10)`, including three 40-mm strokes, capture/release/proof,
preparation/indexing, one bounded retry and settling: 26 s at H=160, v=.3 m/s;
46 s at H=80. This is an allocation, not a timing pass; new closure/capture work
must fit the .10-s allowance or increase it. Failed proof retains capture; common
reader bias survives retry. At assumed false acceptance 1e-4, expected misses are
.64/board without independence, not measured reliability.

With assumed $250 shared reserve, `6400*c_site+H*c_head<250` is necessary for <$500;
at H=160 and c_site=$.03 this leaves **<$.3625/head**, including capture and release.
The $400 band leaves $150 for both inventories; the $200 ideal already fails that
reserve. No BOM, print-time, life or purchased-cost pass is claimed.

**Decision:** retire this fixed-crossing/prescribed-shape embodiment and unsupported
head handover. Pause freely sliding braid detailing; reopen only with a materially
changed finite load path that supplies strand/crossover equilibrium, terminations,
stop take-up and capture through all cuts. A stronger spring or another mu sweep
alone does not do that. Granular reset remains paused. Next useful work is broader
nonfluid constraint/energy-path discovery, informed by the opposed-thread null mode,
not manufacturing an unearned braid cost model. No CEO-owned resource boundary arose.

Self-review: exact segment-distance examples, zero-friction/preload/contact limits,
constant-force return against closed-form kinematics, energy/heat balance and screw
virtual work pass. At 192/384/768 segments nominal stroke converges
1.838404/1.838799/1.838895 mm; .05-N-drag return is approximately
6.764/6.779/6.783 ms. Bending-energy change is much less converged
(−.079/−.794/−.997 microjoules), so no small bending-force advantage is accepted.
Peak tensile strain approaches 1.416% at 768 segments; slack remains. These checks
verify the restricted equations and geometry, not natural braid equilibrium,
material reliability or hardware performance.
