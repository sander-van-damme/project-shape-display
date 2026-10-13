---
status: complete
builds-on: [E-261, E-259]
---

# Resident screw rotary stability and schedule bounds

**Do not credit2000–3000rpm across travel yet.** The moving nut's support and
unloaded overhang matter. Favorable scenarios permit speed, but no hardware
qualification, CAD or purchase follows. Reproduce the linear beam/schedule model:
`OPENBLAS_NUM_THREADS=1 python3 tools/curated-experiment-checks/E-262/stability.py`
(Python/NumPy; `--check` for controls). JSON is disposable.

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

One resident radial station without nut support allows rigid tilt, not cantilever
fixity. Captured thrust must react both drive directions; slope restraint needs
separated radial contacts/stiff housing. No permanent writer or nut-moment
restraint is credited; nut-moment fixity is only a favorable control.

## Explicit bounds and numerical results

Assumed E1000/3000MPa andρ1100/1400kg/m³ are competing endpoints, not PLA priors.
Historical root1.4/OD3.2 is CAD, not the broken specimen's measured section.
Root-only stiffness with root/OD cylinder mass brackets that homogeneous geometry;
ribs, defects and anisotropy may change EI beyond it. Solid OD stiffness would
exaggerate root-only EI by27.3. No process capability is inferred.

Unloaded, ideally clamped base, no credited nut support; values below are **0.8ncr**:

| Travel / thread mm | E1000,ρ1400, root mass / OD mass rpm | E3000,ρ1100, root mass / OD mass rpm |
|---|---:|---:|
|40 /54|2725 /1192|5324 /2329|
|50 /64|1940 /849|3790 /1658|

The mass choice alone changes speed by2.286; increasing root stiffness while
holding mass fixed scales speed with root diameter squared. Increasing stroke
40→50 reduces this cantilever screen by29%. These values cannot be operating
limits under compression or loose seats.

Cubic Euler–Bernoulli stiffness, consistent mass and conservative geometric
stiffness apply compression P below the nut and retain the unloaded overhang.
Nut spring kn=0/.01/.1/1/∞N/mm and base slope spring kθ=1/10/100Nmm/rad are
unidentified competing scenarios; base translation is fixed. Clearance can make
kn zero. A0/20-g lateral lump tests pin/payload participation, not measured or
required miniature load. P0/.2/.4N separates unloaded, near-static20g and added
acceleration/drag scenarios. Guide drag is unmeasured.

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
AtS50, favorable E3000/ρ1100/root-mass/ideal-nut/P.2 gives4428rpm; root2 under
adverse material/mass assumptions gives2023rpm. These conditional escapes
change section/engagement/holding; neither is print evidence.
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
Shared printed/molded/machined beds still owe alignment, tooling and quotes.
E-259's dated motor/driver subset plus unquoted reserve remains$984.64/$1166.40;
extra support is excluded. Preserve$500 and$1000/$1500 comparisons; none is a
complete BOM, finished price or spending approval.

**Decision:** E-263 now implements the optional S40/54-thread/86-pin/b40/N20
manual article with two openable guides and removable second root land. S50
needs separate64-thread/96-pin qualification. Measure section/mass, seated
compliance, straightness and manual travel/hold before guarded speed testing.
E-263 carries the support, stops and protocol; no hardware result is inferred.
Stop on binding, drift, contact or reduced engagement. One cell cannot qualify
neighbors, production yield or a bank. No extra-bearing/fit campaign is selected.

Controls: analytical end modes, SI/scaling identities, rigid-tilt witness,
Euler-load bifurcation, mass/compression effects,20/40/80-element convergence,
whole-position unloaded invariance and1/2-mm position-step comparison, plus
inherited schedule anchor. Self-review only. Missing damping, gyroscopic effects,
helical stiffness, unilateral thread contact, frame modes and wear dominate the
small numerical error; calibrated support/drive measurements are the next useful
discriminator, not a precision simulation or extra-bearing campaign.


## Section alternatives: support can erase a stiffer shaft's advantage

**Retain wider polymer stock conditionally; park the thin-shell metal core before
CAD.** Neither earns2000rpm or another print. E-263's optional manual article
remains the support/holding discriminator, without a deadline or research block.
Reproduce `OPENBLAS_NUM_THREADS=1 python3 tools/curated-experiment-checks/E-262/sections.py`
(`--check` for controls). This extends the same model at1-mm travel sampling,
P.2N, polymer E1000/ρ1400; these are scenarios, not process priors.

