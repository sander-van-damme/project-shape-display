---
status: complete
builds-on: [E-269, E-268, E-267]
---

# Actual-pin readback above solid supports

**Retain post-undock top stereo as a conditional architecture comparator; reject the tested central-patch decoder as verification.**
Narrow local stereo reaches deep empty wells at both pitches. Two shared cameras can cover16 coarse cells from a tall mounting, but
actual image correspondence, calibration, acquisition rate and hidden-pin coverage remain unqualified. Contact probing is a slow
diagnostic. No hardware selected.

Reproduce with `python3 tools/curated-experiment-checks/E-270/verification.py --check`, `python3
tools/curated-experiment-checks/E-270/shared_field.py --check` and `python3 tools/curated-experiment-checks/E-270/image_evidence.py
--check`; omit flags for scenario tables. Python/numpy. Evidence: analytical bounds, ray/box calculations, synthetic images, fault
witnesses and conditional schedules. Self-review, not physical validation or rated force/RPM, manufacturing yield or optical accuracy.

## Support and observation transaction

Retain E-269's opaque bed/keeper, solid screws, intact guides and proposed ribs. Pin→thread→collar→bed→frame carries downward load;
locked keeper→ribs carries docking uplift. Readers neither release support nor take over load. Fine-frame adverse clearance remains
failed.

|Route|Disposition|
|---|---|
|Underside after socket withdrawal|Opaque support still hides pin; screw angle aliases stripped threads. Reject as sole proof.|
|Top stereo after undock/settle|Reads integral terrain cap without support holes. Conditional comparator.|
|Top contact probe|Independent measured Z reaches exposed cap; force/release unqualified. Diagnostic.|
|Lift, observe, restore|Final hidden lowering can fail after successful read; no higher exposure above maximum neighbors. Reject final proof.|
|Witness tail|Adds4096/6400 passages/integrity duties; detached witness aliases top. No refinement.|
|Remove miniature, inspect, replace|Changes loading and hides pin again. Interrupted service only.|

Transaction: stop→undock(.1-s allocation)→settle(.1 s)→fresh actual-cap observation with cell identity→ accept/reject/unknown. Retry
only from a known stable measured state; retain supports. Signed10→20/20→10 missed sockets or stripped threads fail height checks
without identifying cause. Driver-assisted height followed by release slip defeats in-drive proof but fails post-release inspection.
Later creep remains unseen. Stale, occluded or misidentified returns are unknown; persistent fault/unknown has no finite promised
recovery duration.

An opaque25.4-mm miniature base bridges adjacent pins: hidden center heights0/−1 produce identical visible base positions and probe
contacts. Neither modality certifies the hidden pin. Exposure10→50→10 adds80 mm, ≥1.882 s rotation at assumed850rpm/lead3 before
overhead, can lift miniatures, and leaves a final hidden move. Neighbors at50 preclude higher exposure. Removing/replacing m miniatures
at assumed5–15 s/touch adds10m–30m seconds before readback/reloading; not measured or owner-approved UX. Clearing neighbors violates
isolation.

## Local access

Use E-261's assumed integral closed4.4-mm cap, not an open tube/detachable cover. Lowest cap z=0, highest neighbor z=S; actual lowest
tops88/98 at S40/S50 stay above guides/ribs. Pupils at x=±b/2,z=S+H have.5-mm diameter and view a.4-mm central square. Independent±e
pupil/target placement and neighbor expansion give sufficient margin `m=p−2.2−e−[(b/2+.25)t+.2(1−t)+e]`, t=S/(S+H). Affine extrema
occur at the high neighbor's top; higher targets shorten obstruction. Square pupil envelopes conservatively bound circles.

|Pitch / S, mm|b4/H20/e.2 margin|b4/H60/e.2|b20/H20/e.2|
|---|---:|---:|---:|
|6.35 /40|2.183|2.730|−3.150|
|6.35 /50|2.086|2.618|−3.629|
|5.08 /40|.913|1.460|−4.420|
|5.08 /50|.816|1.348|−4.899|

