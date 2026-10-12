---
status: complete
builds-on: [E-208]
---

# Root registration can unload the rocking toe despite a clear extensible path

**Retain rocking only as a conditional lead; do not count its imposed seated
pose as a manufactured support proof.** All sampled extensible paths clear,
but root misfit changes strain, force and whether the toe can remain on its
ledges after tool departure. Symmetric ±.1-mm root registration includes cases
that need substantial downward load to maintain that pose. Tensile root bias
trades this issue for higher force and strain. A floating but still keyed
zero-load witness prevents rejecting the whole mechanism from that bound.

Input main `97ea127`; LAB-336. Evidence: constrained planar elastic-rod
simulation, finite extruded geometry, analytical contact-wrench bounds and
self-review. No measurements, fabrication CAD, calibrated manufacturing prior,
independent review, purchase or print. Reproduce using Python/NumPy:
`OPENBLAS_NUM_THREADS=1 python tools/curated-experiment-checks/E-209/return_path.py`.
JSON output is reproducible and disposable.

## Construction and bounded uncertainty

Inherit E-208's keyed toe, heel ledges, exact-fit reusable side blade, supported
rack lift of 1.5 mm, .22-rad heel rotation and 1.4-mm withdrawal. The writer
continues to impose all toe coordinates throughout release and reversed return;
this does not demonstrate passive reseating. Rack takeover and the blade's
manufactured fit remain unqualified. E-208 contains the finite construction,
load path and comparison with the guided slider and longer torsion return.

The return now permits axial extension at **every** pose, with normalized
energy `U/EI = sum(delta(theta-theta0)^2)/(2 ds)
+ (EA/EI) ds sum((stretch-1)^2)/2`, `EA/EI=12/t^2`.
It retains fixed root/end tangents and the inherited sinusoidal intrinsic
curvature. Trapezoidal tangent integration reconstructs the stretched centerline;
finite thickness polygons join the same rigid collar. The source follows a
local equilibrium branch forward and backward, checks positive constrained
Hessians, and tests leaf/frame, rack, jaw, blade, toe, self and adjacent-row
interference. The shifted finite root ledge/crossbar must still connect to both
side uprights, and both leaf end faces must join their supports. This is an
ideal clamped-root model, not a loose insert or an invisible translating root.

Two geometries are compared: `(L,a,t)=(12,.3,.4)` and `(11.5,.25,.45)` in mm
and radians, both .8 mm wide. The latter inherits E-208's near-taut endpoint
control. Each first has its own matching stress-free root; then relative
root-to-seat offsets are imposed at y=−.1/0/+.1 and z=−.2/−.1/0/+.1 mm.
Positive z shortens the root-to-toe distance. Negative z stretches it. A root
nominally lowered .1 mm with a ±.1-mm height error occupies the z=−.2…0 subset.
These **24 deterministic registration scenarios**, fixed throughout each cycle,
are explicit sensitivity bounds, not X1C capability or a probability model.
The neighbor shift of +.05 mm moves the preceding rack toward the active leaf.
Neighboring returns share the same root error; bank-wide or batch-wide errors
can therefore repeat the failure rather than average away. No independence or
board-yield inference is made. Intermediate parameter combinations are untested.

The material multiplier E=700…2200 MPa is inherited as an assumed range; it is
not a PLA fatigue or creep allowable. Dimensions, intrinsic shape and stiffness
ratio are not calibrated. Root pitch, spatial warp, thickness gradients,
anisotropy, layer weakness, joint compliance, roughness, wear, creep and dynamics
remain outside this homogeneous beam model. Single-extrusion .35… .45-mm stock
remains a process risk. Finite-fiber strain is first-order axial plus bending
strain; a reference-radius correction is reported as a discrepancy diagnostic.
Neither calculation is a nonlinear material or fatigue qualification.

## Full-path results and numerical checks

Six zero-offset runs refine both rod segments and subdivisions per motion
phase through 16/32/64. All clear. At 64 segments, the full cycle includes 257
poses; the 24 registration runs use 129 poses each at 32 segments. No sampled
self or adjacent-row collision occurs. The smallest preceding-rack y-projection
gap in the registration sweep is .366 mm. These are geometric checks under
imposed motion, not a proof of continuous collision clearance or valid motion
after tool release.

| Geometry, zero root offset | Peak absolute fiber strain, 16→32→64 | Peak force/EI, 16→32→64 (mm⁻²) | Largest fiber strain range over cycle, 64 |
|---|---|---|---|
| Nominal | 1.401→1.442→1.462% | .072254→.071371→.071148 | 1.629 percentage points |
| Shorter/thicker | 1.698→1.703→1.705% | .193826→.192308→.191925 | 2.187 percentage points |

**The nominal peak occurs at the end of rocking, before withdrawal**, rather
than at E-208's .988%-strain extensible endpoint. Axial compliance reduced that
endpoint's force but did not eliminate the rocking strain peak. Shorter/thicker
rocking and withdrawal maxima are close enough that mesh refinement exchanges
which is largest. Peak absolute strain and per-fiber cycle range are distinct;
half the latter would be an alternating amplitude, not a fatigue allowable.

Across the 18 unbiased ±.1-mm registration scenarios, full-path peak strain
spans 1.365…2.247% nominal and 1.703…3.188% shorter/thicker. Including the lowered
root's −.2-mm edge increases the maxima to 3.433% and 4.301%. The reference-radius
correction raises those last estimates to 3.544% and 4.436%; the uncorrected
homogeneous-beam prediction is not an exact material strain field.

