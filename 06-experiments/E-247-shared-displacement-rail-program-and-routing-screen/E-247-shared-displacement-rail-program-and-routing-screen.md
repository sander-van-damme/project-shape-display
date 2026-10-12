---
status: complete
builds-on: [E-232, E-238, E-243, E-236]
---

# Shared displacement rails remove pulse transfers, not the physical selector

**Park the specified transverse-selector rail machine before local development.**
A retained nine-way choice can distribute signed displacement directly from
shared rails: one loaded stroke, no intermediate mask rewrites, no column detour.
But the explicit sweep writer needs eight selective passes, and the finite
single-plane routing does not fit the parallelism its timing requires. This is
new conditional motion topology, not a selected architecture or print proposal.

Input main `05c5d0e`. Reproduce:
`python3 tools/curated-experiment-checks/E-247/screen.py` (stdlib, stdout only).
Evidence: **ideal state replay, analytical geometry and scenario calculations;
self-review**. All numerical hardware inputs are labelled assumptions; no CAD,
contact simulation, sourced prices, calibrated process distributions or physical
measurements. Five heights 0/10/20/30/40 mm are a comparator, not product resolution.

## Motion distribution instead of command decoding

Each resident column retains E-236's simple seven shelf levels, two guides and
common row comb. A reusable head has one vertically guided rack shoe per column.
At acquisition all shoes lie at z=-20 mm and engage the appropriate shelf of each
old column. A transverse selector in each shoe chooses one of nine backing rails,
labelled d=-40,-30,...,+40 mm. A single common progress coordinate lambda drives
rail displacement `z_d=lambda*d`; the zero rail is grounded. Eight shared cam or
ratio outputs and their guides provide this law; no cam geometry is constructed.
The selectors are written, positively retained and read while unloaded.

Sequence: program; insert/prove all shoes with row comb present; withdraw row
comb; advance lambda 0→1; insert/prove row comb at target; retract shoes; reset
empty rails and feed to the next row. Load path during movement is column shelf
→shoe→retained selector→chosen rail→cam/drive and local arrest→frame.
Program retention must survive the full signed stroke, including power loss.
Selection cannot be rewritten under load. Common shoe insertion/withdrawal at
different final heights needs a vertically extended release interface, unbuilt.

For selected d=target-old, `h=old+lambda*d` lies between endpoints. All nine
signed deltas are necessary in this **one choice/one displacement** grammar;
there is no universal nine-output lower bound for other mechanisms. Unlike
E-238's ten pulse words, there are no phase tracks or twenty contact stages.
Unlike E-243 there is no apex visit, overrunning pawl, or target-threshold return.
Unlike E-232 fixed targets, the rack shoe acquires old heights at one datum;
there is no rising plane that must release old supports as it arrives.
The nine-way loaded selector and ratio outputs are the explicit price of escape.

Replay checks 15,625 three-cell map pairs / 2,156,250 support observations. A
convex-interpolation argument independently covers intermediate lambda, beyond
the 41 sampled positions. Four injected faults (missing takeover, live code
rewrite, lost arrest, missing reseat) fail the ideal interlocks. Actual sensing
and physical reactions are granted, not proven by assertions.
125 single-cell stable wrong-result/retry cases and 65 on-grid partial cases
recompute delta from actual supported height. These tests do not certify reader
coverage, corrupted unchanged codes, or off-grid recovery. At fractional height
a row comb may not engage; retained rail arrest and controlled completion or
supported service are required. No 30-second repair claim covers a broken rail,
stuck shoe, failed tooth, or unproved contact.

## Finite route and unchanged-column limitation

Concrete routing screen: nine parallel rails across a transverse bay, pitch p.
Each vertical output carries a sliding bridge with a downward post contacting
only the selected rail. At neutral all rails share a height. A bridge spanning
other rails must clear them throughout the stroke. The +40 rail rises **80 mm**
relative to a bridge following -40. A short post therefore collides even at zero
manufacturing error. Keeping the bridge above all rails requires at least 80 mm
standoff plus clearance; 82 mm is the illustrative grant. Isolated post lanes,
anti-rotation, guides and load retention remain unconstructed. This bound is
specific to bridges over coplanar parallel rails; external rotary transmission
or distributed decks changes the route and must pay its own coupling burden.