Ray/box checks confirm wide-case collisions. b4 also clears e=.4. H60 leaves20 mm above an assumed40-mm prop at the pupil plane;
housing/lighting unconstructed. Any miniature across the rays blocks them. Assumed f1200/.1-pixel disparity gives.208/.252-mm
sensitivity at D100/110,b4; not achieved accuracy.

Probe radius.5 plus placement.2/bow.2 gives.9-mm sweep,1.1-mm landing margin and3.05/1.78-mm neighbor clearance. Empty-board reach45/55
mm becomes100/110 at H60. Assumed.05-N contact at effective stiffness .1/1/10 N/mm deflects.5/.05/.005 mm before backlash/frame motion.
No safe force, metrology, crash limit or hands-off retention follows from contact height.

## Complete conditional waits

E-267's16-output writer, physical river/ravine arrays,133 nonempty four-square reveal windows per depth; scenarios, not observed
sessions. S40/N20 versus S50/N30, assumed850rpm/lead3/1000 rev/s². Replace20-ms proof with undock/settle/read; pay macro seeks/return,
docking/drive,4-s common allowance and1-s reader deployment. Grant an upper carrier keeping pace; no drive/proof overlap. Stereo16
grants16 simultaneous100-ms readings and32 local pupils. Stereo1 pays100 ms/cap plus selected-column X travel/return and≥50 ms/move.
Probe1 adds full45/55-mm search/retract at50 mm/s,500 mm/s² plus100-ms contact; H60 adds2.2 s/cap including retry. Release after
probing is not observed again. These are unoptimized conditional scenarios.

One immediate station retry pays full stroke because a stable post-release fault can leave any height; regenerate from fresh
measurements, never blindly replay delta. Lost support/damage stops for service.

|Pitch / S|Reader|Local max,s|Scene max,s|Cold neutral,s|Dense stress,s|
|---|---|---:|---:|---:|---:|
|6.35 /40|Stereo16|24.84|226.69|248.93|369.40|
|6.35 /50|Stereo16|28.84|253.98|309.40|429.87|
|5.08 /40|Stereo16|46.62|328.48|381.30|569.54|
|5.08 /50|Stereo16|56.26|368.48|475.65|663.89|
|6.35 /50|Stereo1|81.30|683.95|1102.34|1222.81|
|5.08 /50|Stereo1|135.33|990.01|1629.43|1817.66|
|6.35 /50|Probe1|734.10|5961.55|10971.14|11091.61|
|5.08 /50|Probe1|1133.73|9200.41|17027.83|17216.06|

Exposed-cap waits compare with~30 s, not occupied-play certification. Source includes serial S40 cases. Cold preparation plus map
update is first use; dense stress is separate. Without mechanical isolation evidence, changed-only reads cannot certify unchanged
neighbors. An added full-board Stereo16 scan costs73.62/110.26 s at64/80; Stereo1 costs866.56/1264.04. Baseline scans cost as much
again and still miss covered pins/later load response.

Top sensing adds no per-cell holes/marks/mirrors/bores/tails/sensors to4096/6400 pairs/seats,8192/12800 guide apertures or126/158
two-layer ribs. Stereo16 has32 pupil/relay duties (nominal4.5-mm envelope before errors), upper XY, registration and lighting.
Bodies/electronics unconstructed. Stereo1 adds inner X; Probe1 adds measured force-limited Z and stylus maintenance. Ten extra seconds
finishing each cap adds11.38/17.78 h.

## Two-camera shared field

For k adjacent cells, center width W=(k−1)p, baseline b and height D above lowest cap, a sufficient margin is
`m=p−2.2−2e−((W+b)/2+a/2)S/D−.2(1−S/D)` for pupil diameter a and e=.2. Low edge caps are limiting. Assume1920 horizontal pixels with10%
reserve: `f=.9×1920×(D−S)/(W+b+.4+2e)` pixels. At low caps, d=fb/D; bounded.1-pixel disparity gives exact worst depth error
`D×.1/(d−.1)` with calibration perfect. The original triangulator receives supplied correspondences, not images.

