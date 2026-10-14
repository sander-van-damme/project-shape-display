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

## Optical and whole-machine obligations

One bin projects to.006714mm at z25; the coding-axis field spans12.5mm at z50.
Four caps run across the *other* axis, requiring19.64/23.45/48.40mm field widths
at5.08/6.35/12.7mm pitch. Thus2048 independently resolved stripe positions across
one row are assumed; no lens, projector pixel pitch, focus or camera footprint
qualifies them. Uniform finite-footprint controls at a bin center preserve the
result at0/1-bin width and return unknown at2/4 bins;128/256 midpoint quadratures
agree. At a bin boundary even a one-bin direct-only footprint returns unknown.
These box averages are sensitivity controls, not a measured optical PSF. Missing
visibility, prop identity, camera sampling, calibration, noise, drift and motion
remain unqualified. No guarantee of finite scan-to-accept time for covered caps.

No resident parts are added or removed:1024/4096/6400 threaded pairs retain their
manufacture, guides, thrust, capture and holding duties. Shared projector/camera,
references and upper carrier replace no mechanical support. E-290's unsourced
base-plus-optics$1068–1778 allocation is inherited only for comparison; it does
**not** price the fine-pattern capability. Retain ~$500 original case, possible
~$1000 finished value and separate$1000–1500 demonstrator, without purchase.
At assumed.1s/frame and four caps/group, acquisition alone costs614.4/2457.6/3840s
at1024/4096/6400. Local1/4/8 groups add2.4/9.6/19.2s before writing, routing,
undocking, settling, calibration and retries. E-270/E-276 conditional gameplay
schedules, S40/S50, minimum/raised neutral and paid preparation remain unchanged;
these are sensing increments versus~30s, not new representative-map results.

**Decision:** retain the direct-dominant absolute-code control; park optical
pattern refinement. A next optical investment needs actual calibrated cap images
or a physically constructed path discriminator and earned resolution/exposure,
not another code-count or threshold sweep. The positive result removes a specific
weak-reflection alias; it does not close actual-height acceptance. No hardware,
print, holding or manufacturing qualification. E-281 remains optional/unprinted.


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

**Decision:** retain shared optical readback conditionally, with the3D side-wall
path as the relevant falsification scene. Do not infer direct-path dominance from
small baseline or a clear central ray, and do not infer dominant reflection from
path existence. The next decision-changing optical check is finite-area
radiometric bounding or calibrated images of a low cap beside a high wall,
including source-address spread; further pattern/threshold sweeps remain parked.
This extension adds no resident/shared hardware or scan frames: the preceding
pitch, S40/S50/neutral, timing, cost, retention and optional-print limits stand.
