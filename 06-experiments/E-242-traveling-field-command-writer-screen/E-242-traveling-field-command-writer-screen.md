---
status: complete
builds-on: [E-241, E-138, E-236, E-239]
---

# Traveling command writers save windings but require more retained hardware

**Park the tested traveling polarized-mask writers before field or rotor detail.**
Reusing signed coils reduces bought electronics and winding labor, but physical
scan time adds banks. At inherited carriage bounds the least allocation is
**$562.22, six banks, 480 flags and 240 writers**. Aggressive flying scans reach
**$509.96, five banks, 400 flags and 100 writers**, with field width and independent
retention granted. The $9.96 miss is not a market lower bound: removing $25 from
assumed costs changes the economic screen. More decisively, coil reuse does not
resolve the inherited flag's switching/reader-retention conflict in the tested
5-V electrical envelope. No complete machine, field-isolation pass or print.

Input main `dc1e1f6`. Reproduce:
`python3 tools/curated-experiment-checks/E-242/screen.py` (stdlib, stdout only;
imports E-241/E-239). **Evidence: calculations, ideal addressing replay and
labelled competing bounds; self-review.** No CAD, new field solution, process
probability or physical measurement. Five terrain levels remain a comparison
workload, not a product restriction.

## Changed physical topology and transaction

Keep E-236's moving-datum support transaction and E-241's passive polarized
command flags. Arrange each head's 80 flags in q tracks, 80/q positions per
track. A common carriage carries q signed coil writers and moves along all
tracks. Each coil writes successive flags; stationary flags preserve previous
bits without powered hold. The next scan reverses direction and command order,
so **no empty carriage return is required**. This is hardware reuse, unlike
E-241's direct bridge on every flag. It does not reduce 32,000 command-site writes
per full map, the five command masks per row or the number of terrain supports.

Compare stopped site writing, flying position-gated writing and direct stationary
electrical control. No moving permanent writer is credited: signed electromagnets
can turn off between sites; a continuously exposed permanent head owes a separate
flux shutter/turnover transaction. E-138's direct loaded magnetic rack drive is
not reopened. Here magnets act only on shared command flags and may be spaced
outside the column pitch; its quantitative 5.08-mm resident-neighbor counterexample
therefore cannot be transplanted as this writer's failure threshold.

At each supported datum, retract the reader/pickups; both resident paths remain
seated. Scan and write either polarity, extinguish current, read the entire
physical pattern, insert/prove selected pickups, withdraw row and selected column
supports, move the shared lift, reseat/prove supports, then withdraw/prove pickups.
Only then scan again. No free buffer, output copier or overwrite during loaded
use is granted. Other rows stay row-supported; unchanged cells in an active row
keep column support. Finite routing, grounded reader reaction, support following,
local arrest and false-proof coverage remain unconstructed.

On interrupted writing, remain resident-supported and rewrite/prove the full
mask. A recoverable mismatch after motion requires actual stable-height readback,
resident reseating, empty-datum reset and regenerated commands, then a full row
retry. Carriage direction/position must also be known before restarting. The
charged common allowance grants this registration; an unknown-position fault
that cannot meet it requires supported shutdown. Stuck flags, invalid support
proof, transmission loss or failed arrest have no guaranteed bounded recovery.
Passive command retention is not power-loss protection for a loaded elevator.

## Full arbitrary-map time and allocation

Let n=80/q, p=along-track site pitch, P=write pulse, w=granted useful field window,
and t(d;v,a) be rest-to-rest triangular/trapezoidal travel. Charge:

- Stopped write: `n(P+.001)+(n−1)t(p)+.003+160B/1e6` seconds.
- Flying write: `t((n−1)p+w; min(v,w/(P+.001)),a)+.004+160B/1e6`.

The 1-ms decay fits inside a flying window; an additional final extinction
allowance is conservative. Endpoint acceleration provides additional dwell.
Widths do **not** establish constant torque, a switching trajectory or immunity.
The last terms allocate physical proof and all signed data at assumed 1 Mbit/s.

E-239 supplies four 2-mm support stages and proofs per pulse, five signed lift
strokes totaling .525 s, row feed, two seconds for preparation/registration/final
verification and settling, one full causal row retry and 30-mm empty reset.
Thus `T=2+.185+(ceil(80/B)+1)[.525+5(.138491+W)+t(5.08)]`.
No arbitrary new-map preparation occurs outside this boundary. Scan acceleration
changes independently of the inherited lift acceleration; gravity following is
not improved by a faster writer.