|Pitch / S, mm|k / D / b, mm|Margin at a=.5|Depth-error bound, mm|
|---|---|---:|---:|
|6.35 /50|4 /300 /16|.621|.047|
|6.35 /50|8 /600 /30|.444|.095|
|6.35 /50|16 /600 /40|−2.090|.129, blocked|
|6.35 /50|16 /1000 /40|.166|.207|
|5.08 /50|4 /300 /16|−.332|.042, blocked|
|5.08 /50|8 /600 /30|−.456|.084, blocked|
|5.08 /50|16 /1000 /40|−.628|.178, blocked|
|5.08 /50|16 /1000 /12|.073|.452|

S40 coarse k16/D1000/b40 margin.843/error.205; fine k16/b40 remains−.046. Fine k4/D300 and k8/D600 clear S40 at.191/.091. Samples, not
global optima. [Edmund Optics' diffraction
explanation](https://www.edmundoptics.com/knowledge-center/application-notes/imaging/limitations-on-resolution-and-contrast-the-airy-disk/)
(accessed2026-10-13) gives ideal Airy diameter2.44λ(f/#); paraxial object-space radius≈1.22λD/a. At550 nm, D1000/a.5 gives1.342 mm
versus.2-mm patch half-width. a3.4 reduces radius to.197 while coarse S50 margin is.0938 mm. Patch width4.83 pixels. This does not
qualify texture, focus, aberration, contrast or centroid accuracy; stop before refining that small geometric margin into hardware.

Uncorrected.1% fb bias produces1-mm error at D1000;10-µrad relative yaw contributes≈.25 mm at b40. Synthetic incorrect neighbor
matching at D300/b40/p6.35 returns41.10-mm height from a flat scene. Its inferred x is off-grid; lattice gating rejects that witness,
but not a whole-pitch camera/grid registration error. Independent identity and calibration are required.

k16 uses two pupils instead of32, with950-mm overhead above highest S50 terrain. Arms, cables, transport, illumination and player
access remain real costs. k4/k8 permit lower stations with inner scanning: pay.1-s undock once, then.1-s settle+.1-s acquisition/group,
selected-group moves/return, deployment and retry.

|Coarse S40 /S50|k4|k8|k16|
|---|---:|---:|---:|
|Local max,s|50.72 /54.72|38.24 /42.24|24.84 /28.84|
|Scene max,s|447.19 /473.31|343.41 /370.71|226.69 /253.98|
|Cold neutral,s|640.09 /700.56|451.45 /511.92|248.93 /309.40|
|Dense stress,s|760.56 /821.03|571.92 /632.39|369.40 /429.87|

Fine k4/k8/k16 local maxima82.28/65.90/46.62 s at S40 and91.92/75.54/56.26 at S50, granting suitable optics; the geometry table
identifies failed fields. k16 reproduces the original schedule exactly. E-267's dated $497.68 subset/reserve
leaves$2.32/$502.32/$1002.32 under$500/$1000/$1500 for all missing drive/frame/optical hardware; no sourced complete BOM or purchase
authorization.

## Pixel correspondence discriminator

Render16 opaque4.4-mm prisms (z=−10 to cap) into two1920×24 images using
[OpenCV's distortion-free projective model](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html)
(accessed2026-10-13). Include side occlusion; neighbor-row access still relies on earlier ray checks.
Compare uniform caps with an ideal view-consistent four-sinusoid texture, periods≈.22–.78 mm: neither
observed PLA nor constructed projection. Use2×2 pixel integration, assigned Gaussian blurσ=.4/1/2 px,
zero or bounded±2/255 noise, seed73. No fitted optical/noise priors, finite pupils, lighting shadows,
distortion, defocus variation, glare or motion. Gaussian blur does not replace diffraction analysis.

Decoder searches0–50 mm at.1-mm steps using pixels and granted board coordinates, never commanded
heights/correspondences. Compare25 bilinear samples per.4-mm patch. Gates: RMS difference≤.01 and both
patch standard deviations≥.02 in unit intensity; surviving heights span≤.5 mm, otherwise unknown.
Outputs are **candidates, not accepted terrain**; narrow sampled sets are not confidence intervals.
Other stereo/edge/silhouette methods are untested. Flat25, alternating0/50 and ramp rows plus two noise
cases give96 cell cases per table row, not a reliability sample.

|Pitch /baseline|Texture /blurσ|Candidates /96|Errors>.25 mm|Maximum matched error, mm|
|---|---|---:|---:|---:|
|6.35 /40|Uniform /each blur|0|0|—|
|6.35 /40|Ideal /.4|84|0|.20|
|6.35 /40|Ideal /1|9|7|1.00|
|6.35 /40|Ideal /2|0|0|—|
|5.08 /12|Uniform or ideal /each blur|0|0|—|

**Reject this gate as verification.** Even noiseless flat25 at blur1 yields two narrow wrong candidates. Texture gating can exclude
true low-contrast hypotheses while retaining another height; blur/resampling also break the assigned photometric model. The
favorable84/96 cannot qualify the decoder: flat25/.4-blur matches fall9→1→0 with2/4/8× integration and.1/.05/.025-mm height grids.
Threshold sensitivity reaches13.6-mm error at RMS.02/contrast.02; no convergence or calibrated confidence claim. A.2-pixel uncorrected
right-image shift gives nine wrong flat-scene matches with.4-mm error; .5 pixel gives1 mm. Fine-grid unknown is scoped to this
short-baseline/tiny-patch matcher, not all stereo methods.

Whole-pitch misregistration assigns the neighboring0-mm cap to a50-mm checkerboard cell. An independently identified frame fiducial at
known x/z instead exposes6.35/5.08-mm registration residual; lattice agreement does not. This is a shared reference duty, not a per-pin
mark. Actual fiducial detection is not implemented.

## Metric reference discriminator and decision

For `d=A/(D−z)+q`, A=fb, inject±.1% scale/±.2-pixel offset, D1000 and independent bounded reference/target
disparity errors. One known z=0 reference cancels offset with nominal A; references0/50 fit A/q exactly
without noise. Frame identity/metrology must be independent of screw commands. Unknown D, pose, distortion
and bending are unmodeled. Maximum errors over corner errors and five heights:

|Pitch /baseline|Each disparity error, px|Uncorrected, mm|One reference, mm|Two references, mm|
|---|---:|---:|---:|---:|
|6.35 /40|0|1.416|.048|<1e−9|
|6.35 /40|.05|1.520|.235|.208|
|6.35 /40|.10|1.624|.422|.418|
|5.08 /12|0|1.907|.048|<1e−9|
|5.08 /12|.05|2.134|.455|.456|
|5.08 /12|.10|2.361|.904|.921|

Fine±.025-pixel error gives.227 mm with two references. The.25-mm comparison is diagnostic, not an approved terrain tolerance. Shared
references remove much uncorrected drift; two do not automatically beat one under bounded noise. Detection, rigidity,
placement/visibility after moves and acquisition time remain unpaid. The earlier1-mm uncorrected bias is not an unavoidable floor for
referenced readout.

**Stop passive central-patch and optical-margin refinement.** Retain top observation conditionally, but 100-ms all16-cap proof remains
an optimistic allocation. Shared illumination or other visible features may supply evidence without per-pin additions; neither is
implemented. Real or independently modeled image formation/segmentation must earn a decoder before optical hardware selection. Hidden
miniature-bearing pins remain unknown even with perfect calibration. Unknown cannot trigger a blind loaded-pin motion retry. Mechanical
isolation/retention need separate qualification; no sensor substitutes for support.

No new resident parts, STL, print, purchase or hardware pass. Return architecture effort to missing shared rotary-drive
routing/assembly rather than another tiny optical clearance optimization. Preserve this failure as the condition for reopening
readback, not a claim that all optical feedback is impossible.

Checks cover finite rays, supplied-coordinate error bounds, covered-pin/identity/transaction faults, conditional timing anchors, raster
projection, a rejected decoder witness,2/4/8× integration sensitivity and exact/noisy reference reconstruction. Source prints counts
and full scenario tables; models only.
