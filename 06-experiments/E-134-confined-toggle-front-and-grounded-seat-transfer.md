---
status: complete
builds-on: [E-133, E-130, E-131, E-126, A-021]
---

# Confined toggles retain endpoints but leave a free conversion coordinate

**Stop the tested circular-shoe conversion front.** Integral stops give the rigid
toggle real, load-derived endpoint barriers, and one stage can change without
releasing the next stage's stop. Confining the active knee to a grounded circular
track nevertheless leaves a driven degree of freedom. Neither the track nor the
stops arrest it during conversion. The proposed transverse drive arm also intersects
an unchanged neighboring guide. These are distinct failures; neither is repaired
by making the deployed links stiffer. No machine or fabrication is selected.

Input main `8884b78`. Reproduce with standard-library Python:
`python3 tools/curated-experiment-checks/E-134/front.py`.
Evidence: constructed rigid-link coordinates, finite circular stop contacts,
slot/arm/guide geometry, exact potential and force balance, deterministic bounds.
No full assembly CAD, dynamics, contact-stress solution, process calibration,
physical measurement or independent review. Reproducible JSON is not retained.

## Changed mechanism and finite construction

This is a **recombination within A-021**, not a new toggle principle. It changes
A-021's synchronized whole-stack width drive into a single-stage conversion front;
only that stage contributes its lifting reaction. It replaces E-133's strained
crowns with rigid links and integral unilateral stops. This justifies the bounded
probe, not renewed optimization of deep planar stacks. No literature/property
transfer is needed for the geometric counterexample; all dimensions and loads
below are explicit engineering assumptions.

Two serial units have equal link length l=2 mm. For angle phi, generate the actual
bottom, knee and top coordinates in the x,z plane:

```
B=(0,z0); K=(l sin(phi), z0+l cos(phi)); T=(0,z0+2l cos(phi))
phiH=−asin(.5/2); phiL=asin(1.7/2); H(phi)=2l cos(phi)
```

The second unit's B coincides with the first's T; its internal angle remains at
one endpoint while the lower unit converts in either direction. Boundary rings
have ideal vertical guidance. The base is grounded; upper rings return force
through the lower links, **not independent fictitious ground anchors**. Bars have
.2-mm capsule radii in separate y=0/.8-mm planes, with transverse hinge pins.
These favorable pin/guide abstractions remain unqualified in strength and fit.

A circular lug of radius a=.15 mm is integral to each lower link, center
`p(phi)=r(sin(phi),cos(phi))`, r=.65 mm, relative to B. Two equal circular seat tips
are integral to the corresponding foot, centered at p(phiH−delta) and
p(phiL+delta), where `delta=2 asin(a/r)`. Lug and tips occupy y=[−1,−.6] mm,
separate from the bars. Their exact gap is `|p−seat|−2a`: zero at the corresponding
endpoint and positive through the interior. Actual normals, not Boolean latch
states, furnish the stop reactions. Foot webs, guide bearings and hinge strength
are granted favorable load paths; their absence cannot cure the failure below.

The lower foot's grounded conversion shoe has a circular knee-pin slot: center B,
pin-center radius l, radial walls l±.3 mm, .2-mm-radius pin, nominal .1-mm radial
clearance. The shoe confines an arc; it does not clamp its phase. Nominally the
lower link centers the pin without wall contact. Even granting wall contact, its
radial reaction does zero work along the tangent. A bilateral tangential drive
must provide motion and recovery; freezing it after input loss is forbidden.
Only the lower front is constructed. Moving the shoe to higher stages, clearing
rings, capture, drive bearings and selection are unresolved, not free mechanisms.

A causal display would select one column with a reusable indexed shoe, convert its
units successively, retain height on their stops, and return load through the
stack to the frame. Top height plus front/stop readback and a proof unload must
precede release. A failed conversion needs retained drive support or an explicit
catch. Neither the readback implementation nor that recovery arrest is supplied.

## Real endpoint barriers; no intermediate arrest

For total downward load F>0 and rigid links, `V=F H(phi)`; no sinusoidal well,
elastic spring or return force is assigned. The constrained endpoint minima are
separated by the maximum at phi=0. At F=1 N:

| Quantity | High endpoint | Low endpoint |
|---|---:|---:|
| Height, mm | 3.872983 | 2.107131 |
| Barrier to dead center, N mm | .127017 | 1.892869 |
| Circular-seat normal, N | 1.581139 | 5.375872 |