Enumerate 1,728 schedules: q divisors of 80 from 1 through 40; p=10.16/20.32/40.64
mm; P=5/10/20/40 ms; flying w=2/4/8 mm; (v,a)=(.2,8),(.5,20),(1,40),(2,80) in
SI units. Choose the first feasible B=4…80; costs grow with banking in this model.
There are 3,897 timed winding cases at 100/200/400 turns. None allocates <$500.

| Least allocation at each carriage bound | B / q / total writers | Full map | Allocation |
|---|---:|---:|---:|
| Stopped, .2 m/s / 8 m/s² | 6 / 40 / 240 | 28.085 s | $562.22 |
| Flying, .2 / 8 | 6 / 40 / 240 | 28.010 s | $562.22 |
| Flying, .5 / 20 | 5 / 40 / 200 | 28.664 s | $518.38 |
| Flying, 1 / 40 | 5 / 20 / 100 | 29.542 s | $509.96 |
| Flying, 2 / 80 | 5 / 20 / 100 | 28.016 s | $509.96 |
| E-241 direct, P5 ms | 4 / 80 / 320 | 29.822 s | $481.75 |

All table minima use 100 turns, 5-ms pulses and p=10.16 mm. The last two flying
cases grant an 8-mm usable window; actual cruise is capped at 1.333 m/s for the
2-m/s case. At the same minimum price there are slower/fewer-writer cases;
price ties select shortest time, not a proven optimum over all physical writers.
A five-row contiguous patch in one bank takes 11.302 s under the fastest listed
case; arbitrary nonadjacent seeks need their actual travel.

The $509.96 ledger is $295 inherited common/bank reserve, $25.26 bridges
(minimum 150-piece price tier), $52.80 magnets, $4.53 shift registers, $22.37 wire,
plus assumed PCB $25, pulse-power increment $20, targets/pivots $20, harness $10,
passives $5, winding fixture $5 and scan guides/mounts $25. It keeps the reserve's
$20 common writer drive; five synchronized slides are granted, not five free
independent positioning machines. Wiring flex life, shielding, regulated current,
position proof and actual drive ratings have no qualified BOM.

