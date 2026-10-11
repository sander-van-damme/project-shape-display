---
status: complete
builds-on: [E-204, E-166, E-165]
---

# Adaptive jaws acquire the slider; long blades do not guarantee its restraint

**Stop this long split-blade/common-comb embodiment and the constructed local
crossbolt control.** Adaptive contact removes E-204's fixed-offset contradiction
without adding resident command channels. However, a bounded contact-force case
consumes the small retained support overlap even with metal-like blades and
optimistic bilateral preload. The local gate relocates the problem into 6,400
additional guided/latching units with failed bounded clearance and no demonstrated
assembly advantage. Neither is a complete supported handoff. Reconsider shared
return/load-seat combinations from E-166 before further underside access work.

Input main `5b00d5c`; LAB-332. Reproduce:
`python3 tools/curated-experiment-checks/E-205/takeover.py` (standard library;
imports retained E-204/E-203/E-202 primitives). Finite rectangular geometry,
contact-footprint reconstruction, bounded elasticity and self-review. No physical
measurements, calibrated probability distributions, material qualification,
independent review, fabrication or purchase. Discard reproducible JSON output.

## Construction and contact sequence

Retain E-204's slider island, downward tang, solid posts, rack footprint and
non-guiding underside base aperture. Replace its U with two independent jaws.
Each tip is .4 mm wide in x, y=[1.5,1.85], z=[−4.8,−3.6]; each integral blade
widens outward to 1.4 mm and extends down to z=−49. Open inner faces are
x=−1.85/−.15. Their reusable roots translate independently below the cassette.
Root guidance, positive locking, drives and local isolation are **boundary
obligations**, not supplied rigid hardware. There is no new resident bearing.

Source inspection also reveals E-204's comb webs ended at z=−4.4 while its spine
ended at −4.5: a **.1-mm disconnect**, in addition to zero nominal tang-bottom
clearance. Here webs extend down to −4.8 and meet a spine at z=[−5.4,−4.8].
This connects the solids and leaves .3 mm beneath the tang. The gate still moves
down 1.5 mm in y=[1,1.25], separate from the jaws. This repairs geometry only;
a connected .25-mm-thick comb is not a stiffness or printability pass.

The executable checks **816 expanded translational sweeps** against the actual
frame, neighboring rows, rack envelope and released gate. Opposite neighboring
head commands retain only **.08 mm** after .1-mm growth per head. Intended
contacts are treated separately from expanded clearance. The wide blades use
the same .35-mm y lane through the .75-mm aperture; the inherited .35-mm outer
base strip remains unqualified.

Sequence, with all 40 sliders initially seated:

1. Insert the open jaws while the comb remains shut. Each jaw approaches its
   actual tang face; stop on contact without commanding slider recentering.
2. Retain every acquired root before opening the comb. All 39 unchanged sliders
   retain their acquired positions. A failure on any jaw inhibits common release.
3. The changed rack must be captured/unloaded by a separate load-bearing head
   before its slider moves to q=−.75. That rack head is an explicit unsolved
   interface, not a Boolean proof of built support. Only under this boundary can
   the rack move through its 40-mm travel while the slider is withdrawn.
4. Return that slider to q=0, close the comb, transfer/prove actual rack load,
   then open the jaws and depart. If the comb cannot close, retain **all** jaws
   and the changed rack head; departure is prohibited.

In 512 corner/end-position cases, reuse the same ±.05-mm comb datum, slot faces,
tab translation, nose/rack errors and writer face/datum errors throughout.
`qlo=−.2+combDatum+leftSlotError−tabError`; tab error cancels from acquisition
rather than being sampled again as retained drift. Acquisition reserve is
**.15 mm**; unchanged support overlap is only **.05 mm**, or **.020 mm²** of the
actual .4-mm-wide island/rack contact. Return to q=0 leaves .05-mm minimum slot
clearance; withdrawal leaves .15-mm rack clearance. Uniform translations cancel;
relative bank bias and coherent adverse errors do not average out over 40 cells.

The ideal retained-root state sequence preserves unchanged contact area at
1/16/64/256 subdivisions. Exact sweeps bound translational access independently
of these samples. This is a **kinematic interface result**, not a force pass or
an implemented load head. Surface depth or jaw command readback cannot establish
positive root retention, load transfer or safe departure.

## Force discriminator and local jam limiting

The rack's vertical reaction still passes through slider → grounded guides →
frame. The jaw must oppose horizontal withdrawal force. A finite competing
contact construction puts a downward-to-right 2° ramp on the support nose and
a horizontal rack corner on that ramp. Its remaining tooth footprint clears the
ramp; frictionless normal equilibrium requires `Fx=W tan(2°)`. This is an explicit
uncertainty scenario, **not** a measured defect angle or a stage-02 load requirement.
It produces a real contact normal, rather than assigning lateral force to a
perfectly horizontal frictionless interface. Guide/contact friction could instead
hold the slider; that unqualified assistance is not credited to positive capture.

One blade's root-to-contact-resultant length is 44.95 mm. Integrating
`(L−s)²/[E I(s)]` includes the last .75 mm of .4-mm-wide tip and the 1.4-mm-wide
body, both .35 mm thick. Independent midpoint quadrature matches the piecewise
integral within 2e−5 relative; a uniform wide-beam upper bound is .020% stiffer. Torsion, root compliance,
slider yaw, contact indentation and shared-frame motion remain omitted.

