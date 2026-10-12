---
status: complete
builds-on: [E-232, E-234, E-238, E-242, E-173]
---

# Head-only overrunning support removes admission writes, not target-writing traffic

**Park this embodiment before pawl, cam or return-spring development.** Moving
one-way support into reusable row heads escapes E-232's rigid-comb ascent
conflict without 6,400 resident moving latches. One six-position target register
can control a whole rise/descent. However, the explicit shared-sweep writer still
uses **five selective binary masks per row**. Its broad-code case needs eight
heads, 640 channels and **28.842 s / $815.80 assumed allocation**. Retaining a
program is not inherently a reduction in physical programming traffic.

Input main `c5fdd0f`. Reproduce: `python3 tools/curated-experiment-checks/E-243/screen.py`.
Evidence: **architecture hypotheses, ideal state replay and bounded calculations;
self-review**. No finite CAD, contact dynamics, sourced prices, manufacturing
priors or physical measurements. All dimensional, force, time and price values
below are assumptions. Five heights 0/10/20/30/40 mm are a comparison alphabet,
not an approved product resolution.

## Changed support transaction and controls

Each column has five broad ramped rack shelves, a distinct bottom pickup foot,
and two guides. One common resident row comb holds all 80 columns while parked.
Each traveling bank head carries 80 independently returning, frame-backed
one-way pawls plus 80 selectively inserted bottom pickup fingers on one elevator.
Pawls engage the periodic rack at one fixed head height regardless of old height;
the actual contacted tooth carries that height. All these pawls, pivots and
returns travel with the head: there are 80B, not 6,400. A retained target bar per
head channel stores U (unchanged) or one of five absolute heights.

1. With the row comb still engaged, write, clamp and read the target bars. Insert
   all head pawls and prove takeover, then withdraw the row comb. U codes leave
   pickup fingers withdrawn. Other codes insert and retain their pickups.
2. Raise the pickup plane from 0 to 42 mm. Until reached, an old column rests on
   its fixed head pawl. After pickup, it rises and the pawl overruns successive
   ramped teeth. There is no commanded old-height release or old-height register.
   U columns remain on their head pawls. Stop at old levels to prove acquisition.
3. At the apex all selected columns are pickup-supported. A common mode rail
   retracts selected pawls; U bypasses that rail and stays supported. A cam
   follower reads each stationary target bar against a common descent coordinate.
   Release each pawl for insertion at plane=target+1 mm, prove its return, descend
   the last millimetre and prove bearing. Keep it engaged thereafter while the
   pickup continues down. Highest target 40 also receives a real return event.
4. Prove the actual final profile, insert/prove the resident comb, clear pickups
   and head pawls, reset the common mode and feed the head to the next row.

The assumed cam is a translated threshold edge, not a five-track decoded word:
bar offset is target code times p; the common reader traverses four p-spaced
thresholds with descent. U occupies a sixth bypass position controlling both
pickup admission and pawl-mode exclusion. Two output paths, their retained
positions and common-mode discrimination remain **unconstructed**. A threshold
formula does not supply the force or travel of either output. Linear reader
motion can be mechanically coupled to lift position; no independent free phase
jump is credited. The cam must release a pawl while maintaining pickup support.

E-173 already identified overrunning pawls and their first-tooth catch problem;
this does not claim a new ratchet principle. Its narrow five-lane resident dog
is avoided. E-232 fixed supports block ascent or release too early; here each
head pawl can overrun independently. E-234 avoids acquisition with paired
resident bars but adds 12,800 bars. E-238 retains pulse words yet preserves all
pulse transfers. This construction changes the support transaction, at the cost
of cyclic loaded head pawls and an unbuilt threshold-to-output linkage.

Ideal replay covers 15,625 three-cell maps / 4,031,250 sampled support observations.
The continuous ideal argument is `h=max(old,plane)` on ascent and
`h=max(target,plane)` on descent for selected cells, with U invariant. This is
only valid if pawls overrun and return and gravity follows. Removing target
gating gives `(10,30,20)->(40,40,20)` when `(20,0,20)` was requested: one-way
support alone cannot encode the target.

3,125 two-cell stable wrong-target cases and 625 stable partial-state retries
re-encode actual supported heights successfully. Wrong-target injection preserves
U: it does **not** qualify a corrupted U code, which can move an unchanged cell.
A bad pre-motion program must be rewritten with resident support present. A late
recoverable mismatch needs stable head support, resident reseating, actual-height
readback, empty reset and then a fresh write/service cycle. A stuck pawl, hanging
column, off-grid position or failed support proof requires supported shutdown;
no 30-second repair or false-acceptance guarantee is asserted.

## Physical writing and complete schedule

