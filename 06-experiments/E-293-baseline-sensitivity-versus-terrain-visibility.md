---
status: complete
builds-on: [E-292, E-291]
---

# Baseline sensitivity versus terrain visibility

**Geometric/direct-image calculations, not measured accuracy.** A diagonal90-mm
pair retains a useful clear patch at12.7-mm pitch with~.5-mm projector bins;
finite-camera and reference models do not establish a working reader.
Reproduce with `python3 tools/curated-experiment-checks/E-293.py`,
`E-293-camera.py` and `E-293-reference.py` in that directory (NumPy).

## Geometry and independent checks

Keep E-292 coarse angular bin dq=.0005, fixed1.927-mm circular projector pupil,
D300 above zero terrain, S40/S50 and harmonic focus. Sampled minimum signed
finest-bit fundamental transfer is.745885 across S50. Grant the camera the same
pupil and perfect rays: an optical control, not a component specification.
Depth of field requires an explicit contrast/frequency criterion
([Edmund Optics](https://www.edmundoptics.com/knowledge-center/application-notes/imaging/depth-of-field-and-depth-of-focus/),
checked2026-10-14); E-292 preserves wave-method limits. Off-axis aberrations,
scattering, noise and calibration remain unqualified.

Place optics at ±(b/2)u, u=(cosθ,sinθ), height D; compare b8/45/90mm and θ0/45°.
Rectified slopes obey q-r=b/(D-z). Exact bin width beginning at z is
`dz=(D-z)^2*dq/(b+(D-z)*dq)`: at z0,5.52147/.996678/.499168mm.
Baselines44.85/89.85mm give1/.5-mm bins, not error guarantees.

Place a low cap beside eight H40/50 opaque columns. Compare pitch/width
(5.08,4.4),(6.35,4.4),(12.7,10.3)mm; the quarter-grid narrow cap is a control,
not an approved surface. Set a=p-w/2, t=(H-z)/(D-z), pupil radius R=.9635.
At target offset c from pair midpoint, a sufficient clear rectangle in each axis is

```
center_i=t*c_i/(1-t)
half_i=(a-t*(abs(b*u_i)/2+R))/(1-t)
interval_i=[center_i-half_i,center_i+half_i] intersect [-w/2,w/2]
```

Competing bounded scenario: move all walls inward.2mm and reserve±.2mm common
registration by replacing a with a-.2 and subtracting.2 from half. These are
correlated allocations, not measured process distributions. Independent2916
segment/AABB cases confirm claimed sampled clear points for both optics' four
cardinal pupil extrema; continuous clearance follows coordinate support bounds.
There are58 clear samples outside the rectangle: zero area is not universal
occlusion. Central-point checks, inverse-bin endpoints, flat terrain and zero
baseline limits agree. Numerical checks do not qualify hardware.

## Visibility results

S50 lowest terrain; fractions are sufficient patch/cap area, not read probability.
Four caps occupy one real grid row at (0,j*p), j=±.5,±1.5; the optics stay fixed.
Conservatively grant every cap eight high neighbors. No individually recentered
views or free rotation is credited.

|Pitch|b / θ|Central clear %|Bounded %|Worst of four caps %|
|---:|---:|---:|---:|---:|
|5.08|45 / 0°|0|0|0|
|5.08|45 / 45°|.137|0|.137|
|6.35|45 / 0°|13.06|0|13.06|
|6.35|45 / 45°|53.24|28.06|31.51|
|12.7|45 / 0°|84.80|76.26|84.04|
|12.7|45 / 45°|100|100|68.21|
|12.7|90 / 0°|0|0|0|
|12.7|90 / 45°|23.63|16.05|18.14|

At b90 smaller pitches have zero central rectangle at both angles. Fine b45
has only.163mm square, lost under bounds: park this embodiment, not all optical
readback. Coarse b90 has5.007mm square centrally, worst four-cap patch5.007×3.843mm.
Patch shifts across caps; rejecting all off-center pixels discards usable geometry.
S40 b45 diagonal clear fractions10.92/99.32/100%; coarse b90 clear50.73%, bounded
39.51%. Raised neutral z30 beside H50 reduces relative relief to20mm but does not
replace full-travel pit testing or mechanical preparation. Broad ravines/walls may
be easier than this enclosing-pit stress; its play frequency is unknown. Covered
caps remain unknown. Source retains all36 configurations.

## Finite-camera and common-calibration control

Use coarse b90/45°, D300, dq.0005 and one fixed camera covering slopes
r∈[-.27,-.07], s∈[-.1,.1] at256²/1024² pixels. Test four caps at z0/25/30/50.
An **oracle** selects pixels wholly inside the clear rectangles, granting actual
height/identity/visibility: segmentation and mixed/hidden-cap detection are not
implemented. Integrate11 Gray bits plus complements/white/black exactly across
pixels (24 frames). Grant sharp direct optics, uniform flat caps and no noise,
indirect light or reflectance variation. E-292 transfer alone does not prove this.
Reject any normalized bit contrast<.5. Exact integration agrees with8192-sample
quadrature within.001 on17 pixels/case; weights sum to1. Four-sample integration
was inadequate near boundaries.

For decoded[qlo,qhi], pixel ray r±dr/2 and common angular±e, baseline±db,
origin±dD bounds, retain the unclipped interval

```
[zlo,zhi]=[D-dD-(b+db)/(qlo-r-dr/2-e),
           D+dD-(b-db)/(qhi-r+dr/2+e)]
```

Independent16-corner checks confirm extrema. Intersect pixels only under granted
flat-cap identity; do not average common error away. e=.0002,db=.1mm,dD=.2mm
are sensitivity allocations, not measured calibration or a product criterion.

|1024² z|Accepted/oracle pixels|Largest ideal pixel interval mm|First cap ideal intersection mm|Bounded intersection mm|
|---:|---:|---:|---:|---:|
|0|20257/24930|.6962|.2969|1.7635|
|25|99090/121961|.5850|.2495|1.5967|
|30|112735/141486|.5639|.2468|1.5708|
|50|142596/175528|.4834|.2062|1.4395|

At256²,z0 first-cap widths1.1875/2.6542mm. All zero-bias intervals contain truth.
Common+.0002 camera-ray bias leaves intensities identical but makes all16
unbudgeted cap intersections miss truth; at z0,2719/20257 accepted individual
intervals also miss. Including bounds restores containment. More pixels cannot
independently average away systematic error; .5-mm bins are not .5-mm accuracy.

## Whole-machine ledger and decision

Retain coarse diagonal geometry conditionally. No resident parts, marks, joins or
support releases added;1024/4096/6400 threaded pairs retain manufacture, support,
powered speed, assembly and repair obligations. One projector/camera, mounts and
calibration remain unpriced;90mm separation is an envelope allocation, not a
packaged head. Compare~$500 bought hardware,~$1000 finished value and$1000–1500
demonstrator without claiming a complete BOM or purchase authority.

Retain24 frames at assumed.1s/frame/four caps:2.4/9.6/19.2s for1/4/8 groups and
614.4/2457.6/3840s dense1024/4096/6400 scans, **before** travel, settling, writing,
retry and proof against~30s play. Recentring each cap would multiply acquisition4×.
Neither fewer bits nor qualified four-cap readout follows from ray clearance.
Initial neutral and40/50mm mechanical travel costs remain; dense timing is a
separate diagnostic. No new print; E-281 remains optional and unperformed.

## Shared-reference identification and transported datum

Run `python3 tools/curated-experiment-checks/E-293-reference.py` (NumPy).
**Algebraic identification and bounded endpoint scenarios, not image calibration.**
Model the rectified disparity as `d(z)=b/(D-z)+a`, adding one common angular
offset a to the earlier baseline b and height origin D. Grant known reference
heights, correspondence and scalar disparity measurements. This omits spatial
distortion, tilt, reflectance, blur and segmentation; it cannot qualify the full
projector/camera system. Multiple lateral points on one plane could supply other
calibration information in a richer model; the rank result below concerns only
these depth-disparity observations.

For three fixed depths 0,h,2h with h=25mm, the exact inverse is

```
R = (d2-d1)/(d1-d0)
D = 2h*R/(R-1)
b = (d1-d0)*D*(D-h)/h
a = d0-b/D
z = D-b/(d-a)
```

At D300/b90/a.0002 this recovers all three parameters and1001 held-out heights
over0–50mm to numerical precision. Independent derivative-matrix ranks are1/2/3
for one/two/three distinct reference depths. A coplanar zero reference cannot
distinguish D300/b90 from D301/b90.3: both match exactly but the latter infers
50.1667mm for a true50-mm target. More repeats of that same observation do not
identify the missing parameters.

Assume ±.00015 slope error for each reference, **not a measured camera bound or
an inference from E-293 pixel count**. Across all eight error-sign corners, fitted
D ranges272.75–333.99mm and b72.90–113.82mm; each fit exactly matches its three
noisy reference readings. Nevertheless maximum height error on the1001 exact
target readings is only.1653mm, rising to.3074mm when target readings also receive
either sign of the same error. These are finite scenario results, not certified
envelopes over every error combination, hardware accuracy or permission to
extrapolate outside the reference range. They show useful interpolation can
coexist with poorly determined physical parameters. Do not use an excellent
three-point residual as evidence that the head geometry is calibrated, or use
these unconstrained fits as an earned replacement for the earlier nuisance bounds.

**Reference attachment changes what is observable.** Rigidly raise the head and
all head-mounted references by.5mm: every reference disparity is exactly unchanged,
while a stationary terrain cap is inferred.5mm too low. The numerical check holds
over the entire0–50mm target range. Such references can track internal optical
change, but cannot prove head-to-board pose. Conversely, a board-fixed staircase
at known0/25/50mm supplies that datum only where it is observed. A common.2-mm
error in its stated heights transfers exactly into a.2-mm terrain error in this
model; hundreds of reference pixels do not remove a common datum error.

A concrete comparison is one rigid three-level target at a board-edge parking
station versus the same target riding with the head. Both add three reference
faces, a carrier and registration/metrology obligations, rather than per-column
marks or mechanisms. The parked target requires travel and stable pose transfer
back to the active region; the moving target retains the unobservable board datum.
Neither has a constructed clear optical path, measured geometry, deployment
repeatability or priced mount. The existing .2-wide angular field spans only
50–60mm over this depth range, so do not assume it observes edge references while
servicing the whole~400-mm board. Adding more stations or a board-pose instrument
would require an explicit count, visibility and calibration construction.

One extra24-frame reference acquisition costs an assumed2.4s **before** station
travel/settling. Recalibration at every four-cap group would add614.4/2457.6/3840s
to dense1024/4096/6400 readback, doubling acquisition alone. For1/4/8 local groups,
it adds2.4/9.6/19.2s; sharing one scan per update costs2.4s but assumes pose remains
valid through every move. No such stability or frame rate is earned. Mechanical
actuation, neutral preparation and40/50mm travel costs remain; the~30s play and
~$500/$1000/$1000–1500 cost comparators above are unchanged, with reference hardware
and metrology still unpriced. No new resident parts, print or purchase.

Retain depth-separated references as a conditional interpolation control;
park head-mounted-only references as proof of absolute board height. Next useful
evidence is an independently observable board datum through actual head movement
or calibrated material images, including reference visibility and cap identity.
Do not extend scalar parameter/noise sweeps into an optics qualification claim.

## Fixed witness camera: simultaneous board-to-reader datum

Run `python3 tools/curated-experiment-checks/E-293-witness.py` (NumPy).
**Ideal pinhole geometry and exact sensitivity witnesses, not measured accuracy.**
A separate fixed overhead camera can observe the moving reader and board together,
removing the common vertical-motion blindness of riding references. This is a
constructed alternative to returning to an edge station, not a qualified reader.

Assume a downward-looking camera800mm above board zero, a90mm square target with
four identifiable corners rigidly attached at reader height300mm, and a600mm-wide
square field at that target plane. At4096 pixels this gives focal length3413.33px;
at the board the field is960mm wide. The target moves over±203.2mm in both axes.
Eight10mm square board reference patches have centers at the corners and side
midpoints of a460mm square. This enlarges the reference footprint to470mm; it
adds an overhead mount and must remain outside hands/props, not inside the
playable terrain. The target-to-optical-center transform is granted known/rigid.
No reference is added to individual columns.

All target corners remain in the field at289 sampled positions; the outermost
coordinate is1694.38px versus2048px half-field. Independent small-rigid-motion
projection Jacobians have rank6 at every position: calibrated ideal corner
observations are locally pose-observable, not a guarantee of unique global pose,
accurate decoding or favorable conditioning. Full tilt/distortion inference is
not implemented; the accuracy calculation below grants parallel planes.

**Visibility is explicit but limited.** Model the reader as an opaque90mm square
at z300. Rays to the board patches cross this plane at.625 times their board XY.
The nearest projected patch centers are143.75mm apart, exceeding the96.25mm
combined reader/patch overlap span: at most one patch can be obscured anywhere
in the continuous translation domain. The289-position check confirms this and
that at least one complete diametric side-midpoint pair survives. Four corner
references alone can lose one point (e.g. reader centered150,150), so a
four-point planar homography cannot simply assume all four remain visible.
Eight patches leave at least seven. Their paths stay outside the±203.2mm terrain
footprint through z0–50: the minimum exterior coordinate at z50 is210.94mm.
Actual gantry members, thick housing, cables, player hands and tall props are
excluded and can invalidate this visibility construction; missing references
must produce unknown, not reuse a stale accepted pose.

For parallel planes, use measured board/head spans sb,sh and known widths460,90:
`head_z=f*(460/sb-90/sh)`. This independently inverts projected scale. A common
.5mm camera lift cancels when **both spans are measured simultaneously**; retaining
a stale board datum instead gives-.5mm error. A.5mm head lift changes its corner
coordinates by up to.3075px at4096, whereas E-293 riding references do not change.
This observes rigid head motion, not optics flex beneath an unchanged marker.

|Square image width|Head span px|Board span px|Exact height-error range mm|
|---:|---:|---:|---:|
|1024|153.6|490.67|[-2.4473,+2.4384]|
|4096|614.4|1962.67|[-.6110,+.6104]|

The table assumes±.25px error at each span endpoint; hence±.5px span error.
Monotonic reciprocal endpoints give exact bounds **only within this parallel,
known-scale model**. This is an allocated subpixel error, not camera evidence.
Correlated inward/outward endpoint shifts realize these errors without averaging
away. Separately, a+.1mm mistake in stated head-target width causes-.5556mm error;
a+.1% focal-length error scales the inferred300mm height by+.3mm. These are
exact aliases with zero scale-fit residual. Lens distortion, board flatness,
target-to-optics calibration, marker warping, tilt, thermal drift and segmentation
remain outside the bound. Adding this datum channel does not replace the local
reader's existing height/identity/contrast uncertainty or qualify .5mm accuracy.

**Architecture decision:** retain simultaneous fixed witnessing as a conditional
way to observe board-to-reader motion; park stale-station and riding-reference-only
claims. Do not choose a camera or tune marker size/resolution from this model.
The construction adds one camera/lens, one overhead support, one reader target,
eight board patches and their mounting/metrology, with no resident pair changes.
It requires visibility and a stable marker-to-optics transform; those are the
next discriminating evidence, alongside actual calibrated imagery. Extra hardware
is unpriced, so it cannot be called a completed~$500/$1000 product or$1000–1500
demonstrator BOM. No purchase, physical accuracy result or new print.

If one witness frame takes an assumed.1s **serially** per four-cap group, add
.1/.4/.8s for1/4/8 local groups or25.6/102.4/160s for dense1024/4096/6400 scans.
Combined local24-frame and witness acquisition is2.5/10/20s or dense640/2560/4000s,
before writer motion, settling, retries and initial neutral preparation. Concurrent
capture might avoid that increment only with earned synchronization/stability;
no rate is qualified. The~30s play reference,5.08/6.35/12.7mm comparisons and
40/50mm physical travel remain unchanged. Witness visibility above terrain does
not make a miniature-covered cap visible to the local reader. E-281 remains the
single optional, unperformed print; this result warrants no extra print job.
