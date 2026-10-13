---
status: complete
builds-on: [E-264, E-156, E-259]
---

# Side access removes tail extraction, not contact and reaction duties

**Retain the 6.35-mm friction route as a geometric escape; stop before selector
or head CAD.** It replaces E-264's 43/53-mm withdrawal with a 3-mm tip lift.
The finite neck rejects the positive-contact envelope at a modest labelled
error bound. The 5.08-mm transit corridor has only .140-mm nominal clearance.
Even the coarse roller needs a credible force reaction and independent selective
engagement. There is no qualified system advantage or fabrication recommendation.
This is a bounded screen, not a rejection of all side-driven rotating nuts.

Reproduce: `python3 tools/curated-experiment-checks/E-265/side_access.py`
(`--check` for controls). Standard library, disposable JSON. Evidence: exact
cylinder/capsule envelope calculations, elastic beam calculations and conditional
schedules; self-review only. No physical measurements, fitted process priors,
gear CAD, purchase, new owner question or change to E-263's optional job.

## Finite connected route

Keep E-264's nut thread z=[0,10], translating screw [u−S−2,u+12], S40/50,
u=0…S, 1.6-mm thread envelope radius, guided nonrotating upper stem and stationary
thrust/radial beds. The union of all tail positions is used, including unchanged
low neighbors. Neither travel nor neutral position is changed to clear the tool.

Explicit **new geometric allocations**, not historical printed dimensions:

- Nut drive rim radius2.2 at z=[−3.5,−2.5]; connecting neck radius1.75 at
  [−2.5,0]. Lower bed envelope radius2.4 at [−.5,0], with shared connecting webs
  at/above that slab; upper capture stays above the service plane. The central
  thread/tail passage remains open. Nut load still goes to captured thrust faces,
  not through the writer. The rim/neck can be integral with the nut.
- Tool wheel radius.8, height2, service z=[−4,−2], transit [−7,−5]. A connected
  radius.5 shaft runs to a bridge bearing at/below −(S+5); the entire bridge is
  below even the lowest screw tail. The shaft is included in the sweep. Motors,
  bearings and transmissions below that plane are allocated, not packaged CAD.
- Transit along x=p/2 between screw columns. At an interstice (p/2,p/2), lift3mm;
  move diagonally toward one of its four surrounding nuts; stop drive and prove
  hold, reverse that diagonal, lower3mm, then seek along the corridor. Opposite
  rows and columns use mirrored routes. External edge access gets a half-pitch
  perimeter bay. Separate bank bridges stop in their own row ranges.
- Positive side pinion: assumed pitch radii2.0/.6, outer radii2.2/.8,
  center distance2.6. Intended tooth-envelope overlap is explicitly exempted
  **only for the target rim**. This is an open lateral gear-contact allocation,
  not a validated tooth mesh. Friction roller: center distance2.95, giving .05mm
  total nominal closure against a 2.2+.8=3.0mm radius sum. Its actual contact
  stiffness and traction are unknown.

For constant-height segments, exact minimum distance from every obstacle center
to the line segment checks the whole swept cylinder, not just sampled endpoints.
Vertical lift uses the full axial union at fixed XY. Screw tails, rim, neck and
bed are separate obstacles. Four target/reverse paths include both adjacent rows;
all non-target rims are always forbidden. Same-quadrant row tools also retain
more than one tool diameter of center separation at arbitrary engagement phases.
Intentional engagement cannot be inferred
from the absence of collision. Bearings, tooth phases and recovery remain unbuilt.

| Geometry, mm | 6.35 pitch | 5.08 pitch |
|---|---:|---:|
| Wheel-to-tail transit gap p/2−1.6−.8 | .775 | .140 |
| Lift cavity clearance to rims | 1.490 | .592 |
| Positive tool-to-target tail / neck | .200 / .050 | .200 / .050 |
| Friction tool-to-target tail / neck | .550 / .400 | .550 / .400 |
| Minimum entire positive route | .050 | .050 |
| Minimum entire friction route | .400 | .140 |

