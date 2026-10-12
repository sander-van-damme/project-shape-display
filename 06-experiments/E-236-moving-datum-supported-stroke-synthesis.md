---
status: complete
builds-on: [E-228, E-229, E-230, E-220]
---

# Five supported strokes remove empty returns without adding column shelves

**Retain the synthesized transaction; park the tested physical writers.**
A moving pickup datum and bounded nonmonotonic codes reduce E-229's six strokes
plus empty returns to **five strokes, 80 mm total travel**, with its existing
seven shelf levels. Direct parallel writing then needs **five banks/400 channels,
26.681 s**, versus E-229's eight/640/26.080 s. The same independent-drive bought
allocation drops $1,002→$675; it still fails the $500 ceiling. E-230's lean shared
drive allocation gives $503, without qualified force, transmission or arrest.
No machine, local mechanism, print or procurement is selected.

Input main `ea72022`. Reproduce with
`python3 tools/curated-experiment-checks/E-236/screen.py` (stdlib, stdout only;
imports E-229/E-228). Evidence: **exhaustive finite synthesis, ideal support
replay and calculations under explicitly assumed physical bounds; self-review**.
No CAD, contact simulation, sourced prices/process priors or physical measurements.
Five levels 0/10/20/30/40 mm remain a comparison workload, not a product restriction.

## Changed mechanism and code synthesis

E-220's shelves are periodic: the pickup need not return to its original datum
after every stroke. Keep its elevator below both resident support planes and
re-engage at another integer shelf phase. Column position remains the only
resident height memory; no travelling media, old-height grips, decoder bars or
extra cell locks. Shared pickup plane is `z=-20+10q` mm; row/column supports are
at 0/-10 mm. This differs from E-228's sign-separated fixed-datum operation.

Generator enumerates closed walks q in {-4,-3,-2,-1,0}, starting/ending zero,
with nonzero integer strokes. A column independently joins or bypasses each
stroke; every intermediate height must remain 0…4. Unchanged columns bypass
all strokes, including codes that would return them to their initial height.
All 25 old/target pairs must be reachable by the same walk. No arbitrary maps
are removed on grounds of rarity. The mask for a transition is selected first
by smallest required shelf depth, then least column travel, then bit order.

| Pulses | Walks tested | Reach all 25 pairs | Also fit seven existing shelf levels |
|---:|---:|---:|---:|
| 2 | 4 | 0 | 0 |
| 3 | 12 | 0 | 0 |
| 4 | 52 | 0 | 0 |
| 5 | 204 | 28 | 18 |

A selected optimum is **[-20,-10,+30,-10,+10] mm**, with pickup q coordinates
**[0,-2,-3,0,-1,0]**. Motion takes .525 s at assumed v=200 mm/s,
a=8,000 mm/s², versus 1.100 s for E-229. It uses five rather than six physical
mask/support transfers. Selection among equal-time codes minimizes worst extra
column travel: maximum **20 mm extra path / 10 mm excursion outside the
old-to-target interval**. For example 0→20 takes 0→30→20, and 10→30 takes
10→0→30. Changed miniatures may therefore reverse direction; they do not leave
the 0…40-mm envelope. Unchanged miniatures have no commanded movement.

An independent reachable-set dynamic program checks the bit enumeration.
The four-stroke arithmetic code [+30,-10,-30,+10] contains every delta as a
subset sum but fails bounded intermediate reachability; subset coverage alone
is insufficient. Within this grammar, six or more strokes cannot beat the
selected five under the stated transfer model: total positive and negative
motion must each be ≥40 mm to reach both extreme transitions. Every stroke is
≥10 mm and trapezoidal, so motion ≥.4+.025n s; adding n×.138491-s transfers
already exceeds the five-stroke 1.217456-s motion/transfer sum at n=6.
This is not a universal optimum over continuous heights, other contact topologies,
above-plane pickups, independent lifts or a different physical transfer law.

For a selected column at height h and datum q, required material shelf index
is `k=2+h-q`. The selected masks keep **0≤k≤6** at every acquisition. Thus
seven shelf levels 0…-60 mm suffice, including resident supports; naively
combining independent worst h and q would demand unnecessary longer columns.
The exact 25 mask/path records are reproducible stdout, not stored generated
output. The pickup stays between -50 and -20 mm, below resident planes.
That avoids a plane-crossing requirement but **does not construct** finite
finger bridges, long selector couplings, column-bottom clearance or guide routes.