All traced states have positive local constrained Hessians (minimum .1032
in model coordinates), residual <1.8e−10 and outward/reverse centerline mismatch
<6.9e−10 mm. Reversibility of this elastic quasistatic branch does not establish
unique equilibrium, absence of other buckled branches, hysteresis or dynamics.
Nine finite-difference work checks including misfit give error <3.9e−10 in
normalized units; residual Jacobians differ by <2.4e−9. An independent straight
axial-bar limit matches `EA delta/L` within 2.6e−15 normalized force. Reducing
t to .01 mm approaches the inextensible force within .0202%. E-208 endpoint
agreement is an inherited-model regression, **not independent validation**.
Hand-solvable support-wrench cases check the load-bound signs.

Additional 32/64/128-segment holdouts at rest, full rock and full withdrawal,
for both geometries at (−.1,+.1) and (+.1,−.2) offsets, change reported force,
strain and nonzero seating bounds by at most .531% between 64 and 128.
They refine these particular poses, not all extrema or a certified error bound.
The 32→64 nominal full-path strain still changes 1.35%; material and boundary
model uncertainty exceed numerical closure. No simulated yield probability or
lifetime follows from zero collisions.

## Why net upward force is not the whole seating condition

Let `(Fy,Fz,M)` be the external end wrench needed to constrain the leaf; its
wrench on the toe has the opposite sign. Upward ledge reactions total `W+Fz`
under a downward rack load W. They cannot pull the toe downward. Thus
`W >= max(0,-Fz)` is a necessary condition even before moment balance.

A second, deliberately favorable relaxation grants upward support anywhere
across y=−1…1.6 mm, including the heel, and the required single signed horizontal
key reaction at any height z=−.2…0. It ignores key end play and grants contact
that may not yet exist. It grants no friction, upper cap, arbitrary opposing key
couple or residual tool moment. With the attachment A=(−.6,−.2), let
`C = Ay Fz − Az Fy + M + zkey Fy`. Force/moment balance requires
`−(W+Fz) <= W yload+C <= 1.6(W+Fz)`.
The source minimizes W over the allowed key height and checks the resulting
reaction interval. The two pad-edge load positions are .8 and 1.2 mm.
This is a **necessary seated-pose load bound**, not a sufficient contact or
stability solution: a toe may move across its clearance, rock or jam instead.
No credit is taken for an unspecified miniature, deadweight or permanent tool.
Actual gravity at other locations would need its own wrench in this balance.

At root offset (−.1,+.1), 128-segment seated holdouts require at least
**.86…2.70 N** (nominal geometry) or **1.67…5.25 N** (shorter/thicker geometry)
for a rack load at y=1.2, across the assumed modulus range. Net-force-only
bounds are much smaller: approximately .12… .36 N and .24… .74 N.
The moment lever amplifies the required load because the upward spring force
acts behind the rack pad. The 0.1-N comparison case fails this seated-pose
condition throughout the assumed modulus range; no minimum miniature load is
a product requirement. This is not a conclusion that the keys necessarily
extract or that the entire mechanism loses all possible support.

Indeed, a separate finite **zero-load counterexample** translates the nominal
stress-free return and toe upward .1 mm with a centered root. It clears the
frame and a rack elevated .1 mm; its keys retain .1 mm of vertical socket overlap.
Thus floating above the ledges while still keyed is geometrically possible.
No loaded equilibrium, dynamic departure path, frictional jamming, height error
under service load or support strength is established for that alternative.
The correct next question is the unilateral-contact equilibrium after writer
departure, not an automatic demand for another 6,400 upper keepers.

Lowering the root is also costly. At offset (+.1,−.2), 128-segment full-withdrawal
holdouts give **3.44% / 4.31%** absolute combined fiber strain for nominal /
shorter-thicker geometries. Their normalized force magnitudes .80582 / 1.10749
mm⁻² imply **2.41…7.56 N / 4.71…14.80 N** across the assumed modulus range.
These are elastic-model outputs, not hardware forces or allowable strains.
Prestretch avoids some uplift but increases baseline strain and writer load;
it cannot be inserted into the architecture as a free assembly adjustment.


## Machine disposition and next discriminator

No architecture is selected or rejected wholesale. The change in evidence is
that root registration cannot be granted a matching, stress-free seated pose
for all manufactured fingers. A shared .1-mm root-height bias can affect an
entire 40-finger comb; all 6,400 returns still need supported behavior after the
writer leaves. Neighbor geometry passing does not prove unchanged-cell support.
Adding preload, a cap or an alignment operation must count its force, contacts,
assembly, wear and replacement burden. The E-054/E-056 slider and E-206 longer
torsion remain comparison leads, with their original limitations intact.

E-208's whole-machine cost and timing obligations remain: <30 s including
acquisition, motion, support proof, departure and retry; with illustrative 6-s
overhead, 40/80/160 heads allow <.15/.30/.60 s per cell. Root-biased force tails
and any added support-check operation consume head/frame and cycle margins;
there is no priced BOM or timing pass. No new purchased parts are authorized
or credited. All 160 comb placements and 6,400 return/seat interfaces remain.

**Next:** construct the unloaded/lightly loaded toe's unilateral-contact
relaxation after the imposed writer pose is released. Include key end play,
heel/ledge contact, rack load, retained key overlap and rack-height change;
compare unbiased and modest tensile root settings. Determine whether the toe
settles into an acceptable retained state or needs a changed load path/capture.
Do not call a raised but retained toe a failure solely for leaving its ledges;
quantify the consequence without inventing a new product tolerance. Stop this
embodiment if adequate retention requires a resident precision guide or if
force/strain and load-dependent motion erase its benefit over the controls.
Seat-clearance/blade-fit synthesis remains owed if this interface survives.
No print: an untested contact-state question currently has greater decision
value than measuring a single nominal curved leaf. No broad search saturation
or new fundamental principle is claimed.
