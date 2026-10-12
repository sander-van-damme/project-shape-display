---
status: complete
builds-on: [E-225, E-224, E-218, E-222]
---

# Horizontal writing removes loaded writer retention, but turnover defeats the banked layout

**Park the bank-owned turnover writer before pusher/comb refinement.** A
stationary horizontal tray allows one shared stroke and binary disengaging
pushers to write independent offsets without individual loaded parking devices.
However, a 64-mm bar at five offsets sweeps a 104-mm union. Even granting free
routing, the sampled schedule needs **20 heads /1,600 selectors /26.995 s**.
A simple separated-depth bay allocation has a best sampled time of **85.001 s**.
No complete machine, fabrication or local mechanism development is selected.

Input main `4828ca4`. Reproduce with
`python3 tools/curated-experiment-checks/E-226/horizontal.py`.
Evidence: **new transaction hypothesis, ideal state replay, finite bar-envelope
calculations, and explicitly assumed force/time/cost bounds**. Self-review; no
physical measurements, process distributions, assembly CAD, reader or sourced
BOM. Five heights 0/10/20/30/40 mm remain a comparison alphabet.

## Change the direction of gravity during unloaded writing

Keep E-224's vertical support bars, common positive row comb and two E-218
bearing lanes. Old terrain remains supported on a grounded cassette. Lower the
unloaded spare into a service bay, lock it, rotate it 90 degrees about the row's
long axis and place it on a **stationary horizontal bed**. Its height offsets
are now horizontal distances; writing no longer raises individual potential
energy or supports terrain.

Open the common comb only after the bed supports all bars. A common end platen
pushes arbitrary prior offsets to zero and returns. Eighty retractable fingers
on one translating beam contact bar ends. Retract the fingers for target zero;
move the beam 10 mm and stop; retract those for target ten; repeat at 20/30/40.
Released bars remain on the stationary bed under a shared low-pressure drag pad.
The other fingers slide the remaining bars. Return the clear beam, read every
offset, and close/prove the common comb. Retract all writer intrusions before
rotating the locked cassette upright. There are **80 binary selectors/head**,
not 80 independent absolute axes and not four branching gates per stream.

The drag pad is a proposed passive friction window for **unloaded, stationary
media only**, not a qualified brake or precision location mechanism. It still
repeats 80 friction contacts per head. Stopped release avoids relying on friction
to stop a freely coasting bar. Elastic recoil, pusher release drag and bed tilt
remain real error sources. Shared normal force must reach every bar despite
thickness/bow; adding 80 sprung pads would be a changed repeated-parts ledger.

With the cassette locked upright, raise incoming support first, prove its dock,
then lower old support. The ideal E-218 law `h=max(old+a,target+b)` preserves
unchanged heights and gives monotone mixed moves. Lower outgoing farther into
the service bay; it becomes the next spare. Empty lift returns, orientation,
reset and arbitrary new-map writing are inside the cycle. A touched row hands
off all 80 cells, even for one changed cell; other rows stay docked. Opposing
cassette errors ±e still permit 2e unchanged-cell displacement.

Before transfer, loss of source or a failed writer/read invalidates the spare
while the old row stays docked. During rotation the common **positive** comb and
retained cassette fixture must carry every bar; friction is not credited. During
loaded lift travel the existing unqualified shared arrest remains necessary.
Require actual offset, comb and clear-writer proofs before rotation, then actual
height/arrest/dock proof before release. One pre-transfer row retry is budgeted.
Hung columns, structural faults and false readback require a supported stop,
without a bounded 30-s recovery claim. Neither software flags nor motor positions
construct those sensing interfaces.

## Finite turnover space is the first architecture discriminator

E-224's bar is 64×3.4×1.6 mm, top `4+h`, bottom `h−60`, with comb at −8 mm.
Relative to the comb, its longitudinal interval is `[h−52,h+12]`. At h=0…40,
the union is **[−52,+52] mm**. Rotating around the row axis therefore needs
radius `sqrt(52²+.8²)=52.006 mm` even before a carrier. Allocate 4 mm radially
for frame: R=56.006 mm, swept bay width **112.012 mm**. This does not include
writer drives, feet, reader, wiring or a complete frame.

Unchanged resident bars can reach z=−60. With a further 4-mm separation, a
service pivot initially at −8 must lower by `D>R+56=112.006 mm`; use **113 mm**.
The inherited 45-mm exchange assumption intersects this envelope. Opposite
rotation direction does not remove the radius. At the horizontal pose, adjacent
bars with left code 40 and right code 0 collide for pivot separations below
104 mm. This is an actual bar-interval counterexample, not only a bounding-box
warning. At 104 mm all 25 pair interiors separate; frames need additional space.

