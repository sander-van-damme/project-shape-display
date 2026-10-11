---
status: complete
builds-on: [E-158, E-126, E-151, E-140, E-148, E-063, A-019]
---

# Dry confinement removes liquid sealing; distributed braid earns a finite release test

**Retain a spring-tensioned braid as a conditional mechanism lead, not a machine.**
Distributed tension can amplify end preload without a ratchet or rigid pads,
while increasing release travel; upward grip stays below preload. Stop unpreloaded
braid, assumed self-resetting granular cartridges and bulk-packing-as-40-mm-memory.
No arrest proof, fabrication, purchase or architecture selection.

Input main `bbf5c5c`. Replay: `python3 tools/curated-experiment-checks/E-159/confinement.py`
(`--all` emits braid cases). Evidence: primary-source principles, derived limiting
force/work models, finite helix kinematics and deterministic state witnesses;
self-review only. No assembled CAD, contact/DEM simulation, calibrated X1C/material
prior, physical measurement, lifetime or yield result. Except stage 02 and explicit
source statements, **all numerical values are design/uncertainty scenarios**.

## Discovery and complete causal combinations

Searches: vacuum-gripper confinement, tensile braid transfer, cable-sleeve material
memory. The third found an automatic-return counterexample. Known principles;
no patent-novelty or saturation claim.

Primary sources, accessed 2026-10-11:

- [Brown et al., 2010](https://jfi.uchicago.edu/~jaeger/group/JaegerGroupPapers/granular/PNAS_jamming_gripper_2010.pdf),
  DOI 10.1073/pnas.1003250107: vacuum-confined grains grip by friction, suction
  and interlocking. Only friction applies here; no dry source/reset prior follows.
- [Dielas, 2026, thesis abstract](https://repository.tudelft.nl/record/uuid:515b28bd-29c1-44eb-9267-e229db9270d8):
  exponential braid amplification, linear preload scaling and twelve tested
  configurations. No dimensions, coefficients or durability transferred.
- [US5505117A](https://patents.google.com/patent/US5505117A/en): shortening expands
  braid; coating deliberately increases crossover friction to retain that state.
  Sleeve elasticity is therefore not a qualified closing spring.

All combinations use 5.08-mm tops, guided stalks, ≥40-mm travel and H indexed
bilateral capture heads on a shared signed elevator. Selected heads take load
before local release; restore/prove support before withdrawal. Capture, independent
release couplings, registration and drive arrest are counted, unbuilt obligations.
Spatial access replaces local powered coils, not resident supports or selection.

| Combination | Retention and grounded reaction | Release/reset and source-loss obligation |
|---|---|---|
| Dry granular annulus around stalk | Stalk friction → confined grains → bottom seat and outer tube → frame. Axial spring platen supplies initial compression; annular walls/screens retain grains. | Head takes load, retracts platen, mechanically expands/splits enclosure if unloading does not unjam, then moves stalk. Return spring must restore packing; force history/dilation remain unknown. |
| Tensioned braid around stalk | Downward stalk friction stretches helical strands; radial contraction increases normal force. Upper braid anchor → frame; lower guided collar is pulled downward by a grounded spring. | Captured head pushes collar upward, shortening/expanding braid; then signed motion. Removing opener lets spring extend sleeve. Return resistance, contact recovery and strand strain must be bounded. No latch-open state. |
| A-019 laminar control | Moving and grounded leaves transfer shear under local retained wedge compression. | Selected head takes load before wedge release; reclamp/prove before withdrawal. Shared vacuum/global unjamming alone disturbs unchanged sites. |
| Bulk granular support, distinct counterfactual | Top rests on grains over fixed grounded floor; height stored in bulk packing. No central rigid stalk friction. | Fixed grain mass/area gives only packing-height range. Adding/removing grains restores E-126 feed transactions; changing floor height merely relocates the actuator. |

E-126 moves particle inventory; this annulus keeps it stationary. Separate anchors
and springs remove E-151's common-tie exchange at 6,400-fold replication. E-140
uses a screw, discs and ratchet; braid tension gives a different directional force
law. E-148's returned jaw remains the arrest control. Dense capture failures remain
open. Granular reset earns no DEM; conditional braid cases earn one finite release
test. Both leads have not reduced solely to earlier failures; no extra axis is
required to close this bounded screen.

## Granular reactions: wall pressure is not a supplied constant

For a radial-pressure idealization, `C=mu*p*2*pi*r*L`. With r=1.5 mm, L=10 mm,
mu=.2, 1/10-N support needs **53.05/530.52 kPa**. A rigid enclosure confines
radial expansion but does not establish p; a spring/platen, interference and
packing history must do so. A membrane under vacuum adds pneumatic infrastructure.

For a compressed annulus let S(z) be axial compression, A=pi(ro²−ri²), p=K*S/A.
During **downward stalk slip**, inner friction acts downward on grains, outer
friction upward. Assuming simultaneous mobilization gives a limiting stress field:

`dS/dz = a*S`, `a=K*(mu_i*2*pi*ri − mu_o*2*pi*ro)/A`,
`C_i = S0*(K*mu_i*2*pi*ri/A)*expm1(a*L)/a`.

At a=0 use L. Bottom seat carries S(L); outer wall carries C_o and
`S(L)−S0=C_i−C_o`. This sign matters: ordinary silo attenuation with both walls
opposing downward grain flow is **not** the force field for a descending stalk.
This calculation is not a granular constitutive model or guaranteed capacity.

At ri/ro=1.5/2.2 mm, L=10 mm, K=.5, both mu=.2: C_i=.8948*S0.
A 192-case grid varies mu_i/mu_o=.1/.3, K=.2/.8, S0=.5/2/10 N,
L=9/11 mm, ri=1.4/1.6 mm, ro=2.1/2.3 mm. Formal capacity spans
**.0570–214.19 N**. The high end is load-amplified internal stress, not demonstrated
strength: at the high-gain geometry, 1-N preload gives 21.42-N inner force and
~13.05-N bottom compression. Housing/seat strength and dilation can invalidate it.
Constant K and simultaneous friction mobilization remain unvalidated.

A 10-N/mm spring compressed .2 mm supplies 2 N; .1/.2-mm packing settlement
reduces it to 1/0 N. Retraction does not prove release; a split shell adds return,
travel, stops and reaction. Zero preload gives zero ideal force; residual compaction
or grain weight is not credited. Stop before DEM until a reversible boundary
condition exists; this rejects unsupported reset, not granular media.

For the **bulk bed**, `h=Vsolid/(phi*A)`. With assumed phi=.55….64, a 40-mm dense
bed expands only **6.545 mm**; 40-mm range requires ≥244.44-mm dense / 284.44-mm
loose depth before top travel and containment. These bounds do not prohibit a
large machine, but packing fraction is not a commanded reversible coordinate;
agitation/reset under a loaded top still needs local isolation and support.

Laminar control at 40 mm²/interface and mu=.1….3 needs **17–50 interfaces** for
10 N at 50 kPa, or **2–5** at .5 MPa. The latter requires 20-N squeeze/site.
The wedge supplies confinement; foil, overlap, return and A-019 wear remain.

## Braid force, work and correlated uncertainty

For an ideal inextensible uniform helix, theta is strand angle to the stalk axis.
Strand curvature resolves axial tensile resultant T into radial normal per length
`dN/dz=T*tan(theta)²/r`. With Coulomb contact, integrate
`|dT/dz|=mu*T*tan(theta)²/r`. Given bottom collar tension P0:

`kappa=mu*L*tan(theta)²/r`,
`C_down=P0*(exp(kappa)−1)`, `C_up=P0*(1−exp(−kappa))`.

Thus **P0=0 gives no finite grip** in this model, and upward friction stays <P0.
No load-independent self-lock theorem follows from substituting a mean tension
into a lumped feedback equation. Upper anchor carries P0+F downward; the spring's
lower frame attachment supplies the opposing P0 reaction. Net frame load is F.
Strength additionally requires total strand tension ≥(P0+F)/cos(theta); at 10 N,
P0=.1 N, theta=55°, the required total is **17.61 N**, not a yarn allowable.

For expansion from r to r+g at fixed strand length/turn count:

`release_stroke = L*[1−sqrt(1−tan(theta)²*((1+g/r)²−1))]`.

Negative radicand forbids this release; this is kinematics, not contact geometry.
At L=20 mm, r=1.5 mm, mu=.2, P0=.1 N, g=.15 mm:

| theta | Downward friction N | Upward friction N | Collar stroke mm |
|---:|---:|---:|---:|
| 30° | .1432 | .05889 | .7127 |
| 45° | 1.3392 | .09305 | 2.2236 |
| 55° | 22.9201 | .09957 | 4.8781 |

Spring-only opening work at 45° is **.2224 mJ**, after capture takes payload;
**1.423 J/board**. Strand strain, crossover slip and bending add work. Closure
returns energy into collar impact, braid strain and heat. Writer raising/lowering
supplies/absorbs F*40 mm: **256/2,560 J** at all-site 1/10 N. Bilateral heads supply
zero-payload motion; passive sleeve closure still needs its spring.

216 deterministic combinations use mu=.1/.2/.3, theta=40/45/50°,
L=19/21 mm, r=1.4/1.6 mm, P0=.05/.15 N, g=.05/.15/.30 mm.
All helix radicands are positive; **105/27** meet 1/10-N scalar hold respectively.
Counts are not yield or accepted geometry. Coherent weak/nominal/strong cases
span **.0654/1.339/89.34 N**; the highest is strength-unqualified. Friction,
angle and preload are shared batch biases, not 6,400 independent draws. Local
clearance/warp variation adds to them. A hypothetical reduction of contacting
length to half/quarter cuts nominal capacity to **.2794/.0948 N**, below 1 N.
No mapping from collar motion to contact fraction is assumed.

For a 1-g collar returning 2.2236 mm under constant .1-N spring, ideal travel time
is **6.67 ms** without drag, **9.43 ms** at .05-N drag; .12-N guide/crossover
resistance prevents return. This favorable travel model omits spring slope,
impact/rebound and contact-dependent resistance. The patent's expanded-state
retention makes that omitted resistance decision-relevant.

## State and loss witnesses: a command sequence is not support

Nine old/target pairs at seven phases (63 guards) cover parked, capture,
take/release, signed move, return, proof and withdraw. Unchanged sleeves stay closed;
failed proof retains capture. Guards do not prove support force. Loss while OPEN
requires closure dynamics or a charged independent head brake. Global opening
releases the unchanged neighbor and fails isolation.

A deliberately favorable fault witness grants full friction instantly after a
2/10/30-ms open interval. Down-positive motion with mass m and constant external
force F uses `x_gap=v0*t+F*t²/(2m)` and `v=v0+F*t/m`; after closure,
`d_stop=m*v²/[2*(C_down−F)]` if C_down>F. Upward motion uses C_up+F.
Use m=.02 kg and F=0/1/10 N as **independent applied-force scenarios**, not a
1-N gravitational payload assigned an inconsistent mass. Initial |v|=.1 m/s.

With the nominal 45° sleeve, downward loss at 1 N totals **1.479/14.113/100.974 mm**
for those delays. The last exceeds the entire 40-mm travel; no impact extrapolation
is credited. At 10 N it cannot hold after closure. Zero-force downward/upward loss
at 10 ms is **1.075/2.075 mm**; the asymmetric grip matters even without payload.
These are witnesses, not drop bounds or acceptance limits. Force rise,
static/kinetic friction and recoil remain; a stuck-open return gives no arrest.

Read actual top and unloaded support. One supported retry is allocated; persistent
slip/jam needs captured service. Assumed false acceptance 1e−4 means .64 expected
misses/board without independence. Common reader bias survives retry; no measured
rate or reliability probability is assigned.

## Board ledger, decision and next gate

The braid repeats 6,400 sleeves, 12,800 terminations, 6,400 upper anchors,
lower collars, preload/return springs and guides, plus stalks/tops. The granular
route instead repeats packs, screens, annular housings, seats, platens/returns and
release boundaries. Nominal grain annuli contain **.521 L** before packing fraction;
20-mm braids require **128 m sleeve**, or **2.90 km strand** for sixteen strands
at 45°, excluding end tails/scrap. Cutting/fraying and termination strength count.
10–30-s handling/site alone is **17.8–53.3 h**. No print time/material total without
geometry. Thin braided stock is bought or fabricated, not a qualified .2-mm PLA wall.

Optimistic full mixed-map allocation: two 40-mm signed strokes and one 40-mm
empty return per head batch, .10 s/batch for capture, local release/restore/proof,
plus 6 s/map for preparation, registration/indexing, final proof, one bounded retry
and settling. `T=6+ceil(6400/H)*(.12/v+.10)`. Acceleration, row access and proof
have no demonstrated implementation: **allocations only**.

| Heads | v=.1 m/s | v=.3 m/s |
|---:|---:|---:|
| 80 | 110 s | 46 s |
| 160 | 58 s | 26 s |
| 320 | 32 s | 16 s |

Strict <30 s needs ≥356/137 heads respectively. Local work uses fewer batches
but owes capture/proof and possibly a full stroke. Unchanged sleeves stay grounded;
frame disturbance remains unbounded. All-cell 1/10 N gives **6.4/64 kN** frame load,
comparison scenarios rather than product requirements.

With **assumed** $250 shared reserve, `6400*c_site+H*c_head<250` is necessary for
<$500 purchased total. At H=160, c_site=$.01/$.03 leaves **<$1.1625/$.3625/head**.
Free heads leave <$.03906/site; the $400 band leaves $150 for both, and this
reserve already misses the $200 ideal. Springs, braid, grains/foil, release drivers,
capture/return hardware, sensors, bearings, wiring, power and guides must be
allocated once. No sourced joint BOM or complete time/cost pass exists.

X1C housing/anchor hole bias, first layers, layer stepping, roughness, warp and
alignment alter contact. PLA anisotropy, interlayer failure, creep/fatigue affect
load paths. Yarn finish, humidity, diameter, abrasion/fraying and spring relaxation
correlate friction and return. These boxes are not fabrication distributions;
no life, actuation-tail or map-yield claim follows.

**Next:** finite braid/collar/stalk with grounded upper anchor, lower spring and
crossover/bending resistance. Test signed motion, partial-contact cuts, low payload,
correlated clearance and unchanged neighbor against an equal-capacity spring clamp.
Stop on failed return, strength or head access. Only a surviving transition earns
sourcing/contact calibration; this is more informative than fitting granular K.
No CEO resource boundary arose.

Self-review: zero-friction/preload and zero-length limits, exact helix strand-length
conservation, independent virtual-work derivative, granular reaction balance including
the zero-rate limit, segment integration convergence to braid exponential, and
braking work balance. Segment force errors halve .0494→.0251→.0127→.00637 N at
100/200/400/800 segments. These verify equations only; no independent reviewer or
physical validation is claimed. Keep source, discard reproducible JSON.
