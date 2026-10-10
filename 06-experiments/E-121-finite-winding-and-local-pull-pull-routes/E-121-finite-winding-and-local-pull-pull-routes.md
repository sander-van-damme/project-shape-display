---
status: complete
builds-on: [E-120, E-099]
---

# Finite winding collides; a local loop clears travel but does not retain tension

**No complete routing/return mechanism is admitted to torque-lock development.**
Reject the tested four-plane helical route at a finite neighboring-core collision.
Retain a different, cell-local pull-pull loop as a **geometric building block**:
it reaches continuously through 40 mm, but its fixed-center/fixed-length embodiment
loses tension inside the declared length/compliance box. Retire dependent private
head and whole-machine work for these embodiments. Reopening requires a finite
preload-maintaining or positively engaged transmission, not another drum radius.
This is a bounded exclusion, not impossibility of tendon machines.

Input main `9916ce0`. Reproduce with standard-library Python:

```
python3 tools/curated-experiment-checks/E-121/finite_routes.py
```

Optional `--scad PATH --winding-scad PATH` exports reproducible primitive geometry;
do not retain generated output. Evidence: generated finite curves, solid primitive
bounds, continuous swept-envelope calculations and self-review. No physical tests,
process calibration, material selection, priced BOM, CAD-kernel/contact solve or
qualified machinery. The installed OpenSCAD launcher points to a missing binary;
its rendering attempt failed. SCAD is uncompiled construction source. Numerical
checks below operate directly on the generated primitives and curves.

## Generation, topology coverage and stopping

Deterministic rules; no random seeds or generic optimizer. Pitch 5.08 mm, nine
initial workload heights 0:5:40 mm, all 81 ordered pairs including identities.
Other dimensions are design assumptions. Curves carry finite 0.30-mm cord diameter.

| Embodiment | Memory / force / route | Result |
|---|---|---|
| Four-plane helical gravity spool | Independent anchored winding; positive locked angle would support tension; gravity supplies descent | Finite rising strand intersects a shallower neighboring spool core; gravity also fails the minimum-mass force box |
| Split antagonistic spools retaining that lifting branch | Second end pulls downward, separate takeup | Reject inherited colliding branch before constructing the remaining return member; not counted as a complete generated pair |
| Cell-local pull-pull loop | One cord, both ends captured at the column carriage; two sheaves, lower sheave privately driven/retained; no accumulating winding | Full-travel geometric survivor; friction/preload and fixed-length slack witness prevent force acceptance |
| Perimeter itinerary | E-120 nearest-edge routing, external retained drums | Control only: reproduced its corridor checks; still lacks finite end fanout/return machinery |
| Direct rack heads | E-099 independently acquired rigid column | Simple control; no cable preload or sheaves, acquisition/price still unqualified |

The loop is a change of topology and storage coupling, not a better four-plane
packing. Each column owns its entire loop; no shared reset or neighbor unlock is
introduced. Neighbor support is conditional on a future private retainer **and**
non-slipping tension path; neither is credited as an implemented machine.

## Finite helical failure witness

Seed radius `r=40/(4π)=3.183099` mm; actual groove pitch .6 mm, cord .3 mm,
one dead turn and a finite anchor. Axial planes are 5 mm apart, colored
`x mod 2 + 2(y mod 2)`. Core radius `r−d/2=3.033099` mm; full groove/anchor axial
span fits the displayed 2.45-mm core envelope. Export shows core, axle, anchor
and wound/path curves; stop before detailed groove-wall/rim fabrication geometry.

The outgoing helix tangent has slope `a/r`, `a=.6/(2π)`. A tangent quarter bend
of radius r/2 redirects upward, then a top half-circle of radius r/2 redirects
toward the descending column anchor. Include exit rise, top bend, winding takeup
and tail motion. Exact taut closure is

`h = [sqrt(r²+a²) − a] θ`.

Using circumference alone misses the shrinking free leg as the exit rises.
Consequently 40 mm needs **2.060900 active turns**, plus the dead turn. Helical
length quadrature discrepancy decreases .098707 → .024686 → .006172 → .001543 mm
for 96/192/384/768 segments; the independent analytic length change is zero.