Prices reuse E-241/E-240's dated observations, including pack quantities; they
are not a new market survey. [TI's DRV8837 datasheet](https://www.ti.com/lit/ds/symlink/drv8837.pdf),
rechecked 2026-10-12, specifies a signed bridge, 1.8-A maximum drive current and
up to 11-V motor supply. **5 V is this screen's chosen rail, not a chip limit.**
Higher voltage, different winding or flux circuit is a changed physical envelope
owing power, current regulation, heat, field isolation and a new ledger.

Removing $25/$50/$100 from assumed allocation gives minima $484.96/$459.96/$409.96
and 53/148/416 timed cases below $500. Therefore the small budget deficit alone
is insufficient for a universal rejection. Relative to E-241 B5/100 turns, the
fast scan saves only $41.02 despite removing 300 windings/bridges: all 400 flags
remain and carriage mounts consume part of the gain.

## Stop before field refinement: inherited motion and retention still matter

Before designing a fringe-field pole, grant the E-241 bore field, its same
.2-g rotor and ±45° swing. This is a favorable **comparator**, not a guaranteed
upper bound on every possible traveling magnetic head. Keep explicitly assumed
.35-mm geometry error, .5 field factor, .85 current and magnetic-moment factors,
6-µN m friction, 2-µJ disturbance, ±30% barrier variation and .010-N reader at
3-mm lever. These are correlated/model bounds, not X1C distributions.

All tested 100/200/400-turn, .2/.4/.8/1.2-A, 5/10/20/40-ms cases satisfying the
chosen 5-V coil+typical bridge drop have empty conservative retention/motion
intervals. An independent midpoint work check also fails the prescribed
triangular trajectory. Retention requires nominal E≥36.517 µJ; the +30% barrier
specimen needs ≥47.472 µJ just to cross the saddle. Even the most favorable
sampled 40-ms electrical case supplies 40.671 µJ to the midpoint against
**54.652 µJ** barrier+friction+kinetic demand in the adverse scenario. Reader is
withdrawn during writing; its force is not double-counted as writing friction.
This is a scoped work inconsistency, not a universal dynamic switching bound.

Model sensitivity is material: N200/.8 A/P20 gives E_high=8.502 µJ at field
factor .5. A zero-reaction reader needs E_low=2.857 µJ and passes that inequality;
a .005-N reader needs 19.687 µJ and fails, but passes at field factor 1 where
E_high=24.145 µJ. Optical readback cannot simply substitute for the mechanical
command-to-pickup interface: a grounded amplification/transfer mechanism must
still be constructed and counted. Do not start a tiny-detent optimization.

For q20, 20 tracks at 20.32-mm transverse spacing and four sites at 10.16-mm
along-track spacing have center spans 386.08×30.48 mm. This is a possible external
layout allocation, not routed CAD. Widely spaced writers avoid borrowing the
5.08-mm column pitch, but adjacent resident magnets along each track remain
10.16 mm apart. An 8-mm writing window leaves only 2.16 mm between windows,
or 1.46 mm with opposing ±.35-mm position bounds. This is an addressing interval,
**not a proven magnetic cutoff or manufactured clearance**. Shared phase bias,
frame warp, rotor orientation and supply droop can affect entire tracks/banks.

Actual moving-head fringe field, cross-talk, coast decay, endpoint attraction,
repeat-pulse behavior and reader reaction remain unknown. E-138/E-241 show why
independent electrical channels do not establish magnetic isolation. Their field
values are not an immunity pass here. The cost/motion screen supplies no reason
to spend on a finer field mesh, shield or local magnet-gap design this cycle.

At B5/q20/100 turns/1.2 A, the granted pulse model draws 120 A summed coil current
and approximately 370 W peak copper. Sharing increases each coil's pulse duty;
full-map switching joules do not fall merely because there are fewer windings.
The power allocation is not a qualified supply or current-rise/decay circuit.

## Replication, manufacturing and service

For the five-bank case, each bank serves 16 rows. Counts are functional sites,
including monolithic printed arrays:

| Function | Per cell / row / bank-head / board |
|---|---|
| Terrain support | 1 column, 2 guides, 7 shelf levels, 2 resident bearing sites/cell; 80 columns and 1 row support/row; 1,280 columns/bank; 6,400 columns, 12,800 guides, 44,800 shelves, 12,800 bearing sites and 80 row supports/board |
| Shared output | 80 column bars, 80 pickup slides, 160 routing contacts/head; 400 bars, 400 pickups and 800 routing contacts/board |
| Retained commands | 80 flags, magnets and pivots, 160 targets and 80 reader sites/head; 400 flags/magnets/pivots, 800 endpoint and 400 reader sites/board |
| Traveling writer | 20 windings/bobbins/bridges and 1 carriage/head; 100 each plus 5 carriages, 200 coil terminations, 25 installed shift ICs and ≥1,300 IC pad joints/board, before passives |
| Shared scan | 1 allocated common drive/transmission, 5 slide/registration systems and moving harnesses; actual bearings, fixtures, catches and transmission joints unconstructed |

No cell spring, tiny lock or new local insert is introduced. It also removes
none of the inherited terrain shelf/support burden. At assumed .3–.6 cm³/bobbin,
100 bobbins use .03–.06 L rather than .12–.24 L for direct B5. Inherited column
blanks remain 8.192 L and 152–455 h at the earlier assumed extrusion rates, before
frame, scrap and setup. Flat replaceable writer modules are plausible; finite
coil access, housings, winding fill, target insertion, reader linkage and print
orientations have not been constructed. At assumed 2–10 minutes/winding,
300 fewer coils save 10–50 assembly hours; 400 flag installs, magnet polarity
checks and pivot/target calibration remain. This is labor sensitivity, not a
measured production route.

A writer fault now affects four flags/scan; a scan-axis fault affects an entire
head. A retained wrong flag can persist through later programming unless proved.
Replace the accessible writer only with both resident paths seated; support
removal still needs temporary support. Repeated guide friction, wear, creep,
comb warp and power-loss arrest retain their earlier qualification limits.

## Decision and next discriminator

Keep the alternating-scan reuse result and the full write-time accounting.
Stop these stopped/flying magnetic embodiments; no fabrication or local magnetic
refinement. They reduce winding work but do not remove the controlling burden:
**five complete physical rewrites and twenty support-transfer stages per row**,
on top of 44,800 resident shelf levels. Further local command optimization is
not justified by a near-budget hypothetical machine.

Next change the **transaction/support encoding**, not the coil gap. Generate
complete constructions that retain one row's program through an entire height
trajectory or encode target height directly in shared support geometry; compare
against this five-rewrite control. First reconstruct E-232/E-234/E-238 so paired
bars, decoded program media and absolute stops are not relabeled as new escapes.
The first executable output must count physical program sites, support transfers,
write/read traffic and a causal retry for arbitrary rows; reject constructions
that restore thousands of fragile memory sites or hide output-copy machinery.
Only a changed topology that removes one of those burdens earns local modeling.

Checks: 1,536 forward/reverse ideal four-bit overwrites, 14,336 retained/unwritten
bit observations, 24 independently expanded full schedules, dwell/extinction and
single-site limiting cases, plus the midpoint energy check. These verify model
consistency and scoped negative evidence, not hardware performance.