The initial rim/tail-only positive sketch missed the connected neck; the final
model includes it. A straight side approach at fine pitch also hits the opposite
unchanged rim (−.520mm gap); diagonal approach removes that witness, not the tight
transit or neck. Nominally both routes clear non-target solids. Subtract coherent
**total gap erosion** E=0/.15/.30/.60mm, representing adverse combined radius,
relative registration, bow and frame errors, not separate independent draws or
X1C priors. At E=.30, coarse friction leaves .100mm; positive gives −.250mm and
fine friction −.160mm. At E=.15 fine friction already fails by .010mm. These
are sufficient bounded-clearance comparisons, not probabilities or calibrated yield.
Neighbor rim spacing and bed disks also fit nominally (fine bed gap .28mm); bed
manufacture/strength and globally correlated frame shifts have no qualification.

The 1.75−1.60=.15mm gross neck radial stock, before passage running clearance,
is a **repeated manufacturing warning**,
even though it principally transmits drive torque, not miniature thrust. A .2-module
interpretation of the positive radii implies20 resident/6 tool teeth:81,920/128,000
resident teeth, tiny tool teeth and an unqualified low-tooth-count mesh. Do not
assume standard involute compatibility or solve this with another micro-tooth
campaign. Molding or machining a rotor might change the process envelope; it does
not remove thousands of neck/thread/traction duties. The envelope is not ready to
print. The inherited ~.4-mm-nozzle process has not earned these repeated margins.

## Force and support: the tool must reach and react

