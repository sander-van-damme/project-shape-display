# B — Alternative actuation architectures and a positive rack transfer

**Preserved initial investigation.** Subsequent timing and hardware reviews rejected the traveling-head recommendation. The DES-008 main report and final disposition govern the current recommendation; these notes retain the alternatives, mechanisms and reasons tested along the way.

Workstream author: independent alternatives agent. Date: 2026-10-14.
Scope: screw alternatives with complete load and selection paths. This is a
decision note, not a machine qualification. Read current `AGENTS.md`, mission,
current prototype priorities, owner short-thread results and ADR-017/022.

## Decision

The strongest non-screw mechanical principle found here is **a long ladder rack
on each terrain column, a permanently grounded passive pawl for each column,
and a scanned row head with positive moving dogs**. It eliminates screw friction
and the need to drive a fine-pitch screw at high rpm. It can support positive
upward and downward movement without changing an unaffected pin's support.

It is not yet a full-machine winner. Shared displacement requires either fast
independent release at each target, several written subset masks, or a true
mechanical release-height memory. Those three transactions have different time
and hardware counts. A binary subset memory must not be credited with the
continuous independent-stop timing below.

A scanned row of individually driven screws/racks is the simpler control
architecture: 64 or 128 reusable direct drives replace 4,096 individual drives
at 6.35 mm pitch. It should remain the cost and performance comparator. Current
main's manual screw tests favor preserving the screw comparator: five short
thread pairs completed five manual cycles without damage or postprocessing,
but their 10.3 mm nuts do not prove the fine-pitch geometry. Historical 4.4 mm
Trial-5 success is owner-reported; the new supported replica was not functionally
tested. This evidence establishes no motor torque or array yield.

## Candidate comparison

| Principle | Complete movement/support transaction | Repeated hardware / active count | Decisive result |
|---|---|---|---|
| Individually driven scanned screw row | Seat rotary couplers, drive each target independently, stop, withdraw; resident screw holds terrain | 4,096 screws/nuts; 64–128 reusable motors plus transport | Strongest simple comparator. Requires compact stable screw geometry, positive coupling and torque/speed evidence; motor packaging is substantial. |
| Individually driven scanned rack row | Capture each long rack using a pinion or dog, take its load, retract that pin's ground pawl, drive, restore ground pawl, unload and disengage | 4,096 racks/pawls; 64–128 reusable linear/rotary axes | Positive down motion and fast linear travel. Removes screws but adds a loaded handoff and persistent rack/pawl complexity. |
| Shared positive rack shuttle | Engage selected dogs at common plane; unload/retract only selected ground pawls; translate common Z; return each pin to its fixed pawl | 4,096 racks and passive pawls, 64 moving dogs per bank; selector count depends on program transaction | Best shared non-screw mechanism. Fast continuous stopping remains an untested latch handoff; serial binary writing creates real schedule work. |
| Common bottom platen with timed catches | Raise released selected pins to a common upper level, capture them, lower while locking at targets | 4,096 catches and a means to capture/lower each selected pin; typically multiple banks | Old-height acquisition/reset costs at least a complete sweep. Gravity is not positive down drive; a capture mechanism adds another transfer. No advantage over the long rack. |
| Crossed row/column rigid supports | Both row and column support must withdraw at the desired intersection; shared lift supplies motion | Few long bars but two support contacts per pin | Static Boolean AND does not prove unchanged neighbors stationary. Removing one support transfers neighbors to a second datum with real tolerance error, or unloads a previously single-supported pin. Entire bars also accumulate friction/load. Park absent a different load path. |
| Phase-change / electrostatic clutch array and one platen | Individually unlock pins while a shared plate moves; relock each at its target | One clutch per pin, distribution electronics and common actuator | Real published demonstrations support the principle, not this speed/cost. Thermal clutch cooling and adjacent heat transfer conflict with 30 s; electrostatic friction retention needs dielectric/HV and wear qualification. Not the shortest path to an accessible prototype. |
| Binary structural layers / stepped supports | Program each level then transfer pin support into selected height stack | Several local load-bearing state elements per pin | Exchanges motor count for 16,384+ small retained components at four bits, plus handoff/clearance. Historical repository work already exposes substantial complexity; no new simpler embodiment emerged. |

## Exact rack/pawl construction proposal

Coordinate convention: X across columns, Y along scanned rows, Z vertical.
Preliminary full-machine pitch is 6.35 mm, 64 × 64 = 4,096 outputs over 406.4 mm.
Five pins per square at 5.08 mm can be compared later; no mechanical clearance
claim from this section automatically applies at that pitch.

