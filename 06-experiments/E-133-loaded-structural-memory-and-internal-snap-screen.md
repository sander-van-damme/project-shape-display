---
status: complete
builds-on: [E-132, A-021, A-022, E-126, E-131]
---

# Loaded structural memory: internal stability and phase-front arrest are separate gates

**Stop the freely snapping radial-crown stack and the smooth, unarrested tape-front
embodiment.** A top clamp does not stabilize internal exchange modes in a long
series stack; a bistable tape's two end states do not establish intermediate
height memory. Fixed-radius Kresling trusses remain an unresolved comparison,
not a survivor: endpoint compatibility supplies neither a loaded barrier nor a
controlled transition. No architecture, material, printing or purchasing is selected.

Input main `023e0e9`. Reproduce with Python standard library:
`python3 tools/curated-experiment-checks/E-133/structural.py`.
Evidence: primary-source analogies, exact elastic-truss energy calculations,
finite spoke coordinates/envelope bounds, bounded sensitivity and abstract
support-state replay. No shell FEA, contact dynamics, complete CAD, calibrated
process prior, physical measurement or independent review. Large-strain outputs
are counterfactual screening values, not material predictions. JSON is reproducible
and not retained.

## Discovery and causal machines

Three materially different source-domain/kinematic searches were productive:
Braille shell inversion (curvature stores state), twist-buckled deployables
(rotation and extension coupled), and space-boom phase fronts (distributed
curvature changes the deployed length). A fourth recombination search into
foldable zipper columns returned E-126/E-131's existing assembly/arrest distinction;
do not count it as a new operating principle. Cross-checks included D-010, M-003,
A-021/A-022 and repository shell/bistable/tape/chain/interlock searches. This is
local novelty evidence, not landscape saturation.