## Supported operation and failure boundary

For each pulse, with both resident supports seated: write/read 80 retained
commands; insert/prove selected fingers on an arrested elevator; withdraw row
and selected column supports together; perform the signed stroke; seat/prove
both resident paths; retract/prove fingers. Keep the elevator at the new q.
Only then overwrite commands. Unselected cells in the active row retain column
support; all other rows retain their row supports. Digital code synthesis does
not supply these physical stages or their sensing.

The source replays **15,625 three-cell maps / 390,625 support observations**,
checks all 150 single-cell partial-path retry cases, and rejects five injected
missing-write/pickup/arrest/reseat or active-overwrite interlocks. Piecewise
linear selected motion preserves bounds between checked endpoints. This checks
ideal support flags, not force equilibrium, capture, dynamics or sensor coverage.

During writing, power loss leaves resident combs supporting terrain. During a
stroke, mechanically retained selection and lift arrest must survive source
loss; a common motor brake alone does not cover a broken bank transmission.
At a detected recoverable error, first establish actual resident support and
read actual heights, withdraw fingers, return the empty datum to zero and
regenerate masks. Replaying the original code from an unknown partial height
is invalid. Timing charges one complete extra row plus worst 30-mm empty reset
and .010 s for regeneration/read allowance. False support proof, structural
breakage, non-level jams and failed arrest require a safe stop, not a <30-s
repair claim. Safe seating after such faults remains unconstructed.

## Complete online timing and writer comparison

Retain E-229's explicit four 2-mm stages, each with .003-s proof:
`H=4[t(2)+.003]=.138491 s`; direct writing `W=t(2)+.003=.034623 s`.
No physical preparation occurs before map receipt. Charge all five overwrites,
row indexing t(5.08), two seconds of common registration/processing/final settling,
one full retry and .185 s of recovery reset/read. Unbuffered full map:

`T=2+.185+(ceil(80/B)+1)[.525+5(H+W)+t(5.08)]`.

All five pulses are budgeted for every visited row; rows containing all 25 pairs
supply a worst-useful workload. A five-row regional patch in one bank takes
**10.831 s** under these allowances; remote banks stay parked. Nonadjacent
seeks need their actual transport. Monotone six-pulse moving-datum control
[-10,-10,-20,+10,+10,+20] needs **30.10 s at B5** (rounded), hence B6;
merely deleting empty returns is not the entire improvement.

| Writer, least-allocation sampled case | Banks / channels / retained bits | Time | Bought allocation |
|---|---:|---:|---:|
| Direct, no buffer | 5 / 400 / 400 | 26.681 s | $675 |
| Reset/set scanner, double buffer | 8 / 640 / 1,280 | 27.949 s | $1,290 |
| Mechanical matrix, double buffer | 5 / 400 / 800 | 28.422 s | $855 |
| Scanner, fewest channels | 16 / 256 / 2,560 | 29.866 s | $1,938 |

Sweep: B=1…80; q divisors 1/2/4/5/8/10/16/20/40/80; direct q=80;
single/double registers. E-229 supplies physical writer reset, set, feed,
return, read and finite .35-mm headway-error scenarios. Buffer service and writer
selectors remain separate physical axes; causal two-register recurrence permits
reuse only after old service finishes. No unbuilt output copying is granted.
The five-pulse program writes 32,000 binary commands/full map, not 32,000
independent information bits. Commands depend on both old height and target.

Direct B4 needs **32.445 s**. Free writing gives 28.810 s: only **11.334 ms/pulse**
remains for *additional* physical writing, compared with the charged 34.623 ms.
At 1/2/4-mm contact throws (writer stroke unchanged), direct needs B4/5/6,
with $566/$675/$784 allocations. This is sensitivity, not permission to shrink
functional contacts. Proof latency, seating time and downward drag are unqualified.

## Whole-machine burden, manufacturing and service

For the direct B5 case, each bank has 16 rows/1,280 columns; shared head serves
one row at a time. Compared with E-229's B8 direct control:

| Function | Cell / row | Bank/head | Board |
|---|---|---|---|
| Moving column / lateral guide stations | 1/2; 80/160 | 1,280/2,560 resident | 6,400 / 12,800 |
| Periodic shelf levels / resident bearing sites | 7/2; 560/160 | 8,960/2,560 | 44,800 /12,800, unchanged |
| Row support axes/keepers | shared; 1 | 16 | 80 |
| Column bars / reusable pickup slides | shared | 80/80 | **400/400**, formerly 640/640 |
| Retained command bits / endpoints / routing contacts | no added resident hardware | 80/160/160 | **400/800/800**, formerly 640/1,280/1,280 |
| Lift/arrest/row carriage/reader systems | shared | 1 each | 5 each, formerly 8 |

No resident spring, motor, insert or socket is added; head springs, retainers,
bearings, fixtures and wired interfaces still need a real parts list. Common
printed combs retain every tooth's failure site. Added local moving precision
hardware is not licensed by the timing result. An assumed 80-mm 4×4 column
blank remains 8.192 L, 152–455 h at 15–5 mm³/s effective extrusion, before
subtraction, caps, frame, setup and scrap. Command blanks 20×4×3 mm add .096 L.
At assumed 5 s/column insertion, assembly is 8.89 h; 10 s per 480 support axes
adds 1.33 h, before 400 pickups, retainers, wiring, fixtures and calibration.
X1C's 256-mm bed still requires segmented 406.4-mm rows and controlled joints.

Inherited competing combined errors e=.15/.35/.70 mm, **not measured priors**,
leave .85/.65/.30 mm in a hypothetical 4-mm groove/2-mm tooth. Moving datum
alignment, coupling tilt, residual deflection and contamination consume that
margin. Opposing support-height errors still allow 2e=.30/.70/1.40 mm settling;
unchanged commanded height is not unchanged physical height. Common comb warp,
module bias, scanner phase and reader errors can affect whole rows/banks.
No IID yield, print resolution, nominal clearance or replay pass qualifies them.
Layer orientation, anisotropy, roughness, creep, fatigue and wear remain unknown.

A row-comb failure exposes 80 cells; a column-bar fault affects 16; a head failure
halts 1,280. Retire a faulty head with both resident paths proved; buried comb
replacement requires temporary support and access. Guides, adjacent contact
lanes and service extraction remain unconstructed; they are not zero-cost.

Independent-drive allocation: $130 common hardware +5×$65/head +400×$.50 data
channels +400×$.05 retention = **$675**. E-229 source itemizes controller,
power, frame, wiring, freight, transport, phase drive, readers, lift drives,
brakes and bearings. These are **assumptions, not market lower bounds**.

Sharing lift, phase and row-feed motion using E-230's lean $195 common plus
$20/bank, $.50/channel and $.02/retained-site categories gives **$503 at B5**.
Synchronization/branch enable and local arrest remain obligations. At the
assumed 3.27 N/cell, .5-kg head, .003-kg columns, friction allowance .2 and
8 m/s² acceleration, all five active rows demand **1.624 kN, 16.24 N·m at
10-mm radius and 464 W peak input at .7 efficiency**. A .4-m end-loaded,
12-mm-diameter shaft at assumed G=80 GPa twists by **.399 mm height-equivalent**.
These demands do not qualify the allocated $30 drive or $20 supply. The
1/10-N load scenarios scale payload terms, not head mass. Gravity-only descent
of a 3-g cell at 8 m/s² still tolerates only .00543 N guide drag; positive
capture would need its own finite geometry, force and backlash accounting.

## Decision and next discriminator

This is useful architectural progress: 37.5% fewer head selectors/pickups and
one fewer write/transfer per row without extra resident shelves or media.
It does not overcome physical writing, affordable common drive, finite pickup
routing and support proof. **Park these three writer embodiments; no smaller
tooth, detent, guide or higher-acceleration campaign.** A $3 nominal budget miss
is not the decision-driving uncertainty; the shared force/transmission is.

A changed next construction can test whether a common *mechanical command
inhibit* permits physical overwrite during a supported transfer phase, with
retained outputs until both resident supports are proved. B4 then has a useful
oracle: $441.40 lean shared allocation and 28.810 s with writing removed.
It must actually construct output disconnection, writing overlap, readback,
reconnection, power-loss state and local bank arrest inside the 11.334-ms
additional-per-pulse window; neither concurrency nor affordable torque is
assumed. Compare the added shared interfaces with the 80 channels saved.
Stop if those costs or safety needs erase the gain. The five-stroke code remains
reusable independently of that hypothesis. No currently justified print.
