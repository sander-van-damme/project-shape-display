---
status: complete
builds-on: [E-218, E-223, E-217, E-222]
---

# Compact vertical support bars do not rescue the tested branching-rail writer

**Park this writer before gate or keeper refinement.** A vertical support bar
escapes E-218's long staircase sweep and E-223's loaded-relief transport conflict.
However, a finite follower occupies a selector longer than a point model assumes.
With the specified 2-mm follower and ±.35-mm error box, the sampled multi-follower
writers miss 30 s. The smallest timing survivor gives **each bar its own four
gates: 2,560 gates / eight heads / 29.403 s**, even granting unbuilt routing and
continuous arrest. Compact media is a useful hypothesis, not a selected machine.

Input main `43e051d`. Reproduce:
`python3 tools/curated-experiment-checks/E-224/rails.py`.
Evidence: **mechanism construction, ideal support replay, necessary geometric
inequalities and schedule/stock calculations under labelled bounds**. Self-review;
no assembly CAD, measured process envelope, actuator quotation or physical pass.
Five heights 0/10/20/30/40 mm are a comparison alphabet, not product resolution.

## Changed support and complete transaction

Replace the translating staircase with one **64×3.4×1.6-mm vertical bar** per
bearing lane. Its top is `4+h`, bottom `h−60` mm. Five broad side notches at
12/22/32/42/52 mm below the top let a common translating row comb support every
bar at z=−8. Two guide stations at z=−16 and 0 remain covered in all five codes.
A positive common keeper retains the comb; vertical load goes bar → comb →
carrier → grounded dock. No individual spring, detent or rotary bearing is
proposed. There are still 6,400 resident moving bars and keeper engagements.

All codes occupy the same 3.4-mm width at 5.08-mm pitch. Stock's vertical union
is **−60…44 mm**, 104 mm before frames and exchange motion. This removes the
72-mm horizontal sweep of E-218; it does **not** establish full cassette packing.
The second 1.6-mm bearing lane and .8-mm separating gap inherit E-218's hypothesis.
Long bar tails, guide frames, comb teeth and writer extraction must all clear the
other cassette. No complete carrier or below-board transport route is constructed.

One spare cassette per bank is written **unloaded**:

1. Old cassette remains docked under terrain. Place spare on reset/transport rails,
   release its common keeper, push all bars to zero with a common 40-mm reset
   platen, then return the platen. Individual old spare codes need not be copied.
2. Feed the spare through four stations. At station k a retractable rising tongue
   selects climb toward height 10k or bypass at the previous height. Bars already
   below that station pass beneath it. A short selective rise clears the fixed
   rail; a following fixed ramp supplies the remaining rise. Rails at five levels
   support completed settings through the rest of the scan. All commands come
   from the newly received map; no prewritten spare or media inventory credit.
3. Keep **all** bars on rails until the common comb closes into their aligned
   notches. Prove keeper and actual heights. Withdraw the locked cassette from
   the writer, return empty feed machinery, then transport below the target row.
   Lifting away from the rail bank, its five bypass clearances, split-stream
   fanout and cassette-frame routing remain unconstructed.
4. Use E-218's two bearing lanes: raise incoming support, dock it, then lower old
   support and recover it as the next spare. Ideal `max(old+a,target+b)` preserves
   unequal unchanged neighbors; replay includes (40→0, 0→40, 20→20). The loaded
   terrain never rides through the writer. Two loaded strokes and two empty
   resets are charged; 45-mm strokes are an **optimistic borrowed allowance**,
   not demonstrated clearance for these longer bars.
5. Pre-transfer read, keeper or extraction failure leaves the old support docked;
   reset/rewrite the spare. During transfer use E-218's proposed arrested lifts
   and proved docks. Power loss while writing can invalidate only unloaded media;
   source loss during a loaded stroke still requires the unqualified common
   brake/arrest. Keep both supports after a fault; reread before resuming.

One complete row retry is budgeted. Hung followers, broken support, false readback
and structural faults require a supported service stop, without a <30-s recovery
claim. Every touched row hands off all 80 cells; untouched rows remain docked.
Unchanged-cell height is invariant only in the ideal contact model. Opposing
cassette height errors ±e allow 2e settling; no regional-disturbance pass follows.

## Finite selector occupancy is the new discriminator

This specified rising tongue retracts vertically to let a low follower pass under
a fixed upper rail. Assume follower vertical thickness and rail thickness each
1.6 mm. With each face position bounded by ±e, a **necessary** rise is
`d=3.2+2e`. This is a touching-envelope lower bound; positive running clearance
would increase the stroke. It is deliberately favorable, not a print tolerance.

