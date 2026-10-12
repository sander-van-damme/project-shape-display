---
status: complete
builds-on: [E-212, E-211, E-209, E-206, E-054, E-056, E-124, E-125]
---

# Axial tail access clears translation; passive guide take-up recouples the capture

**Retain axial docking geometry; stop the tested passive sleeve/tight-pin
combination as a separated load path.** A short pin avoids the through-pin's
neighbor collision. Longitudinal separation removes E-212's jaw/guide crossing,
but the guide-contact poses intersect the pin in all nine tested cases. The pin
would carry transverse reaction before the intended guide couple develops.
Depth staggering clears head packing but introduces a slender-tail compression
failure. These reject embodiments, not axial access, staggering or guides.

Input main `f22e1a8`; LAB-340. Evidence: generated convex prisms, exact axis sweeps,
prescribed rocking samples, rigid contact limits, elastic and timing scenarios;
**self-review only**. No measured process priors, priced BOM, fabrication or
hardware qualification. Run `OPENBLAS_NUM_THREADS=1 python
tools/curated-experiment-checks/E-213/tail.py` (Python/NumPy). E-212/E-208 provide
rack/frame geometry and collision predicates. JSON is disposable. This is
functional recombination, not new fundamental physics or broad search saturation.
E-124/E-125 already expose remote guide-play and retained-cup failures; new
results here concern finite tail/pin contact, docking and depth-dependent stock.

## Construction and load paths

Coordinates follow E-212: x across columns, y toward rack, z upward; mm/N/MPa.
Rack h=0…40 plus 1.5-mm unload. A 1.6×1.6-mm tail centered at y=1.95 has bottom
z=−76+h and overlaps the widened moving web by .1 mm. Its last 34.1 mm contains
a through-window at local z=1.5…2.5, y=−.5….5: two .3-mm side ligaments, a
1.5-mm bottom bridge and solid stock above. Local coordinates reference the
tail bottom and y center.

The reusable sleeve has 3.7×3.7-mm outside dimensions, 2.1×2.1-mm aperture,
1-mm floor below z=0, four .8×.8-mm corner posts and four-sided bearing bands
at z=5.5…6.5 and 17.5…18.5. Posts connect bands and floor. A right-side pin guide
at x=1.05…1.85 has finite walls around aperture y=±.4, z=1.6…2.4. These are
bearing solids, **not implemented drives or qualified fits**.

| Combination | Causal load path / outcome |
|---|---|
| Cup without pin | Rack end → floor → height drive; sleeve contacts carry transverse reactions. Positive upward force only; no controlled pull-down against adverse drag or unloaded capture. Gravity/friction is not granted as a return. Compression-only control. |
| Cup + through-pin | .6×.6-mm pin spans x=−1.85…1.85; 2.95-mm withdrawal clears tail but reaches x=4.8. It hits the next shaft at 5.03-mm pitch, with target h=20 and neighbor h=0. Stop this access route. |
| Cup + short pin | Pin spans x=−.6…1.85; 1.7-mm withdrawal gives x=1.1…3.55. Floor bears downward load; pin/window face bears opposite height force; separated bands are intended to carry moment. Prescribed geometry clears; passive contact take-up recouples pin and guide. |
| Short pin + alternate depth | Actual head solids clear independent height/dock phases at tested 80/82-mm offsets; 20/40/60/62 mm fail. Account at 82 mm, not an optimized minimum. Extended stock fails the 10-N compression screen below. |

Resident load-path comparison uses E-211's uncut rocking toe, wider keyed
seats and 1.2-mm withdrawal. Collision checks use E-212's conservative filled-
pocket toe envelope; E-211's .02-mm bowed released-pose acquisition is not rerun.
Rack tooth → toe body →
heel/forward ledges → grounded frame is the service path; keys locate the toe.
The return is not the tabletop support. Cup height force and guide moment
must be established **before** the toe releases. Its independent y/z/pitch tool
and acquisition remain necessary: the lower head cannot reach it. E-211's
four-shoe tool and E-212's cap remain failed/conditional controls, not repaired
components. Thus there is **no complete supported machine survivor**.

E-054/E-056 remains the grounded sliding-pawl control: 6,400 guide fits and
25,600 shelf faces, with pressure eccentricity, attachment and unloaded capture
unresolved. E-206's favorable longer torsion return needs ~20–22 mm at its 10-N
scenario and still owes lip/yaw fit. Neither supplies this writer's release.

## Finite reach and acquisition

Start with floor 20 mm below the tail bottom, leaving its upper band 1.5 mm
clear. Raise to actual floor contact, insert pin, prove takeover, unload 1.5 mm,
release toe, translate, restore/prove resident support, retract pin and lower
below all tails before horizontal transport. A nominal command proves neither
contact nor support.