Translate a bottom-plane site to XY=0. Its vertical riser crosses
**(3.183099, 1.543824, −22) mm** inside its upper-plane right neighbor, centered
at (5.08,0). Riser radial distance is 2.445737 mm. Even the entire cord cross
section lies inside the neighbor's solid core by **.437362 mm**. This is not
merely an overlapping rim envelope. Riser XY is independent of height and its
vertical span straddles that core throughout 0–40 mm. Exact endpoint/monotonic
bounds support the continuous witness; 41 height evaluations are a cross-check.
Changing groove pitch alone or adding an antagonistic member cannot remove it.
Different cross-layer itineraries, drum placement or internal pitch are not excluded.

Gravity descent needs `m g > Fguide + Frouting + Fresidual_drive` over the whole
stroke, without relying on a miniature remaining aboard. Explicit competing
boxes: moving mass .3–3 g; guide drag .005/.03/.1 N; routing loss .001/.01/.05 N;
residual drive drag 0/.01 N. Required mass is **>.612–16.310 g**. The .3-g minimum
fails even the least-drag scenario; maximum-box ballast alone would exceed 104 kg
for 6,400 cells. These are assumed force bounds, not friction measurements or a
universal ballast prohibition. No gravity return through 40 mm is demonstrated.

## Local loop geometry and continuous checks

Two sheave centers are (0,−1.3,0) and (0,−1.3,48) mm, axes parallel to y.
Cord centerline radius 1.5 mm, core radius 1.35, flange radius 1.85, width 1 mm;
open groove width .5 mm. The .8-mm shafts have 1-mm bearing bores and two finite
cheeks apiece. Do not substitute a closed toroidal cavity for an open groove.

The carriage at z=4+h captures two .6-mm terminal beads at z=4+h±.4, behind
.34-mm cord bores in .64-mm spherical seats. A two-part clamp must be joined
around them; closure fasteners/process and strength are **unqualified**. Finite
seat walls/web include .13/.16-mm features: this is a serious repeated fabrication
risk, not a print-ready termination. Bead containment is checked; loaded seat
contact/creep and assembly under dimensional error are not.

A T-section stem and slotted guides at z=10 and 40 prevent the clamp bridge from
colliding with a closed guide ring. Stem flange: x±.7, y=1…1.5; web: x±.3,
y=.1…1.2; length 86 mm, occupying z=h−34…h+52. Side/lip/back guide primitives
leave nominal .3-mm sliding clearance. The clamp finger passes the lip opening;
the bridge stays forward of the guide. Lowest guide remains engaged at maximum
height by 3.2 mm. Caps are 4.68-mm squares, 1.2 mm thick. Tail travel is modeled.

One finite cord goes from upper bead up the right span, over the upper sheave,
down the left span, under the lower sheave and back to the lower bead. Its length
is **104.624778 mm**, invariant with h; lower sheave rotates **4.244132 turns**
per full stroke if traction holds. There is no helical pitch or cross-layer
passage in this topology. Its bend diameter/cord diameter is 10, unqualified.

Exact swept unions of translating boxes cover every intermediate h, old/new pair
and arbitrary neighboring heights. Cord's union is two straight spans and two
semicircles, with intended groove/termination contact separated from obstacles.
Piecewise quadratic segment-to-box distance is exact for chords; arc sagitta
inflation makes the clearance conservative. At 192 chords/semicircle:

- Translating solids versus fixed solids: minimum .300 mm.
- Cord versus unrelated solids: lower bound .554136 mm; sagitta .0000502 mm.
- Neighbor full-sweep hull separation: .400 mm, including unequal caps/tails.
- Entire cell sweep: x,y±2.34; z=−34…93.2 mm, a 127.2-mm height envelope.
- Reserved under-map approach box: x±1, y=−1.8…−.8, z=−38…−1.95 mm;
  .1-mm clearance to machinery. **An empty approach box is not a torque head.**

24/48/96/192-chord refinements converge; exact circumference/straight-length and
translation invariance checks are independent bounds. No vertical sampling gap
is hidden in a nine-height pass. Cable self-contact away from adjacent curve
segments is excluded analytically by 3-mm straight-span separation and disjoint
upper/lower arc slabs. These are rigid, taut geometry results, not sag/contact
or frame-deflection predictions.

## Force closure, uncertainty and the decisive slack corner

