---
status: complete
builds-on: [E-203, E-198, E-201]
---

# Underside access clears; fixed open jaws lose support and the rescue prop hits the base

**Stop this open-jaw/common-comb handoff and rigid bottom-prop embodiment.** A
changed approach plane avoids E-203's side-entry collision and upper-post window,
but acquisition does not restrain unchanged sliders after common-gate release.
The traveling prop cannot be installed through the cassette base. Retain the
underside access geometry as a conditional lead, not a supported interface or
hardware pass. Failures are scoped to these embodiments.

Input main `c29c477`; LAB-331. Reproduce with
`python3 tools/curated-experiment-checks/E-204/orthogonal_service.py`.
Python standard library; imports retained E-203 collision primitives/control
(and transitively E-202). Finite solids, exact translation sweeps, support-area
reconstruction and analytical bounds; self-review only. No measurements,
probabilistic yield, contact dynamics, physical load proof or independent review.
No fabrication/purchase. JSON output is reproducible and discarded.

## Underside continuation: access is not takeover

The changed interface replaces the outboard tab with an integral **downward
tang** x=[−1.3,−.7]+q, y=[.85,1.9], z=[−4.5,−2]. A 1.4-mm-long crossbar
x=[−1.75,−.35]+q, y=[−1.8,1.9], z=[−2,0] joins it to the inherited island.
Moving the tang .2 mm left is necessary: retaining the original x position
collides with the lower guide at positive retained drift. The spring/spine and
old under-slider stop are removed; the comb is now the retention element.

Keep solid, **unwindowed** posts x=[−2.5,.15], y=[−2.35,−1.95]/[2.05,2.35],
z=[−46,0], and the three inherited guide bridges extended across the row.
An underside U has inner x faces −1.85/−.15, .4-mm jaws, y=[1.5,1.85],
z=[−4.8,−3.6], joined by a bridge z=[−5.3,−4.8]. Its integral command tongue
is 2.3 × .35 mm, z=[−49,−5.3]. It enters vertically from below; independent
x commands span −1.30…+.55 mm to accommodate .55-mm nominal lost motion on
each direction. This is 1.85-mm head travel for .75-mm slider travel.

That tongue crosses the intact base. Cut a **non-guiding longitudinal aperture**
y=[1.25,2.0] through z=[−47,−46]; retain base strips y=[−2.35,1.25]/[2,2.35].
The outer strip is only .35 mm wide and has no strength/printability acceptance.
The original solid-base insertion has a .056-mm³ collision witness. A guiding
bearing in this aperture is not credited: it would add resident precision.

The comb has slots x=[−1.5,−.5], webs z=[−4.4,−3.6], y=[1,1.25], and a
continuous back spine z=[−5.1,−4.5]. Translation **down 1.5 mm** releases the
tangs while staying separate from the writer lane and the entire rack envelope.
The spine nominally touches tang bottoms when closed; independent z errors can
interfere. The retained source also leaves a .1-mm gap between web bottoms
z=−4.4 and spine top z=−4.5: these solids are disconnected. Its sweep result
therefore does not construct a force-transmitting comb; joining them is owed.
A real closure clearance, actuator, mechanical stop and retained
closed state are not supplied. No robust gate pass is inferred from nominal fit.

The source checks **628 expanded exact sweeps** for writer approach/acquisition,
command and comb release against ground/neighbor parts, with .10-mm expansion
on writer and .05 on obstacles (face and relative-datum bounds), or .05 on both
comb/obstacles. Forty heads at opposite commands retain **.53-mm** separation
under .10 expansion per head. Intended slider-guide and closed tang-comb fits
are checked nominally only, separately from this clearance result. Error growth
cannot certify these zero-clearance contact fits. The old .924-mm³ side-entry
collision remains a regression control; no surface opening is needed below.

**The decisive failure is support, even granting that geometry.** A fixed open U
at head x=0 has a jaw-only q range [−.55,+.55] after the comb opens (other
guides may limit its positive end), versus the nominal rack
support boundary q=−.50. The executable footprint reconstruction follows the
island top from .20 mm² contact area to zero before the left jaw arrests it.
At 32 independent ±.05-mm jaw/tab/datum/nose/rack corners, the adverse q is
−.70 and signed rack overlap **−.30 mm**. Nominal loss is already .05 mm;
this is a permitted escape, not a prediction that friction always causes drift.
The gate had limited q to ±.35 in its own adverse case; acquisition clearance
has silently enlarged that admissible motion if called “takeover.”

A universal fixed preposition does not repair it. With the same bounds, approach
without colliding with any retained tang requires head x≤.15; guaranteed
nonnegative overlap after opening needs x≥.30. Their **.15-mm incompatibility**
is independent of software depth confirmation. Acquisition is reconstructed
from shared comb/tab/head errors; tab error cancels rather than being counted
twice through a separately sampled retained-q bound. Closing/recentering each head
while the comb remains locked could change this constraint, but needs a finite
adaptive contact/limiter sequence. It is not a smaller aperture or a common
blind offset. During one-cell updates all **39 unchanged sliders** also need
restraint; alternatively capturing all 40 racks introduces another full-rank
load-support obligation. Keeping the comb shut preserves support but prevents
the changed cell from retracting. The tested sequence therefore stops before
comb release; command or depth readback cannot authorize departure.

## Traveling recovery construction and real seams