Exact swept solids clear nominal docking/departure, pin travel, independent
neighbor-shaft heights 0…40 and all twenty unequal five-height transitions.
Head and tail move together; the pin never traverses the guide bands. The old
E-212 jaw/guide control still clears at 1.099 and collides at 1.101-mm lift.
Existing toe rocking/withdrawal clears at 16/32/64 subdivisions (33/65/129
poses); elastic return and continuous whole-path clearance are not re-proven.
The 76-mm length is an allowance, not a minimum. A 60-mm tail hits a resident
ledge at 41.5-mm lift; 66 mm was not rejected. No carrier, motor housings or
cable bends were constructed. These prescribed sweeps do **not** cover the
failed loaded poses below.

All **64 parallel-fit corners** clear: head x/y ±.05 mm, tail half-size ±.05,
window half-size ±.05, pin axial registration ±.05 and pin half-size ±.02.
Minimum pin/window gap is **.08 mm**. These are deterministic uncertainty
bounds, not X1C distributions; bank/stock biases and reusable-head errors may
be common cause. Separately rotate actual tail prisms about the bottom and
seat their lowest point on the floor. Among 16 pitch-sign/x/y/size corners,
collisions are **0 at ±.005 rad, 4 at ±.01, 16 at ±.02**. No lead-in or automatic
centering is modeled. This is not the full joint angular/size uncertainty set.

## Separated faces are not a separated loaded path

For 10 N at y=.8 versus a centered floor reaction at y=1.95, reference moment
is 11.5 N·mm. A contacting 12-mm guide pair needs **.958 N**, versus E-212's
.583 N for 7 N·mm. Full-area floor pressure is **3.906 MPa**, versus E-211's
177.8-MPa opposed-jaw scenario. These are reference allocations, not actual
pressure distributions or material allowables; floor-edge contact changes them.

For tail half-width a and guide half-aperture b, the finite-band limiting pose
at opposite edges z=5.5/18.5 solves:

`13 tan(theta) + 2 a / cos(theta) = 2 b`, with `y(z)=(z−12)tan(theta)`.

Exact rotated tail prisms clear the actual guide in all nine combinations
of a=.75/.8/.85 and b=1/1.05/1.1 mm. At pin plane z=2, however, center offset
is **.2304….5368 mm**, nominal **.38371 mm at .038352 rad**. Pin/window transverse
clearance is only .2 mm. Actual solid intersections occur in **9/9** cases;
both pitch signs have the same coupling. An installed pin limits motion first:
it becomes a moment member or binds. This is a contact incompatibility witness,
**not a dynamic equilibrium or proof that every load reaches that pose**.
External column guidance could prevent it, but must be built/counted. Actual
load arm, floor pressure and pin reactions need a coupled contact solve.

A favorable pull-force resultant at x=0 is 1.05 mm beyond the pin-guide root.
Gross beam demand `6 F*1.05/(.6*.6²)` is **29.17/291.67 MPa at 1/10 N**.
Ligament bending, bearing, stress concentration, friction, compliance, fatigue
and creep are unmodeled; this is not a material failure measurement. Metal
pins would consume the same head allocation and still need qualified guides.

E-209 return demands remain: **2.247/3.188%** nominal/short-thick root-error
strain; **3.44/4.31%** and up to **7.56/14.80 N** at the −.2-mm tensile edge.
These are inherited old-path elastic scenarios, not new maxima. No tensile bias
or hidden toe guide is reinstated. Lower rack capture does not remove E-211's
toe-tool section/force problem.

## Depth and full-board consequences

Adjacent short-pin heads clear at equal height because a pin enters the next
sleeve's open bay; independent heights produce collision. Sweep relative phases
through ±61.5 mm, including 20-mm park and 41.5-mm lift. The 82-mm offset clears
head solids. A through-pin aimed at a deeper neighbor still hits its continuous
shaft: staggering flanges does not remove material above them. A shallow head
also hits a deep shaft when indexing across columns at its usual park. Two-tier
heads must stay in their assigned column depth while indexing rows (finite
route clears), or charge extra lowering below the deeper tails.

Smooth stock between last guide and web junction grows from 15.6 to 97.6 mm.
For 1.6-mm square stock, I=1.6^4/12 and ideal pinned Euler load is
`pi² E I/l²`; fixed/fixed is four times this. E=500/2200/3500 MPa are **assumed
elastic scenarios, not sourced PLA grades**. At 97.6 mm even fixed/fixed gives
**1.132/4.979/7.922 N**, below the 10-N comparison load. The unbuilt web endpoint
receives favorable ideal fixity. At 15.6 mm pinned values 11.07/48.73/77.52 N
merely avoid this rejection. Imperfections, eccentricity and creep are omitted.
Rayleigh energy quadrature recovers the fixed/fixed eigenvalue at 32/64/128
intervals (relative error <3e−16). Larger/stronger tails, intermediate guidance,
lower loads or relocating teeth/retention can reopen this topology. No new
product depth/load requirement or universal stagger ban follows.