Twenty bank centers are only 20.32 mm apart. Twenty simultaneous turnover bays
cannot share a plane. A simple sufficient **parked-bay** allocation uses
`K=ceil(112.012 / bank_spacing)` interleaved depth levels, separated by
116.012 mm (bay plus 4-mm gap). At 20 banks it needs six levels; deepest lift
travel is **693.062 mm**, and bottom extent is about 757 mm below reference zero.
This is a scoped construction, not a universal minimum depth. It checks bay
occupancy, not cassette paths through higher bays or the resident frame.

The schedule favorably grants bank-center delivery and clearance of intervening
machinery. Lateral cassette delivery, transitions through upper decks, writer
actuator footprints, two-cassette handling and carrier openings are unconstructed
and can only add work to this policy. Sequencing overlapping bays, sharing a
remote writer, or using external side space are different transport architectures;
they cannot inherit the simultaneous schedule for free.

## End-to-end timing and manufacturing bounds

Assume linear v=200 mm/s, a=8,000 mm/s²; rest-to-rest triangular/trapezoidal
`t(d)`. Unloaded 90-degree rotation uses v=2π rad/s, a=16π rad/s²: **.375 s**
each way. Slower bounds π and 4π give .75 s. These are assumed axis capabilities,
not measured gravity-following, torque or capture limits.

Writing = `3t(40)+4t(10)+6[t(3)+.002]` = **1.219379 s**: reset/return and clear
writer return; four stopped increments; preset plus five 3-mm finger releases
with 2-ms proof each. Comb/read/dock/registration receive .5 s auxiliary/row.
Loaded exchange conservatively stops at the 40-mm load-free crossover:
`2[t(40)+t(D−40)]+2t(D)` = **2.410 s at D=113**. Add two 2.4-mm lane moves,
one 5.08-mm row hop (.119682 s total), and two rotations (.750 s). Row total is
**4.999061 s**. No offline preparation or free cycle overlap.

Full map = `2+(80/B+1)·row_time`: two global seconds and one worst-row retry;
sampled B divides 80. Independent banks run in parallel. A patch concentrated
in one bank receives no help from the others. Initial bay delivery/referencing
must fit the global allowance; this has not been constructed.

| Layout / sensitivity | B | Binary selectors | Calculated full-map s |
|---|---:|---:|---:|
| Grant all routing, one depth | 10 | 800 | 46.992 |
| Same | 16 | 1,280 | 31.994 |
| Same | 20 | 1,600 | 26.995 |
| Same, .75 s per rotation | 20 | 1,600 | 30.745 |
| Same, .75 s per rotation | 40 | 3,200 | 19.247 |
| Same, 1-s auxiliary | 20 | 1,600 | 29.495 |
| Same, loaded 1-mm indexed arrest plus 1-ms proof/step | 20 | 1,600 | 34.090 |
| Separated-depth bays, still granting delivery | 16 | 1,280 | 87.680 |
| Same: best in B=1/2/4/5/8/10/16/20/40/80 | 20 | 1,600 | 85.001 |
| Same | 40 | 3,200 | 93.565 |

A tempting 45-mm/no-turnover control would hide the new transport obligation.
Horizontal writing removes E-225's finite rail-switch headway, but **does not
beat its favorable 1,024-gate/28.608-s comparison** as a complete banked machine.
E-222's loaded in-place sweep cannot drop parked shoe retention: gravity/load
would move a released shoe. The horizontal escape works only on unloaded media.

Friction scenarios: bar mass 1 g, tilt 2°, disturbance .005/.05/.1 N, μ=.1… .4,
and pad normal load N0 with ±50% spatial spread. All are **competing assumed
bounds**, not PLA priors. Require `.1·.5N0 > .001g sin(2°)+disturbance`.
At .005 N disturbance, N0=.1 N fails by .000342 N; .3 N leaves .009658 N.
At .05 N disturbance even N0=1 N narrowly fails. Worst sliding force plus bar
inertia at 8 m/s² is `.4·1.5N0+.008`: at N0=.3/1 N the row requires
**15.04/48.64 N**, before guide binding and pusher friction. Pad relaxation,
shared tilt and print thickness bias can affect a whole row; no probability or
yield is inferred. A released bar's error must be read, not assumed zero.