1. Each pin has a square upper stem, an approximately 6.10 mm terrain cap and a
   **3.8 mm wide by 3.8 mm deep lower ladder rack**. Left and right side notches
   are 0.60 mm deep, 1.0 mm high, at 2.0 mm Z pitch. Notches have horizontal
   load faces; a small insertion chamfer is not a load-bearing ramp. A 2.6 mm
   central web remains between opposing notches. Geometry and print anisotropy
   need qualification; these dimensions are a starting design, not allowances
   demonstrated by printing.
2. Put a permanent ground pawl against the left notches, at one common Z datum.
   Its tooth projects 0.60 mm into the notch, is about 3.8 mm wide in Y and
   1.0 mm thick in Z. The pawl has 0.80 mm transverse release travel and a
   release heel accessible from the scanned row head. It is normally engaged.
3. **Support its tooth/slider foot on a grounded ledge directly underneath it.**
   Terrain force goes rack ledge → pawl tooth → grounded ledge → cassette/frame.
   A long flexure returns the pawl sideways; it must not be the vertical column
   carrying the terrain. This distinction is important: the calculation below
   gives only ~0.84 N Euler load for the unbacked candidate flexure.
4. A 20 mm long, 0.6 mm thick, 3.8 mm wide PLA leaf is a low-waste experimental
   spring. Orient its length along Z in the assembly, bend along X, print it flat
   so bending is in-plane. An approximately 0.8 mm release requires ~0.041 N
   for an assumed isotropic E = 2 GPa, and calculated outer fiber stress is
   ~3.6 MPa. Neither fatigue life nor actual printed stiffness is established.
   Production leaf material should be spring strip with the same function;
   its dimensions require a new stiffness calculation rather than copying PLA.
5. Pawls can be made as a single flexure comb per 16 or 32 columns, plus a
   grounded ledge cassette. A 32-column comb is 203.2 mm wide and fits a
   256 mm bed. Thus 128 combs can contain all 4,096 local springs; these are
   still 4,096 spring functions, not 128 output latches. Broken teeth should be
   repairable by replacing a small comb segment. A 400 mm one-piece comb does
   not fit the owner's standard printer.
6. The right notches accept a moving positive dog from the row head. The dog
   captures both upper and lower notch faces, giving positive push and pull.
   Its keeper is mechanically supported by the head carriage and constrained
   against lateral withdrawal while loaded. A bare gravity shoe cannot perform
   this function. The dog is independently selectable per reusable lane.
7. The row head carries 64 dogs on one common Z shuttle. A stationary part of
   the head reaches the 64 local ground-pawl release heels. A long sliding cam
   or keyed follower carries each lane's selection command to its vertically
   moving dog. Two cam stages provide capture-before-release and
   ground-before-withdraw. The moving dog must have a small vertically compliant
   overtravel element, with a hard mechanical end stop, to tolerate transfer.
8. Use two guides separated by roughly 35–45 mm. All rack notches and latch
   motion occur below those guides; the playable caps cannot strike the head.
   The guides must not rely on neighboring pins for lateral support. End stops
   prevent extraction or a pin dropping into the head.

### Why the rack must be longer than the terrain stroke

If pin travel is H and the common dog sweeps S, every rack must intersect the
dog at every combination of pin height and head height. Hence the common toothed
length is at least H + S + engagement/end margin. At H = S = 40 mm this is
approximately **86 mm**, not a 40 mm rack. Adding upper terrain travel and
guidance yields an approximately 125–145 mm pin and a roughly 150–180 mm deep
machine. These are packaging estimates to be developed in CAD. A binary
increment head with less excursion may use a shorter rack but must include its
actual reset trajectory.

At 0.5 N pin load, 3.8 × 0.6 mm projected tooth bearing area gives ~0.219 MPa;
a 1 mm thick, 0.6 mm projecting tooth has nominal root bending stress ~0.474 MPa.
These ideal static numbers are modest. Printed defects, notch stress, fatigue,
ledge wear, shock load and actual bearing area dominate the qualification.

64 simultaneously loaded pins at 0.5 N require 32 N before guide friction and
inertia. An 8 mm effective belt radius at 80% mechanical efficiency requires
~0.32 N m. A shared stepper class drive is plausible; small selector actuators
must not supply this terrain force. A heavier hand load is outside this nominal
case and should reach a mechanical stop or force-limited shared drive.

## Positive up/down transfer sequence

This sequence is for a stopped subset pulse, which is easier to validate than
continuous target release. It works for either sign; the direction of the
terrain movement is independent of the short unload movement.

