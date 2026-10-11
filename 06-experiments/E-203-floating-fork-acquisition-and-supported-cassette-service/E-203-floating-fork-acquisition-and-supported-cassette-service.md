---
status: complete
builds-on: [E-202, E-201, E-092]
---

# Floating acquisition consumes the retention lane; intact-row service is narrower

**Neither constructed writer earns complete-machine development.** The tapered
pin can move within a finite floating head, but the attempted retention gate
intersects that head, its resident tab exceeds the inherited row allocation, and
sliding-guide friction can defeat recentering. A direct slider removes the taper
and resident command pin; its locked cassette has a clear longitudinal service
path, but the constructed bilateral writer bridge intersects the next row.
Retain that service topology and redirect the next construction to direct-writer
access from another plane. These are scoped embodiment failures, not bans on
floating forks, tapered transfer, direct sliders or row cassettes.

Input main `b6011cd`; LAB-330. Reproduce with
`python3 tools/curated-experiment-checks/E-203/fork_service.py`.
Standard-library finite solids, exact translational box sweeps, E-202 clipped
frustum paths, analytical contact bounds and support-connectivity controls.
Self-review only; no measurements, probabilistic yield, contact dynamics,
material qualification, readback qualification or physical experiment.

## Tapered fork: capture, movement and the missing retained departure

Use E-202's .8-mm square, 5.4-mm double-taper pin, keeper top z=0 and cam bottom
z=4. A connected collar/tab spans x=±.7, y=[−.4,1.8], z=[2.45,2.95] relative
to the lower pin end q. It remains inside the axial gap for q=−2.3…+.9 mm,
including retained drift: minimum plate clearance .05 mm under ±.05 tab/plate
translations. This tab is an added finite feature, not a free pin attachment.
Its root stress and pin bearing are not qualified.

Two .4-mm-thick jaws span x=±1.1, y=1.25…1.75, with inner z faces 2.00/3.40
relative to writer f. A rear wall y=1.95…2.35 and two ledges connect the jaws.
At f=−2 or +.6, the 1.4-mm opening admits the collar at all 32 combinations of
retained drift ±.30 and independent tab/jaw/writer z errors ±.05. Worst capture
reserve is **zero**, not a manufacturable clearance pass. The y bearing remains
.35 mm under the specified edge/datum errors.

An inboard control locates these jaws across the plate rim y=.65… .95:
its nominal penetration is **.264 mm³**. Independently, the retained q range
consumes 3.2 mm of the 3.9-mm worst plate gap, leaving .7 mm for a collar and
following jaws; the chosen .5 collar + two .4 jaws + two .05 clearances need
1.4 mm. Following the actual retained z coordinate cannot repair this package.
The outboard jaws avoid the plates in 20 expanded-solid approach/withdrawal
sweeps. This certifies only plate clearance; it does not ignore the gate below.

A floating carriage has two finite T shoes at y=2.6/4.0, each x=±.6,
y half-width .3, z=1.2…1.6; narrow necks and a spine join them to the fork.
Split-roof channels, floors and side webs react both z directions. The source
makes 210 nominal shoe/neck/spine-versus-guide collision checks. Nominal
.15 side/.20 vertical gaps leave .05/.10 under two adverse .05 face shifts;
angular motion and distributed bearing pressure are not solved. The x stops
allow ±.65 nominal, conservatively ±.55 after relative errors. A wide-mouth
acquisition **aperture bound**, not a manufactured or contact-solved funnel,
leaves .1525 mm at arbitrary initial carriage offset; final side reserve is .05.

E-202's 2,048 bounded cases still admit both transfer directions within these
stops: pin |x|≤.3475, recentering≤.2225 and minimum straight-shank overlap .175
mm. Entry continuity is rechecked with the inherited vertex routine; simply
projecting a discontinuous pose is not credited. This is permitted motion under
prescribed contact-following x, not proof that passive friction realizes it.
Nominal positive z drive needs f=−2.45…+1.05, **3.5-mm writer travel**, because
of .45-mm lost motion each way; it cannot inherit the 2.6-mm pin-command stroke.
The source does not claim a synchronized error-bounded actuator trajectory.

