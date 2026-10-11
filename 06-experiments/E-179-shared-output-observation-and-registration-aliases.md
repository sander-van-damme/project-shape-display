---
status: complete
builds-on: [E-178, E-176, E-173, E-166, E-148, E-056]
---

# Shared output images retain depth aliases and incompatible mirror paths

**Do not replace support/pickup proof with the tested shared silhouette reader.**
An active pickup within a ±.05-mm edge scenario has exactly the same pinhole
projection as a nominal clear pickup. E-178's mirror also intersects E-173's
spine. Separate relocated mirrors can see narrow output bands individually, but
the tested lower strip blocks the upper view. Retain shared height sensing and
multi-view output sensing as conditional functions; no architecture is selected.

Input main `76b98d8`; LAB-293. Reproduce with
`python3 tools/curated-experiment-checks/E-179/observation.py` (standard library;
imports E-178's vector, box and timing routines). Evidence: finite specular rays,
opaque boxes, deterministic aperture search, exact projection counterexample and
analytical interpolation bounds. Self-review only; no optical render, physical
measurement, calibrated process distribution, purchased component or fabrication.
JSON output is disposable.

## Finite access rather than command flags

Use E-173's actual 5.08-mm cells, five heights 0…40.4 mm, Y-indexed ground dog
and Y-sliding pickup. Its spine is X=±.6, Y=±2.3, Z=h−41.4…h+50 mm. The
E-178 row mirror from (Y,Z)=(.9,.7) to (2.3,−.7), spanning X, intersects that
spine at **all five heights**. Its positive optical clearance for a narrower
hypothetical tail never established compatibility with this rack.

Try moving a continuous mirror into the inter-row corridor Y=2.30…2.78.
Camera is (X,Y,Z)=(48.26,2.54,−60). Mirror center Y=2.54; normal in YZ is
(cos α,sin α). Search α=15…75° and center Z=−8…4 mm, first with 2°/.2-mm
steps, then 1°/.1-mm steps. Zero-thickness half-length is
`(.24−2e)/sin α`: independent spine and mirror lateral errors each consume e
at either side. This **only erodes the mechanical aperture**; target/ray errors,
pupil, backing, warp, attachment and operating clearance are not granted a pass.
The mirror exhausts that envelope, with no positive clearance at adverse contact.

Ground targets are front-face samples immediately above/below the load seam,
X=1.7, Y=.9(j−2)+.25, Z=±.08 for five lanes. Also test larger profile samples
Z=−.5/+.6. Pickup targets are actual front-face centers X=−1.7, Y=.5/2.2,
Z=−2.5, for active/clear. These are minimum access samples, not a full image or
complete contact patch. The ray must reach the +Y face from in front.

| Target set | Best fine-grid α / Z | Half-aperture reserve, e=0 / .05 mm |
|---|---|---:|
| Ground seam only | 45° / 0 | +.2270 / +.0856 mm |
| Ground profile | 47° / .2 | −.5628 / −.6995 mm |
| Pickup centers only | 45° / −2.5 | +.3394 / +.1980 mm |
| Ground seam and pickups | 75° / 2.7 | −1.9527 / −2.0562 mm |

Reserves are along the mirror. Both grids agree on the sign of all these cases;
the pickup coarse grid misses its better centered solution. Combined-case optima
move substantially, so do not call this a converged global impossibility proof.
No all-angle, alternative-camera, perforated-strip or changed-rack exclusion.
Seeing only a seam is not rejected merely because the whole profile does not fit.

But **stacking the individual survivors does not assemble a reader**. For the
45° lower strip at Z=−2.5 with Y half-width .14, all **200** camera-to-upper-mirror
rays (20 columns ×10 seam points) strike its finite opaque surface. This occurs
before any mirror backing or housing is added. Offset paths, more cameras, another
scan pose or different geometry must be constructed and counted.

Testing the lower strip alone against real finite spines at every neighbor height
blocks **3/20 active-pad center rays**, versus **0/20 clear-pad center rays**.
One witness is column 0 at h=0: mirror point (.01176,2.54,−2.5) to pad center
(−1.7,.5,−2.5) crosses its own spine. A hidden active pad could legitimately cause
rejection; occlusion alone is not false acceptance. Other solids and full images
remain unqualified. The surviving clear rays do not establish state discrimination.

## Seeing an output is not necessarily observing its state

Three mechanism controls separate depth, topology and capacity:

| Family | What the proposed view can miss | Consequence |
|---|---|---|
| Direct head / positive support | Visible contact seam can coexist with inadequate depth overlap, broken grounding, or E-056's unfavorable pressure location | Actual contact geometry and a retained load path remain necessary; no optical strength certification |
| E-166 comb hook | Along +Y, a toe extending Y=0…1 versus 0….3 has the same XZ silhouette, but a rack starting at Y=.4 changes overlap from +.6 to −.1 mm | Depth/orthogonal view or a demonstrated loaded transfer is needed; this does not rehabilitate the failed rear backing |
| E-148 field jaw | Identical closed pad positions at summed normal force 120 N give 12 versus 2.4 N holding for assumed μ=.1 versus .02 | A closed image cannot distinguish adequate versus inadequate 10-N comparator capacity |

The hook witness is an orthographic finite-toe counterexample; perspective can
add depth information. The jaw example holds force fixed while friction changes,
not E-148's differently sized springs for different design μ. Ten newtons is a
comparison scenario, not a new product requirement. Neither is a reliability rate.

**The pickup alias survives finite perspective and small dimensional variation.**
The lower mirror's virtual camera is C=(48.26,60.04,−2.5). At column 10 the
nominal clear pad box is
`[48.6,49.6] × [1.2,2.2] × [−3,−2]`.
Scale every vertex about C by
`(60.04−.5)/(60.04−2.2)=1.02939142462`. This gives an active pad:

`[48.609993,49.639385] × [−.529391,.5] × [−3.014696,−1.985304]`.

Every edge is within **.039385 mm** of its nominal active position. All eight
vertices have identical normalized pinhole coordinates to the clear box, hence
identical untextured cuboid silhouette; the mirror clips the same rays. This is
an inter-part/unknown-geometry alias, not two states of one perfectly calibrated
part. It defeats guaranteed single-view classification over the declared ±.05
edge box without per-part knowledge. It is not a photometric rendering: calibrated
texture, illumination, independent depth, or learning both actual endpoints could
change the result. Fixed row fiducials cannot identify the unknown part shape.
At far-off-axis cells this particular homothety requires larger errors; no
whole-board common alias or false-accept probability is inferred.

A second X viewpoint breaks this specific alias. Baselines 5/10/20 mm give
.147/.294/.588-mm equivalent object-plane disparity, or 1.85/3.70/7.41 pixels
at the hypothetical 1,280 pixels per 101.6-mm field. This is an ideal separation,
not stereo accuracy, matching/contrast, physical access or a purchased sensor.
Both images need independently bounded errors; zero silhouette discrepancy in
the first image cannot compensate for an obstructed or stale second image.

## What common fiducials can actually correct

Assume apparent row displacement `b+s*x+A sin(πx/L)` with L=101.6 mm,
b=.7 mm, s=.003, A=.3 mm. These are labelled adversarial scenarios, not measured
warp. Endpoint calibration removes translation/scale exactly but leaves .3 mm
between them. With bounded curvature K=A(π/L)²=.000286836/mm, piecewise linear
interpolation on spacing d has error ≤Kd²/8.

| Intervals per field | Simulated maximum residual | Curvature bound + other errors |
|---|---:|---:|
| 1 | .3000 mm | .5301 mm |
| 2 | .0632 mm | .2525 mm |
| 4 | .0211 mm | .1831 mm |
| 8 | .0057 mm | .1658 mm |

Other bounds are .04-mm fiducial error + .04-mm residual optics + .08-mm local
part/mark error, combined adversarially, not in quadrature. Four intervals
(25.4-mm spacing) conditionally reach .2 mm; the curvature-derived maximum
spacing is 33.4 mm. Five fiducials/field become 1,600 placements over four cameras
and 80 rows, or 1,360 if adjacent field endpoints are actually shared. Location,
visibility, mark manufacture and correct row/frame association are still owed.
This does not imply 6,400 manual calibrations are necessary for height reading.

Without a curvature bound, arbitrarily narrow between-fiducial distortion remains
possible. A .25-mm local mark displacement is likewise invisible to stationary
references; adding row fiducials cannot reduce it. Shared mirror/print biases,
spatial bow, local shape and model uncertainty remain distinct. No X1C tolerance,
probability distribution, independent-cell assumption or board yield is asserted.
Hole/layer/first-layer effects, warp, roughness, wear and creep must fit the explicit
geometry/registration budgets; optical resolution is not finished-part accuracy.

## Full-machine consequence and decision

Keep E-176's actual pickup proofs and E-178's height-only limitation. Two copies
of its stopped scan cost 18.806 s: direct B4 + scans is 38.275 s; broadcast B4
40.300 s. A granted one-pass dual acquisition with .04-s row slots is 11.023 s,
and direct B4 + that scan is 30.492 s. These are incremental allocations, possibly
double-counting replaceable height checks; no blanket family rejection follows.
Credit overlap or remove old time only after identifying the replaced physical
observation. A lower mirror blocking an upper one earns no dual-acquisition credit.

Two complete strip layers would mean 320 module strips / 65.024 m before height
marks, mounts and cameras; actual access may demand different inventory. Preserve
6,400 ground and 6,400 pickup interfaces and the complete writer/drive/abort/recovery
boundary. No $500 BOM pass, assembly-time, print-time, regional-disturbance or
arrest improvement is established. On ambiguous output retain support and inhibit
ascent; do not accept missing pixels as clear. A persistent failure is outside
one bounded reacquisition, and a final scan cannot provide fast motion arrest.

**Stop** direct scanner transplantation, this stacked-strip repair, and single-view
uncalibrated silhouette clearance proof. Reopen with a materially changed path or
independent depth cue and actual output geometry, not a faster camera or code.
Shared height sensing remains conditional; no print/purchase is justified.

Next compare a reader carried by the already-required writer, with two viewpoints
of the actual pickup, against a mechanical proof that constrains travel until the
pickup is clear. First test depth/access and whether failed outputs physically
inhibit movement without 6,400 new precision relays. This is a competing verification
axis, not a reason to refine the failed lane keeper. Stop optical refinement if
access restores per-cell relays or sensing removes no replicated function; reopen
broader architecture discovery rather than another mirror-angle sweep.

Self-review: full 3D specular direction/path length independently checks the reduced
YZ search winners; nominal reflection limit; exact segment/box and segment/plane
witnesses; all eight perspective vertices; two search grids; 10,001 interpolation
samples checked against the analytical bound. No external review or continuous
nonlinear tolerance/optical certification is claimed.