| State | Ground pawl | Moving dog | Common Z / load path |
|---|---|---|---|
| 0 parked | Fully in, carrying pin | Out | Pin → ground pawl → grounded ledge; neighboring pins have this state throughout |
| 1 capture | In | Slide into rack notch | Common Z aligned to the known 2 mm tooth phase; don't retract a ground pawl to search for a notch |
| 2 take load | In, unloaded | In, carrying pin | Raise common Z by measured small clearance/preload, nominal 0.2–0.4 mm; selected pin may move by that amount, unchanged pins do not |
| 3 release ground | Out | In, positively captured | Cam can retract the ground pawl only after dog engagement and preload |
| 4 move | Out | In | Drive the shared Z pulse up or down; do not use gravity for the down stroke |
| 5 restore ground | In, full-depth insertion proved mechanically | In | At destination phase, keep selected pin slightly above ground bearing position while pawl enters; notch must have clearance for this overlap |
| 6 seat | In, carrying pin | In but unloaded | Lower common Z by the transfer preload; pin settles onto its own unchanged ground datum |
| 7 release head | In | Out | Only after the pawl is fully in and dog unloaded; reset Z and index Y with all dogs and release heels clear |

The transfer preload must fit the vertical notch clearance: 1.0 mm notch height
and a 0.6 mm dog height can permit nominal 0.2 mm transfer, while a 1.0 mm tooth
in a 1.0 mm notch cannot. Final CAD must distinguish tooth structural thickness
from the entering tip thickness. This is a specific design constraint, not a
minor tolerance to be discovered after printing.

A three-state cam slider (park / capture-overlap / move) is preferable for a
first rig. It avoids the mistaken binary assumption that ground disengagement
and moving engagement can happen simultaneously. The return cam should be
blocked by the ground-pawl heel until the ground pawl is fully seated. Cam
position alone does not prove full insertion if a tooth is obstructed.

The selected pin's 0.2–0.4 mm unload movement is permitted preliminary movement;
an unaffected neighbor must not move. Unchanged pins' pawls remain completely
untouched. There is no swap to a second global support datum for those pins.

## Selection transaction and timing: three distinct choices

### A. Reusable direct selector on every lane

All up-moving pins capture at the bottom shuttle endpoint. The shuttle sweeps
up; each lane transfers to ground at its required positive displacement. At
the top, down-moving pins capture and the shuttle sweeps down. Total full-stroke
travel is 80 mm per row, ending where it began. Mixed targets do not require
many complete motion pulses, but each stop is a physical finite-time handoff.

[`analysis/rack-screen.py`](../analysis/rack-screen.py) computes a complete optimistic row transaction with two
trapezoidal 40 mm strokes, 1,000 mm/s² acceleration, 0.12 s endpoint transfer
for each cohort, one 6.35 mm row index at 100 mm/s, and 0.05 s settle. It assumes
intermediate individual releases occur during the strokes. At 80 mm/s a
four-bank machine is around 27 s, with **256 independent reusable selectors**.
This is computationally conditional, not qualified performance.

The weakness is explicit: a 1 mm notch opening passes in 12.5 ms at 80 mm/s;
0.8 mm compliant overtravel buys only 10 ms. A small hobby servo does not
establish this transfer speed. A cam + spring + fast solenoid may, but the
mechanical seating interlock must be built and tested. At 40 mm/s, four banks
take well over 30 s; eight banks are needed under this model. A latch that stops
the rack while its drive dog remains rigidly connected jams the common shuttle.

### B. Serial writer plus binary subset memory

A few writer solenoids can set 64 reusable retained selection sliders before
each common pulse. This can reduce bought active devices dramatically. It does
not independently stop 64 heights on one sweep. Count all subset writes,
capture/preload, pulse, ground restoration, seating, dog retraction, Z reset,
writer indexing and row indexing. Mixed signed deltas require multiple groups
or a signed pulse code. Programming and settling can dominate travel.

There may be a viable five-level D&D transaction using signed 10/20 mm pulses,
but a claimed two-sweep/80 mm schedule cannot simply be reused. Intermediate
height limits matter: representing a negative delta as a large positive pulse
followed by −40 mm may exceed the 40 mm travel limit. The throughput agent should
search physically executable pulse programs against every old/new height pair,
including unchanged pins, before choosing this construction.

### C. Programmed mechanical release-height memory

One reusable stepped slider or cam per lane could store absolute release
displacement (and direction), letting the common shuttle trip a lane at its
programmed target. This could combine a low actuator count with one sweep.
It is **not equivalent to one bit**: at 2 mm resolution it stores 21 positions
and direction. A few reusable writers must set these positions across 64 lanes
within the row time. Eight writers with eight 0.2 s writes already consume
1.6 s/row before terrain motion; four banks then spend 25.6 s just programming.
Sixteen writers, faster coarse cam writing or double buffering may help, at the
cost of mechanical memory, more axes and collision-prone packaging. This is a
bounded escape route, not the preferred prototype until a concrete writer is
shown. Do not assume an arbitrary height encoder is free.

## Minimum meaningful experiment

