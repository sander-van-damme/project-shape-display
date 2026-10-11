---
status: complete
builds-on: [E-176, E-173]
---

# Sliding-cam pickup keeper fits locally but does not close the shared reset

**Stop this cam/leaf/straight-writer package.** A finite under-pad cam can avoid
E-175's overhead obstruction, but its broad capture is conditional on friction,
an additional shoe guide and substantial rail bracing. The tested straight writer
posts either collide or need unqualified .05-mm gaps. No complete keeper, writer
or machine is accepted. Broadcast safe-state reset remains a conditional function;
this rejects one implementation, not bistability or shared clearing in general.

Input main `a4b890b`; LAB-289. Reproduce:
`python3 tools/curated-experiment-checks/E-177/keeper.py`.
Evidence: generated convex-prism/box sections, ideal constrained quasistatic
contact, linear beam calculations and explicit bounded scenarios; self-review.
No fabricated parts, process calibration, full CAD, dynamic contact, independent
review, priced BOM or hardware qualification. Generated output is not retained.

## Concrete mechanism and what is still granted

E-176 supplies an individually armed pickup pad q=0, a clear stop q=1.7 mm,
and a shared reset tooth at deck home d=−2 mm. Ground supports carry every
column during pad setting/clearing; the keeper does not carry service load.
The new combination places a two-sided cam **below** the pad, with a leaf-driven
flat shoe pressing in X. Cam ascent stores spring energy; either descending
flank pushes the pad toward its corresponding stop. The row writer pushes from
the opposite Y side. Home reset pushes toward clear only. Actual pad observation
must inhibit deck ascent if a pad remains intermediate/active.

This is a finite embodiment of the ordinary cam-detent control, not a new
operating principle or an independent architecture search. It tests the specific
missing broad-keeper grant in E-176. Both explicit clearing and broadcast can
use a keeper; no advantage is assigned merely for adding one.

Geometry, mm, relative to the same cell/deck as E-173:

- Pad remains X=−2.2…−1.2, Y=q±.5, Z=d−1…d. A neck below it connects to
  a cam extruded over Z=d−2.4…d−1.4. Its local u=Y−q spans −.2…1.1;
  back X=−2.2, front `X=−1.75+.34−.4|u−.45|`.
- Shoe has Y=.9…1.7, Z=d−2.4…d−1.4, X thickness .6. Its left face is
  the maximum cam X within that Y footprint. Contact occurs at a shoe corner
  on each flank, or at the cam crest beneath the shoe. It never penetrates the
  actual convex cam polygon in the ideal X guide.
- Leaf is nominally 8 mm long, .6 thick in X and .8 wide in Y; neutral front
  X=−1.85. A conservative monotone-deflection box contains it below the shoe.
  Root connects to a longitudinal moving rail, X=−1.1…−.8, Z=d−10.9…d−10.4.
  This rail is a **clearance section**, not a proven structural support.
- The opposite-side writer tooth is X=−2.15…−1.35, Y=f…f+.4,
  Z=−2.8…−2.2 at home; f runs 2.6→.5. Reset uses E-176's connected tooth,
  post and rail. Local tooth access is modeled separately from the long writer
  shaft and carriage that must reach it.

The shoe's X prismatic constraint, pad guidance/end stops, lateral shoe force
reaction, external rail supports and reader are explicit unresolved interfaces.
The leaf envelope is not a nonlinear beam/contact solution. Granting the shoe
constraint makes this an optimistic discriminator: failure under the grant is
useful, while a pass cannot establish an unguided printed leaf mechanism.

## Finite clearance and access results

Separating-axis intersection of actual convex sections gives no nominal external
penetration in **150/210/570 part poses** at 1/4/16 subdivisions, including all
cam-contact breakpoints. Every pose checks all eight neighboring lattice sites,
five column heights and both pad states. Separate 8/20/68 home-interface poses
check reset and opposite-side arm sweeps. A holdout checks keeper neighbors at
all combinations of endpoints/contact breakpoints. The continuous separation is
also bounded by the X/Y envelopes: cam X≤−1.41; leaf/shoe X≤−.81; spine starts
at −.6; the root rail begins .2 mm inward of the parked comb tooth's X edge.
Cam Y spans −.2…2.8 and neck starts at −.4, clear of parked teeth at −1.3…−.9
and their 5.08-mm repeats. Contacts and intended root/rail bonds are excluded
from penetration. Z only separates additional parts further.

