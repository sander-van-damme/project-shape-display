---
status: complete
builds-on: [E-110, A-018, A-017]
---

# Close the material cycle before optimizing thermal release

Input main `629f70b`. **A finite sealed bath can eliminate E-110's modeled
external groove transport, but its whole-bath implementation heats about nine
times the local collar inventory. A short-stroke thermal structural strut is a
more informative next geometry investigation, conditional on a finite flexible
boundary and service creep.** Neither implementation passes a complete-machine
gate. No new material properties, physical measurements or qualified seals.

Reproduce: `python3 tools/curated-experiment-checks/E-111/material_cycle.py`;
`--all` includes all 81 deterministic strut parameter cases. These are one
strut topology, not 81 architectures. Source retains generator, units, bounds,
rejection reasons and verification; no random distributions or seed.

## Separated seals and enclosed return

Keep E-110's R=1.5, radial gap=.1, key depth=.2, width=.4, period=1 and
collar L=5.2 mm. For S=40-mm travel, the finite keyed tail must span L+S=45.2
mm. Its swept interval is L+2S=85.2 mm. With .2-mm end margins, fixed seals
can be placed **85.6 mm apart on smooth lands** without any groove crossing
either seal. Each smooth land must span at least 40.2 mm, plus the seal's
finite contact width and registration allowance. Minimum modeled tail length
is 125.6 mm before those additions. Equal-area through-rods cancel net piston
displacement. Both dynamic seals remain material/friction/wear obligations.

Exact interval integration gives 119.732–120.084 mm³ liquid over groove phase:
83.365 mm³ smooth annulus, plus all moving groove inventory and local cup
keys. The groove inventory stays inside the cartridge at every intermediate
stroke; it no longer leaves with the rod. This closes the **geometric inventory**
cycle, assuming the sealed bath is completely filled and every obstructing
volume is molten. Expansion and freeze shrinkage still require accommodation.

The modeled whole bath uses 384.27 kJ/board, or **12.809 kW averaged over 30 s**,
at E-063's generic .5 J/mm³ assumption. The 30-s denominator is a favorable
limit, not a demonstrated <30-s schedule; colder structure, cooling and repeated
cycles add burdens. This is about nine times E-110's 13.283–13.635-mm³ local
holdout. No stage-02 power ceiling permits declaring the physical family
impossible from wattage alone. Deprioritize this embodiment because its resolved
transport problem creates a much larger energy/cooling and wet-depth burden.
Reopen with demonstrated local drainage/return or another geometry reducing
heated inventory without leaving frozen material in the translating groove path.

A local drain reservoir alone does not resolve that path. E-110's frozen-solid
intersection remains if material carried beyond the heater freezes in a groove.
Perfect drainage and full entrainment remain competing unmeasured cases. A
continuously heated gutter or nonwetting drain might change this, but neither is
credited without a finite return path and a bounded retention/entrainment model.

## Enclosed short-stroke structural strut

Changed operating principle: a dry rack's sloping shoulder rests on a guided
retracting jaw. The guide transfers vertical service force to ground. The
shoulder also pushes the jaw outward; a sealed **solid phase-change strut**
between jaw and frame carries that horizontal component. For an ideal
frictionless shoulder at angle α from horizontal, `H=F tan(α)`. At F=10 N and
α=30°, H=5.774 N. The thermal material is in the service load path. At α=0 this
advantage disappears: it reduces to a supported mechanical latch needing only
a release command, already represented by A-017. Friction and ramp compliance
are not credited as extra holding capacity.

A collet first takes vertical load and unloads the shoulder. Melt the strut,
withdraw the jaw by engagement plus clearance, translate the dry rack, reseat
the jaw, restore the material and freeze. Proof unload before collet release.
A drive and return spring/cam must supply withdrawal and reservoir forces;
melting itself supplies no motion. Individual heaters need electrical isolation;
unchanged jaws remain frozen and supported. Failed freeze retains collet support;
a stuck-on heater needs a mechanical service catch. Schedule, catches, guides,
readback false acceptance and recovery have not been solved by this calculation.

Reduced capsule representation: two equal-area, variable-length liquid chambers
connected by an internal duct. Their caps attach to sealed flexible boundaries,
not a grooved sliding feedthrough. Main chamber length is `h+s−x`; reservoir
length is `h+x`, for `0≤x≤s`. Thus `V=A(2h+s)+Vduct`, independent of stroke.
Molten material transfers `A s` each withdrawal and returns on seating; there is
no modeled external export. A rigid fixed-volume capsule with no moving reservoir
**cannot** accept that displacement for incompressible liquid. A nominally empty
reservoir is not a demonstrated return mechanism.

These are exact fluid-domain volumes and rigid-cap sweeps, **not generated
flexible membrane surfaces or an accepted seal**. Bellows/diaphragm folds,
attachments, rupture, buckling, contact, fatigue and their true displaced volume
remain unresolved. The compactness screen only allocates .3 mm around each cap;
it does not pack both chambers, the rack, guides, actuator and duct at pitch.
The reservoir can be staggered in depth, but its finite route must be generated.
Frozen load transfer assumes a fully connected filled solid; voids or creep
through the duct can defeat it. The effective allowable stress below is a
whole-strut hypothesis including those effects, not a compressive material test.

## Bounded comparison and sensitivity