The architecture-changing question is the **supported signed transfer**, not
whether a rack can slide or a screw can rotate. A four-pin row on 6.35 mm pitch
is enough for the first mechanism experiment; a second unchanged row is needed
to establish transport clearance.

Recommended first module: four cap/stem/racks, one four-pawl flexure comb, one
grounded ledge block, two guide plates, four moving capture dogs, a small common
Z carriage and four manually set three-state cam sliders. Shorten useful
terrain stroke to 12 mm and preserve real pitch, tooth size, guide gaps and
the complete handoff. The rack tooth span must still be 12 mm terrain + 12 mm
shuttle + margin. Reuse ordinary PLA and temporary printed hand knobs; do not
require special spring metal or purchased solenoids for this first answer.

Test sequence: begin [4, 8, 4, 8] mm; move only pins 1 and 3 by +4 mm; restore
their ground support and detach the head; then move only pins 2 and 3 by −4 mm;
then use several pulses to reach [0, 12, 6, 4]. Pins that are unaffected by a
pulse retain their original ground pawls at all times. Place simple witness
marks by every cap, so unintended neighbors or head motion are evident. Record
any manual fitting, missed insertion, tooth damage, latch not returning and
which step jams. Repeat at least ten cycles and repeat the nominal pawl geometry
so a single lucky fit cannot hide variation. This is not a yield estimate.

After this mechanism passes, the next question is reusable writer reset and
mask transfer across rows. An automatic whole-display timing claim additionally
needs measured selector force/time under load and repeated transfer at the
promised speed. Preparing a large automatic print package before the four-pin
handoff is working would spend filament before the key decision.

## D&D geometry remains a separate interface constraint

6.35 mm pitch means four terrain samples per 25.4 mm game square. A full-width
raised boundary pin leaves 19.05 mm in a one-square corridor, failing normal
25 mm bases. The rack proposal does not solve that. A separate thin wall
interface is required, and the finite thickness matters: even a 0.8 mm wall
centered on each boundary leaves only 24.6 mm at floor level. A raised miniature
base carrier, walls offset away from the nominal floor corridor, or an honest
larger physical square are product choices requiring a dimensioned example.
No mechanism should be recommended as playable solely because its pitch divides
25.4 mm. Walls can be thin manually placed panels for a prototype, but automatic
walls would then remain unresolved, not silently considered satisfied.

## External primary evidence and its limits

* [MIT, Peters 2011 thesis](https://dspace.mit.edu/entities/publication/be884414-04ae-4b22-987f-0510b765b98e)
  documents a shared magnetic plate and per-pin fusible-alloy clutch. It supports
  the common-power / local-retention principle, not this project's response time.
* [US20120279812A1](https://patents.google.com/patent/US20120279812A1/en)
  describes that phase-change approach and a reconfiguration timescale of up to
  20 minutes in some implementations. It is not evidence for a 30 s display.
* [US7436388B2](https://patents.google.com/patent/US7436388B2/en)
  describes row/column bars engaging pin grooves. The intersection addressing
  idea is prior art, but a patent disclosure does not validate datum transfer,
  manufacturing yield, dynamic isolation or this project's force budget.
* [US20090063092A1](https://patents.google.com/patent/US20090063092A1/en)
  documents pin-array locking approaches. Global clamping is useful for fixed
  tooling, but releasing global friction support cannot preserve arbitrary
  selected neighbors without another complete support path.
* [Dassault/SIMULIA pawl-ratchet analysis](https://3dexperience.fiir.upb.ro/internal/docv6/English/SIMA3DXEXARefMap/simaexa-c-pawlratchet.htm)
  explicitly treats engagement impact. It reinforces using stopped, supported
  transfer as the first experiment rather than crediting instantaneous catches.

Accessed 2026-10-14. Analogies are design principles; none qualifies the proposed
geometry, proves freedom to operate, or supplies purchased component pricing.

## Honest state of evidence

* Computationally demonstrated: ideal leaf stiffness/load estimates; minimum
  rack overlap length; conditional timing for the specified two-sweep transaction.
* Supported by physical observations: only the repository's owner-reported
  threaded pair results and historical Trial-5 family, not this new rack design.
* Unresolved: actual positive handoff geometry, flexure/ledge wear, compact
  manufacturing yield, selector transfer speed, complete writer mechanism,
  whole-machine assembly labor, D&D wall/base interface, final cost.
* Failed as stated: global bottom platen with gravity called positive lowering;
  crossed Boolean support credited as zero-motion isolation without datum
  analysis; binary selector memory credited with independent continuous stopping;
  40 mm rack claimed sufficient for 40 mm terrain plus 40 mm moving pickup.

The rack architecture merits a small supported-transfer prototype and a complete
serial-writer timing screen. It does not yet justify an assertion of a fast,
affordable, playable full machine.
