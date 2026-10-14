---
status: complete
builds-on: [E-290]
---

# Absolute projector address height discrimination

**Absolute codes escape E-290's weak-reflection phase bias, conditionally; they
do not identify which optical path is direct.** Run
`python3 tools/curated-experiment-checks/E-291.py` (standard library).
This is a new source-address construction, not another periodic-carrier sweep.
[Gupta et al., IJCV 2012 project](https://www.cs.cmu.edu/~ILIM/projects/IL/lightscan/lightscanindex.html)
(accessed2026-10-14) documents conventional Gray-code failures under indirect
illumination and alternatives for different transport regimes. It establishes
neither our transport bounds nor a usable projector. All numerical inputs below
are explicit synthetic scenarios; no captured images or measured PLA behavior.

## Construction and discrimination

Retain D300/b8 and camera ray r from E-290. Projector coordinate
`q=r+8/(300-z)` occupies field[-.025,.025). Divide it into2048 bins and encode
each index as11-bit reflected binary Gray code `n XOR (n>>1)`. Capture each
bit and complement plus all-white/all-black: **24 frames**. This is absolute
addressing within a finite field, not a sinusoidal phase or modulo carrier.
Forward intensity is `ambient+1000*gain*sum(weight*bit(q))`. Nonnegative
transport weights have no direct/indirect label in the measurement. Decoder
subtracts complementary pairs, requires normalized contrast≥.5 on every bit,
checks pair sums against white+black within2DN, rejects flat/saturated returns,
then intersects the decoded bin's height interval with physical0–50mm travel.
It receives calibrated r and travel, never commanded height or oracle masks.

Calculation: 90 rounded12-bit direct controls (z0/10/25/40/50, gain.05/.2/1,
ambient120/300DN, three rays) contain the true height in the returned interval;
maximum midpoint error.11530mm. All2048 index/code roundtrips pass a separate
integer check. Maximum height-bin width is.27441mm near minimum height;
this is quantization only, not a calibrated accuracy bound or product tolerance.

For direct weight1 and total indirect weight≤.2, every point-sampled bit retains
the direct sign: minimum normalized contrast `(1-.2)/(1+.2)=2/3`.
Six indirect-ray cases confirm the analytic bound. In particular true25mm plus
20% return from the45mm projector ray gives interval[25,25.23060]mm instead of
E-290's false28.3788mm. Equal25/45 weights return unknown. This proof assumes
static linear transport, sharp bins and no local temporal drift; it does not
establish that actual caps have a dominant direct path.

**Counterexample:** true25mm with direct weight.2 and reflected weight1 from the
45mm ray returns[44.90948,45.10791]mm, midpoint45.00870mm, with minimum contrast2/3
and exact pair sums. Relabeling the same two weights as a true45mm direct surface
plus a weak25mm reflected path changes **none of the24 raw intensities**. Both
hypothesized cap points lie on the calibrated camera ray within a4.4mm cap.
This is an admitted nonnegative transport ambiguity, not a radiometrically
constructed scene or evidence that our PLA realizes these weights. The geometric
extension below constructs a compatible reflected source address only. More source patterns alone cannot
label the same transport distribution's direct component. A stronger contrast
threshold can reject this example, but cannot establish directness: a sufficiently
weak direct return can leave an arbitrarily confident reflected address.

## Finite footprint control

The original field assumes 2048 independent stripe positions: one bin is
0.006714 mm at z25 and the coding field spans 12.5 mm at z50. Uniform box
footprints at a bin center retain the result at 0/1-bin width, return unknown at
2/4 bins, and agree at 128/256 quadrature points. At a boundary even a one-bin
direct footprint returns unknown. These are synthetic controls, not optical PSFs;
there are no captured images or qualified scan-to-accept times. The finite-field
screen below replaces the assumption of freely available optical resolution.

## Finite terrain geometry: stripe plane versus a single ray

**Geometric calculation, not material measurement:** a taller neighboring
column can deliver the false45-mm source address to the true25-mm cap through
one side-wall interaction. This removes a geometric objection to the abstract
transport witness; it does **not** establish its assumed5:1 reflected/direct
ratio, two-scene indistinguishability, or any observed error frequency.

Coordinates here are `(coding axis, cross-row axis, height)`; projector is
`(0,0,300)`, camera `(8,0,300)`, observed target `(0,0,25)`. Caps are opaque flat
rectangles with vertical sides, no props, centered grids and maximum height50.
These ideal assumptions exclude roughness, transmission, lean and multiple
reflections. No new manufacturing tolerance distribution is assigned.

A tempting **2D-only control** grants a ray through the target center. With
actual height h and claimed height v, its projector slope is
`q=-8/(300-h)+8/(300-v)`; at the actual plane its intercept is
`8*(v-h)/(300-v)`. For all h,v in[0,50], the complete source-ray segment inside
the terrain slab stays within1.6mm of center; the camera segment within1.333mm.
The bounds follow from linear endpoints and monotonic denominators, cross-checked
at2601 integer height pairs. A4.4-mm cap leaves.6mm in this plane (10.3mm leaves
3.55mm); these are **ideal geometric reserves**, not tolerance qualifications.
The old25→45 source ray hits x=.627451 on the same cap. A single reflection
between two points on that flat cap cannot propagate through free space to its
center. This rules out that particular coplanar construction only.

**A stripe address is a plane of rays, however.** Put the neighboring column
at cross-row distance p and height50. Its near vertical wall is at `y=p-w/2`.
The45-mm source stripe reaches
`R=(.581818,p-w/2,45)`, then can travel down to `(0,0,25)`:

| Pitch / width (mm) | Wall y (mm) | Incident normal cosine | Outgoing normal cosine |
|---|---:|---:|---:|
|5.08 /4.4|2.88|.011293|.142471|
|6.35 /4.4|4.15|.016272|.203090|
|12.7 /10.3|7.55|.029595|.353042|

Executable segment/box intersection checks show the source first reaches the
neighbor's near wall at R, then the open outgoing segment remains outside both
solids until reaching the target cap. Both directions are on the reflecting
side of the wall; target receives light from above. Direct source and camera
paths stay unobstructed. Positive cosines admit diffuse reflection geometrically,
but the grazing incident angles caution against assigning strong weights without
radiometry. This is a point-path construction; integrating finite wall area,
projector pixels, BRDF, cap return and camera footprint is still owed.

## Finite-wall radiometry: path existence does not earn dominant return

**Numerical integration and continuous bound, not physical measurement.** The
same executable now integrates the *whole* near wall, including its distribution
across source addresses. Assume a point projector with uniform radiant intensity
per solid angle, a Lambertian wall of reflectance rho≤1, a Lambertian target,
one reflection, static geometry, and the preceding central target at25mm beside
one50-mm neighbor. These assumptions are a control, not a prior for printed PLA.
[PBRT's diffuse model](https://www.pbr-book.org/4ed/Reflection_Models/Diffuse_Reflection)
uses BRDF=rho/pi and cautions about grazing-angle deviations; its
[surface-reflection equation](https://pbr-book.org/4ed/Radiometry%2C_Spectra%2C_and_Color/Surface_Reflection)
supplies the irradiance integral (accessed2026-10-14). No material reflectance,
roughness or projector angular-uniformity measurement is inferred from these sources.

Let wall distance `a=p-w/2`, wall point `(x,a,z)`, target `(0,0,25)` and source
`(0,0,300)`. Integrate x over[-w/2,w/2], z over[25,50]. Normalizing by direct
irradiance `I/275²`, the differential reflected/direct ratio is

```
rho/pi * [a*275² / (x²+a²+(300-z)²)^(3/2)]
       * [a*(z-25) / (x²+a²+(z-25)²)^2] dx dz.
```

The first factor in brackets is normalized wall illumination; the second is
wall solid angle times target incidence cosine. Target diffuse reflectance
cancels in this ratio. The entire wall is granted illumination, even if the
actual four-cap projector field clips it; no new optics are assumed earned.
Source slope is `x/(300-z)`: integrate separately inside each Gray-code bin,
then form all24 raw observations from the histogram and unit direct return.

| Pitch/width mm | Total reflected/direct, rho=1 | Continuous upper bound | Contribution in false45-mm bin |
|---|---:|---:|---:|
|5.08/4.4|.00224428|.0069696|.000003772|
|6.35/4.4|.00241817|.0100430|.000003847|
|12.7/10.3|.00521917|.0182710|.000003758|

Independent bound: wall irradiance/direct≤`a*275²/250³`; a single vertical wall
occupies at most half the target's cosine-weighted upper hemisphere, so multiply
by≤rho/2. This bound does not depend on quadrature or code sampling. Doubling
vertical samples256→512 and within-bin samples1→2 changes the histogram by
less than.0062% in relative L1 norm across the three cases. Black-wall and
half-reflectance controls give zero and half transport. This checks this smooth
integral, not model discrepancy or real optics.

The reflection spreads across722/722/1688 bins. All three raw-data decodes retain
the true25-mm address, minimum contrast.99748/.99716/.99368. Even the continuous
bounds are below the total-indirect/direct≤1/3 sufficient condition for the
existing.5 contrast threshold, absent blur/drift/noise. The original5:1 reflected
witness is therefore **not produced by this finite diffuse wall**. Total reflection
would require an aggregate amplification of958–2228× to reach5:1, and merely
amplifying this broad distribution does not concentrate it into the false45 bin.
These factors are sensitivity ratios, not permissible BRDF multipliers or proof
against glossy materials, props, multiple walls/bounces or a suppressed direct path.

The abstract dominant-path witness remains conditional, not a likely result for
this diffuse neighbor. Retain direct-dominant coding, with finite optics still
owed. Material response, exposure, identity and covered-cap visibility remain
unqualified; no further threshold or arbitrary-reflector sweep is justified.

## Finite projector field: a working code is not a working optical reader

**Sourced specification plus ideal-pinhole calculations, not hardware tests.**
[TI's LightCrafter 4500 guide, revision F, table 1-1 and section 1.2.1](https://www.ti.com/lit/ug/dlpu011f/dlpu011f.pdf)
(accessed 2026-10-14) gives throw ratio 1.2, focus range 0.5–2 m and a
912-column × 1140-row diamond array. Revision F explicitly changes the older
1.4 throw figure. Native diamond pixels are not the model's rectangular stripes.
The stock engine does not earn focus at D300 (250–300 mm surface distance).

Even **granting 2048 independent positions across its full horizontal field**,
without claiming this native mapping, angular bin width is
`dq=1/(1.2*2048)=0.000406901`, 16.67 times the earlier assumed bin.
Put its closest surface at the specified 500-mm focus limit: D550 for S50.
The field at the highest terrain is 416.67 mm. With the unchanged 8-mm baseline,
a height bin beginning at zero spans **14.967 mm**. Cropping the active image
reduces field and active pixels together; it does not improve angular sampling.
This is a scoped failure of stock optics as a substitute for the fine-field
model, not a rejection of structured light or a claim about measured accuracy.
Focus range also does not establish simultaneous depth of field over 50 mm.

The executable uses `dz=D-b/(b/D+dq)` for that zero-start bin, checks the inverse
projection independently, and bounds any in-range bin by `D²*dq/b`. It separately
screens an **unpriced custom 1920×1080 square-pixel projector/lens scenario** at
D300/b8. Put four caps across the long axis and one across the short coding axis;
cover them at z50. Required short-axis field is
`max(cap_width,(3*pitch+cap_width)*1080/1920)`. Ideal sharp pixels, perfect focus,
calibration and unoccluded direct return are granted; these are favorable
necessary accounting controls, not selected hardware.

| Pitch mm | Four-cap width mm | Coding field mm | Zero-start projector bin mm | With one same-size camera pixel mm |
|---|---:|---:|---:|---:|
|5.08|19.64|11.048|0.460|0.918|
|6.35|23.45|13.191|0.549|1.095|
|12.7|48.40|27.225|1.130|2.252|

The last column adds projector and camera angular interval widths, then applies
the same inverse relation; it is interval uncertainty, not RMS error or a claim
that subpixel estimation is impossible. The previous exact camera ray was free
calibration. Preserving the old angular bin while spanning all four caps would
require at least **3218/3843/7930 cross-axis square pixels**, respectively.
Coarser mechanics need fewer cells but wider four-cap optics; they do not
inherently improve optical sampling.

A custom full-board 406.4-mm square field at z50 on the same 1080 coding rows
has a **16.029-mm** zero-start projector bin, before camera uncertainty. Achieving
an illustrative 0.5-mm bin requires at least **36,516 coding rows** at this
baseline and distance. The 0.5-mm allocation is a diagnostic, not a new product
gate. Larger baseline, subpixel inference or another lens/topology changes the
problem and must re-establish occlusion and calibration; none is supplied here.
The full-board idealization grants framing without extra edge/offset margins.

**Decision:** park the stock-engine substitution and the small-baseline
whole-board absolute-pixel reader. Retain local optics only as a conditional
construction requiring a priced lens/projector/camera with earned focus, spatial
transfer and synchronization. Do not buy an engine or tune code thresholds from
these numbers. The concrete next optical discriminator is whether a finite local
lens can preserve useful contrast through the entire S40/S50 depth, rather than
another ideal code. Covered caps still return unknown; optical verification does
not establish load retention or repair.

No resident parts change: 1024/4096/6400 threaded pairs and their manufacturing,
support and service burdens remain. No camera/projector BOM or quote was earned;
the inherited $1068–1778 allocation cannot price these custom optics against the
~$500 reference, ~$1000 finished value or $1000–1500 demonstrator. The 24-frame
sequence is retained for comparison: at assumed 0.1 s/frame, local 1/4/8 groups
owe 2.4/9.6/19.2 s, and four-cap dense scans owe 614.4/2457.6/3840 s before motion,
exposure qualification and retries. A full-board 2.4-s acquisition would have the
coarse bins above, so it is not a proven shortcut to the ~30-s gameplay reference.
Minimum/raised neutral and paid preparation remain as previously modeled. No
new print, purchase, physical evidence or change to optional E-281.