One horizontal register per head avoids upright loose-bar gravity retention.
Its six positions span D=5p. A common reset pushes all unloaded bars to zero;
q retractable pushers on a common ram write groups of 80/q. Each group presets
all pushers, releases the code-zero subset, makes five stopped p strokes,
releasing the appropriate subset at each interior boundary, then clears the
last group and returns empty. Temporary drag holds early-retired bars until a
common positive clamp seats and is read. Friction hold/clamp geometry is unbuilt.

Thus each group needs **five selective q-bit decisions**, plus preset and final
clear. Whole-row selective traffic remains 400 bits / 32,000 per full map, just
like five 80-bit rewrites in E-242. It additionally writes 6,400 multilevel states.
Packing a code into three electronic bits does not build a three-bit mechanical
setter. A direct absolute-position ram would be a different, richer channel.
Minimum basic reads/row: 80 program, 80 pickup-mask, 400 level-pawl outcomes and
160 old/final heights = 720, before row-comb and actual bearing proofs. Shared
views and 3/10-ms proof/read allowances are grants, not a sensor design.

Let t(d) be rest-to-rest motion at 200 mm/s, acceleration 8,000 mm/s²,
J=t(2)+.003=.034623 s, n=80/q. Writer:

`W=2t(D)+2J+.010+n[5t(p)+7J+t(D)]+(n-1)t(5.08)+t((n-1)5.08)`.

Service grants eight contact stages for pickup on/off, head-pawl approach/clear,
row-comb out/in and mode out/back. Ascent is four 10-mm strokes, 2-mm overtravel
and five proof dwells. Descent is 1 mm to the first pre-seat point, five 1-mm
seating strokes, four 9-mm inter-level moves, five J return/proofs and five
bearing dwells. Add row feed and two height reads: **S=1.296283 s**. Actual
mode/pickup routing may need more stages. No overlap or second buffer is granted.

Full map, including one causal whole-row retry and conservative empty reset:
`T=2+(ceil(80/B)+1)(W+S)+t(42)+.010`. Two common seconds allocate ingestion,
initial registration/homing, final proof and settling. Lift-acceleration
sensitivity changes only lift motion; writer/contact/feed retain their bound.
Three separately expanded timelines cross-check the equation.

| p mm / lift acceleration m/s² | B / q / writer channels | Full map s | Assumed bought allocation |
|---|---:|---:|---:|
| 4 / 8 | 10 / 40 / 400 | 28.419 | $771.00 |
| 6 / 8 | 8 / 80 / 640 | 28.842 | $815.80 |
| 8 / 8 | 9 / 80 / 720 | 28.424 | $893.40 |
| 6 / 2 | 14 / 40 / 560 | 29.614 | $1,001.40 |
| E-238 retained pulse control, 6-mm codes/tracks | 8 / 40 / 320 | 27.842 | $588.60 |
| E-242 favorable flying magnetic control | 5 / 20 / 100 | 28.016 | $509.96 |

New rows minimize allocation over q divisors of 80 and B=1..80 for each stated
p/acceleration. Controls have different unresolved physics; none is a machine
pass or price floor. Broad-code B8 has only .1053 s additional allowance per row.
Five contiguous rows plus retry need 16.752 s; sparse seek needs real routing.
Selected cells visit 42 mm (up to 32-mm detour); U is invariant only ideally.

## Replication, manufacturing, force and service

B8 has ten rows/800 cells per bank. Counts are functional failure sites, including
monolithic printed arrays; all positions and forces still require qualification.

| Function | Cell / row | Head or bank | Board |
|---|---|---:|---:|
| Columns / guide stations | 1 / 2; 80 / 160 per row | 800 / 1,600 | 6,400 / 12,800 |
| Rack shelves / resident comb bearings | 5 / 1 | 4,000 / 800 | 32,000 / 6,400 |
| Resident comb axes / positive keepers | 1 each per row | 10 each | 80 each |
| Head pawls / pivots / individual returns / grounded stops | shared | 80 each | 640 each |
| Pickup fingers / retained selection / guide duties | shared | 80 each | 640 each |
| Target bars / clamp sites / drag sites / cam followers | shared | 80 each | 640 each |
| Code positions / output paths | shared | 480 / 160 | 3,840 / 1,280 |
| Writer fingers / binary channels | shared | 80 each | 640 each |
| Lift arrest / reader / row registration | shared | 1 system each | 8 systems each |

Target follower and pickup returns add at least 80 more return duties/head;
exact part sharing, socket/insert/fastener and guide-face counts are unresolved,
not zero. Compared with the seven-shelf control, 12,800 resident shelf levels
are removed. Upward overrun adds wear: all 20 unequal height pairs produce 40
ratchet crossings, mean two/changed cell; a full all-0-to-40 map has 25,600
crossings. Pawls are serviceable shared wear components, not zero-cost logic.

