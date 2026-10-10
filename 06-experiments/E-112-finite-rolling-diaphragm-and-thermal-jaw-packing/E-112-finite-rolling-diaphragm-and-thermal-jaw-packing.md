---
status: complete
builds-on: [E-111, A-018]
---

# Finite strut boundaries change return travel and packing

Input main `138b41d`. **A rolling boundary removes the assumed flat membrane's
meridional stretch, but adds fluid displacement, circumferential deformation
and reservoir travel. The prescribed geometry fits only part of the bounded
population; it is not yet a pressure-stable or manufacturable capsule.** No
material properties, calibrated manufacturing distribution or physical result
are introduced. Keep the simple dry mechanical jaw as comparator; do not start
thermal optimization on the strength of these kinematic survivors.

Reproduce: `python3 tools/curated-experiment-checks/E-112/boundary.py`.
`--all` prints all 486 deterministic cases and rejection reasons. They vary
parameters within one circular rolling-fold topology, not 486 architectures.
The taut flat annular membrane is a separate analytical comparator.

## Generated boundary and exact displacement

Revolve a liquid-facing U-shaped meridian about the capsule axis. Inner radius
is a, outer radius b=a+2ρ; q is moving-cap position, the outer clamp is at zero.
For total stroke S, allocate straight-leg length `L=S/2+2m`, m=.1 mm. The fold
center moves as `zc=(q−L)/2`; its semicircle is
`r=a+ρ−ρ cos θ`, `z=zc−ρ sin θ`, 0≤θ≤π. Inner and outer straight legs complete
the surface. Both retain at least m length through −S/2≤q≤S/2. The deepest
point is `−(S/2+m+ρ)`. A rigid base adds clearance c=.1+e mm below that point.
A parallel dry face at thickness t reduces the fold radius to ρ−t; ρ≤t is an
offset cusp, and `2ρ−2t−2e≤0` is a conservative closed-gap scenario including
relative lateral error. Caps, .3-mm wall/flange allocation and .2-mm piston
plate are included in envelopes; attachment fillets and seals are not designed.

The enclosed liquid volume, with B=S/2+m+ρ+c, is exactly

`V(q)=πb²B + πa²q + π(b²−a²)zc − π²(a+ρ)ρ²`.

Thus `dV/dq=Aeff=π(a²+b²)/2`, **not πa²**. Fold motion displaces fluid as well
as the cap. A second chamber at opposite q closes inventory for identical
geometry; unequal chambers need unequal travel. The main and reservoir capsules
sit at different vertical levels with an assumed .8×.2×2-mm connecting duct.
That route's volume is retained from E-111; its bend, thermal path and finite
connections remain ungenerated, so this is not complete cartridge packing.