These checks cover a common deck inside one bank. Segmented-bank boundary
bridges, tilt, shoe-guide bodies and sensing geometry are absent. Independent
center and facing-edge bounds ±e consume up to 4e of a gap; rail/spine and
rail/tooth gaps of .2 mm have no strict margin at e=.05. Cam-flank corner contact
also needs edge rounding/contact stress and wear evidence, not a nominal area
allowable. No X1C accuracy or yield is inferred.

Local arm-tooth clearance does not supply its remote connection:

| Tested vertical post, from Z=−45 to −2.2 | Finite result |
|---|---|
| Outer X=−2.8…−2.5, Y=2.5…2.9 | Intersects parked reset rail by **.060 mm³**. |
| Inner X=−1.1…−.8, Y=1.35…1.75 at q=.85 | Intersects the keeper shoe. |
| Thin X=−2.45…−2.25 in the rail/pad corridor | .2-mm wall with **.05-mm gap** each side; strict margin requires e<.0125 under the four-term bound. |

Stop these straight-post routes. A dogleg/retracting head or moving reset rail
is not disproved, but requires new connected geometry and charged transport;
no such extra machine is assumed here. The failed outer route is independent
of dimensional variation.

## Capture, energy and friction

Finite shoe breadth creates a flat energy crest over **q=.45…1.25**, width
.8 mm. E-176's assumed snap threshold 1.0 is therefore not supplied by this
geometry. Reset must cross 1.25, while arming must cross below .45. At q=.85,
spring force exists in X but produces **zero restoring force in q**, even at
zero friction. A stalled reset may remain there indefinitely.

With threshold/stop errors ±e and command error ±b, positive reset margin needs
`1.25+e+b < q_command < 1.7−e−b`. The inherited command 1.35 loses strict margin
already at e=b=.05. At e=b=.1 the interval is only 1.45…1.50: changing command
can fix the ideal scalar window, but does not solve friction, rail compliance or
shoe guidance. These are independent bounded errors, not process distributions.