Illustrative column stock 80x4x4 mm remains 8.192 L. Program stock
(5p+4)x4x3 mm at p6/B8 is .261 L. Together 8.453 L implies 157–470 extrusion
hours at assumed 15–5 mm³/s before other hardware, travel/setup and scrap;
10% scrap multiplies by 1/.9. Print orientation must balance rack-root layer
strength and guide finish. 406.4-mm rows require modular joined datums on the
256-mm bed. Eight sets of pawl/pivot/pawl-return/program/follower/follower-return/pickup/writer
placements per channel mean 5,120 head placements, 14.22 h at assumed 10 s each;
column insertion adds 8.89 h at 5 s each, excluding wiring and calibration.

A generous common horizontal enclosure takes bar length (5p+4) plus the larger
of its 5p setting travel and 4p reader sweep: **10p+4 mm** feed-axis depth.
At p6 that is 64 mm, limiting a single planar allocation to six banks before
frames: **38.513 s** even with q80. Eight banks owe depth staggering and real
head access. p4 permits nine bays, but the least-allocation ten-bank case does
not fit; a faster q80/nine-bank allocation costs more. No routed CAD is implied.
Bottom-foot pickups and rack pawls require separate lanes during overlap;
E-231's thin side-blade problem is not assumed solved.

Competing error bounds e=.15/.35/.70 mm are not X1C priors. A 2-mm code probe
at p6 has `(p-2)/2-e`=1.85/1.65/1.30 mm indexing margin. A 2-mm pawl in a
4-mm axial opening, inserted at the centered 1-mm pre-seat offset, has
**1-2e=.70/.30/-.40 mm** worst insertion margin under opposing errors.
Inserting at target+2 would have zero nominal margin; the schedule does not
credit that edge coincidence. These inequalities omit rotation, deflection,
ramp contact, roughness and rebound. Opposing comb/pawl height errors can cause
2e=.30/.70/1.40-mm takeover movement of U cells. Common batch bias, joined-frame
warp and reader phase error correlate a row/bank; no iid yield is inferred.

At assumed .5-kg moving equipment/head, 3-g columns, .005-N guide drag, a8 and
0–5 kg payload concentrated in active rows, B8 lift force is **109–198 N**,
31–56 W input at .7 efficiency and .2 m/s, before pawl-ramp reaction. If ramp
reaction is r per rising cell, add up to 640r N; r=.05/.2/1 N adds 32/128/640 N.
These are sensitivity bounds, not measured friction/spring loads or a required
D&D payload. Gravity following still needs drag <.00543 N per unloaded 3-g cell
at a8, with zero preload at equality. Spring force, tooth strength, PLA creep,
wear and eccentric guide loads are unresolved. No local spring design follows.

During ascent a returned pawl can catch the next rack shelf after a drop up to
one 10-mm pitch, with unmodelled impact. During descent retracted pawls may offer
no arrest above the target. Therefore local elevator arrest remains mandatory;
passive pawls do not qualify power-loss safety. A head fault affects 800 cells
scheduled in its bank; a row keeper fault threatens 80. Service needs resident
support before head extraction and temporary support for failed comb removal.

Allocation (not quotations): inherited common $195 for controller, power, frame,
wiring/spares, lift/brake, phase/feed/writer drives and shafts/bearings; $20/head
for reader/enable/arrest/mounts; $.50/complete writer channel; $.02/program
retention; $.10 for each of 160 spring/pivot/return duties/head. B8 totals
$195+$160+$320+$12.80+$128 = **$815.80**. Its non-channel reserve is $495.80,
leaving only $.00656/channel under $500; deleting all $128 return-duty allocation
still gives $687.80. These are budget sensitivities, not market-wide lower bounds.
Actual supply, sensors, fixtures, couplings and rated arrests can increase them.

## Decision

Preserve head-only overrun as a **conditional admission principle**, and the
counterexample showing that one-way support still needs target gating. Stop the
specified sweep-written target-cam machine: fewer row programs did not mean less
physical command traffic; banking, repeated head parts and finite packaging
outweigh the ideal transfer simplification. No print or local pawl work.

Next investigate **load-path transposition**: can an accessible shared support
store height without either a repeated rack interface or copying a program into
hundreds of retained outputs? Start with finite routing and material/information
flow for flexible tensile supports versus compression-media controls. A cable is
not an answer until its anchor, stored length, support during rewriting, loaded
neighbor isolation and 6,400-path assembly/service are counted. Reject if this
only relocates a spool/brake per cell. Reuse E-126/E-163/E-234 as controls before
new work; do not repeat the magnetic writer or target-cam refinement.