| Assumed E (MPa) | Blade stiffness (N/mm) | Force consuming .05-mm overlap minus .02-mm root lost motion (N) |
|---:|---:|---:|
| 1,000 | .002643 | .0000793 |
| 3,000 | .007929 | .0002379 |
| 200,000 | .528626 | .0158588 |

These are polymer-like/metal-like scenarios, not material allowables. At 1 N and
2°, Fx=.0349208 N; the metal-like single blade deflects **.06606 mm**, exceeding
the entire .05-mm overlap even with zero root lost motion. Root stress demand is
393.15 MPa/N before concentrations; no allowable or endurance credit is assigned.
This small metal-like deflection is within the linear beam's small-rotation
regime; huge polymer predictions are only failure diagnostics.

Preloading both jaws can at best double stiffness while both contacts persist.
With the assumed .02-mm root lost motion its overlap-loss threshold is still
only **.0317176 N**, below .0349208 N. With *zero* lost motion the optimistic
preloaded 1-N/2° case can survive; 10 N/2° still fails. The source also reports
0/.25/2° and .1/1/10-N cases and 0/.01/.02/.05-mm lost-motion sensitivity.
A 1-N/.25° single-blade case retains .02175 mm under the .02-mm allowance.
These changes of disposition prohibit declaring all adaptive capture impossible.

A scalar local trip would need `Frequired < Ftrip < Foverlap-loss` (and below
material damage). Here the 1-N/2° intervals [.034921,.015859] N, or even
[.034921,.031718] N with ideal preload, are **empty**. A limiter cannot repair
this restraint: slipping releases support, while a higher threshold permits
support loss before isolation. No finite brake/limiter is credited after this
necessary-condition failure. Any future drive isolation must be downstream of
shared actuation yet preserve the retained load path; a common limit sized for
40 channels can deliver 40 normal-channel forces to one jam.

Recentring every slider under the closed gate would restore .4-mm worst overlap,
but changes the sequence into 40 loaded slides. Assumed μ=.05/.2/.5 and W=1/10 N
require .05…5 N before guide moments; the same metal-like single blade has only
.20088-N capacity within .38 mm. This is no free correction, though bounded low
loads may survive. A close **reusable** distal guide, changed force topology or
proven lower load/slope envelope can reopen takeover; adding 6,400 precision
sleeves is not accepted merely to rescue this blade layout.

## Local-gate control, machine burden and next move

Split the repaired comb into 4.68-mm-wide segments, each with a downward stem,
finite guide cheeks grounded to the negative-y post, and a transverse crossbolt.
The source constructs the stem aperture and pin, their retraction/release sweeps,
and a positive pin/stem collision after .21-mm attempted gate descent. The pin
rests on the grounded guide lip; gate load then passes through pin to guide. Unchanged
gates stay closed, so only the changed slider requires a writer. There are 140
nominal/neighbor sweep checks and .30-mm expanded intersegment gap.

This control fails manufacturing screening: **.05-mm guide clearances become
−.05 mm** under opposing .05-mm surface errors, and stem ligaments are only
.05 mm. Bolt retention in its own withdrawal direction, actuation, returns,
strength and fault recovery remain unconstructed. It is a finite nominal latch
comparison, not a separately qualified retained control. A jammed-open local
gate must leave its changed rack head engaged; neighbors retain their own gates.
No robust failure-to-close or power-loss pass is inferred.

Shared takeover repeats 6,400 original sliders/tangs/guide fits plus 160 combs;
H=40/80/160 adds **80/160/320 reusable blade roots**, their locks, contact finding,
local isolation and verification. The local control repeats **6,400 gate stems,
guides and crossbolts**, replacing 160 common gate coordinates with 6,400
independent ones (6,240 extra); no carrier or assembly saving is demonstrated.
Neither has a priced BOM. `Cshared+H*chead+6400*ccell<500 dollars` remains necessary;
a hypothetical $250 remainder is only $.03906 per resident site before other
purchased hardware. No precision components are assumed free because printed.

Under the inherited illustrative 6-s map overhead, strict slot ceilings remain
.15/.30/.60 s at H=40/80/160. All-jaw acquisition, retention, rack takeover,
release, positioning, reseating, actual support proof, departure, settling and
bounded retry must fit. For a one-cell change, common release still needs 40
restrained sliders. No timing, regional-disturbance or hardware-reliability pass.
False acceptance can expose an entire half-row; zero simulated failures under
ideal roots says nothing about its probability. Print bias/warp, roughness,
layer effects, creep, wear, fatigue and process anisotropy remain uncalibrated;
all stated ranges are epistemic bounds, not X1C accuracy or yield claims.

**Decision:** preserve the adaptive acquisition result, stop these two normal
handoff embodiments, and leave rescue/dock detail downstream. Next reconstruct
E-166's backed hook with a release direction that bypasses its fixed-stop
collision, comparing shared return manufacture against the existing grounded
slider. Require an actual support/release path and repeated-interface advantage
before deeper machine development. E-165 remains a laminate/assembly comparator,
with its feed and local-clamp burdens intact. No print request or approval wait.