Generator: α=15/30/45°; effective stress σ=.25/1/5 MPa; coherent error
e=0/.05/.15 mm; added dead-volume fraction=0/.5/1. Radius is resized to
`sqrt(H/(πσ))+e` so the smallest bounded radius still meets the assumed load
cut. Stroke `s=.3+.15+e` mm; end gap h=.2 mm. Duct is .8×.2×2 mm. The same e
also closes its height. This is conservative design sizing and a correlated
corner scenario, not predicted manufacturing yield. Dead volume is a sensitivity
allowance, not a verified upper bound on membrane or expansion-reservoir volume.
18/81 cases exceed the cap-only 5.08-mm radial allocation; all are weak-stress
30°/45° cases. Other cases are merely not rejected by this necessary screen.

At α=30°, 50% added dead volume:

| Effective σ MPa | e mm | Inventory mm³ | Cap radial allocation mm | Ideal board W / 30 s |
|---|---:|---:|---:|---:|
| .25 | 0 | 29.925 | 6.023 — fails | 3192 |
| 1 | 0 | 7.841 | 3.311 | 836 |
| 1 | .05 | 8.860 | 3.411 | 945 |
| 1 | .15 | 11.163 | 3.611 | 1191 |
| 5 | 0 | 1.952 | 1.813 | 208 |
| 5 | .05 | 2.307 | 1.913 | 246 |
| 5 | .15 | 3.175 | 2.113 | 339 |

Against E-110's 14.608-mm³ middle-strength/.05-error annular grid minimum,
the middle strut has less **assumed** inventory. The stresses describe different
failure modes; no measured strength equivalence or dominance is implied. A
mechanical jaw has zero phase-change heating but retains actuation/addressing
burdens. The whole bath closes geometric transport with dynamic seals; the
strut trades those seals for two flexible moving boundaries per cell. There is
no defensible cost/reliability winner yet.

For 0.5-s liquid transfer, rectangular-duct Stokes flow gives middle/.05-error
forces of .000777/.00777/.388 N at assumed viscosities .002/.02/1 Pa·s. At
.15-mm coherent closure the .2-mm duct shrinks to .05 mm; the 1-Pa·s force rises
to **15.207 N**, before membrane, return, bends, wetting and shoulder friction.
This reverses any claim that short travel implies negligible actuation force.
The viscosity range is a scenario, not alloy/polymer data; non-Newtonian flow,
partial freezing and solid debris are outside this model. Transfer time is an
input, not a full-map timing result. The exact rectangular series corrects the
infinite parallel-plate conductance for sidewalls; reducing height has cubic
leading sensitivity. A closed duct is an explicit failure, not infinite flow.

Equal nominal volumes also do not remove manufacturing/thermal accommodation.
For cap radii r+b±d, a prescribed paired stroke s leaves mismatch
`ΔV=4π(r+b)d s`: common radius bias b alone cancels; differential mismatch d
combines with it. The middle/.05 case with d=.05 mm needs .442 mm³ compensation.
An additional **assumed ±5%** material-volume excursion adds .443 mm³. Together
these require up to .1533 mm extra reservoir travel using its smaller cap area,
if both adverse extrema coincide. This extra envelope is not included in the
nominal cap packing. A free reservoir can take unequal travel; forcing equal
travel with a rigid linkage instead creates pressure/void risk. Accommodation
on both sides of the cycle is required; the sign of expansion is not assumed.

All scenarios can apply to every cell in a print/material batch. The computation
does not multiply independent success probabilities. Thermal expansion,
solidification density change, creep, wetting, gas voids and membrane life need
material-specific evidence. X1C dimensional spread, layer/warp effects and
anisotropy are not represented by a calibrated distribution; no FDM thin-membrane
claim is made.

## Full-board decision and next discriminator

The strut repeats at least **12,800 flexible boundaries**, 6,400 liquid return
paths/charges, heaters, isolated switches and jaw/guide interfaces, before collets,
sensors, service catches and shared motion. With an illustrative $250 shared
reserve, the remaining <$500 bought budget is <$0.0391/site; if the two boundaries
alone consumed it, each would need to cost <$0.0196. This is a budget division,
not a quote or a rejection of integrated sheet manufacture. Lamination/sealing,
fill/degas, inspection, cartridge repair and thermal isolation are major burdens.
Do not call reduced heating an affordability result.

Continue the existing A-018 campaign with a **finite sealed strut boundary,
reservoir return and jaw packing gate**, alongside a simple mechanical-jaw
comparator. It must close the .15-mm-scale mismatch/expansion allowance without
reintroducing 40-mm wet motion, preserve the solid service load path, and show
an affordable repeated boundary process. Stop this strut implementation if no
such geometry survives; do not substitute a command-only thermal latch and call
it a new architecture. Only then is a transient thermal discriminator informative.
No print or purchase is justified by this inventory screen.

## Verification and evidence limits

Independent midpoint integration at 10k/100k/1M slices on three off-grid finite
bath holdouts has maximum errors .013411/.002056/.000376 mm³. All checked
translations preserve exact inventory; seal-clearance inequalities cover the
entire swept interval. Capsule checks conserve volume over 101 stroke states;
analytical identities cover the intervening continuum. Mismatched areas and
blocked ducts are fault cases. Checks include linear pressure scaling in flow
and viscosity, the independent parallel-plate pressure bound and α=0's
command-latch limit. No membrane/contact solver, thermal model or independent
review ran. Self-review validates the stated reduced calculations, not hardware.