Linear cantilever relation `k=Ewt³/(4L³)` follows `I=wt³/12` and `k=3EI/L³`;
see [MIT's end-loaded cantilever problem](https://ocw.mit.edu/courses/1-050-solid-mechanics-fall-2004/fd4eff39aec922b8c07660006f40686e_pset04_11.pdf).
It supplies the beam model, **not PLA properties**. E=2,000 N/mm² is an assumed
central effective modulus. The resulting k=.16875 N/mm gives endpoint/crest
deflections .26/.44 mm, energy barrier **.010631 N·mm**, peak spring reaction
.07425 N, root bending strain .00619 and tip rotation .0825 rad. None is a
material-life acceptance. Two-axis linear leaf compliance without the shoe guide
would give about **.161 mm transverse Y displacement** at the uphill flank with
μ=.2; this exceeds the original .1-mm command margin. Rotation, torsion and
contact relocation require a coupled model before deleting the guide.

Resolving normal/friction forces on a flank of slope m=.4 gives, for spring
reaction S and separate pad/guide drag G:

`F_drive = S(m+μ)/(1−μm)+G`

`F_completion = S(m−μ)/(1+μm)−G`.

With G=.001 N, central minimum completion/peak drive forces are:

| μ | Completion near stop, N | Peak drive bound, N |
|---:|---:|---:|
| .1 | .01166 | .03967 |
| .2 | .00713 | .04942 |
| .3 | .00292 | .06006 |
| .4 | −.00100 | .07171 |
| .6 | −.00808 | .09870 |

Positive values are conditional quasistatic force margins, not snap times. For
μ≥m there is **no guaranteed self-completion even with zero separate drag**;
increasing spring stiffness cannot change that sign. Explicitly driving to each
stop can overcome cam friction but restores the stroke/individual-clear burden
and E-176's shared exact-stop mismatch. A stopped reset therefore needs actual
pad readback and continued inhibition, not inference from comb command/current.

A 96-corner sensitivity set uses E=1,000/3,000 N/mm², t=.5/.7 mm,
L=7.5/8.5 mm, μ=.1/.3/.6, G=0/.005 N and coherent preload offset ±.1 mm.
These deliberately uncalibrated epistemic bounds are neither sampled priors nor
fabrication acceptance. Minimum completion ranges **−.03333…+.05066 N**;
peak drive ranges **.00721… .35161 N**. If bank geometry/materials make all
1,600 B4 pads adverse together, reset force spans **11.53…562.58 N** before
comb friction, deformation and dynamics. Central μ=.2 gives 79.08 N.
No independence, force-tail probability or zero-failure claim is made. Some force
corners also exceed nominal geometric envelopes; this is sensitivity, not a joint
feasible population. Creep/preload loss, fatigue, layer anisotropy, roughness,
first-layer effects, warp and wear remain uncertainty, not hidden priors.

## Shared rail closes the optimistic section

The .3×.5-mm longitudinal rail has lateral EI=**2.25 N·mm²** at the central E.
Grant simple supports at the ends of one 20-row, 101.6-mm bank rail. Twenty
aligned .07425-N spring reactions, at half-pitch-spaced stations, require
EI≈**405,985 N·mm²** to keep lateral displacement below the chosen .05-mm
alignment budget: a **180,438× stiffness shortfall**. The budget is a scenario,
not a product requirement. This does not predict a gigantic real deflection;
the linear model is used to reject the small-deflection condition.

Independent checks sum simply supported point-load compliance and use uniform
load `w=S/5.08`, `δ=5wL⁴/(384EI)`; they differ by .1%. Under this section/law,
the latter permits an unbraced span only **4.931 mm** for .05-mm displacement,
less than one row pitch. Thus a nominal clearance rail cannot supply the spring
reaction. Actual transverse bracing or a different deep support topology must
be generated and cleared. End fixity alone cannot close this order-of-magnitude
shortfall. No same-sign bias is averaged away. The reset comb itself still needs
its separate force/stiffness proof.

Source also checks spring strain energy against the independent unit-load
integral, integrates zero-friction cam work, reconstructs 2D contact equilibrium
for both travel senses, and includes frictionless/self-locking limiting cases.
Geometric refinement does not validate constitutive law or impact dynamics.

## Machine comparison and disposition

E-176's conditional B4 allocations remain **22.919 s explicit / 21.494 s
broadcast with scan / 19.469 s direct**. This experiment does **not** promote
21.494 s to an executable machine time: reset completion, support structure and
writer access remain unresolved. A 1.425-s modeled saving is insufficient reason
to assume these interfaces away. Known local-update/readback tradeoffs remain.
Five nominal levels still span 40.4 mm at 5.08-mm pitch; no requirement is relaxed.

A cam can be integral to each of 6,400 pads, but adds a flexing keeper and
shoe/cam contact per site, plus the additional constrained shoe interface in this
model. Broadcast adds its 6,400 teeth/posts and four B4 reset drives. Bought parts
are unpriced; a printed spring is not automatically a bought cost. An added
$.02/site costs $128; a 10-s/site operation is 17.8 h. No slicing or scrap estimate
exists. Ground selection/support, bank input-loss arrest and reader false
acceptance are still unresolved in the comparison architectures.

Stop detailing this package. Reopening requires a materially different reaction
support and writer route, plus either demonstrated μ/drag margins or a retention
principle without sliding-cam self-locking. Do not print a friction coupon yet:
geometry and bank support already prevent accepting this embodiment, so that
measurement would not change the disposition.

The useful next search axis is **reducing setter/readback replication while
preserving positive grounded support**, comparing direct heads, shared lift and
E-148's field-selected jaws. First cross-check existing mask/coincidence and
mechanical reader work; generate concrete cost/throughput causal alternatives
before another keeper optimization. Broad reset can return if a different family
already supplies a supported bistable selector. No architecture is selected.