All torques .05/.35/1Nmm, roller friction .15/.30/.60 and metal shaft E=200GPa
are labelled scenarios, not measurements or selected materials. For nut torque T,
positive contact Ft=T/2, illustrative20° pressure-angle radial force Ft tan20°;
friction contact requires N≥T/(2.2μ), with tangential force T/2.2. These are force
balance calculations. [KHK's spur-gear reference](https://khkgears.net/pdf/spur-tech.pdf)
(checked2026-10-13) requires matched module/pressure angle; it supplies no rating
for this hypothetical small pinion. No catalog gear is selected.

At T=.35Nmm, positive Ft=.175N, radial=.0637N, resultant=.186N. Roller N is
1.061/.530/.265N for μ=.15/.30/.60; at μ=.30 resultant=.554N. At K32/head the
coherent roller normal sum is16.97N/head (33.94N across two heads), before guides
and acceleration. The frame reacts net loads; each slender shaft still carries
its local load. Neighbor torque is excluded geometrically only while those gaps
remain; frame compliance or failed retraction can invalidate isolation.

For a bare cantilever, I=πd⁴/64 and deflection FL³/(3EI). The below-tail bridge
leaves L=S+2=42/52mm. At d1 and the .35/.30 case, total deflection is .468/.889mm
for positive contact and1.393/2.643mm for the roller. These are linear-elastic
estimates, not physical contact solutions. A .2mm displacement allowance would
require spans ≤31.6/22.0mm respectively. Bigger shafts deserve a fair control:
coarse transit plus target-tail clearance with E=.30 permits **at most d2.1mm**,
with zero residual radial gap at the limiting location and no bearing housing.
Even this favorable diameter gives roller **normal** bending .0686/.1302mm.
That exceeds the entire .05mm fixed closure before any roller compression.
Thus the fixed-position long-cantilever roller cannot deliver the required
.35Nmm under these assumptions; it is not enough to make the tip fit.

For this optimistic maximum shaft, the .05mm closure torque ceiling is
.255/.134Nmm at S40/50 and μ=.30, before material compression, shaft twist,
runout, fatigue, joints or dynamic excitation. The .05Nmm torque scenario is not
excluded. A stronger near-tip reaction, larger radial feed with force control,
or balanced opposed rollers could escape the specific closure failure. They add
routing, controls or tools and must earn a new architecture comparison; none is
quietly added here. A physical torque envelope is still absent. Do not interpret
these scenario thresholds as rated safe torque or proof all friction drive fails.

Nut thread/thrust capture carries axial load throughout. Static holding after a
proved stop and **moving** power loss remain different questions. E-156's
.15mm lead/40,000rpm belt-inertia/coast numbers do not transfer to this3mm/2000rpm
scenario. Its causal warning does: slip is not a guaranteed energy sink; retained
contact can reflect drive inertia, and separation can leave a nut rotating or
backdriving. Positive contact is no power-loss brake. Roller slip invalidates
encoder-only height inference. Actual top/holding proof, bounded disconnect and
fault recovery remain required; no free reader or friction-arrest pass is granted.

## Paid switching and the whole machine

Reuse E-264's physical river/ravine scenarios, fixedN20/S40 or configurable
shallow/deep at fixedN30/S50, B2 and K32, conditional2000rpm at the nut, lead3,
1000rev/s², 200mm/s and5000mm/s² translation. Every visited row pays two3mm Z
moves and two diagonal moves, sequentially. Existing .08s selection/docking,
.02s proof, row seeks/return, four-second allowance and one full-row retry remain.
Diagonal access is.16818s/coarse friction or.14331s/fine; positive.17575/.15432s.
Per-output radial selection is **granted but counted**, not a constructed selector.
Unchanged tools remain retracted even when the common Z axis rises. Engaging all
nuts and merely leaving their motors unpowered is not an isolation substitute.

| Grid / S / neutral | Free access | Closed E-264 | Side friction | Side positive |
|---|---:|---:|---:|---:|
|64 /40 /20|22.12s|38.95s|27.67s|27.92s|
|64 /50 /30|25.38s|45.51s|30.93s|31.18s|
|80 /40 /20|28.07s|48.98s|33.94s|34.39s|
|80 /50 /30|33.50s|58.51s|39.38s|39.83s|

These are schedules **conditional on unqualified contact/selection/speed**, not
hardware survivors or typical-play measurements. At64, roller cold neutral prep
is31.53/38.13s, dense0→40/50 stress44.73/51.33s. At80:46.24/58.54s prep and
70.84/83.14s dense. Rough lead2 sensitivity increases scene maxima to32.87/37.78s
at64 and41.14/49.33s at80. Software zero provides no extra travel. Both pitches
cover406.4mm; coarser cells change representation as documented in E-257/E-258.
~30s remains a play benchmark, not a rejection gate. Unimplemented sensing,
homing, settling and prop workflow have no measured deadline. Tool speed is
~6667rpm for the positive radius ratio or5500rpm for a nonslipping roller at
2000nut-rpm; inherited channel dollars do not qualify that transmission.

Resident:4096/6400 translating screws/stems, nuts with rims/necks, thread pairs,
radial/thrust capture sites and8192/12800 guide apertures. No resident selector,
spring or added brake. Head-only:128/160 rotary tools, shafts and drive channels,
**128/160 selective radial slides/return duties**, two short-Z carriages, two
seek axes, lower bridges/transmissions, wiring and readers. Reusing motors across
outputs would require a new schedule. Split shared beds must permit local nut
replacement under safe support, not whole-board unthreading. A10s resident touch
adds11.38/17.78h; an extra minute fitting costs68.27/106.67h. Batch casting/molding,
machining or automated assembly could help but needs tooling, scrap and service
costs; 4096 hand-fitted traction rims are not a production plan.

E-259's dated motor/driver subset plus unquoted reserve is$984.64/$1166.40,
**not a current quote or complete side-drive BOM**. Against$1500, remaining
$515.36/$333.60 is only$4.03/$2.09 per installed output for every missing
transmission, slide, return, bearing, reader and power correction. $500 is already
exceeded; $1000 leaves$15.36/−$166.40. This does not forbid a delightful premium
product, but no demonstrated UX gain or finished-price estimate offsets the new
contact burden. No purchases are authorized.

**Disposition:** stop the tested positive interface, fine-pitch route at the
stated error bounds, and the .35Nmm fixed-closure unsupported roller. Keep the
coarse friction swept route and its torque breakpoint as reusable negative and
conditional evidence. No selector optimization follows. The simpler independent
next comparison is whether slower fixed-screw axial writing with more/smaller
banks can buy comparable waits without side-contact/selection duties, counting
installed channels, price and cold preparation. This does not assume E-262's
850rpm control is a safe rating and does not wait on optional E-263 printing.

Checks: exact interior-segment witness; four mirrored engagement/release paths;
coherent gap bounds; force/diameter scaling; all inherited zero-access scene
anchors; exact dense access increments and no-op control. No independent review
or hardware qualification is claimed.