Inherited 4-mm notch/2-mm comb gives 1-mm centered margin. With independently
bounded ±e writer-position and notch errors, residual = 1−2e:
.70/.30/−.40 mm at e=.15/.35/.70. These are necessary engagement windows,
not acceptable final height errors or load-qualified contacts. Shared beam bend,
reader zero and comb warp add correlated errors. Also, a 4-mm notch around a
2-mm tooth permits **2 mm axial play**: centered engagement is not a final height
datum. Rotation may seat a bar on a different face, or leave it hung by friction.
Read actual heights after upright seating before transfer; the ideal replay
assumes correctly seated profiles. No compensating datum or seating method is
constructed here. The inherited .8-mm dual-lane
gap falls to .1 mm under opposing ±.35-mm errors; turnover does not fix it.
Do not turn this conditional layout into another narrow-clearance optimization.

## Replication, economics and service

Ledger at the optimistic B=20 comparison (four resident rows and one spare/bank):

| Functional item | Per cell / resident row | Bank or shared head | Board |
|---|---|---:|---:|
| Display columns / guide stations | 1,2 /80,160 | 320,640 | 6,400,12,800 |
| Media bars / active comb contacts | 1,1 /80,80 | 400 each including spare | 8,000 each |
| Bar guide stations / notch positions | 2,5 /160,400 | 800,2,000 | 16,000,40,000 |
| Common comb+keeper sets | shared /1 | 5 | 100 |
| Alternative row docks | shared /2 | 8 | 160 |
| Binary pushers / slide guides / drag-pad sites | head-owned | 80 each | 1,600 each |
| Loaded lift/arrest sets | head-owned | 2 | 40 sets; ≥80 dog functions if indexed |
| Reset, sweep, rotary fixture, lane transfer, carriage, readers | shared | ≥1 each | ≥20 each |

No individual resident spring, detent, insert or motor is proposed. Head return
springs/retainers, rotary bearings, rails, fixtures, fasteners and wire routes
are unknown, not zero. Rotation adds clamping/registration and at least two
trunnion bearing stations/head; 406-mm beams need joined printed modules.
A selector fault affects a lane in its bank, a common keeper fault exposes 80
cells, and deck obstruction can block several banks. Buried media still require
positive support before removal. A shared writer is not automatically accessible.

Solid bars total **2.785 L**, plus the 4.608-L column-stock comparator, excluding
notches removed, frames, beds and writers. At assumed 5–15 mm³/s effective flow
and 10% scrap, bars alone need **57.3–171.9 h**. Eight thousand placements at
10/30 s take **22.2/66.7 h**; add 6,400 column insertions, 1,600 selector setups,
100 comb settings, 160 dock alignments and 20 rotary fixtures. These are stock
and assembly scenarios, not slicing or measured labor. Print orientation,
slender-bar buckling, comb creep, pad wear and connected-frame stiffness remain
unqualified; the .375-s rotation owes inertia, counterbalance and clamp torque.
Loaded row forces remain 80/261.6/800 N for assumed 1/3.27/10 N per cell.

Even a **$250 assumed nongate reserve** leaves <$0.15625 per complete selector
under $500, <$0.09375 under $400 at 1,600 channels. At 3,200 it halves. Twenty
heads' drives, forty lift/arrest sets, rotary fixtures, readers, frame and supply
have no demonstrated fit within that reserve. These are budget ceilings, not
quotations or universal cost floors; no procurement route is selected.

## Decision and verification

Keep the causal principle: changing the orientation of **unloaded** memory can
remove loaded writer retention; a common comb must capture it before transport.
Park the specified one-writer-per-bank turnover architecture. Do not design a
smaller finger, stiffer pad or thinner comb for it. A changed allocation that
shares writers among exchange banks would need explicit buffers, delivery,
rotation occupancy and source-loss support before receiving mechanism work.
As a cheap future discriminator, aggregate writing alone needs ≥4 80-channel
writers for 81 services in 28 s; writing plus .75-s turnover needs ≥6, before
transport/proof and pipeline startup/drain. This lower bound is not a scheduler
or a preferred architecture. It prevents resurrecting a single free writer.

Checks: 15,625 three-bar old/target cases with ideal two-cassette handoffs;
eight interlock combinations; 90-degree finite corner sweep versus analytical
radius; exact 25-pair horizontal bar intervals; all sampled bay allocations;
independent motion limiting cases and timing monotonicity. No dynamics, gravity
following, pad stick-slip, finite carrier assembly, physical power-loss test or
independent reviewer is claimed. The decision is about complete-machine burden,
not a proof that every horizontal writer or cassette is impossible.