A concrete stationary keeper gate has slots z=.1…1.3 and 2.7…3.9, with solid
webs [−.3,.1], [1.3,2.7], [3.9,4.3], x=±1.3, y=1.2…1.6. The slots fit the
two retained collar levels nominally, but the webs **intersect the installed
fork jaws**. Thus even the extended package has no completed simultaneous
head takeover → gate release → set/reset → gate re-engagement → head departure.
Opening a gate first and letting the pin float axially is not a repair. The
source reports a .308-mm³ positive-volume witness. Gate error slack, operating
linkage, cam-working-stroke clearance and power-off arrest are not accepted.

The resident cam rear rim y=−4 through tab end +1.8 consumes **6.0 mm** including
.2 total edge/datum allocation, versus E-202's 5.20. The illustrated floating
head/guide reserves **6.9 mm x and 8.7 mm y**. These are this layout's allocations,
not universal lower bounds. Staggering levels or servicing alternate rows would
change the architecture, throughput and support schedule; none is silently added.

## Guide force and local overload

The outboard z force acts nominally at y=1.5 while the two guide shoes are
centered at 3.3, span L=1.4. Their opposing vertical reactions have absolute sum
at least `Fz max(1,2e/L)=2.571 Fz`, e=1.8, before other loads. On a prescribed
sliding branch their x friction adds to the resistance being recentered.
With E-202's adverse taper ratio and μtaper=.5, G=Fz/R=5.33081:

`Fz = G (R0 + μguide * 2.571 * Fz)`.

The feedback coefficient is .685/1.371/2.742 at μguide=.05/.10/.20. Only the
first has a positive finite solution for R0>0; even it amplifies the original
force by 3.18. At μguide=.10, e=1.55…2.05 and L=1.3…1.5 give coefficients
1.102…1.681. These are assumed Coulomb sliding/moment bounds, not a prediction
of a reached jam or calibrated PLA friction. Rolling bearings, flexure guidance,
relocated force or another contact mode change the result and need construction.

A common 80-output limiter still inherits E-202's inadequate protection cases.
A reusable per-head limiter must isolate each loaded fork **downstream** of any
shared drive. It cannot repair a nonpositive sliding denominator. No finite
limiter, strength of the taper lip/tab, fatigue or damage threshold is supplied;
no shank bending capacity is assigned to the tiny taper tip. The direct writer
also needs its own local jam limit. These omissions forbid a force pass, rather
than becoming assumed free components after geometric clearance.

## Direct comparator and supported cassette removal

Remove the spring and command pin. Keep E-198/201's rack/grounded-slider load
principle, now with an outboard tab x=[−1.1,−.5]+q. A grounded row-comb slot
x=[−1.3,−.3], occupying y=1.3…1.7, retains the seated tab. Independent ±.05
slot/tab/datum errors permit q=±.35; including independent nose/rack errors
leaves **.05-mm rack overlap**. At positively held q=−.75 the rack clearance is
.15 mm. A retracted slider cannot enter that comb slot: the slot is a seated
lock, not proof that an arbitrary stuck state is supported. Comb actuation,
strength and complete rack-guide fit remain unqualified.

The tab also needs a window through its own +y post: x=[−2.05,−.05],
z=[−2.2,.2]. Finite remaining pillars are .45/.20 mm wide with an upper
connecting bridge. Expanded tab solids clear this window at retracted and
retained extrema, but these frame ligaments have no strength or printability
pass. An intact solid E-201 post cannot be silently retained.

A U-shaped writer captures the extended tab at y=1.95…2.35. Its x opening is
[−1.55,−.05], jaws .4 thick; the tab extends to y=2.4. The retained-state
acquisition reserve is again zero at the declared bounds. More decisively, its
back bridge x=[−1.95,.35], y=[2.55,2.95], z=[−2,0] intersects the neighboring
row's grounded post by **.924 mm³ at nominal dimensions**. Omitting that bridge
would omit the positive bilateral force path. This is an actual solid collision,
not an envelope warning. Another approach plane is a new useful discriminator.