Let selective ramp run be w, follower's axial contact footprint f, and pitch p.
A gate must hold its state from leading-edge arrival until trailing-edge departure:
occupancy is **w+f**, not w. Opposing adjacent placement errors reduce headway by
2e. The free switching distance is `g=p−w−f−2e`. Alternate codes 0/10 demand ON
then OFF at the first gate; codes 30/40 give the same witness at the last gate.
If g≤0, the intervals overlap and no switching speed can satisfy those commands.
This applies to the specified rigid tongue that must remain fixed throughout
contact; moving-under-contact tongues or lateral bypasses need new constructions.

For w=f=2 mm, p=5.08 mm, gate acceleration 8,000 mm/s², speed cap 200 mm/s and
1-ms endpoint proof, use `v=.8 min(200, v_cam, g/[move(d)+.001])`. The factor .8 is
an assumed operating allowance. Cycloidal segments satisfy peak slope `2d/w`
and follower acceleration `2πd(v/w)²`. Competing slope limits 4/8 and acceleration
100 m/s² are deliberately favorable screening bounds, not wear/impact allowables.

| Per-face error e (mm) | Free distance g (mm) | Allowed scan speed (mm/s), slope-8 case |
|---:|---:|---:|
| 0 | 1.08 | 21.073 |
| .15 | .78 | 14.568 |
| .35 | .38 | 6.732 |
| .70 | −.32 | Conflicting occupancy; no adjacent-stream solution |

At e=.35, a point-follower relaxation gives **42.162 mm/s**, over six times the
finite result. Making the subsequent fixed ramp longer does not shorten tongue
occupancy. Uniform x bias cancels from adjacent headway; with zero differential
x error but the same adverse vertical box, speed rises to **19.132 mm/s**. Thus
correlation matters: these are competing boxes, not independent Gaussian draws.
Shared rail/datum errors can instead affect an entire cassette. No yield is inferred.

## Whole-machine schedule and economic screen

Each of B contiguous banks has one exchange head and s granted parallel writing
streams; n=80/s bars/stream, **4Bs independent gates**. The grant assumes spatial
routing even when the tracks would overlap in one plane. Each stream traverses
four selective and four fixed ramp segments, `(n−1)p`, and follower/end margins.
All bars remain rail-supported until the common keeper closes. The scan and its
empty return are charged, plus 40-mm reset and return, gate preset, four 45-mm
lift/reset moves, two 2.4-mm lane transfers, one row hop, .5 s/row auxiliary
proof/dock allowance, 2 s global work and one worst-row replay. No offline writing
or free transport overlap. Full cassette delivery/fanout remains omitted, so these
are **optimistic schedules of the stated serial policy, not passes or universal
minimum gate counts**.

Grid: B=1/2/4/8/16, s=1/2/4/8/16/40/80, w=2/3/4 mm; both slope limits; error
boxes above. Fixed ramps use `2(10−d)/slope` length. All axes use the fast bounds
above. A constructed timing fallback stops each loaded 1-mm arrest step and adds
1-ms proof; continuous arrest is a relaxation.

| Case | B×s | Gates | Calculated s |
|---|---:|---:|---:|
| Zero error, **point** follower, slope 8, continuous | 16×4 | 256 | 29.313 |
| Zero error, 2-mm follower, slope 8, continuous | 16×16 | 1,024 | 26.512 |
| ±.15 mm, 2-mm follower, slope 8, continuous | 16×40 | 2,560 | 24.504 |
| ±.35 mm, 2-mm follower, slope 8, continuous; two bars/stream | 16×40 | 2,560 | **35.002** |
| ±.35 mm, 2-mm follower, slope 4, continuous; **one bar/stream** | 8×80 | 2,560 | 29.403 |
| Same, indexed arrest | 16×80 | 5,120 | 26.562 |
| ±.35 mm vertical but common x bias, slope 8, continuous | 16×16 | 1,024 | 27.367 |

One-bar streams escape adjacent switching by duplicating the four gates for every
bar in the head; their negative/short gap is irrelevant because no following bar
arrives in that scan. Their routing is not constructed. This duplicates selection hardware across the head. Even **scan rate alone** for multi-bar streams at e=.35
requires ≥173 streams /692 gates under a 28-s scan allocation; constant-speed
scan length per row exceeds 80p in the sampled geometry. Reset, support motion
and routing consume more time. This bound excludes one-bar streams and does not
cover a different feed policy or larger programmer pitch.

Eight-head one-bar case: .25/.5/1/2-s row overhead gives
26.653/29.403/34.903/45.903 s. Merely increasing the assumed exchange stroke from
45 to 65 mm gives **33.803 s**. A five-row patch in a single bank takes 16.947 s
with one replay under the .5-s/slope-4 assumptions; all ten rows of that bank
consume the full critical-path time. Parallel banks do not accelerate one bank.