The reaction follows `N n·p'(phi)=F H'(phi)`, with n the actual contact normal.
Both reactions are compressive. Loads .2/1/10 N scale barriers and forces linearly;
they are sensitivity scenarios including output weight/bias, not service requirements.
At zero total load the barrier vanishes; upward load destabilizes these endpoints.
No unbuilt down-bias spring is credited. At 10 N the low stop carries 53.76 N on
a tiny unqualified contact, so static equilibrium is not strength acceptance.

Extension goes low→dead center→high, lifting 1.892869 mm before settling .127017 mm.
Retraction first lifts .127017 mm, then lowers 1.892869 mm. Thus neither direction
can be treated as an unloaded reset. Tangential drive magnitude is `2F|sin(phi)|`,
at most 1.7F over this arc: local actuation avoids A-021's sum of synchronized
stage reactions and has no dead-center force singularity in this coordinate.
The low-link near-horizontal limit remains singular for axial force as phi→pi/2;
this construction never reaches it.

**Input-loss witness:** phi=asin(.8/2)=.411517 rad. Both seat gaps are positive,
.396004/.362908 mm. The upper link applies `(F tan(phi),−F)` to the knee.
Dotting with the unit tangent `(cos(phi),−sin(phi))` leaves **.8F**; lower-link
and shoe radial reactions cannot balance it. Loss of input at rest therefore
admits motion toward the low stop, with **1.558930 mm available height loss**.
The same pose occurs in both loaded extension and retraction. At dead center the
first derivative vanishes but curvature is −4F N mm/rad²: unstable, not a hold.

This is a frictionless rigid-model counterexample, **not proof of failure at every
possible friction/preload**. No friction material, interference fit or dissipative
arrest was specified. Adding them changes the retention mechanism and requires
kinetic evidence, as E-131/E-132 show. With other stages kept seated, the active
stage has bounded kinematic rollback, improving on unlimited feed. This is not a
dynamic guarantee that impact leaves those stages seated. Impact survival, settling,
accurate recovery and retention at an interrupted pose remain unestablished.
No allowable-drop requirement is invented. The .127017-N-mm high barrier equals
.05-kg effective moving mass at .07128 m/s at 1 N; this is an energy sensitivity,
not a predicted impact or escape speed for an unbuilt drive.

The pair has one remaining active angle after fixing the other angle and enforcing
ring continuity. Its upper stage stays seated throughout; material behind the
front need not unlock. That is useful discrimination from E-133 internal exchange,
but **spatial confinement has not removed the active input coordinate**.

## Geometry, coherent errors and board consequences

At 64/256/1024 intervals in each direction and both upper endpoint states, the
model checks 260/1,028/4,100 pair poses. Link lengths, shared-ring position and
slot clearances hold; stop gaps never become negative. Angular distance to each
seat also bounds the continuous interior. These checks do not cover every hinge,
ring, web or self-contact in a manufactured assembly.

Body x envelope [−.7,1.9] mm leaves 2.48 mm between same-orientation copies at
5.08-mm x pitch. This limited clearance is not a dense routing pass. The proposed
shoe arm is x=[q−.3,q+.3], y=[1,8], z=[k−.2,k+.2], where q=l sin(phi), k=l cos(phi).
Each unchanged site has a guide mast x=[−.35,.35], local y=[−2,−1.6], z=[0,110].
At phi=0 the arm **intersects the y=5.08-mm neighbor's mast by .096 mm³**. This
exact solid intersection is independent of the neighbor's height. A guide-fixed
neighbor is still an obstacle. Tiers, a different arm or local drives would be
changed constructions, not implied repairs. Assumed 4.8-mm tops leave .28-mm gaps.

The 81 deterministic cases combine link length {1.95,2,2.05} mm, coherent stop-angle
bias {−.05,0,.05} rad, r={.60,.65,.70} and a={.125,.15,.175} mm. Nominal angular
stops are retained before adding bias; dimensions vary independently across these
scenarios but coherently across all units within one scenario. These are **bounds,
not X1C priors or probabilities**. Stage travel spans 1.505144–2.033143 mm;
23-stage travel is **34.618–46.762 mm**, so nominal 40-mm reach is not robust.
The worst box needs 27 stages. High-state barrier at 1 N spans .079831–.186382 N mm;
maximum endpoint normal spans 4.658–6.253 N. Common bias accumulates rather than
averaging away. At only .05-mm adverse wall, pin and pose errors the slot's .1-mm
margin becomes −.05 mm; this is a clearance bound, not a printed-interference test.