For selector range D=8p, a bridge blank D+4 long translated through D occupies
`16p+4` mm along the feed direction. At p=6 this is 100 mm, so only four such
bays fit within 406.4 mm even before frames. At p=3/4/8 the corresponding caps
are seven/five/three. Different elevations could exceed these caps, with new
head access, output extensions and transport not credited here.

A 48-mm cantilever, 3.4×6-mm rectangular section, under assumed 1 N has
2.353 MPa bending stress and .201–.602 mm deflection for assumed E=3–1 GPa.
At 10 N: 23.529 MPa and 2.008–6.024 mm (large-deflection linear estimates signal
model limits). These are competing material/load bounds, not PLA allowables or
miniature requirements. Wider/deeper bridging needs a fresh packaging ledger;
no beam optimization follows this screen.

Unchanged d=0 columns do not deliberately move in the ideal law, but **all 79
unchanged columns transfer support** when one cell in a row changes. They rest on
the grounded zero rail while the resident comb is withdrawn. Opposing row/shoe
height errors permit up to 2e takeover movement (.30/.70/1.40 mm at e=.15/.35/.70).
One takeover/return reduces repeated exposure versus E-236's five cycles; it does
not establish disturbance-free regional isolation. Retaining the row comb for
unchanged cells requires segmentation or selective resident releases, absent here.

## Full online schedule and allocations

Assume rest-to-rest t(d) at 200 mm/s, 8,000 mm/s²; J=t(2)+.003 s. A horizontal
sweep writer resets all selectors, releases subsets at eight stopped increments,
then clamps and reads the program. For q writers, n=80/q:

`W=2t(D)+2J+.010+n[8t(p)+10J+t(D)]+(n-1)t(5.08)+t((n-1)5.08)`.

Ten command stages/group are preset, eight selective releases and final clear.
Temporary drag holds retired selectors before the common lock. Eight masks mean
640 selective bit decisions/row, **51,200/full map**, versus E-236's 32,000.
Four electronic code bits do not build a four-bit physical setter. A richer
absolute-position oracle replaces the bracket with `2t(D)+.010`; its independent
multilevel actuator, force and sensing are deliberately unconstructed.

`C=W+4J+2t(40)+t(5.08)+.020`;
`T=2+(ceil(80/B)+1)C+t(40)+.010`.
The four stages cover shoes in/out and row comb out/in. Loaded stroke and empty
reset, first physical write, row feed, reads, initial/final two-second allowance,
one causal complete-row retry and conservative extra empty reset are included.
No buffering or prewritten map. Three expanded timelines cross-check the formula.
Scan B=1..80, q divisors of 80, p=3/4/6/8; restrict B for the planar control.

| Scenario | B / q / channels | Map seconds | Assumed bought allocation |
|---|---:|---:|---:|
| Sweep p3, fits bay bound only | 6 / 80 / 480 | 29.673 | $672.60 |
| Sweep p6, routing granted | 8 / 80 / 640 | 27.748 | $831.80 |
| Sweep p6, four planar bays | 4 / 80 / 320 | **50.942** | $513.40 |
| Absolute oracle p3 | 6 / 40 / 240 | 28.169 | $552.60 |
| Absolute oracle p6, routing granted | 8 / 40 / 320 | 29.173 | $671.80 |
| Absolute oracle p6, four bays | 4 / 80 / 320 | **40.206** | $513.40 |
| E-236 direct pulse control | 5 / 80 / 400 | 26.681 | $675.00 |

New-case allocation: $195 common controller/power/frame/wiring/spares/lift-brake/
feed/writer/shafts-bearings categories, $20/head reader/enable/arrest/mounting,
$.50/complete writer channel, $.02/selector lock, and $2 per rail/head for
additional guide/backing/arrest duties: `195+39.6B+.5Bq`. Cam manufacture,
force-rated drives, sensors and mountings are not sourced at these allowances.
At broad B8, non-channel allocation $511.80 already exceeds $500; removing the
entire $144 rail allowance still leaves $687.80 with sweep writers. These are
allocation sensitivities, **not market price floors**. Five visited rows at B8/q80
cost 16.151 s including the same retry/reset, before sparse seek extensions.

