---
status: complete
builds-on: [E-261, E-259]
---

# Resident screw rotary stability and schedule bounds

**Do not credit 2000–3000 rpm across travel yet.** The moving nut can restrain
lateral translation without fixing screw slope. At retraction, its long unloaded
overhang can limit speed even with ideal nut guidance; near extension, compression
and compliant guidance matter. Favorable stiffness/mass cases still permit high
speed, so this is not rejection of resident screws. Select a single supported
article to measure these uncertainties before adding heads or resident bearings.

Evidence: primary guidance, analytical bounds and a one-plane linear beam model;
no physical qualification, CAD, fabrication or purchase. Reproduce:
`OPENBLAS_NUM_THREADS=1 python3 tools/curated-experiment-checks/E-262/stability.py`
(Python/NumPy; `--check` for controls). JSON is reproducible and not retained.

## Guidance, spans and what the nut constrains

[Nook miniature catalog](https://www.nookindustries.com/media/2427/pmbs-miniatures-catalog.pdf),
PDF page8/printed12–13, checked2026-10-13: critical speed depends on end support,
root section and span; its recommended operating screen is80% of calculated
critical speed. Axial restraint alone is not moment fixity. Its steel constants
and ball-nut limits are not printed-polymer ratings.
[Thomson lead-screw guidance](https://www.thomsonlinear.com/downloads/screws/Lead_Screws_cten.pdf),
printed47, independently uses root diameter, bearing span and80% for alignment
and straightness allowance. Neither source qualifies our nut as a radial bearing.

Reconstruct with mass density: `ncr=60/(2π)·β²/L²·sqrt(EI/μ)`;
`I=πd_root⁴/64`, linear mass `μ=ρA_mass`. Exact uniform-beam β is1.875104 for
fixed/free, π for simple/simple,3.926602 for fixed/simple. Thus relative factors
are.3562/1/1.562, avoiding mixing the miniature catalog's1.56 with the1.47
fixed/simple factor in [Nook's other screw catalog](https://www.nookindustries.com/media/2425/nook-screw-catalog.pdf).
These are undamped bending-mode screens, not full rotor stability predictions.

Keep E-261's nut10/margins2 construction: S40/50 needs L54/64 usable thread.
Nut lower edge q=2+u, upper edge q+10. Effective point x=q+5 gives compressed
span7→47/57 mm and unloaded overhang47/57→7 mm. Actual axial/lateral contact
can lie anywhere in the10-mm nut; the edge sensitivity is retained in source.
A guide that prevents pin rotation about z does **not** necessarily restrain
screw transverse translation or bending slope. Thread clearance, pin bending,
guide clearance and plate compliance lie in series with that lateral reaction.
Two guide planes for the pin are not two bearings on the screw.

One resident radial station without nut support permits rigid screw tilt; it
is not a cantilever. A captured thrust seat must carry axial load in both drive
conditions. Moment restraint needs separated radial contacts/stiff housing.
The underside writer supplies torque; no permanent writer support is credited.
A moment-fixed nut is only a favorable control, not inferred from10-mm engagement.

## Explicit bounds and numerical results

Inherited competing E=1000/3000MPa plus **assumed** ρ=1100/1400kg/m³ are sensitivity
endpoints, not measured PLA ranges or probability priors. Historical nominal
root1.4/OD3.2mm is CAD, not the broken specimen's measured section. Root-only
stiffness with mass between root/OD cylinders brackets geometric mass **for
solid homogeneous stock of that geometry**; defects, ribs and anisotropy can
change effective stiffness beyond these scenarios. OD as a solid bending section
would exaggerate root-only EI by27.3. No printed-process capability is inferred.

Unloaded, ideally clamped base, no credited nut support; values below are **0.8ncr**:

| Travel / thread mm | E1000,ρ1400, root mass / OD mass rpm | E3000,ρ1100, root mass / OD mass rpm |
|---|---:|---:|
|40 /54|2725 /1192|5324 /2329|
|50 /64|1940 /849|3790 /1658|

The mass choice alone changes speed by2.286; increasing root stiffness while
holding mass fixed scales speed with root diameter squared. Increasing stroke
40→50 reduces this cantilever screen by29%. These values cannot be operating
limits under compression or loose seats.

The executable model assembles cubic Euler–Bernoulli stiffness, consistent mass
and conservative geometric stiffness from compression P below x; the unloaded
overhang remains in the mass/stiffness matrices. Nut-to-ground bilateral spring
kn=0/.01/.1/1/∞N/mm and base slope spring kθ=1/10/100Nmm/rad are competing
contact scenarios, **not identified stiffnesses**. Base translation is fixed.
Zero-clearance rigid support is favorable; an open clearance can have kn=0.
A0/20-g lateral lump tests whether pin/payload motion participates in the mode;
20g is an illustrative total moving load, not a measured miniature or required
per-cell payload. P=.2/.4N separates near-static20-g loading from additional
acceleration/drag; P=0 is the unloaded control. Guide drag remains unmeasured.

At root1.4/E1000/ρ1400/OD mass/P.2, minima across the sampled travel are:

| Support case | S40 /S50 minimum 0.8ncr, rpm |
|---|---:|
|Fixed base, no nut lateral support|273 /static instability|
|Simple base, ideal point nut|1436 /991|
|Fixed base, ideal point nut|1468 /1009|
|Simple base, ideal nut translation+slope|1574 /1070|
|Simple base and stationary tip, no nut support|2920 /1919|
|kθ10, kn.1, no lateral lump|859 /636|
|kθ10, kn.1,20-g lateral lump|531 /522|
|kθ10, kn1,20-g lateral lump|1128 /841|

Moving the effective nut station from its lower to upper edge changes the S50
simple-base/ideal-point/P.2 minimum from885 to1122rpm (midpoint991), all limited
near retraction. These are point-support alternatives, not a finite-contact fit.
A favorable E3000/ρ1100/root-mass case with ideal nut/P.2 gives4428rpm minimum
atS50; root2 with the adverse material/mass assumptions gives2023rpm. These
are real conditional escapes in the model, not evidence for a particular print;
a larger core changes thread depth, engagement and holding.
At kn.01/kθ1/P.2/20g, static instability appears; no positive universal speed
bound exists for unspecified support. Mesh refinement40→80 changes the checked
positive frequencies by at most1.3e−7 relative; this says nothing about model error.

The root/no-nut S50/P.2 model loses static stability at high extension: lowering
RPM cannot cure that case. A finite spring/mass case can have its lowest mode
inside travel, so checking only the endpoints is inadequate. The nut-slope-fixed
control still has a long free overhang. Extra base moment stiffness alone cannot
make that tail disappear. No favorable mode is a load-retention or thread-strength pass.

Alignment bounds are deliberately separate from material bounds. With effective
kn=.1/1N/mm, an imposed .05/.2-mm relative guide offset entails .005–.2N of
spring reaction before friction/contact redistribution. In a simple undamped
single-mode eccentric-rotor illustration, added displacement/eccentricity is
`r²/(1−r²)`:1.78 at r=.8 versus.333 at r=.5. Initial eccentricity.05/.2mm
then implies total orbit.139/.556mm at r=.8. This is **not** a prediction for
our screw; it shows why80% is not a clearance guarantee. Global plate bow,
module registration and lot stiffness are correlated errors; no independent-cell
yield or tight FDM alignment distribution is assumed.

## Gameplay consequences, with paid setup and stress separate

Reuse only E-259's36 owner-selected physical river/ravine commands, two heads,
K32 powered outputs/head,1000rev/s² and existing seek/dock/proof/return/retry/4-s
allowances. Installed channels remain128/160. Shallow deltas apply to N20/S40;
deep presets use N30/S50. No map expansion, position-dependent speed optimization,
extra head or free proof/homing is granted. Constant speed scenarios below are
conditional reruns, **not rated caps**; rounded850/1200 approximate the unloaded
cantilever screens and500 represents a softer guided/mass case.

| Grid / lead mm | rpm | Shallow / deepest max s |
|---|---:|---:|
|64 /3|500 /850 /1200|52.47/65.66;35.54/43.29;28.60/34.08|
|64 /3|2000 /3000|22.12/25.38;19.22/21.37|
|64 /2|850 /2000 /3000|47.77/59.40;27.32/32.23;22.68/25.93|
|80 /3|850 /1200 /2000 /3000|46.40/59.31;36.87/45.99;28.07/33.50;24.70/28.13|
|80 /2|850 /2000 /3000|63.34/82.72;35.27/43.45;29.07/34.47|

At64/lead3/850, cold N20/N30 preparation is42.58/58.11s and dense40/50 stress
73.64/89.17s, separately paid. At2000 they are25.98/32.58 and39.18/45.78s.
At80/lead3/850 they become71.29/100.23 and129.17/158.12s. Source retains both
leads, all speed scenarios and both grids. Slower waits miss the~30-s reference
without automatically rejecting an enjoyable product; they materially weaken
the old timing proposition. No slowdown can rescue static instability.

## Repeated burden and smallest justified article

Baseline still has4096/6400 each pins, screws, thread pairs, thrust seats,
radial locating duties and underside sockets; two shared pin guides repeat
8192/12800 apertures. All need manufacture, load retention and local repair.
A second base radial land adds4096/6400 contact/alignment duties, taking screw
radial stations to8192/12800. Monolithic split beds can avoid separate bearing
insertion, but not wear, registration, inspection or service. Catalog bearings,
individual preload and hand fitting are not selected. Just30s added fitting/site
would add34.1/53.3 maker hours; $.10/site would add$409.60/$640, both illustrative.

A stationary far-tip bearing also adds4096/6400 sites and a support route through
or around the moving hollow pin; no such route is constructed. Its numerical
control is not a buildable escape. A temporary writer pilot adds128/160 shared
support interfaces, but must provide measured restraint while driving and leave
resident static support after withdrawal; it does not fix a free upper tail.
Compare openable printed/molded beds and bored/machined shared plates before
thousands of bought bearings. These routes still owe alignment, tooling and quotes.
E-259's dated motor/driver subset plus unquoted reserve remains$984.64/$1166.40;
extra support is excluded. Preserve$500 and$1000/$1500 comparisons; none is a
complete BOM, finished price or spending approval.

**Decision: one intact full-height screw/pin in two openable shared-style pin
guides, with a removable second root radial land, is the smallest discriminating
article.** Start with S40/54-mm usable thread/86-mm pin/b40 and N20 as the simpler
comparison. A subsequent interchangeable64-mm screw/96-mm pin addresses S50;
do not silently claim50-mm capacity from the40-mm article. Minimum engagement,
cap clearance, bidirectional thrust reaction and mechanical end stops must be
verified before any powered test. Historical trial5 is not a qualified mating pair.

A separate bounded handoff may prepare that article and one optional print job;
this result creates no print files or owner request. First measure section/mass,
seated lateral/slope compliance, straightness and loaded manual travel/hold at
retracted, mid and extended positions. Only then conduct guarded speed ramps,
recording runout/contact, torque/current, reversal and stop/withdrawal. Include
physical interruption without losing support. Use measured miniature loading
separately from stress loads. Stop on binding, drift, bow/contact or loss of
engagement; do not increase speed to meet the old schedule or iterate micro-fits.
A single cell cannot qualify neighbor isolation, manufacturing yield or a bank.

Controls: analytical end modes, SI/scaling identities, rigid-tilt witness,
Euler-load bifurcation, mass/compression effects,20/40/80-element convergence,
whole-position unloaded invariance and1/2-mm position-step comparison, plus
inherited schedule anchor. Self-review only. Missing damping, gyroscopic effects,
helical stiffness, unilateral thread contact, frame modes and wear dominate the
small numerical error; calibrated support/drive measurements are the next useful
discriminator, not a precision simulation or extra-bearing campaign.