A reusable under-row sled z=[−54,−52], y=±1.8 carries one rigid compression prop
x=[1.3,2.1], y=±.5 from z=−52 up to the faulted rack bottom h−42. Its integral
shoe x=[1.2,2.2], y=±.6 is .8 mm high. This changes the recovery load path to
rack bottom → prop → traveling sled → cabinet/dock, independently of the jammed
slider. It assumes the original rack head continues supporting the column until
actual contact and load transfer; no unsupported preliminary lift is permitted.
The rigid prop is an exact-height geometric candidate, **not** an adjustable
jack, an available stock kit or a qualified ground connection.

At all five h=0/10/20/30/40, the prop **intersects the actual cassette base by
.8 mm³**. The same intersection holds at intermediate h. The writer aperture
is in the wrong y lane to help. Thus this recovery fixture cannot be installed
as drawn; removing the load-bearing base first is not supported recovery. Stop
there for this embodiment. A through-base access opening plus an adjustable or
height-matched prop is a different candidate, with loss of base section and
supported installation still to construct.

To expose a second independent service obligation, an explicitly optimistic
control grants that opening and exact-height prop. A finite cabinet end member
x=[end+.2,end+1.2], y=±2.35, z=[−54.5,−51.5] then intersects the sled during
outward extraction: **5.76 mm³ at 1-mm travel**. Moving that member down 4 mm
clears its expanded sweep. These are competing *assumed cabinet constructions*,
not discovered dimensions of an existing machine. They show why a transverse
clearance certificate cannot establish passage through module ends. The new
cassette/sled envelope itself clears adjacent rows by **.18 mm** with .10-mm
outer bounds; the inherited 4.8-mm surface tops still limit gap to .08 mm.

At the central half-row seam, unrecessed 203.2-mm bases butt with zero nominal
allowance. Opposed .10-mm face/datum bounds create **.912 mm³** of actual base
intersection. End relief or a registered joint is required; moving column pitch
apart is not silently permitted. At the outer dock seam, granting aligned rails
but a .5-mm gap reduces their supported longitudinal length from 203.2 to
**202.7 mm** while crossing. The earlier constant-contact calculation applied to
zero gap. It proves neither acceptable bending nor traversal of a step. No
finite dock attachment is completed after these failures; fastener grounding,
level adjustment, gap/step accommodation and power-off support remain unearned.
Service results agree at 1/16/64/256 subdivisions and with the exact sweeps.

## Overload, repeated burden and disposition

The underside geometry does not justify a long printed command tongue. For its
43.7-mm unsupported span, 2.3 × .35-mm section, x bending gives
`I=.35*2.3^3/12` and `k=3EI/L^3`. Explicit E=1,000/3,000/200,000-MPa scenarios
permit only **.00128/.00383/.255 N** at .1-mm deflection; at .1 N the linear
predictions are 7.84/2.61/.0392 mm. Large-deflection predictions merely flag
failure of the .1-mm stiffness allowance; they are not nonlinear equilibria.
Root bending demand is 141.6 MPa per N, before stress concentrations. These are
labelled material-like bounds, not sourced PLA/metal allowables. The actual x
force/contact eccentricity, y bending, torsion, short jaws, guides and dynamic
loads can only add obligations to this favorable single-axis estimate.

Each channel needs a local overload window
`Frequired < Ftrip < min(Fdamage, k*allowed deflection)` downstream of shared
drive. None of these thresholds is qualified. A common limiter set to 40 normal
channel loads can place that whole load on one jam; it is not local protection.
No finite limiter or fail-safe brake is granted. Reusable metal tongues or a
close traveling guide may change the stiffness result; resident guiding sleeves
would multiply another precision interface across 6,400 sites.

The underside tang replaces a tab rather than adding 6,400 command pins. It
still repeats 6,400 sliders/tangs, rack contacts and existing guide fits, plus
160 combs, 160 slotted half-row bases and their assembly/registration. At least
40 independently restrained channels accompany each released half-row; adaptive
jaws add work per *writer*, whereas local resident gates repeat per *cell*.
The rescue prop/sled is reusable, but its installation, adjustability and dock
have failed or remain missing. No priced BOM, assembly time, print yield or
manufactured strength is claimed. The existing `<$500` purchased-cost equation
still applies; unpriced extra channels cannot be called an affordable machine.

With the inherited illustrative 6-s map overhead, H=40/80/160 channels leave
strict slot ceilings **.15/.30/.60 s** respectively. Slots must now include
all-head acquisition and adaptive restraint, rack takeover/unloading, comb
release, travel, reseating, comb closure, load-transfer proof and departure.
Registration, preparation, bounded retry and settling remain charged. A false
support acceptance endangers a whole released rank; no independence or perfect
reader is assumed. No full/regional update-time pass and no fabrication.

All dimensional/material cases are epistemic bounds. Coherent aperture bias,
comb warp, common row offsets and correlated head error can affect all 40 sites;
no cancellation across cells is assumed. Shrinkage, burrs, first layer, warp,
friction, tilt, creep, layer anisotropy, fatigue and wear are not calibrated by
these expansions. Support loss exists even at nominal geometry, so a tolerance
coupon cannot resolve the current mechanism contradiction.

**Decision:** stop the fixed-open underside U/common-comb handoff and this rigid
bottom-prop recovery embodiment. Retain the cleared underside route, solid
posts and the cheaper direct-resident topology as useful partial results. Reopen
only with positive adaptive takeover **before** common-gate release (or a
concrete independently retained gate), plus a service load path installed while
the rack remains held. The next useful discriminator is a short finite
clamp/comb overlap sequence against a locally retained gate, including the
repeated-channel burden. Do not continue dock fastening or tune tongue material
until that changed interface earns support continuity. A failure there warrants
reconsidering E-166/E-165 sharing principles rather than another access variant.
