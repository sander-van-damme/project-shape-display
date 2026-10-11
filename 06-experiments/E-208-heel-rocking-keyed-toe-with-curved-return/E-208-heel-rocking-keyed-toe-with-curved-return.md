---
status: complete
builds-on: [E-207, E-206]
---

# Rocking clears the keys; shallow curved return trades clearance for cyclic strain

**Retain the shallow curved-return rocking toe as a conditional geometric lead.**
E-207's key collision is avoidable without a resident axle or full-stroke guide:
rock the unloaded toe about its rear heel, then withdraw it. A finite reusable
blade in a side pocket supplies the imposed translation and pitch. A shallow
precurved return accommodates the attachment rise that the previous straight
inextensible leaf cannot. Deeper curves collide with the preceding row's rack.
This is a changed release topology, not a new fundamental operating principle,
complete writer, reliability pass or architecture selection.

Input main `88c44f5`; LAB-335. Reproduce with
`OPENBLAS_NUM_THREADS=1 python3 tools/curated-experiment-checks/E-208/rocking.py`
(Python + NumPy; imports E-207/E-166). Evidence: finite extruded polygons,
constrained planar rod equilibria, analytical key bounds and self-review.
No physical measurements, calibrated process distribution, independent review,
fabrication CAD, purchase or printing. Generated JSON is disposable.

## Mechanism, support and actual input

Inherit E-207's 5.08-mm cell pitch, thick 3-mm-wide toe, inset rack pad,
paired keyed ledges and five 10-mm-spaced height positions over 40 mm. Dimensions
are mm; x crosses columns, y points toward the rack, z is upward. E-207 remains
the source for grounded service-reaction and rack-capture limitations.

Add heel ledges at y=−1.05…−.7, z=−.8…0, on both existing side supports
x=±(.85…1.7). The unloaded toe rotates .22 rad (12.605°) about (y,z)=(−1,0),
then translates 1.4 rearward at that angle. These ledges provide actual heel
contact; **there is no pin and no assumption that a unilateral heel contact
alone controls the trajectory**. The reusable tool supplies that control.

A blind side pocket occupies x=−1.5…−.9, y=−.6…−.3, z=.8…1.2. The source
constructs the remaining toe as connected finite pieces around this pocket.
A blade spanning x=−2…−.9 enters from −x and connects to a shank at
x=−2.2…−1.8. Its opposite pocket faces supply signed planar forces and a pitch
couple. This model grants exact closed fit, not a free physical fit solution:
an adjustable/preloaded interface, lateral retention, force limiting and actual
head drives remain owed. Three controlled planar coordinates (y,z,pitch), plus
blade acquisition, are now explicit writer obligations. A cam may couple them,
but no cam has been constructed. There are 6,400 new passive pockets, not 6,400
new moving guides; tool wear, roll moment from one-sided engagement and pocket
strength remain unqualified.

The E-207 C jaw acquires the rack before release and lifts it **1.5 mm** to
clear the rising pad. Blade insertion, jaw acquisition and lift have 33 sampled
poses apiece. During release the rack stays on that jaw; its 10-N service
scenario still requires up to 40-N upward/30-N downward jaw reactions. The blade
only controls the unloaded toe. Positive blade/socket bearing reactions are
constructed for the planar rod end wrench; the small slot is not a qualified
three-dimensional clamp. No friction credit is needed for that planar wrench.

On return, reverse the same imposed path with the rack still supported, lower
onto the pad, prove support, then depart. Reversal is a quasistatic geometric
witness, not a demonstration of passive spring reseating, dynamic capture,
jam recovery or source-loss arrest. No model grants that an apparently closed
key or blade depth proves rack support. The nominal compressive service
reactions and unchanged-cell support remain those of E-207; common frame
flexibility, tilted loads and actual load sharing are unsolved.

## Key clearance and its narrow manufacturing margin

At 32/64/128 subdivisions per phase, finite toe and blade bodies clear the
frame, lifted rack and C jaw. The open toe/rack y-projection gap is **.462667 mm**.
The source also checks adjacent row/column bodies; this is not whole-machine
head transport. Unchanged toes remain seated rather than being reset.

