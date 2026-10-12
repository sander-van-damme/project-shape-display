---
status: complete
builds-on: [E-230, E-236, E-237]
---

# Retaining a row program trades writer channels for physical decoding

**Park the tested retained pattern bars and direct phase-bit registers.**
Combining E-230's retained programs with E-236's shorter supported motion does
not justify their fabrication burden. With 6-mm code and phase-track pitch,
the least-allocation sampled bar machine needs **eight banks, 320 writer
channels, 1,280 bars, 12,800 index sites and 64,000 decoder lands**, at
**27.842 s / $588.60 assumed bought allocation**. Three-mm codes reduce this
to 160 channels/$508.60 but leave only .15-mm margin at the .35-mm adverse
error bound. No local decoder, tooth, keeper, scanner or print is selected.

Input main `4c48018`. Reproduce with
`python3 tools/curated-experiment-checks/E-238/screen.py` (stdlib; stdout only).
Evidence: **exact finite synthesis, ideal support replay and calculations under
labelled assumptions; self-review**. No sourced process distribution, quoted BOM,
finite routed CAD, contact dynamics or physical measurement. Five heights
0/10/20/30/40 mm remain a comparison workload, not an approved product limit.

## Joint stroke/program synthesis

A bar stores one **whole-row-duration pulse program per column**, clamped before
service. Five or six pattern tracks are read in turn by a shared phase carriage.
An inactive second register can be erased, written and read while the active
register remains clamped. Outputs still perform E-236's four supported contact
stages per pulse; retention eliminates pulse rewriting, not load transfers.
This differs from E-237's attempt to overwrite a live command during withdrawal.
The alternate control stores one independent binary slide for every phase,
avoiding multilevel positioning but multiplying retained sites.

Generator: all closed pickup walks on q={−4,−3,−2,−1,0}, starting/ending zero,
with five or six nonzero integer strokes. Enumerate every binary participation
word for each of 25 old/target pairs; reject intermediate heights outside 0…4,
required shelves outside 0…6, and any movement of unchanged cells. Exact set
cover is separable by net delta: one word has only one delta; dynamic programming
over the up-to-five starting-height requirements finds the fewest distinct words.
Tie-breaks are deterministic. Group into 53 equivalence classes containing every
sequence-dependent schedule/inventory input; retain low-travel representatives.

| Strokes | Walks tested | All pairs reachable | Seven shelves sufficient | Fewest retained codes |
|---:|---:|---:|---:|---:|
| 5 | 204 | 28 | 18 | **10** |
| 6 | 820 | 397 | 277 | **9** |

E-236's [-20,−10,+30,−10,+10]-mm walk needs two different +20-mm words:
0→20 can use +30−10, whereas 20→40 can use −10+30. Their compatible-word sets
have empty intersection across all three old heights. Thus its nine possible
deltas are **not** nine reusable physical programs. Four digital address bits
could name ten codes, but a four-bit mechanical decoder is not free; E-230's
sign/magnitude two-gate construction does not supply this truth table.

The finite-track least-allocation bar case selects **[−20,+10,+10,−20,+20] mm**,
pickup q=[0,−2,−1,0,−2,0]. It uses ten codes, .525-s motion, seven shelves and
at most 20-mm extra column travel / 10-mm detour outside its endpoint interval.
For this walk −10 mm has two words, chosen from actual old height. It reduces
worst empty-datum recovery to 20 mm; it does not reduce physical phase decoding.
Six-stroke nine-code walks can take .550-s lift motion, but their extra transfer
and decode outweigh reduced bar-writing travel in the finite-track cases here.
No optimum is claimed over longer walks, continuous heights or other decoders.

Replay covers **46,875 three-cell maps**, including the selected five-stroke
walk, E-236's walk and a six-stroke control; partial retry checks cover every
selected representative. Five injected interlock failures are caught. These
are ideal support/invariance checks, not independent validation or contact proof.

## Physical writing, phase travel and complete update boundary

Position writer: unlock an inactive register, reset all bars, retract resetter,
push q bars to commanded absolute positions, retract, index to the next group,
return the writer, clamp and read. Previous groups need temporary drag retention
until clamping. For K codes at pitch p, D=(K−1)p; n=80/q groups:

`W=2t(D)+2t(2)+.010+n[2t(D)+.010]+(n−1)t(5.08)+t((n−1)5.08)`.