Wider OD4.4/root2.6 retains.9-mm thread depth/lead3 but needs a5.6-mm pin at6.35
pitch. It cannot fit5.08 pitch. Root EI grows11.90×, OD-cylinder mass1.89×,
unloaded speed about2.51×. With.15-mm radial cutter relief, nut wall is.45 mm.
These are section allocations, not mating CAD or transferred holding evidence.

Metal control:1-mm core in1.2-mm bore through root1.4. [Outokumpu's steel EPD](https://www.outokumpu.com/-/media/files/sustainability/epd-cold-rolled-austenitic.pdf?modified=20241112103155&revision=c2c8d414-293e-41b4-a5ac-2fb17396483e),
p7, checked2026-10-13, gives200GPa/7900kg/m³ for austenitic sheet; transfer to wire
is a material analogy, not a supplier rating. Use
`EI=Ep*(Iroot−Ibore)+η*Es*Icore`, `μ=ρp*(AOD−Abore)+ρs*Acore`.
η1 grants full bending transfer; η0 credits none but retains metal mass. These
are model-credit contrasts, not bounds on debond/jam/separation. Adhesive and
end-transfer geometry are absent. Axial/rotary transfer and straightness are unbuilt.

| S50 section | Ideal point nut | kθ10,kn.1,20-g lump | kθ10,kn1,20-g lump |
|---|---:|---:|---:|
|Historical|991|522|841|
|Wider polymer|2487|514|1021|
|Core, full credit|6050|532|1178|
|Core, no credit|566|399|525|

Entries are minimum0.8ncr rpm, **not operating limits**. S40 ideal-nut values
are1436/3604/8767 for historical/wider/full-core; soft-support values531/533/536.
Added mass can lower the mode despite higher EI. Fixed P/lateral mass isolate
section effects; actual changed pin mass and distributed screw weight need updating.

Independent rigid-tilt Rayleigh trial `w(z)=zθ` gives generalized stiffness
`kθ+kn*x²−P*x`, mass `μ*L³/3+m*x²` in SI. Its frequency is an **upper bound**
on the first mode, not a safe lower bound. S50 minima after the.8 multiplier are
535/520/532rpm for historical/wider/full-core with soft support: unlimited shaft
EI cannot remove that support mode. Each finite-EI minimum is checked below it.

Wider stock adds no parts but consumes lateral room: E-261's.24-clearance/b40
scenario gives guide-only neighbor gap.030/−.084mm atS40/S50, before axis error.
Negative means conflicting permitted envelopes, not proven assembled collision;
nut stiffness could constrain them. No fine guide-fit rescue is selected.
The core adds4096/6400 inserts/interfaces and leaves only.10-mm radial polymer
ligament, unqualified against the.4-mm nozzle. Insert molding/casting still owes
location, transfer, tooling, release and inspection; no economical route is proven.

AtS50,64-mm cores total262.144/409.600m and1.627/2.541kg steel; modeled net added
mass1.211/1.893kg. Wider screws add2.629/4.107kg in the **OD-mass scenario**, not
actual helical mass;96-mm/.44-wall wider pins add.830/1.298L excluding caps/nuts.
The80-grid wider figures count replication only, not feasible5.08-mm packing.
An extra10s/site adds11.38/17.78hours;30s adds34.13/53.33. $.05/site adds$204.80/$320.
E-260 leaves$.14582/$.072125 per site under$1500 after motors/reserve, for **all**
missing resident/feedback/docking/tooling purchases. At$1000 only$.02375/−$.006;
$500 is already exceeded. These are allocations, not quotations or final prices.

Conditional64-grid/lead3/B2/K32 timing remains25.38s deep at2000rpm versus43.29s
at850, with paid N30 setup32.58/58.11 and dense50 stress45.78/89.17s. No support
scenario earns these speeds physically. First measure guide/seat response and
participating mass; do not replace thousands of shafts to fix an assumed RPM.
Checks: section identities, baseline equivalence, independent composite cantilever,
rigid-tilt bounds,40→80-element change≤2.61e−5 in checked cases, packing/ledger
arithmetic and25.38-s inherited schedule anchor. Self-review; no hardware pass.