## Whole-machine manufacturing and service ledger

Broad B8 means ten rows/800 cells per bank. Functional sites count even when
monolithic; the head is reusable but must be built eight times.

| Function | Per cell / row | Per head or bank | Board |
|---|---|---:|---:|
| Columns / guide stations | 1/2; 80/160 per row | 800/1,600 | 6,400/12,800 |
| Fixed shelf levels / resident bearing sites | 7/1 | 5,600/800 | 44,800/6,400 |
| Row comb axes / retained keepers | 1 each/row | 10 each | 80 each |
| Vertical shoes / transverse selectors / load posts | shared | 80 each | 640 each |
| Shoe guides / selector guides / locks / temporary drag sites | shared | 80 each | 640 each |
| Nine-way selectable rail contact locations | shared | 720 | 5,760 |
| Rails (eight moving + one grounded) / end guide duties | shared | 9/18 | 72/144 |
| Writer channels / output interfaces | shared | 80/80 | 640/640 |
| Ratio outputs / bank-local arrest systems / row readers | shared | 8/1/1 | 64/8/8 |

A bank arrest must ground every coupled degree of freedom, not just the input
shaft; broken downstream paths remain faults. Exact added springs, sockets,
inserts, bearings, fixtures and wire terminations are unresolved, not zero.
Resident fixed shelves are not equivalent to 44,800 moving failure sites.
At 10 s each, four head placements per channel already mean 7.11 h; column
insertion at 5 s means 8.89 h, before 72 rails, 80 keepers, wiring and calibration.
A selector fault affects a cell; a rail/cam/registration fault can affect a
cohort or row, and stops work on its 800-cell bank. Head extraction requires
resident support; failed comb replacement needs an independent support fixture.

Illustrative solid stock: 80×4×4-mm column blanks 8.192 L; 640 bridge/post blanks
(52×3.4×6 and 82×3.4×4 mm) 1.393 L; 72 rails at 406.4×4×8 mm .936 L. Total
**10.521 L**, excluding shoes, frames, cams and guides; 195–585 extrusion hours
at assumed 15–5 mm³/s, multiplied by 1/.9 at 10% scrap. Not slicing estimates.
The 256-mm bed needs modular beams; horizontal bridge strength competes with
vertical post/guide print orientation and joined-datum accuracy.

With a 2-mm selector follower, lateral margin `(p-2)/2-e` is .15 mm at p3/e.35
versus 1.65 mm at p6. Shared bias, rail parallelism, 82-mm-post tilt, warp,
backlash, contact deflection and wear are not independent. Example 1-degree
post tilt displaces its end 1.43 mm; no such angle is asserted as a process
prior. Common proof cannot certify every loaded seat. No yield is calculated.

Assume .5-kg moving head equipment, 3-g columns, .005-N drag/cell and 0–5 kg
external load concentrated in the eight active rows. Treating all moving mass
at maximum acceleration bounds nominal lift demand at 109–198 N /31–56 W
input (.7 efficiency, .2 m/s), before cam, slider or guide loss. Unloaded 3-g
columns still need total downward guide drag below .00543 N at 8 m/s²; gravity
following is unqualified. Opposing rail loads cannot be assumed to cancel.
Cam contact stiffness, creep, shaft sag, actual running torque and braking
remain open. No mechanism derives free support from the kinematic equation.

## Decision and next discriminator

Keep the monotonic displacement-distribution principle and its finite bridge
obstruction. Stop this sweep-written transverse bridge embodiment: broad pitch
requires too many bays; narrow pitch does not fix allocation, loaded slider
multiplicity, or unchanged-row takeover. Do not refine its selector lock, post,
cam groove or spring. No CAD or print is justified.

Next screen **unloaded binary composition of a retained selector position** as a
shared-programming principle, against this eight-pass writer and E-243's five-pass
writer. The question is whether weighted shared strokes genuinely reduce physical
writing without three/four retained clutches per channel, carry interference or
unproved temporary holding. Start with finite operation/retention accounting and
reject before contact detail if it merely relocates the decoder. This is an
investigation direction, not permission to resume any parked loaded mechanism.