Assumptions: v=200 mm/s, a=8,000 mm/s²; contact throw 2 mm; per-stage proof
.003 s; initial/final row-height reads .010 s each. Inherit E-230's finite-gap
binary scanner with .35-mm adverse phase error; direct phase bits require
400/480 retained sites per register. All reset, feed, return and read time is
inside the map boundary. No new media is prepared before map receipt.

A spatial strip needs physical track selection. Retain E-230's favorable
`J=t(2)+.003` per-phase decoder release/proof allowance; **add** n−1 moves
between tracks and return to track zero. At 6-mm track pitch, five phases add
`4t(6)+t(24)=.365 s/row`; six add .450 s. Normal re-engagement is granted within
the pickup-acquisition stage. This is a named, unconstructed coupling, not a
proof that the layout fits. A rotary or stationary multi-probe decoder could
change this cost but owes its own finite geometry and replication ledger.
The **zero-span oracle** deletes lateral travel only; it is not a free decoder.

Service is lift motion + four contact stages/pulse + nJ + phase travel + row
feed + two height reads. Two physical buffers use separate writer/service
selection interfaces, each charged J. Writing register i waits for writer i−1
and service i−2; service i waits for its write and prior service. Include 2 s
common processing/registration/final settling. After a detected recoverable
fault: establish resident support, read actual heights, return the empty datum,
regenerate and **then** write and serve a complete retry. The model charges this
serial retry after the pipeline, including its phase reset and conservative row
feed; this also bounds inserting it earlier without overlap credit. Never retry
from the original delta. No <30-s jam, structural repair or false-proof claim.

Sweep B=1…80, q={1,2,4,5,8,10,16,20,40,80}, one/two registers, code pitches
3/4/5/6 mm, and five/six-stroke equivalence classes. Least-allocation examples:

| Encoder | Phase travel | Buffers | Banks / channels | Full map incl. retry | Allocation |
|---|---|---:|---:|---:|---:|
| 3-mm code bars | zero-span oracle | 2 | 5 / 200 | 29.937 s | $447.00 |
| 4-mm code bars | zero-span oracle | 2 | 6 / 240 | 27.486 s | $494.20 |
| 6-mm code bars | zero-span oracle | 2 | 7 / 280 | 29.165 s | $541.40 |
| 3-mm code bars | 6-mm tracks | 2 | 8 / 160 | 27.859 s | $508.60 |
| 4-mm code bars | 6-mm tracks | 2 | 7 / 280 | 29.240 s | $541.40 |
| 5-mm code bars | 6-mm tracks | 2 | 7 / 280 | 29.780 s | $541.40 |
| 6-mm code bars | 6-mm tracks | 2 | 8 / 320 | 27.842 s | $588.60 |
| Five direct phase bits | 6-mm tracks | 2 | 7 / 280 | 29.273 s | $631.00 |
| 6-mm code bars | 6-mm tracks | 1 | 14 / 560 | 28.665 s | $777.40 |

The broad-code B8 example is 23.847 s without retry; a contiguous five-row
patch in one bank is 17.848 s including retry. Unvisited banks keep resident
supports; unchanged cells in a visited row depend on their column bars while
row support is withdrawn. Common feed may traverse no-op rows for sparse maps;
no free independent seek is claimed. Opposing support error can still cause
settling even when logical height is unchanged.

## Full-machine replication, fabrication and service

Resident hardware is unchanged: one column, two guide/wear stations, seven
shelves and two resident bearing sites per cell; 80/160/560/160 per row;
800/1,600/5,600/1,600 per B8 bank; **6,400 columns, 12,800 guides, 44,800
shelves and 12,800 resident bearing sites** per board. One row support axis/row,
ten/bank, 80/board. No additional resident moving latch, spring, motor or insert.
Common comb printing does not eliminate the individual bearing failure sites.

For the B8/two-register/6-mm bar construction:

| Added/shared function | Per bank/head | Board |
|---|---:|---:|
| Column-bar axes / reusable pickups / decoder probes | 80 each | 640 each |
| Output links | 160 | 1,280 |
| Program bars / temporary retention sites | 160 each | 1,280 each |
| Index sites / patterned decision lands | 1,600 / 8,000 | 12,800 / 64,000 |
| Common program clamps / buffer selection interfaces | 2 each | 16 each |
| Independent multilevel rams / ram guide duties | 40 each | 320 each |
| Lift, phase carriage, row carriage, reader, bank enable, local arrest | 1 each | 8 each |