Primary references accessed 2026-10-10 (operating analogies, no property transfer):
[Abbasi et al.](https://arxiv.org/html/2307.10933v1) combine magnetic shell actuation
and pneumatic loading for Braille; [Kidambi/Wang](https://arxiv.org/abs/2003.10411)
model geometry-sensitive axial/twist/off-axis Kresling dynamics;
[Yao et al., pp.2–3](https://ntrs.nasa.gov/api/citations/20220018348/downloads/A%20Multifunctional%20Bistable%20Ultrathin%20Composite%20Boom%20for%20In-Space%20Monitoring_AIAA%20Scitech%202023_revA.pdf)
use tailored composite curvature and stored energy for boom deployment;
[Ding/van Hecke](https://arxiv.org/abs/2204.06488) show geometry/shear-dependent
hysteron pathways. [Kim/Jung, §2.3](https://pmc.ncbi.nlm.nih.gov/articles/PMC10204548/)
still need driven friction pulleys and storage springs for a folding zipper arm.
None qualifies a 40-mm, full-pitch PLA structural memory.

| Machine | Selection, energy, memory and load path | Verification/recovery; disposition |
|---|---|---|
| Coaxial crown stack | Bank heads acquire changed tails bilaterally; displacement inverts annular crowns. Elastic wells retain height; all crowns/spacers transmit full load to base. A lumen probe could select individual stages. | Tail position and force during proof; retain head on failure. Internal snaps defeat top-only control; probe/capture unbuilt. **Stop top-only embodiment.** |
| Opposite-handed Kresling pairs | Torque head docks to local spline; alternating twist aims to cancel top rotation. Walls store extension and transfer load through rings/base. | Read height/ring twist; axial writer supports transitions. Asynchronous snaps defeat assumed cancellation. **Unresolved.** |
| Guided tape/front | Dock feed rollers at base; magazines store curved tapes that form guided compression support. Elastic curvature is proposed memory; former grounds load. | Read length/front; retain feed support on failed proof. **Smooth-front memory fails** below; brake changes mechanism. |
| Solid-stop control | Reuse E-132's nine ground-pin seats at 0/5/…/40 mm. Writer acquires/unloads, pin withdraws, writer moves, pin reseats/proofs before release. | Failed acquire retains pin; failed seat retains writer. 81 abstract endpoint traces; unchanged sites stay seated. **Control only:** E-132 dense access/capture failure remains. |

Heads still need travel, capture, drive arrest, readers and power-loss support;
none receives free mechanism credit. Unchanged sites are not deliberately actuated,
but frame deflection, vibration and probe collision remain disturbance paths.

## Exact nonplanar truss screen, not a fitted shell model

A crown has six equal axial elastic spokes between concentric rings: outer radius
2.1 mm, inner radius .7 mm, radial span r=1.4 mm, signed rise q, natural rise h.
Ideal free joints and rigid rings are favorable abstractions. Each spoke has
A=.16 mm² and E=2,000 N/mm² in the nominal **assumption**. With
L=sqrt(r²+h²), C=6EA/L, and l=sqrt(r²+q²):

```
U(q) = C/2 (l-L)²                        [N mm]
U'(q) = C q (1-L/l)                      [N]
U''(q) = C (1-L r²/l³)                   [N/mm]
V(q) = U(q) + F q                       downward dead load F
```

Both ±h are zero-load wells. The positive-height well vanishes at
l=(Lr²)^(1/3), q=sqrt(l²-r²), Fcrit=−U'(q). Solve V'=0 on each monotone
branch and subtract saddle/well potentials for the loaded barrier. A crown is
in series, so F is not divided by the number of stages. Fixed spacer length
h+.8 mm keeps nominal stage heights positive; it does not add a latch.

| h mm | Stages for unloaded ≥40 mm | Spokes/board | Shortening strain at q=0 | Fcrit N | Zero-load barrier N mm |
|---:|---:|---:|---:|---:|---:|
| .2 | 100 | 3,840,000 | 1.005% | 1.056 | .1371 |
| .4 | 50 | 1,920,000 | 3.848% | 7.965 | 2.069 |
| .8 | 25 | 960,000 | 13.176% | 51.744 | 26.872 |
| 1.2 | 17 | 652,800 | 24.074% | 131.903 | 102.593 |

Larger crowns trade repetition for gross axial strain, exceeding illustrative
repeatable strain limits .5/1/2% (**not PLA allowables**); the shallow crown exceeds
the first two. Buckling, joint bending, interlayer weakness and creep can invalidate
the axial law. Flexural shells need their own law; large forces above are no pass.

At h=.2 and F=.2 N, the barrier is .09936 N mm and loaded state separation
.39919 mm; 100 stages give 39.919 mm. At 1 N the barrier shrinks to .001611 N mm
and separation to .36607 mm: only **36.607 mm**, despite a nominal 40-mm free
stroke. Expanded-height sag relative to 100h is 6.387 mm. At 10 N the expanded
well is absent. These loads are inherited sensitivity scenarios, not new service
requirements; output weight must be included in F. More stages could restore
travel under one load but increase repetition and do not resolve instability.

**Internal-mode counterexample:** hold total stack height perfectly. Put one
crown at q=0 and the remaining n−1 at +h, a zero-load constrained equilibrium.
Perturb the first by x and every other by −x/(n−1). Total height is unchanged;
energy curvature is `U''(0)+U''(h)/(n−1)`. For the 100-stage case this is
**−13.5093 N/mm**. All four examples are negative. In fact
`U''(h)/abs(U''(0))=(r/L)(1+r/L)<2`, so any n≥3 identical crowns have this
unstable exchange direction at this configuration. An infinitely stiff top head
cannot remove it. It can support the external load while the inside snaps; this
is **not** a claim of external free fall, nor proof that every dynamic programming
path is impossible. It falsifies the proposed smooth top-only control path and
leaves internal impact/landing and reproducible stage selection unsupported.

Equal crowns give n+1 nominal heights, not 2^n: internal codes share top positions.
Height readback can miss weaker internal states. Loaded mixed-state stability,
dynamics and shell contact were not simulated and receive no pass.

## Manufacturing, geometry and model uncertainty

The 81-case deterministic grid uses E={1,2,3} GPa, square spoke width
{.3,.4,.5} mm, rise=.2+{−.1,0,.1} mm and radial span=1.4+{−.1,0,.1} mm,
coherently across a stack/batch. Fcrit spans .03066–10.103 N; 61/81 cases retain
the high well at .2 N. **This is not yield**: no calibrated distributions, fatigue,
stability or reach pass. Free 100-stage travel spans 20–60 mm. Alternating
±.1-mm rise errors cancel to 40 mm but still leave weak stages; coherent bias
does not cancel. Thickness, modulus and rise dominate thresholds. Correlated
warp can eliminate routing margin throughout a region. No IID assumption.

Spoke coordinates are generated at six azimuths and three states, with 65 samples
along each, and .2-mm capsule radius. Their exact all-state circumcylinder has
radius 2.3 mm; neighboring axes at 5.08 mm leave .48-mm envelope clearance,
including opposite states. Same-radius adjacent-stage axial gaps have at least
.4-mm surface projection margin for the shallow crown; that projection is **not**
a complete closest-contact or spacer collision check. The inner lumen radius
.5 mm admits a .3-mm-radius probe with .1-mm pose error and only .1-mm margin.
Opposing .1-mm hole shrinkage and shaft growth make that margin −.1 mm.
Two .15-mm radial growths plus .2-mm relative warp make the neighboring envelope
margin −.02 mm. Negative envelope margin is loss of a clearance guarantee,
**not a demonstrated actual solid intersection**. Rings, spacer connectors,
probe capture surfaces and drive routing remain unconstructed. This small audit
stops a nominal-clearance claim; it does not validate dense actuation.

The .4-mm spoke matches a nozzle scale, not finished accuracy. Layer quantization,
first-layer effects, shrinkage and assembly alignment enter the ±.1-mm bounds only
provisionally. Roughness/friction, joint stiffness, anisotropy, interlayer failure,
creep, wear and fatigue have no calibrated law. Shared stiffness loss reduces all
Fcrit proportionally. No service life, force-tail probability or board yield claim.

## Other families: reach is not retention

For a hexagonal fixed-radius Kresling **two-length truss**, R=2.1 mm and
α=60°. Equal natural edge lengths at two states imply
`theta1=pi−alpha−theta0` and
`H1²=H0²+2R²(cos(theta1)−cos(theta0))`. The source enumerates
H0={2,4,8,12} mm and theta0={0,15,30,45}°: 13/16 cases have a positive real
second height. Best sampled stroke is 2.33567 mm, requiring 18 stages, with
120° twist per stage. The general two-length fixed-R stroke bound is ≤2R=4.2 mm,
so even a better search needs ≥10 stages at this radius. Eighteen hexagonal units
repeat 1,382,400 axial/diagonal truss members at twelve/unit before hinges/rings.
Longer starting tubes do not automatically provide greater bistable stroke.

Endpoint identities are checked, but facets, hinges, loaded barriers, off-axis modes
and intersections are unknown. Twist cancellation needs coordinated states. The
crown law does not transfer. Wider understructure owes explicit dense routing.

For a homogeneous tape, let deployed length be x, elastic release per length g,
and downward force F. Away from ends, `V(x)=(F−g)x+constant`; the front either
moves or is neutrally balanced at F=g. There are no isolated intermediate minima.
This ideal model omits front friction/imperfections; those cannot be credited as
qualified state retention. A *changed* spatially patterned front with periodic
barrier `B/2[1−cos(2πx/s)]` needs `B>|F−g|s/π` merely to preserve wells. At
s=5 mm and g=0, 1/10 N require B>1.592/15.915 N mm, before disturbance margin.
That equation specifies a target for real geometry, not a supplied mechanism.
A .4-mm PLA strip bent to strain bounds .5/1/2% needs coil radius ≥40/20/10 mm
from t/(2R); even the favorable coil spans four pitches. Offset/tiered magazines
are possible but unbuilt; internal pitch is not itself a product requirement.

## Full board and decision

At 6,400 sites, 1 N/site through 40 mm requires 256 J ideal work. Local 1/10-N
loads are sensitivities, not simultaneous service requirements. Shallow crowns
repeat 640,000 compliant stages and are 80–120 mm deep before tails/heads/supports.
Monolithic printing might reduce assembly, but captive joints, support removal,
scrap, print time and repair remain unresolved. Even 10–30 s inspection/assembly
per whole site means 17.8–53.3 hours.

Allocate 6 s/map for registration, non-cell transport, preparation, settling,
readback and one bounded retry. Complete-cell service times .02/.1/.5/1 s then
need at least 6/27/134/267 simultaneous heads for strictly <30 s, before integer
scheduling or shared-drive conflicts. These are optimistic rate bounds, not
benchmarks. Eighty heads get <.3 s/cell; 100 separately handled crowns get
<3 ms/stage before capture/travel. Global excitation substitutes 6,400 local gates
and half-selection/common-cause accounting for serial dwell.

A $250 shared bought reserve leaves $0.02344/$0.03906 per site at $400/$500 total.
The reserve must cover motors, drives, readers, electronics, wiring, supplies,
bearings and hardware; it is an assumption, not a sourced BOM. Printed memory
avoids bought springs but not millions of cyclic strain sites. No cost pass.
False-acceptance scenarios 10⁻³/10⁻⁴/10⁻⁵ per site imply expected missed sites
6.4/.64/.064 without requiring independence; shared datum errors can corrupt banks.
Retain writer support until proof succeeds; latent internal-code ambiguity needs
another observable or constrained path. Persistent faults stop a module and lie
outside successful-map timing. No perfect readback or retry cure is assumed.

Self-review: energy derivatives checked by finite differences; independent
trapezoidal force-work integrals at 100/1,000/10,000 intervals converge from
1.365e−5 to 1.365e−9 N mm error. Zero-load wells, fold stiffness, above-fold loss,
Kresling length identities, distinct-height counting and the fixed-height exchange
curvature were checked. No time integration/FE mesh convergence applies; no solver
completion is being used as physical validation.

**Next discriminator:** change from freely snapping series stages to a spatially
confined conversion front with integral compression seats. Construct the smallest
finite pair of adjacent structural units plus a grounded conversion shoe, and ask
whether reversible extension transfers load without unlocking the unchanged
material behind the front. Compare against a smooth tape and the solid-stop
control. Derive the barrier from geometry, not an assigned sinusoid. Stop on an
unrestrained feed coordinate, unsupported transfer, neighboring-output contact or
unaffordable repeated constraints. This is a topology question, not permission
to repeat zipper inventory or another friction-head fit.

Reopen the crown stack only with internal-mode control and sufficient loaded
reach across justified process bounds, or a materially different shell law.
Reopen smooth partial deployment only with actual front pinning/ground arrest;
interlocking the deployed column alone does not satisfy it. Kresling earns further
work only through a finite loaded, supported transition that addresses hidden
modes and torque routing. Do not deepen the stopped strain/clearance embodiments
or print for missing generic material data: computation has already isolated the
more valuable topology question.