An assumed $250 allowance for *all nongate hardware* leaves **<$.0977 per complete
gate** at 2,560 gates under $500, or <$.0586 under $400. At 5,120 gates the $500
allowance is <$.0489. These are budget ceilings, not component quotes or a proof
against every custom selector. Drive, retention/return, guide, wiring, sensor and
mount must fit. The nongate allowance still owes every lift, arrest, carriage,
dock, reset/feed drive, reader, supply, frame and fastener. No credible BOM exists.

## Replication, manufacturing and service

Counts at the favorable eight-head case; bank has ten rows plus one spare.

| Functional item | Cell / resident row | Bank including spare / head | Board |
|---|---|---|---:|
| Display columns / guide stations | 1 / 80 columns,160 stations | 800 /1,600 | 6,400 /12,800 |
| Independent support bars / active comb engagements | 1 /80 each | 880 each | 7,040 each |
| Bar guide stations / notch positions | 2 /160; 5 /400 | 1,760 /4,400 | 14,080 /35,200 |
| Cassettes and common comb/keeper sets | shared /1 | 11 | 88 |
| Alternative ground docks | shared /2 | 20 | 160 |
| Loaded lift/arrest sets; two dog functions/set | shared | 2 sets /≥4 dogs | 16 /≥32 |
| Writer gates / five-level rail lanes | shared | 320 /400 | 2,560 /3,200 |
| Common reset, feed/return, lane transfer, carriage, readers | shared | ≥one function each; packaging unresolved | ≥8 each |

At least one sliding/contact surface exists per bar guide station; rail followers,
comb engagements and gate junctions add wear. No separate media spring is required
in the hypothesis, but keeper/dock/arrest/gate springs, inserts, bearings, fixtures
and fasteners are **unknown**, not zero. Common combs do not erase 7,040 active
load-bearing contacts. A dock failure exposes 80 cells; a head fault its 800-cell
bank. Jam repair must support the affected row before removing buried media.
The 406.4-mm row needs joined modules on the 256-mm print bed.

Solid bar blank allocation is **2.451 L** at B=8, **2.674 L** at B=16, versus
E-218's 11.796-L staircase allocation at B=16. Notch removal, heads and frames
are excluded; display column stock adds the earlier 4.608-L control. At assumed
5–15 mm³/s extrusion and 10% scrap, eight-head bars alone need **50.4–151.3 h**.
7,040 bar placements at 10/30 seconds add **19.6/58.7 h**, plus 6,400 columns,
88 keeper setups, 160 docks and thousands of gates/rail registrations. These
are stock/time scenarios, not sliced parts or an assembly qualification.

Error sensitivity is function-specific: bar-to-bar nominal x gap 1.68 mm leaves
1.38/.98/.28 mm under ±.15/.35/.70 mm opposing errors; the .8-mm lane gap leaves
.50/.10/−.60 mm. A proposed 4-mm notch around a 2-mm comb tooth has centered
1-mm margin, reduced to .70/.30/−.40 mm if both positions vary independently
within those boxes. These are necessary clearances, not evidence that the slot,
comb or guide works under load. Correlated warp, shrinkage, debris, roughness,
layer anisotropy, creep and guide friction remain unmeasured. No tolerance prior
or board reliability claim follows.

For assumed F=1/3.27/10 N per cell, load is 80/261.6/800 N per row; ideal 10-mm
radius lift torque .8/2.616/8 N m before friction/inertia. Gravity following and
loaded arrest remain E-218's unresolved gates. For assumed unloaded bar resistance
R=.05/.3/1 N, an 80-stream, slope-8 one-bar writer can demand a quasistatic
**32/192/640 N** drive envelope (one occupied segment/stream); inertia and gate
switch force add to it. Shared motion has neither free force nor free stiffness.

## Decision and useful reopening condition

Keep the compact bar/common-comb encoding and finite gate-occupancy inequality as
reusable knowledge. Do not refine this writer, add local latches or request prints.
Its more favorable point model conceals a manufacturing-relevant throughput cost;
longer passive ramps and shared drive motors do not remove it.

A meaningful next change is **different media handling**, e.g. spreading unloaded
followers only while writing, then restoring 5.08-mm registration before the
positive exchange. First construct that full spread/write/repack/return path and
count its movable carriers, joints, supports and time. A per-cell pantograph,
independent conveyor or another set of retained loops does not get a free pass.
Alternatively bypass serial branching entirely with a genuinely different shared
programming transaction. This is an invention direction, not an adopted mechanism.

Checks: 15,625 old/target three-cell rewrites and exact E-218 support-event replays;
four missing-proof stops; common-notch/guide coverage; explicit adjacent-command
overlap; point-versus-finite monotonicity; cycloid acceleration convergence at
64/256/1,024 samples (relative errors 8.03e−4/5.02e−5/3.14e−6); independent stock
units and coherent-versus-relative error scenarios. These verify the model and
bounds, not hardware, sensing, finite bypass geometry or independent validation.