Lands count functional solid/bypass positions, not separately assembled parts.
Every program bar needs a slide guide and retention contact; 320 ram guides,
probe guides, output connections, end stops, fixtures and wired terminations are
additional. Exact spring/socket/insert/bearing counts remain **unconstructed**,
not zero. A six-mm pitch does not fit a 30-mm-wide five-track pattern at a
5.08-mm cell pitch: staggered bays and output bridges remain explicit routing
obligations. No compactness pass is inferred from scalar timing.

Assumed 62×30×3-mm program blanks total **7.1424 L**, 132–397 extrusion hours
at 15–5 mm³/s, before guide/carriage/frame stock and setup. Add the inherited
8.192-L column blanks (152–455 h); 10% scrap multiplies stock/time by 1/.9.
At assumed 10 s/program-bar insertion, bars add 3.56 h; 3,200 bar/pickup/probe/
link placements add 8.89 h, before rams, guides, wiring, fixtures and calibration.
Columns add 8.89 h at 5 s each. These are work estimates, not measured prints.
256-mm build volume requires segmented 406.4-mm support rows and aligned joints.

With a 2-mm probe, code spacing p permits `(p−2)/2−e` positional margin.
At e=.15/.35/.70 mm, p=3 leaves .35/.15/−.20 mm; p=6 leaves
1.85/1.65/1.30 mm. Four/five-mm pitches are also screened, not excluded by an
arbitrary clearance threshold. Index-clamp seating, probe deflection, drag,
roughness, wear and contamination consume margin. The resident 4/2-mm shelf/
tooth example still leaves 1−e mm, and opposing support errors allow 2e settling.
Bounds are competing assumptions, **not X1C distributions or IID reliability**.
Module warp, batch shrinkage, common writer bias and phase-carriage error can
corrupt entire rows/banks; no zero-failure replay establishes production yield.

A bad code threatens one head channel; phase/clamp faults threaten 80 cells;
a column-bar fault spans ten rows; row-comb failure exposes 80; a bank fault
halts 800. Replacement requires proved resident support and accessible modules;
buried guide/comb removal and temporary support remain unconstructed. Program
readback alone cannot establish load-bearing contacts. Assumed camera/folded
views owe code, phase, pickup, bar and actual-height coverage with declared
latency and fault detection. A common end flag is not 80 contact proofs.

## Allocation, force and decision

Inherit E-230's **unqualified** $195 common categories (controller, supply,
frame, wiring, spares/freight, lift/brake, phase/feed/writer drives and shafts/
bearings), $20/bank for reader/enable/local arrest/mounting, $.50 per complete
writer channel, $.02/media site, $2/buffer interface and $16 common buffer
drives. B8/q40 gives $195+160+160+25.60+32+16 = **$588.60**.
Even these optimistically price a multilevel ram like a binary gate. The
non-channel allocation is $428.60; meeting $500 would require each complete
320-channel writer to cost at most **$.223125**, with every other allocation
unchanged. This is a spending threshold, not a sourced impossibility theorem.

At E-230's uniform 3.27-N/cell scenario, eight active rows require **2.598 kN,
25.98 N m output torque, 742 W peak input** and .638-mm height-equivalent twist
of its assumed end-loaded 12-mm steel shaft. These are **load scenarios, not
established D&D product requirements**; they must not become a universal
rejection threshold. Writer reset adds `640R` N at B8 for drag R per bar;
320 simultaneously active rams add `320R` N during setting. R=.3/1/3 N gives
reset 192/640/1,920 N. These forces and acceleration of unweighed media/cams
are not covered by a qualified $20 writer-drive purchase.

Power loss during writing must leave the active program clamped and resident
support intact. During motion, output engagement and bank-local arrest must
survive loss of the common shaft. The allocated brake and $3/bank arrest do
not establish that behavior. No cheaper force-rated drive or brake is assumed.

**New durable result:** supported five-stroke programs need at least ten codes
in this grammar; retaining them trades command rewrite time for state, decoding
and actual phase transport. Cheap digital information capacity does not supply
a cheap mechanical decoder. Keep the exact compiler and schedule comparisons;
stop this retained-strip embodiment before fine-feature refinement. E-236's
simpler direct control remains a comparator, not a selected product.

Next decision-relevant work should resolve the **physical shared-drive and
writer-channel allocation**, rather than another decoder contact: establish
bounded total-board/miniature loading and worst active-row concentration, then
compare complete purchasable actuation/arrest and command-channel implementations
for the simple direct control. Report exact load/price tipping points without
inventing a product load requirement. Only a credible machine-level escape can
reopen retained strips; no narrower codes, free phase travel or nominal cheaper
channel suffice. No print is justified by this screen.