The flexible-line capstan bound `Thigh/Tlow ≤ exp(μ π)` follows
[Slocum, FUNdaMENTALS Topic 5, pp. 5-3–5-4](https://pergatory.mit.edu/resources/FUNdaMENTALs%20Book%20pdf/FUNdaMENTALs%20Topic%205.PDF).
It supplies an equation, **no cord/PLA friction property**. With instantaneous
mean drive tension P and demanded tension difference F,
`F < 2 P tanh(μ π/2)` is the strict no-slip condition. Positive P−F/2 prevents
slack. Reverse motion exchanges the loaded branches; geometric reach is unchanged.

Assumed load .05/.2/.5 N, all drag 0/.05/.15 N, μ=.05/.15/.3; no distributions.
Worst F=.65 N, μ=.05 needs **P>4.146534 N**. A hypothetical maintained
P=4.5…5 N offers at least .705409 N traction, requires up to .975 N·mm torque,
26.666667 rad stroke, 5.475-N terminal capacity and 10.3-N shaft reaction bounds
(including conservative extra idler-loss allowance). Offset guide moment at
.5 N and assumed guide μ=.3 contributes .029155 N drag; it is charged within,
not added for free beyond, the .15-N all-drag allowance. No fit or bearing model
establishes that allowance. Force/torque work identity is checked.

**That preload is not implemented.** The generated fixed-center route has no
adjuster, compliant tension keeper or positively engaged belt teeth. Effective
axial rigidity EA=20/200/2000 N and free-length error ±.5 mm are competing
uncertainty scenarios. The linear taut estimate is `ΔP=−EA ΔL/L`; negative
predictions mean slack, not compressive cable force. At EA=2000 N, nominal P=4.5 N,
+.5 mm excess length gives **−5.057965 N → slack**, invalidating transmission
and support. The same error can be a common batch/cutting bias across a board.
To retain worst-case traction from P=4.5 N at EA=2000 N allows only **+.018491 mm**
free-length drift, before additional load redistribution, seating, creep or wear.
No such accuracy or retention is established. An ideal externally prescribed
preload must not be passed downstream as completed machinery.

Conservative load-change height bound `.65 L/EA` is 3.400/.340/.034 mm;
EA≥136.012 N would be needed for an illustrative .5-mm error budget (not a product
requirement). At 5.475 N, axial strains are 27.4/2.74/.274%; the low-EA linear
estimates are outside a small-strain model and not credible material predictions.
A homogeneous .3-mm monofilament bent at 1.5 mm has outer-fiber geometric strain
10%; flexible braided behavior, fatigue and hysteresis cannot be inferred from EA.
An actual cord construction is an unresolved interface input, not a chosen material.

Geometric error boxes use independently opposed location/size errors ±e, giving
nominal clearance−3e. e=.025/.05/.1/.2 mm yields neighbor margins
.325/.250/.100/−.200 mm and guide margins .225/.150/0/−.300 mm. Pulley side gaps,
axial bearing gaps and the approach roof start at .1 mm and admit interference
already at e=.05. Common rigid translation cancels; common solid growth .05 mm
closes opposing .1-mm gaps. Common radius bias .1 mm changes an angle-only 40-mm
command by 2.667 mm. Common length bias changes preload rather than canceling.
These boxes are neither X1C priors nor independent-cell yield estimates. Anchor
seating, shell warp, roughness, layer anisotropy, creep/wear and frame correlations
remain unmodeled; they cannot improve the demonstrated bad corner by assumption.

## Consequence and retained interfaces

Retain executable helical taut-length correction, the core-intersection witness,
local loop/guide/clamp finite geometry, continuous clearance evaluator and the
conditional load envelope above. **Do not proceed to private lock detail, machine
pricing or printing for the fixed-length loop.** A locked sheave cannot support a
slack/slipping cord. Reopen with generated, load-reacting preload control covering
length/compliance/creep and assembly errors through all 40 mm, or finite positive
engagement replacing friction; verify the cord construction/bend and termination
capacity alongside it. Wider internal pitch and changed routing remain legal.

The loop would still repeat 6,400 cords/clamps/preload settings/locks, 12,800 ends,
12,800 sheaves/axles, 25,600 bearing interfaces and 12,800 guide stations. Its cord
alone totals **669.599 m**, before end-making allowance/spares, versus E-120's
740–881 m incomplete perimeter itinerary. Thus “local” does not mean negligible
cord or assembly burden. Cost, print time, durability, <30-s updates, output
readback and recoverable support remain unestablished; E-099 direct heads retain
their conditional comparator status. No whole-product Pareto winner is claimed.