Layer quantization, hole shrinkage, first layers, warp and assembly registration
are only loosely represented by those boxes. Contact compliance, guide friction,
roughness, anisotropy, interlayer strength, creep, wear, fatigue and impact damping
remain model uncertainty. Tiny pads/bars are experimental at the .4/.2-mm nozzle
process; resolution does not qualify them. No yield, life or force percentile.

Nominally **23 stages** give 40.61461-mm travel and stack heights 48.464–89.079 mm,
before base/top hardware. Across 6,400 cells: 294,400 links, 300,800 unique pin axes
(sharing adjacent boundary pins) and 294,400 stop interfaces, plus guides, feet and front hardware.
Monolithic flexures change the rigid-joint model. At a $250 shared bought reserve,
a $500 ceiling allows only **$.000831 per bought pin axis** if every remaining dollar
goes there; printed joints still cost assembly, wear and repair. The reserve must
also cover drives, readers, electronics, wiring, power and bought hardware; it is
an allocation, not a sourced BOM. Even granting free cells, no cost pass follows.

Assume 6 s/map for preparation, registration, non-cell transport, final verification,
settling and bounded retry; .05 s/cell capture/proof; per-stage service includes
conversion, reposition and local settling. For all cells changing all 23 stages:

| Stage service assumption | Complete map with 80 heads | Minimum heads for <30 s |
|---:|---:|---:|
| 5 ms | 19.2 s | 45 |
| 20 ms | 46.8 s | 137 |
| 50 ms | 102.0 s | 337 |

Integer batching is included; shared-drive conflicts and actual front access are
not solved. At $500/$250 reserve the corresponding optimistic per-head allowances
are $5.556/$1.825/$.742 with free local parts. Worst-box 27 stages worsens timing.
All-raising 1-N/40-mm field work is at least 256 J. Local changes can leave other
stops engaged only if routing clears and frame disturbance is bounded; neither is
qualified. Height alone cannot distinguish which equal stages are high. Assumed
false acceptance 10⁻³/10⁻⁴/10⁻⁵ per site implies 6.4/.64/.064 expected misses without
independence; common guide/readback bias can affect whole banks. Proof and one retry
are obligations, not perfect sensing. Persistent faults stop the module.

## Comparison, decision and next discriminator

- Smooth tape/front E-133: translationally invariant `V=(F−g)x`, no isolated
  intermediate minimum; matching release energy g to F gives neutral balance.
- Confined rigid toggles: genuine endpoint minima and no need to release the next
  stage, but a free active angle, dense drive collision and heavy repetition.
- Solid-stop E-132: an independent writer takes load before the pin withdraws and
  returns it before release. Its dense capture failure remains; no new fit pass.
- E-126 chains/E-131 bands: assembled compression stiffness does not arrest feed.
  E-130 pockets: ground seats hold endpoints, moving carrier needs restraint.
  The confined shoe reproduces that **transition-arrest obligation**, despite a
  useful endpoint barrier and bounded one-stage rollback. No chain novelty claimed.

Stop toggle/front detailing and do not print. Reopen only with a changed geometry
that constrains the moving coordinate after input loss, checks impact/recovery
where relevant, routes past unchanged guides and preserves loaded travel under
coherent bounds. More nominal barrier, a frozen cam angle, or a friction assumption
alone is insufficient. A-021 and E-133 are not reopened as complete architectures.

**Change functional axis next: shared energy delivery and local addressing**, while
holding a simple positive service stop as an explicit control. Investigate whether
spatially localized waves/resonant command receivers can replace traveling capture
heads without moving unchanged supports. Compare frequency addressing, crossed
spatial excitation and conventional positive mechanical coincidence; first bound
manufacturing detuning, bank coupling, half-selection, arbitrary-map preparation
and force/energy needed only to switch an unloaded command. Compare A-001/A-016
and E-074–083 before crediting novelty. A resonance name is not a gate or load path.
Stop an axis if it merely adds per-cell actuators, needs implausible selectivity,
or returns an already tested threshold ratchet without a changed isolation mechanism.
This is the next bounded exploration question, not a selected acoustic architecture.

Self-review: actual contact-normal torque balance, independent knee-force projection,
zero-load/dead-center limits, reversed paths, exact arm/guide overlap, coherent corners
and integer scheduling. Trapezoidal force-work error falls
5.7824e−5→3.6140e−6→2.2587e−7 N mm with 4× refinement; height finite differences agree
with force. These verify the reduced model, not dynamics or manufactured support.
