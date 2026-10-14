---
status: complete
builds-on: [E-292, E-291]
---

# Baseline sensitivity versus terrain visibility

**Geometric calculation with an inherited optical control, not measured accuracy.**
Larger baseline is a conditional escape from E-292: a diagonal 90-mm pair can
retain a substantial unobstructed patch at 12.7-mm pitch while quantizing height
into approximately .5-mm bins. This does not establish a working reader or an
acceptable terrain error. Run `python3 tools/curated-experiment-checks/E-293.py`.
No new resident mechanism, print, purchase or calibrated image.

## Construction and independent checks

Keep the E-292 coarse angular bin dq=.0005 and fixed 1.927-mm circular projector
pupil, D=300mm above zero terrain, S40/S50, and harmonic focus. Its sampled minimum
signed finest-bit fundamental transfer is .745885 across S50, using the existing
pupil calculation without a new aperture search. Grant the camera the same pupil
size and otherwise perfect calibrated rays. This is an optical control, not a
camera specification or complete optical transfer chain. Depth of field requires
an explicit spatial-frequency/contrast criterion; stopping down is not a free
resolution fix ([Edmund Optics](https://www.edmundoptics.com/knowledge-center/application-notes/imaging/depth-of-field-and-depth-of-focus/),
rechecked2026-10-14). E-292 supplies the wave-method derivation and limitations.

Move projector and camera to opposite sides of the target: positions
`±(b/2)*(cos(theta),sin(theta))` at height D. Compare b=8/45/90mm, grid-axis or
45-degree diagonal baseline. This changes both baseline and centering from the
old projector-over-target layout. In rectified slope coordinates,
`q-r=b/(D-z)`. With perfect camera ray and a bin beginning at height z, its width is

```
dz = (D-z)^2*dq / (b+(D-z)*dq).
```

At z0 the three widths are5.52147/.996678/.499168mm. Baselines44.85/89.85mm
are required for1/.5mm bins under this exact quantization convention. Bin width
is not measured error, a guarantee across blurred bit boundaries, or an adopted
product tolerance. Off-axis aberrations, camera sampling, scattering, noise and
calibration drift remain unearned. In particular the inherited on-axis optical
control is not an off-axis qualification at b90.

For each pitch p and cap width w, put a low cap at z0 and all eight neighboring
opaque columns at H=40/50mm. Use (p,w)=(5.08,4.4),(6.35,4.4),(12.7,10.3)mm;
the quarter-grid control retains the inherited narrow cap, not a new surface
coverage choice. Let a=p-w/2, t=(H-z)/(D-z), R=.9635mm. A ray between local cap
coordinate x and pupil coordinate X passes height H at `(1-t)*x+t*X`.
The inner square opening |x|,|y|<a yields a sufficient continuous clear rectangle.
For each axis i and target offset c_i from the pair midpoint, its interval is

```
center_i = t*c_i/(1-t)
half_i = (a - t*(abs(b*u_i)/2 + R))/(1-t)
interval_i = [center_i-half_i, center_i+half_i] intersect [-w/2,w/2].
```

Empty intersections yield no guaranteed patch. For sensitivity only, also move
all inner walls inward .2mm and require ±.2mm common registration reserve in each
axis: replace a by a-.2 and subtract .2 from half_i. These are competing geometric
bounds, not measured printer/camera distributions or independent per-cell errors.

The inner square is deliberately conservative: real column seams leave openings.
An independent segment/AABB intersection check over2916 cap/height/baseline/angle
cases confirms every sampled point inside the claimed rectangle clears actual
neighbor solids for the four cardinal pupil extrema on both optics. Continuous
pupil clearance follows from its coordinate support bounds. There are58 clear
samples outside the rectangle; thus zero rectangle area does **not** prove no
possible ray. Central-point blocked/clear outcomes agree separately in all
sampled configurations. Exact inverse-bin endpoints agree with the formula;
flat-terrain and zero-baseline limiting cases pass. Checks validate calculations,
not manufacture or hardware.

## Results and the shared-field obligation

Fractions below are sufficient clear rectangle area divided by cap area, not
probability of successful readback. All are S50 at the lowest terrain point.
The bounded column applies the correlated .2/.2mm sensitivity scenario.

|Pitch|Baseline / angle|Central-cap clear %|Bounded clear %|Worst of four grid-row caps clear %|
|---:|---:|---:|---:|---:|
|5.08|45 / 0°|0|0|0|
|5.08|45 / 45°|.137|0|.137|
|6.35|45 / 0°|13.06|0|13.06|
|6.35|45 / 45°|53.24|28.06|31.51|
|12.7|45 / 0°|84.80|76.26|84.04|
|12.7|45 / 45°|100|100|68.21|
|12.7|90 / 0°|0|0|0|
|12.7|90 / 45°|23.63|16.05|18.14|

At b90 both smaller pitches have zero central rectangle at either angle.
At b45 diagonal the fine-grid rectangle is only .163mm square; it vanishes under
the stated bounds. Do not tune alignment around that narrow nominal patch.
At coarse b90 diagonal the central rectangle is5.007mm square; the four-cap
worst rectangle is approximately5.007×3.843mm. Four target centers lie on an
actual grid row at `(0,j*p)`, j=±.5,±1.5, under one fixed pair; they are not four
individually recentered readers. Each target is conservatively granted all high
neighbors even though other low targets in a real group can improve visibility.
The clear rectangle shifts across each cap: rejecting all off-center pixels
would unnecessarily lose this result. Finite projected field, common decoder,
camera pixel density and complete pupil transfer still need construction.

S40 improves visibility without changing bottom quantization: central b45 diagonal
clear area is10.92/99.32/100% across fine/quarter/coarse pitches. Coarse b90 diagonal
has50.73% clear,39.51% with the bounded errors. The source contains all36 cases.
For ground at a raised neutral z30 beside H50, the relative20mm relief reduces
occlusion; this must not be substituted for the full-travel pit test. A neutral
coordinate change alone buys neither physical travel nor ray clearance. Broad
ravines and isolated walls may be easier than this enclosing-pit diagnostic;
its frequency in actual play is not known. Miniature-covered caps remain unknown.

## Whole-machine decision

Retain the coarse diagonal reader as a **conditional geometric survivor**, not
an architecture selection. Park the fine-grid b45 full-travel central-patch
embodiment under the stated registration bounds; do not treat gaps or another
threshold as robust observation. Larger baseline and diagonal placement are
materially different geometry, not proof that all large-baseline readers work.

No additional per-cell parts, marks, joins or support releases are introduced.
The machine still has1024/4096/6400 threaded pairs; support, powered rate,
manufacture, assembly and repair remain the independent mechanical obligations.
The shared reader retains one projector, one camera, mounting and calibration;
90mm separation is a mechanical envelope allocation, not a priced packaged head.
Diagonal mounts and optical clearance must coexist with tabletop use. Custom
optics remain unpriced against ~$500 bought hardware, ~$1000 finished value and
$1000–1500 demonstrator references. No complete BOM or purchase authorization.

Conservatively retain E-291's24-frame protocol at assumed .1s/frame and four
simultaneously observed caps. Coarser bins may permit fewer code bits for a
constructed field, but no unimplemented reduction is credited. Acquisition is
2.4/9.6/19.2s for1/4/8 groups,614.4/2457.6/3840s for dense1024/4096/6400-cell
scans before motion, settling, actuation, retries and proof, against the~30s
play reference. Four-cap *ray clearance* does not earn four-cap image readout.
If eventual optics require recentering each cap, acquisition becomes4× these
numbers; moving/rotating views to chase seams similarly incurs real preparation.
Minimum/raised neutral,40/50mm travel and initial mechanical preparation retain
their existing costs. Dense timing is a diagnostic, not automatic rejection.

**Stop local baseline/angle sweeps here.** Next discriminating work is a finite
four-cap forward image/decoder at the surviving coarse diagonal geometry, with
camera sampling and calibration error charged, or calibrated actual imagery.
It must establish recoverable height intervals and reject mixed/hidden pixels,
not merely render more rays or assume image errors vanish. The narrow fine-grid
patch does not earn lens development. E-281 remains the sole optional unperformed
print test; this result neither requires another print nor waits for it.