For service, keep each whole 40-cell/203.2-mm cassette, its grounded supports,
locked sliders and columns together. The direct resident envelope is asymmetric
y=[−2.35,+2.4], not ±2.4 or ±2.45 by convenience. With .05 face plus .05 row
datum bounds on each exterior edge, adjacent row clearance is **.13 mm**;
4.8-mm tops have .08 mm. Exact longitudinal sweeps at any terrain heights have
no overlap with neighboring rows. Each half-row must leave toward its own
outer board edge; an inward exit through the other half is not available.
Longitudinal module seams, fastener release and the dock attachment are not
constructed, so this certifies transverse clearance, not full-display removal. A dock continuing both bottom rails by 203.2 mm keeps their
combined cabinet/dock contact length constant throughout extraction. Rail
strength, joint step/gap, leveling and operator handling remain unqualified.
This is a conditional whole-row service path, not in-place single-slider repair.

Same-plane 5.20-mm and tabbed 5.80-mm resident row constructions fail this
neighbor test; finite edge-rail witnesses are retained in source. Their body
envelopes include **additional** ±.10 outer edge/datum bounds. The result is
specific to these edge-rail placements and does not reject vertical staggering.

Support connectivity survives intact-row removal only when every column is
already seated and the row comb is positively retained. In a 39-seated/one-
withdrawn fault, that column has no ground path after a stationary writer leaves.
A traveling rescue support repairs the abstract connectivity, but none is built:
**jammed-row service fails**, rather than being described as a successful dock
transfer. Opening a common comb during normal operation similarly requires
holding every affected slider, including unchanged columns, until it closes.
Forty heads per half-row or a separately retained local gate must be accounted
for; a single free head cannot release the row lock safely. Depth/command
readback alone does not prove load support. False acceptance remains unsafe.

## Scope, scale and next decision

The transfer repeats 6,400 pins plus 6,400 sliders and their guides/gates. A direct
writer deletes the resident transfer pins but still repeats 6,400 sliders/tabs
and rack contacts. Float shoes, acquisition, local limiting and proof repeat per
writer channel; cassette service adds dock rails and a still-missing rescue
fixture. No precision-channel saving is inferred from a low nominal part count.
At 40 cells/cassette, 160 cassettes cover the board and fit the printer's nominal
256-mm build length; width/height, joints, print orientation and yield still need
engineering. No bought-cost estimate, fabricated assembly or durability claim.

The inherited illustrative `6+ceil(6400/H)*s` still requires s<.6 s at H=160.
Extra capture lost motion, floating-guide settling, gate sequencing, readback,
transport, bounded retries and reset must be charged; no update-time pass.
Cost remains `Cshared+H*chead+6400*ccell<500 dollars`; a hypothetical $250 reserve
leaves <$0.03906/resident site. Service downtime is not hidden inside the normal
update target. No fabrication or purchase is justified by these failed interfaces.

All errors/frictions are **epistemic scenarios**, not X1C distributions. Coherent
relative row/part biases are allowed; common absolute translation cancels.
Shrinkage, warp, roughness, burrs, tilt, layer anisotropy, creep, wear and fatigue
are not absorbed into the .05 bounds. No board failure probability is estimated.
Checks include solid overlap controls, an interior swept collision missed by
endpoints, tangential noncollision, retained corners, inherited transfer paths,
and identical service conclusions at 1/16/64/256 subdivisions. Analytical sweep
intervals and axial/guide-moment bounds supplement sampled poses. The model tests
an interface and service topology, not a complete assembly or physical support.

**Action:** stop this same-plane floating-fork/retaining-gate package and the
side-entry direct U writer. Preserve direct intact-row service as the less
burdensome lead. Next construct a direct bilateral writer entering from another
plane, with row-gate takeover and one traveling recovery support, before any
machine promotion. Reopen transfer if a changed force/retention layout eliminates
its eccentric guide reaction and gate collision with a credible packing benefit.