Eight deterministic socket corners combine end play .07/.13, relative socket
translation ±.05 and key depth .15/.25, held coherent throughout each path.
All clear. This reuses E-207's bounded scenario, not an X1C accuracy prior or
eight statistically independent trials. Relative minimum end clearance is .02.
For the deepest key, the maximum outward excursion of the front-bottom corner
is `sqrt(2.15²+.25²)−2.15 = .014486 mm`, leaving only **.005514 mm** reserve at
the tightest corner. The rear edge moves forward while still below the ledge,
so it does not strike the rear wall. At .22 rad, the lowest key point is
`1.85 sin(.22)−.25 cos(.22) = .159750 mm` above the ledge. This independent bound
covers continuous rocking of the rectangular keys; the rest of the bodies
have sampled, not certified continuous, collision checks.

These tiny worst-corner reserves do not establish manufacturability. Additional
socket shape error, roughness or angle error can reverse the result. Increasing
end play trades clearance against lost motion and reduced bearing margin;
it is not cost-free. The tested path assumes a valid initially seated fit and
exact tool pose. No yield probability follows.

## Curved-return equilibrium, collisions and strain

Keep the .8-mm-wide return and its finite tapered collar. Replace the straight
leaf by a stress-free planar centerline with arc coordinate s, nominal L=12,
and tangent angle from +z `theta0(s)=−a sin(2πs/L)`. The toe attachment is
(y,z)=(−.6,−.2). The root is placed below it by the integrated reference height;
it joins the grounded crossbar. All sections have finite thickness, and the
last leaf face is checked against the transformed collar face at every pose.
The nominal a=.3 curve has .268485 mm of arc-length slack and a root-to-tip
height of 11.731515 mm. A straight 12-mm inextensible rod cannot reach the
rocked attachment; an extensible straight return is a different, untested
constitutive option, not a forbidden principle.