[The Bellofram design manual](https://damapi.marshbellofram.com/uploads/Bellofram_Diaphragm_Design_Manual_2022_7a922642c3.pdf)
(p. 3, accessed 2026-10-10) specifies effective area at the diameter midway
between piston and bore. Our prescribed circular/inextensible-meridian surface
instead exceeds `π(a+ρ)²` by `πρ²`. This is a retained model discrepancy, not a
correction to the manufacturer's hardware formula. It is 6.15% in the smaller
holdout and 1.65% in the middle-strength holdout. Neither formula supplies
pressure equilibrium for our generated wall. Displacement exceeds the piston-area
estimate by 31–73% in the two .05-mm-error main-chamber holdouts below.

## Volume accommodation and coherent errors

Scenario force: 10 N on a 30° rack shoulder, giving H=5.774 N lateral strut
load. Nominal core radius `a=sqrt(H/(πσ))+e` preserves the assumed effective
solid-stress cut at the smaller radius. σ=1/5 MPa is a whole-strut hypothesis,
not a film, PLA or alloy strength. Withdrawal `s=.45+e` mm includes .3-mm
engagement and .15-mm clearance. Opposite radius errors make the main chamber
a+e and reservoir a−e. This is an explicit adverse differential corner;
no independent-cell yield is inferred. Full errors can repeat across a batch.

Reservoir range must accept both signs of assumed volume excursion η=0/.05/.1:

`Sr=(Am/Ar)s + 2ηVtotal/Ar`.

Vtotal is the sum of the finite chambers and duct, and increases with Sr.
The script solves this feedback, rather than appending E-111's .1533-mm allowance
to a changed geometry. It verifies volume closure at each main-cap endpoint and
both excursion signs. The reservoir must move freely: rigidly imposing equal
stroke overconstrains this system. A return/preload device must maintain suitable
pressure through filling, freezing and withdrawal; none is credited here.

For ρ=.2, t=.05, η=.05 and the one-sided 1-mm rack layout:

| σ MPa | e mm | s / Sr mm | Liquid mm³ | Side-bay margin mm | Hoop excursion |
|---|---|---|---|---|---|
| 5 | 0 | .450 / .586 | 2.946 | +.404 | 40.6% |
| 5 | .05 | .500 / .805 | 3.924 | +.135 | 53.6% |
| 5 | .15 | .600 / 1.398 | 6.489 | −.558 | 66.0% |
| 1 | .05 | .500 / .727 | 12.462 | +.213 | 22.6% |

The 1-MPa/.05 case exceeds E-111's 8.860-mm³ reduced estimate; the former
50% dead-volume allowance is not an upper bound. Under the inherited generic
.5 J/mm³ assumption, the 5-MPa/.05 and 1-MPa/.05 cases demand respectively
419 and 1,329 W averaged over 30 s before losses and cold-structure heating.
This is not a <30-s schedule or a product power-limit failure.

## Deformation and dry-jaw comparison

Material coordinate u runs along the conserved-length meridian. As the cap
moves, a given u migrates between the inner leg, curved fold and outer leg.
Its circumference changes with r(u,q). Report maximum
`r(u,−S/2)/r(u,+S/2)−1` across that same material, rather than calling the fold
strain-free. This is a cycle excursion, not strain relative to an established
stress-free manufactured shape. Constant-thickness surfaces are geometric
scaffolds: a nearly incompressible film would also change thickness as it
stretches. No hyperelasticity, wrinkling, volume-conserving solid-wall mechanics,
pressure equilibrium, fatigue or snap-through model has been solved.

A taut flat annulus across the same radial width 2ρ needs at least
`sqrt(1+(Sr/(4ρ))²)−1` meridional extension when moving from flat neutral to
an extreme. The three 5-MPa rows require 23.9%, 41.9%, 101.4%. Preformed slack
can alter this requirement but introduces another folding geometry. A rolling
fold trades this stretch for hoop excursion and bending; t/(2ρ)=12.5% is only
an unqualified bending-strain scale for these holdouts.

The same manufacturer manual (pp. 24–25) discusses circumferential change,
wrinkling, alignment and maintaining differential pressure to conform to
supporting hardware. These are reasons to demand a supported-pressure model,
not transferred life/strength claims at our scale or in molten material.
The generated free fold and clearance do not implement those backing surfaces.

For the dry jaw, generate equal 30° rack-underface and jaw-top line segments
with .3-mm engagement. A collet first raises the rack .1 mm; the gap throughout
outward jaw motion is `.1+dx tan(30°)`. At full withdrawal its tip clears the
rack by at least .15 mm, so the dry rack can translate 40 mm without crossing
this jaw. Reverse the sequence to engage and freeze while collet-supported;
proof-unload only afterward. At service, the frozen core lies continuously
between the piston and fixed base; it carries lateral H, while a grounded jaw
guide must carry vertical force. The guide, tooth contact pressure, collet,
preload drive, service catch and proof sensor are still obligations. This
section check establishes geometric separation, not their load qualification.

Place the capsule alongside a centered rack of width w=1/1.5/2 mm, .15 mm
from its edge. Require transverse diameter `2(a+e+2ρ+.3)≤5.08` and
`w/2+.15+max(s,Sr)+.1+ρ+c+.5≤5.08/2` along the capsule axis. This is a specific
one-sided placement; relocation below the rack changes the routing question.
For the 5-MPa/.05 holdout, increasing w from 1 to 2 mm creates .365-mm overrun.
A mechanical jaw replaces the thermal capsule with a positive stop and release
actuator: it has no two-film return cycle or melt heat, but its addressing,
load transfer and reset must still be implemented. No affordability winner is
established by comparing these envelopes.

## Disposition and verification

Grid: σ=1/5 MPa; e=0/.05/.15 mm; ρ=.1/.2/.3 mm;
t=.025/.05/.1 mm; w=1/1.5/2 mm; η=0/.05/.1. Of 486 cases, 149 are not rejected
by these necessary geometry cuts: 104 at e=0, 45 at .05, **none at .15**.
Overlapping failures: 300 side-bay overruns, 144 closed gaps, 54 offset cusps,
27 transverse-pitch violations. These are bounded scenarios, not probabilities.
Smallest inventory is 1.948 mm³, but assumes zero dimensional/volume excursion;
do not promote it as the nominal design. Assembly misalignment, clamp thickness,
thermal warp and coating/film variation can further reduce the window.

Retain the finite geometry source; retire E-111's cap-only estimate as a packing
or accommodation claim. **Do not print or scale the free circular-U capsule.**
The next discriminating gate is a pressure-stable, guided containment and
return mechanism with a plausible repeated fabrication process, against the
mechanical jaw. A thin FDM film is not assumed: 25–100 μm film would be a bought
or separately formed part, repeated at least 12,800 times, plus 6,400 sealed
charges, ducts, heaters and connections. The earlier <$0.0196/boundary residual
budget remains an unsourced obligation. Stop this embodiment if supported film
and compatible sealing cannot credibly fit that repeated process; revisit
containment topology or park the strut rather than doing thermal tuning first.

Self-review: independent signed-frustum volume integration at 32/128/512 fold
segments gives maximum errors .0012261/.00007667/.00000479 mm³ on off-grid
holdouts. 101-state sweeps check leg lengths, base clearance and dry-jaw
separation; analytical monotonic bounds cover intervening states. Checks include
opposed-chamber conservation, a closed-form reservoir-travel holdout,
mismatch/expansion extremes, zero-excursion and zero-stroke limits, cusp/closed-gap faults and hoop-coordinate refinement
(500/2000/8000 samples, <2.4e−6 excursion change). No contact/material solver,
thermal qualification, independent review or physical measurement occurred.