| Obligation | H=40 / 80 / 160, or board total |
|---|---|
| Tail head | 80/160/320 guided outputs: H vertical axes + H pin slides; 80/160/320 moment-guide stations, eight faces/head plus floor and pin bearing |
| Resident/tool | 6,400 toes/returns, 12,800 keys/socket interfaces, assumed 160 comb placements; four-shoe control adds 160/320/640 guided outputs, plus toe y/z/pitch and carrier positioning |
| Added cell burden | 6,400 integral tails/windows and 12,800 thin side ligaments; no new assembly joint, but repeated fit, inspection and repair |
| Single depth | 40 heads/row at 10.16-mm spacing: 1/2/4 longitudinal rows for H=40/80/160; actual carriers/indexing still owed |
| Two tiers | H=80: one 80-head row; H=160: at least two physical rows, each in two tiers. A 160-cell row at 2.54-mm pitch is not a routing solution. |
| Under-datum depth | Parked floor 97 mm below toe datum; 179 mm for deeper tier, before actuator/carrier thickness |
| Added material | ~547.94 cm³ tail stock/board; half-board 82-mm extension adds 671.74 cm³. Sleeve 76.666 mm³/head before drives. No print-time/scrap estimate. |

Head slides off the tail from below; no loose captive cell pin. Comb service
still requires supporting its cells. Full-width modules exceed the 256-mm bed;
registration, tall-tail straightness and fixtures remain unmodeled. A hypothetical
ten-second window inspection totals 17.78 h, not a measured assembly rate.
Shared frame must react loads: aligned 10-N/head loads sum to 400/800/1600 N.
No rigid carrier, harmless jam or cancellation is granted.

With 6-s map overhead, strict service slots are **.15/.30/.60 s**. Safe horizontal
park is below the lowest tail: dock distance is 20+old-height; departure is
20+new-height. Add two 1.5-mm unload/reseat moves, height difference and two
1.7-mm pin strokes. Rest-to-rest triangular time is `2 sqrt(distance/a)`;
no velocity limit is favorable. Maximum five-height cycle is 10→40 or 40→10,
also the continuous maximum of this model, rather than 0→40 alone.

| a (mm/s²) | Motion alone (s) | Including .08 / .16 / .32 s auxiliary |
|---:|---:|---:|
| 1,000 | 1.50256 | 1.58256 / 1.66256 / 1.82256 |
| 5,000 | .67197 | .75197 / .83197 / .99197 |
| 20,000 | .33598 | .41598 / .49598 / .65598 |

Auxiliary time includes toe acquisition/release/return, registration, settling,
support proof and bounded retry. Map overhead includes common transport/home,
not free height preposition. **0/9 scenarios fit H=40 or 80; 2/9 fit H=160** as
necessary conditions only: loaded mechanism, motors and recovery are unproved.
A continuous-motion/overlapping schedule must be constructed before claiming it.

`Cshared + H*chead + 6400*ccell < $500`; with $250 elsewhere, head allocations
are **<$6.25/$3.125/$1.5625**, less resident purchases. Free heads instead leave
<$0.0390625 per resident bundle. At $400/$200 total, the same reserve leaves
$150/negative residual. These are allocations, not quotations. Printed volume,
precision, scrap and assembly remain costs even without a formal print ceiling.

## Proof, uncertainty and disposition

The executable state sequence requires continuous resident/head support and
forbids departure on failed proof; its flags are **obligations, not sensors or
force simulation**. Takeover needs observed floor load, pin engagement and rack
pose. Return needs resident seating plus head unloading without rack descent.
A .04-mm backoff fits the .08-mm parallel-gap bound, but sensing, tilt and false
acceptance are unbounded. Failed proof retains capture and stops the module;
source-loss arrest is absent. False-acceptance p implies 6,400p expected missed
supports regardless of independence. No reliability probability is reported.
Unchanged cells keep seated toes; frame compliance/jams can still disturb them.
Warp, hole shrink, first-layer/layer effects, roughness, anisotropy, wear and
creep are unresolved. No iid yield or regional-disturbance pass follows.

**Stop** the long through-pin route, passive short-pin/sleeve load separation,
and 82-mm staggering of unbraced 1.6-mm tails at the 10-N scenario. Keep axial
access and single-depth multirow packing. Do not tune miniature windows or print
coupons while resident release and the load path remain unsolved.

**Next recombination:** compare load-centered axial writing with explicit
resident moment guidance against a reusable guide that acquires the real pose
and permits transverse float at height capture. E-124/E-125's bilateral cup is
a control, not new novelty: its retained channels fail compact packing and its
sparse layout still loses overlap during loaded closure. Require a changed
contact/access topology, one finite supported acquisition/departure, resident
release tool and real guide/drive inventory before further optimization.
Reopen this tail only if capture avoids unintended moment without worsening
head allocations or repeated precision. Self-review checked connected solids,
old failure witnesses, sweep/touch limits, contact compatibility, safe-park time
and energy/section limits; no independent challenge is claimed.