The solver minimizes `U/EI = sum((delta(theta−theta0))²)/(2 ds)` subject to
both endpoint coordinates and the imposed end angle. A Newton/KKT solve with
line search follows the branch. Local constrained Hessian positivity is checked;
it is not a global uniqueness or snap-through proof. Length coordinates use
trapezoidal tangent integration. Elastic modulus scales force; geometry is
independent of its value in this homogeneous inextensible model. The
[Elastica theory documentation](https://www.cosseratrods.org/cosserat_rods/theory/)
provides the reference-curvature constitutive law and distinction between
Kirchhoff bending and stretch/shear-capable rods (accessed 2026-10-11). This
implementation is a planar reduction, not a run of PyElastica or a material
calibration.

| Reference angle amplitude a | Finite return-path result at 32 segments/subdivisions | Peak outer-fiber bending strain, t=.4 |
|---|---|---|
| .3 | No sampled collision | 1.434% |
| .5 | Hits preceding row rack after 1.00625-mm withdrawal | 1.705% counterfactual full path |
| .7 | Hits preceding row rack already at rest | 1.849% counterfactual full path |

Motion after first collision is counterfactual, not a physically executed
sequence. More slack does not monotonically improve the architecture: it buys
lower tension by consuming adjacent-row space. No extra service aisle is free.

For the a=.3 return, 16/32/64/128 segment and command subdivisions all clear;
peak strain is 1.389/1.434/1.455/1.465%. Peak force divided by EI converges
.093526/.092365/.092072/.091998 mm⁻²; the 64→128 force change is .080%, while
the peak strain still increases .70%. These are discretization observations,
not a rigorous error bound. Finite energy differences at three holdout poses
agree with force-plus-moment work within 3.25e−10 in normalized units. The
stress-free reference has zero calculated energy/load; the source checks
endpoint residuals, positive local constrained Hessians, leaf/collar continuity
and compressive support-reaction balances. Self-review only.

Eight additional coherent return scenarios combine L=11.5/12.5, a=.25/.35,
t=.35/.45 and the preceding row shifted .05 toward the leaf. All sampled paths
clear in the inextensible model. Full-path bending strains span **1.289–2.711%**.
However, the shorter/flatter curve approaches a taut chord: peak force/EI
ranges .02540–2.34530 mm⁻² across these scenarios. These corners have matching
root placements and reference shapes, rather than a random independent-cell
manufacturing distribution. They do not include arbitrary initial misfit.

This force tail exposes a **constitutive-model failure**, not a credible 31-N
hardware prediction. With assumed E=700/2200 MPa and t=.35/.45, the inextensible
force screen reaches 31.35 N, but its implied axial compliance is no longer
negligible. An independently assembled extensible rod adds segment strains,
normalized axial stiffness EA/EI=12/t², and the same intrinsic bending law.
At full withdrawal, 32/64-segment holdouts give:

| Geometry | Inextensible force/EI, 64 segments (mm⁻²) | Extensible force/EI, 32→64 (mm⁻²) | Extensible maximum axial / combined fiber strain, 64 segments |
|---|---:|---:|---:|
| L=12, a=.3, t=.4 | .092072 | .071371→.071148 | .09486% / .98776% |
| L=11.5, a=.25, t=.45 | 2.157667 | .192308→.191925 | .32386% / 1.70311% |

The adverse extensible force is **.816–2.565 N** for the assumed modulus range,
roughly an order of magnitude below the inextensible estimate. Finite-difference
Jacobian checks differ by <2.4e−9, equilibrium residuals are <1.5e−14 and the
holdout constrained Hessians are positive. These richer **endpoint holdouts do
not certify the full extensible collision path or its maximum cycle strain**.
The nominal inextensible force range is .275–.864 N; its ideal pocket bearing
construction can require about 1.29–4.06 N at individual opposing contacts.
Such forces require actual contact area and tool stiffness, not just a small
net force. No strain value is a sourced PLA fatigue, creep or strength allowable.
An illustrative .5%/1%/2% cyclic-strain ceiling would change the disposition;
none is established by this experiment.

The model uses a stress-free manufactured curve and matching root placement.
Bias in free shape, root/collar registration, layer quantization, first-layer
thickening, warp, joint stiffness and shared clamp distortion can preload the
leaf and prevent seating. Those effects are not absorbed into invented random
noise. X1C/PLA with .4-mm nozzle remains the baseline; a .35–.45-mm leaf may be
single-extrusion and needs process qualification. Anisotropic stiffness,
interlayer fracture, creep, fatigue, wear and collar stress concentration are
unmodeled. Rod/toe self-weight, inertia and damping are neglected. Local thickness
changes affect inextensible-model force cubically and strain linearly;
a homogeneous modulus bound does not represent a layered beam.

## Machine consequences and next decision

The comb still allocates 160 placements for 40 fingers each, with 6,400 toes,
returns and side pockets and 12,800 keys/socket fits. No separate toe inserts,
axles or resident translation guides are added. Ground/clamp assembly,
replaceability of a failed finger, jaw drives, blade drives and proof sensors
remain real burdens. The E-054/E-056 guided slider is the service-support
comparison; E-206's longer torsion strip remains an alternative with different
lip/seat and stock constraints. Neither is displaced by this limited success.

Full-machine timing still requires all preparation, acquisition, unload,
rock/withdraw, up to 40-mm height motion, return, support proof, departure,
settling and bounded retry within <30 s. With the inherited illustrative 6-s
shared overhead, 40/80/160 heads allow strictly <.15/.30/.60 s per cell. Added
pitch control and blade docking have no demonstrated duration. Purchased cost
remains `Cshared + H*chead + 6400*ccell < $500`, preferably $200–400 or less;
there is no priced BOM or reliability/timing pass. A failed return must leave
the rack on the writer; common power loss and false support acceptance remain
unresolved rather than credited to the curved spring.

**Next:** discriminate the shallow return's manufactured seat/tool fit and
cyclic deformation before detailed recovery or fabrication. Synthesize a
larger-clearance seat and a positive reusable capture with bounded registration,
then compare the resulting repeated fits and writer complexity with the slider
and longer torsion controls. Stop if the benefit requires another resident
precision guide or if plausible return variation consumes the clearance/strain
margin. A small process test becomes useful only after a surviving interface
has a prediction it can calibrate; no print is justified to reproduce the
already modeled deep-curve collision. No broad search saturation is claimed.
