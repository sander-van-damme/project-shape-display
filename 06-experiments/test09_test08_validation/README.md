# Test09 — falsifiable validation of Test08

**Decision: Test08 is better defined and weaker as a near-term build candidate;
it is not fundamentally disproved. Do not build an 80-channel head yet.** Its
conditional timing is reproduced, but the legacy notch cannot establish a full
missed-step correction, full-scale structure is unresolved, and realistic
purchased allowances exceed $500. No physical measurement has been made.

The smallest decision sequence is **process fits → six passive cells → one
driven retained rotor → eight simultaneous channels → representative lift**.
A failure stops the dependent stages. Begin by printing PLA clearance/web
coupons on the actual X1C; do not buy eighty motors or print 6400 parts.

## Reproduce from repository root

Python 3.11+, standard library only; no package installation for this workflow:

```text
python 06-experiments/test09_test08_validation/run.py
python 06-experiments/test09_test08_validation/run.py --render
```

The second command also needs **OpenSCAD 2021.01** on PATH (`openscad.com` on
Windows). It exports STLs and renders, checks bounding boxes against 256 mm,
rejects compiler warnings/errors and runs the scoped historical contact checks.
It may take several minutes. `--cad` omits PNG rendering. OpenSCAD success is
not slicer, fabrication, whole-assembly collision or physical validation.

Individual commands are `analyze.py`, `checks.py`, `qualify.py`, and
`cad_check.py --render` in this folder. `run.py` repeats analysis and verifies
byte-identical analytical output. The workflow relies on the preserved Test08
`params.json`, `analysis.py` (mass/cross-check only) and `coupon.scad` within this
repository; no historical generated results are needed. `cad_check.py` creates
a local generated snapshot so it never changes historical source or results.
During coupon-only iteration, `cad_check.py --render --coupons-only` reruns the
new exports into `cad_coupons.json` without repeating unchanged historical
contact checks. Run the complete command for a fresh checkout.

## Evidence and next actions

| Artifact | Purpose |
|---|---|
| [uncertainties.csv](uncertainties.csv) | 31 hypotheses, current assumptions/evidence, test methods, pass/fail thresholds and architecture consequences |
| Engineering analysis below | Historical source audit, geometry, return, detent, structural, timing and reliability interpretation |
| [params.json](params.json), [analyze.py](analyze.py) | Reproducible analytical model and joint sensitivity sweep |
| [coupons.scad](coupons.scad), [cad_check.py](cad_check.py) | Fit/wall/hole/slot, replaceable detent, one-motor bench parts and spliced beam specimens; historical passive geometry exports |
| Physical plan below | Ordered A–E fabrication, instruments, counts, acceptance/stop gates and exact bench assembly |
| [measurements/](measurements/) and [qualify.py](qualify.py) | Blank physical records and conservative measured-input timing replay; currently `NOT_MEASURED` |
| [bom.csv](bom.csv), [sources.md](#sourcing-ledger) | Current price evidence, speculative targets, allowances, missing delivered quotes and contingency |
| Multi-row analysis below; `multirow_bom.csv` | Separate 1–5-row independent/shared-motion screen and later selector test |

`results/` is already gitignored by the repository. It contains a 540-case
timing sweep, 36 map transitions, ordered worst schedule, 60 multi-row cases,
fit/level/detent/structure/lift/reliability tables, input hashes, measurement
gate and CAD records/STLs/PNGs. These are reproducible calculations, not records
of fabricated parts. Keep future physical records outside `results/`.

## Findings at the committed defaults

- Independent timing: **26.251 s**, only **0.749 s** to the ≤27 s engineering
  target. No measured operating region exists. Inspection/recovery can consume
  that margin immediately.
- Legacy notch point-follower capture envelope: **±8.72°**, smaller than an
  18° missed step. The new broad detent's restoring torque is only **0.00298
  mN m** in the ideal leaf model; friction and seating remain unverified.
- Four/five levels remain geometrically plausible; six has almost no angular
  reserve and does not align with full steps. Eight or more fail this toe width.
- Full-width illustrative box beams sag **0.799 mm** at the stated load/modulus;
  closer support is needed. Splice compliance, racking and brake remain gates.
- Purchased estimates with contingency: **$411.60 optimistic / $1089.65
  realistic allowance / $5993.85 conservative retail**. Only the speculative
  combination fits; no matched delivered BOM qualifies.
- Four/five-row shared motion has a **conditional** timing window, but needs
  complete selectors below roughly **$0.54/$0.43** each. Retain a later 2×4
  dynamically selected latch coupon, not a full travelling head.

## Exact next print

Start with `results/fit_tile_0.05.stl`, `fit_tile_0.1.stl`,
`fit_tile_0.15.stl`, `walls.stl`, `bushings.stl` and `slider.stl`, PLA/X1C,
0.4 mm nozzle/0.12 mm layers. Repeat critical failures on 0.2 mm/0.08 mm;
inspect actual sliced walls. Then make 30 winning interchangeable cell sets
across three batches and test measured drag against half measured weight.
Stage A failure is useful evidence; no quantity is marked passing by simulation.

## Engineering analysis

Evidence words have their literal meanings: **calculated** is an equation;
**simulated** is an event schedule; **sourced** is a documented supplier claim;
**assumed** is an input awaiting evidence; **measured** requires a physical record.
All physical gates are currently **unverified**. `uncertainties.csv` is the
31-item canonical register, including thresholds and architecture consequences.
Values between an acceptance and a hard failure threshold are inconclusive and
do not permit scaling. Stage procedures below govern the required sample counts.

### Historical audit

Read the root target, architecture report, test guide, fabrication/miniature
context, backlog, and all Test08 documentation, parameters, BOM, sources,
analysis/checks/CAD/strength/plot scripts and blank measurement template.
Inspected historical **mechanism source**, not only Test08's historical table:

| Source | Finding relevant to Test09 |
|---|---|
| test01 `bolt-v3.scad` | 4 mm screw, 2 mm pitch, 50 mm length. Twenty rotations for 40 mm still require a qualified rapid coupling; printable screw memory does not make actuation free. |
| test02 `models/pixel.py`, `models/grid.py` | Explicit slider widths and guide cavities are useful for process coupons; no actuation or retention evidence. |
| test03 `actuator.scad` | 6 mm body exceeds target pitch. Screw/coupling dimensions are designs, not friction measurements. |
| test04 `frame.scad` | 4.64 + 0.44 = 5.08 mm spacing; long thin guide walls already present. |
| test05 `actuator.scad`, `calibrate_rect_tube.scad` | 4.4 mm hollow body, 3.2 mm screw and 3 mm lead; clearance sweep precedents. No empirical fit tolerances. |
| test06 `test-strip.scad` | Comments and geometry explicitly cam an entire release strip when one column rises. Cannot reuse this as independently holding latches. |
| test07 `grid.scad`, `caddy.scad` | One comb per row still couples cells in that row. Feeders are schematic; 12.6 mm motors in two ranks cannot pack at 5.08 mm pitch; 5.1 mm tube OD also exceeds it. Multi-row speed therefore deserves a fresh screen with different local retention. |

Test08's six checks were rerun and passed. Its optional NumPy 1.26.3 cam-strength
screen was also rerun: 4.96488 N converged ideal critical load, with the uniform
beam check within 3.3e-9 relative error. These check model behavior, not parts.
Its nominal schedule was independently reconstructed rather than copied. CAD
reuses the historical source by generating a local snapshot, records its hash,
and rechecks its specified contacts. No historical source is edited.

### Return and fabrication

The historical relieved-body volume predicts solid **2.069 g** and hollow
**0.997 g** at assumed density 1.24 g/cm³. Their measured values remain blank.
The 2× return margin requires drag below **10.15 mN** / **4.89 mN** respectively.
Test09 does not assign a friction coefficient. Normal forces from bow, guide
misalignment, layer ridges, lateral load and contamination dominate; a guessed
PLA-on-PLA coefficient would not establish breakaway force.

The fit sweep subtracts combined width/bore error and `12*tan(tilt)` from total
body clearance: a dimensional sensitivity screen, not a printer tolerance.
Fixture tilt relative to gravity and misalignment between guide tiers are
different experiments. Tilting the board changes weight components and contact;
offsetting a guide changes preload and can jam even a vertical board.

Increasing clearance at fixed 4.68 mm width consumes already thin webs:
0.05/0.10/0.15 mm per side leaves 0.30/0.20/0.10 mm webs. A 4.48 mm body with
0.10 mm clearance leaves 0.40 mm webs at unchanged **5.08 mm pitch**, but lowers
surface fill from 84.87% to 77.77% and reduces weight. It is an experimental
fallback, not a silent Test08 improvement; full follower relief/toe dimensions
and mass must be revised if selected. Do not insert the wider follower in it.

First compare PLA solid followers printed upright and on their side, 0.4 mm
nozzle at 0.12 mm layers, then 0.2 mm at 0.08 mm layers for the fine guides.
These are starting slicer settings, not qualified recipes. Record actual wall
paths in the slicer; a missing or single fragile web fails even if STL is valid.
Set 100% infill for the solid comparison; weigh it because actual infill/voids
change mass. No CF-filled material is assumed usable with the 0.2 mm nozzle.

If gravity fails, first reduce guide preload/contact length and test solid
bodies. Individual ballast adds lift mass and assembly. Even 0.02 N return
springs add 128 N to the platen; 0.1 N adds 640 N. Printed springs require life
and creep testing. A common pull-down cannot pull an individually stuck column
after other columns stop unless a releasable individual linkage is added.
Positive return is a new mechanism; latch/shared-motion alternatives also need
an explicit down-reset solution and do not automatically solve friction.

### Rotor, detent and coupling

The calculated toe half-envelope is **23.50°**. Four levels leave **21.50°**
nominal margin and 13.33 mm steps; five leave **12.50°** and 10 mm steps; six
leave **6.50°** and 8 mm steps. Six also needs up to 6° correction from 18° full
steps; there is only 0.50° geometrical reserve at a ±6° seating gate. Eight,
nine and ten levels have negative nominal toe clearance. Four and five align
exactly with this motor's full steps. Five remains a useful hypothesis; four
is the first fallback. Height resolution is a product tradeoff, not free margin.

Original individual cell parts fit conservative ±2.50 mm XY envelopes, leaving
0.08 mm between neighboring envelopes at 5.08 mm pitch for arbitrary heights
and rotations. This is only a rigid nominal bound: shared guide plates are
intentional connections; new detents, retention, frame and elastic deflection
are excluded. Stage B's mixed-height checks and Stage D's integration gate are
still necessary. The scripts reject changing the baseline grid/stroke without
revising the coupled historical geometry/mass and reliability screens.

The Test08 wheel has 0.25 mm radius cutouts centered on a 1.65 mm radius. A point
follower reaches a notch only within `asin(0.25/1.65)` = **±8.72°**. Elsewhere
the circular rim supplies no deterministic angular restoring gradient. A finite
tip alters the boundary but does not demonstrate ±18° correction. The historic
notch is therefore not evidence for the missed-step gate.

New wheel: `r(theta)=1.65-0.10*(1+cos(5 theta))` mm. A replaceable PLA leaf
10×1×0.45 mm with assumed 0.05 mm preload rides its continuous scallop. Ideal
basin half-width is 36°, enough geometrically to investigate one missed step.
`F=E*b*t³*delta/(4*L³)` and `T=-F*dr/dtheta` give only **0.00298 mN m** peak
restoring torque at assumed E=1500 MPa. Maximum strain is about **0.169%**.
Neither is a material allowable or measured holding torque. Friction can stop
it well before center, and nib geometry changes the torque curve; measure both
directions and release from multiple angles. Bench leaf is flat for controlled
layer orientation. A vertical axial leaf is a possible packing change, but its
clamps, home lug, thrust stack and head still need an integrated full-pitch CAD
check before Stage D. The flat bench assembly is explicitly **not tileable**.

A further warning: an assumed 1° circumferential plateau slope under 1 N at
1.35 mm radius would produce `F*r*tan(slope)` = **0.0236 mN m** disturbance,
about eight times the candidate leaf's peak restoring torque. Even 0.1° is
comparable. This is a sensitivity calculation, not a measured printing error
or predicted slip (contact friction may resist it). Test loaded angular drift
and vibration; the unloaded capture test alone cannot qualify passive memory.

Toe contact pressure remains roughly 3.11 MPa at 1 N / 15.54 MPa at 5 N.
The Test08 cam beam screen predicts 4.96 N with an ideal clamped root and no
eccentricity or creep; it gives **no acceptable 5 N margin**. Do not treat
coupon STLs or the proposed detent as repairing this weakness. Toe edge wear,
bridge layer failure and cam bow are Stage B stop conditions.

An 18° motor electrical step is not a rotor encoder. A friction coupling slips
at the hard stop and can leave arbitrary relative phase. Home 22 pulses toward
the stop; record actual rotor angle on reversal, including backlash, first-step
motion and deliberate slips. A motor rotor that turns successfully while the
face slips can silently miswrite. A detent can only rescue errors inside its
**measured** attraction range.

The bench coupling uses a replaceable 2.3 mm face pad against the Test08 drive
disc, an axially guided motor carrier and external compression spring. Test
0.1, 0.2, 0.5 and 1 N preload, 0.5–1 mm disengagement travel; these are trial
values. With effective radius 0.75 mm and required torque 0.15 mN m,
`mu*F >= 0.20 N`; no mu is presumed. Measure slip torque, running torque and
axial force together. Require mechanism torque < half measured motor running
torque, a non-slip write, and controlled stop slip without damage. A narrow or
empty slip window rejects the friction coupling. At 0.5 N per channel the head
must distribute 40 N, not merely align eighty unloaded shafts.

### Timing and reliability

`worst_schedule.json` covers reset/reference, 41 mm raise, 79 accelerated index
moves, 80 complete engage/home/write/disengage/seat transactions, park, lower,
settle, inspection and recovery. All-low is still rewritten. High→low,
low→high, inverse checkerboard and one-high-per-row all use global unloading;
old heights cannot reduce this stroke. The transition cross-product is a
schedule test, not a dynamic collision or successful return simulation.

The result matches Test08: **26.251 s**, with **0.749 s** to 27 s. A 1 s final
inspection alone loses the engineering target. Doubling coupling time to
50 ms each way loses the hard 30 s limit. The 540-case sweep covers rates,
coupling, all three settling durations, acceleration
and inspection jointly; favorable points are assumed, never a measured region.
`qualify.py` uses recorded maxima ×1.2 and minima /1.2, not an optimistic average.
At least 1000 rows spanning cold/warm/worn/misaligned conditions are needed even
for its **conditional timing** gate. A real measured operating region is absent.

For independent cells, `P(perfect map)=(1-q)^6400`; for separate row and module
events the screen multiplies by `(1-q_row)^80*(1-q_module)^64`. These independent
event classes are a simplifying assumption; clustered wear and shared supply
faults invalidate simple pooling. A 99% perfect-map goal needs cell q≤1.570e-6
even with no correlated faults, and **1,907,667** zero-failure independent trials
for a one-sided 95% bound. Eight channels ×10,000 gives a 3.745e-5 bound under
independence, far short of this goal. Count row transactions separately.

Detection is therefore required for a credible larger prototype unless far more
reliability evidence appears. A camera/fiducial/lighting allowance is included,
but a top view can miss height errors and occluded columns. Test oblique views
or rotor fiducials with known false states; no coverage or latency is claimed.
Current sensing/driver fault lines catch rail and electrical faults, not all
stuck followers or slipping couplers. Detected failures keep READY false;
aborting a map is **not** successful <30 s readiness. Time a retry including
unload and inspection. Unbounded/manual repairs fail the product timing gate.

### Structure and lift

13.24 kg of calculated solid columns plus 2–6 kg assumed platen gives
**15.24–19.24 kg** moving mass before user payload. Models assume a cleared board.
Use 4 kg platen and 10 mN drag as an illustrative case: **236.57 N** peak lift.
Eight simply supported hollow beams, 20×30 mm with 2 mm walls, each taking 1/8
of distributed load, give **0.799 mm** sag over 406.4 mm at assumed E=1500 MPa.
At 203.2 mm support spacing the same line load gives **0.0499 mm**. The flat
2 mm strip's linear result is outside small-deflection validity by orders of
magnitude: it establishes failure of that idealization, not a literal sag.

These are 1-D beam bounds. They exclude module joint compliance, shear,
torsion, screw mounts, creep and load redistribution. Four corner screws do
not magically give every interior beam end a rigid support. Candidate: 64
10×10 guide tiles on a two-direction box grid, with 9 support nodes on a
203.2 mm grid or 16 closer nodes; compare with deeper beams on four screws.
Printed 203.2 mm half beams and two bolted splice plates allow a worst-position
joint test before a whole grid. Modular assembly needs measured datums and
shimmed tile registration, not assumed rigidity across bolted PLA joints.

`lift_drive.csv` explores 4/9/16 screws, 2/4/8 mm leads and 0.2–0.5 efficiency.
At 35 mm/s those leads need **1050/525/262.5 rpm**: a finer self-locking candidate
trades speed and motor torque. Self-locking is **not** inferred from lead alone.
One synchronous belt needs tensioners, shaft thrust bearings and either reliable
braking or a normally engaged catch. 10° skew with 8 mm lead makes 0.222 mm
height error, nearly the entire flatness budget. A motor's holding torque is
not its available torque at operating rpm. Measure loaded torque with a 2×
reserve. Reprice nine/sixteen screws and any deeper structure; current BOM has
only four and therefore is not a qualified structural purchase list.

The realistic Test09 allowance including brake, inspection, freight/import
reserve and contingency is **$1089.65**, optimistic **$411.60**, conservative
retail scenario **$5993.85**. Even realistic non-motor hardware exceeds $500
after contingency. This does not prove no custom cheap implementation exists;
it rules out qualification of the currently specified/allowed one. Cost and
physics must be met in the same design. Full-scale purchases are not justified.

## Multi-row architecture screen

`analyze.py` writes 60 cases to `results/multirow.csv`: 1–5 rows × 20/40/80
parallel columns × 150/300 mm/s stroke speeds × two mechanisms. Pitch stays
5.08 mm and stroke 40 mm. Last partial groups are counted with ceil; a 3-row
head needs 27 stops across 80 rows. Column groups use serpentine scanning with
accelerated diagonal transitions, then return to origin. No scanning overlap
is credited. Motor/body fan-out is necessary: adjacent 8 mm motors cannot sit
on a 5.08 mm grid. At least two ranks along a row are needed, with additional
routing space for adjacent rows, boards and compliant output shafts.

The full-width subset at **150 mm/s**, **4000 mm/s²** stroke acceleration:

| Rows | Stops | Available dwell at 27 s | Direct full stroke total | Shared stroke total | Direct head kg / axes | Shared head kg / selectors+drive |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 80 | 0.209 s | 66.97 s | 87.17 s | 1.70 / 80 | 0.94 / 81 |
| 2 | 40 | 0.461 s | 36.91 s | 47.01 s | 2.90 / 160 | 1.18 / 161 |
| 3 | 27 | 0.709 s | 26.98 s | 33.80 s | 4.10 / 240 | 1.42 / 241 |
| 4 | 20 | 0.983 s | 21.51 s | 26.56 s | 5.30 / 320 | 1.66 / 321 |
| 5 | 16 | 1.247 s | 18.38 s | 22.42 s | 6.50 / 400 | 1.90 / 401 |

All times and masses above are **calculated from assumed inputs**, not measured.
The 300 mm/s sweep retains stroke acceleration rather than simply halving times.
It gives two-row direct 29.25 s (no 27 s reserve), three-row direct 21.81 s,
four-row shared 24.31 s and five-row shared 20.62 s. Narrower 20/40-column heads
pay for extra stations; five×40 direct at 300 mm/s reaches 26.21 s but its
200 independent drives fail screened cost. No 20/40-column shared case meets 27 s.

### Transactions, reset and selection independence

**Independent:** all r×c axes raise through up to 40 mm and retract through
40 mm each stop, plus 100 ms assumed contact/settling/control overhead. A
passive per-cell latch must preserve independently chosen positions as rods
retract. Motor axes have 4 conductors each (320–1600 for full-width heads).
There is no evidence for a complete $2 full-stroke axis at 15 g; these are
optimistic costing and mass assumptions, not PM-motor specifications.

**Shared:** one common actuator advances 10 mm at each of four height planes,
rest-to-rest, with local selectors deciding which columns remain coupled; each
plane adds 20 ms selection and 15 ms settling. It then retracts 40 mm, plus
100 ms transaction overhead. The local selector travels only an assumed **1 mm**;
the shared mechanism still performs the **full 40 mm**. Each of r×c selectors
needs two conductors in this screen, plus four for the shared drive. This is
644/804 wires at four/five full rows before buses and sensors. Remote shared
power and fan-out can lower carriage motor mass but cannot eliminate independent
state selection. A fixed mask does not count as arbitrary-map programmability.

Both start from a **globally released low map**. The fixed 3 s allowance consists
of 0.5 s reference, 1.5 s release/down-reset, 0.5 s final settling and 0.5 s
inspection. None is measured; each must be timed, including gravity return and
release of the previous high map. A reset jam invalidates readiness. With only
3 s fixed overhead this is an optimistic screening bound. Extra reset/detection
time adds directly, and all selected cells reaching every level is adversarial.
The shared case must selectively disengage without dropping already held cells;
Test06/07's whole-row moving comb is unsuitable for this independence requirement.

### Mass, acceleration, force and cost

Scan v=250 mm/s and a=4 m/s² are assumed. Force `m*a` ranges from **6.8–26 N**
for 1–5-row direct heads and **3.76–7.6 N** for shared heads. Rail friction,
cable drag and motor torque/speed must be added. Minimum triangular acceleration
to move a distance d in a slot t is `4*d/t²`; keeping a five-row 25.4 mm hop
inside 160 ms requires about **3.97 m/s²**, before vibration settling. Bolting
more actuators onto a carriage does not establish this acceleration.

Head mass model is 0.5 kg frame/loom plus 15 g per direct axis; shared is
0.5 kg +0.2 kg drive +3 g/selector. Weigh actual hardware; these figures exclude
any later heavy reinforcement. At 400 columns and 10 mN drag the moving columns
alone need about 12.12 N (weight plus drag), plus shared tooling inertia and
latch forces. The large shared stroke and force remain real even though local
selector stroke is short. A jam can bend multiple outputs or stall the whole
head; force limiting and individual fault detection must be costed.

The $220 fixed hardware allowance is decomposed in `multirow_bom.csv`; it covers
scan axes/rails, power/control, reset and inspection. Direct local axes are
$2/$5/$10; local selectors $0.40/$1.50/$4.46 plus $25 shared drive. For large
banks the last value combines the sourced $3.96 solenoid tier with a $0.50
driver allowance. Its actual 12.6 g mass is greater than the custom-selector
3 g hypothesis, and 320 simultaneously powered solenoids would draw 1760 W.
That retail case needs a much larger supply, loom and head than the lean base
allowance; its shown cost is therefore already-failing lower-bound costing.
Add 20%
contingency. These are allowances, not purchasable matched assemblies. The
screen's base is deliberately leaner than Test08's lift/rotor programmer.

| Full-width choice | Optimistic / realistic allowance / conservative incl 20% | Maximum delivered local hardware price to fit $500 |
|---|---:|---:|
| 3-row direct | $840 / $1704 / $3144 | $0.819 per complete axis |
| 4-row shared | $447.60 / $870 / $2006.64 | $0.536 per selector including its driver |
| 5-row shared | $486 / $1014 / $2434.80 | $0.429 per selector including its driver |

Sourced commercial solenoids do not fit this budget. A $0.40 custom selector
is **speculative**, and five-row optimistic cost has only $14 left below the
ceiling. No measured region jointly satisfies timing, price and packaging.

### Later test decision

**Retain a dedicated shared-motion selector experiment**, contingent on a
credible <$0.54 delivered selector/driver route. Four rows offer more cost room;
five offer more time. This is a newly quantified research window, not grounds
to build a 320/400-channel head. Direct full-stroke arrays have timing regions
but fail even optimistic cost in those regions.

The smallest later prototype is a **2×4 full-pitch array** of individually held
columns, eight dynamically controlled selectors, one common four-increment
40 mm stroke and shared down-reset. First test all 256 binary masks and then
mixed five-level maps, measuring loaded selection ≤20 ms, no neighbor release,
reset reliability and selector/driver price. A manually swapped mask can test
passive mechanics only; it cannot pass dynamic programming. This experiment
belongs after the present process coupons and is not silently implemented as
an improved Test08. It can also test backlog R02/R03/R09 building blocks.

## Physical validation plan

Use the [uncertainty register](uncertainties.csv) as the decision record.
Copy the header-only CSVs under `measurements/` into a dated run directory;
preserve raw videos, gauge readings, controller event traces and failures there.
Commit compact measured records separately from generated `results/`. Do not
populate blank measurements with these calculations. Every result carries part
revision, slicer project/3MF, printer/material lot, operator, instrument and
calibration/uncertainty. Photos of a standing column are not a friction test.

Acceptance uses the adverse measurement uncertainty: force+uncertainty below
limit, clearance-uncertainty above limit. If the instrument cannot distinguish
pass from fail, record **inconclusive**. Stage gates authorize only the next
prototype, not product qualification. Stop at first destructive failure, retain
the failed part, record the condition and redesign before repeating that stage.

### A — process and return calibration, before purchasing a motor

**Make:** `fit_tile_0.05`, `_0.1`, `_0.15`, `fit_tile_narrow`, `walls`, `bushings`,
`shaft`, and solid 4.68 mm sliders from `cad_check.py` exports. Narrow tile uses
a separately exported 4.48 mm slider (`-D body=4.48`), never force a 4.68 mm one
through. Export real Test08 solid/hollow followers and slotted guides as well;
the simple slider cannot establish friction of the relieved follower.
Each tile is 3×2 at 5.08 mm pitch. 0.05/0.10/0.15 are **per-side clearances**.
Hole/slot strip runs 0.05 to 0.25 mm per side, left to right; walls run
0.20/0.30/0.40/0.60/0.80 mm left to right. Mark sample IDs on the external base.

**Print matrix:** first one of each on 0.4 mm nozzle/0.12 mm layers in PLA;
repeat critical fits on 0.2 mm/0.08 mm. Screen upright and side-printed followers
and record seams/support-contact faces. Use calibrated dry filament, no arbitrary
XY compensation, 100% infill for solid mass tests. Retain failing prints. Then
make **30 winning cell sets across three separate batches**, ten each distributed
between center and corners. Randomly swap followers and guides between batches.
No universal X1C tolerance is assigned.

**Instruments:** 0.01 g balance (prefer 0.001 g for dust), micrometer/calipers,
optical microscope for webs, 0.01 mm dial indicator, adjustable tilt stand,
small calibrated masses and a force gauge resolving ≤1 mN. Verify force gauge
with 0.1 g increments (~0.981 mN); a luggage scale is unsuitable. Film returns
at ≥240 fps with a time reference. Gauge-scale friction must be measured and
subtracted if a pulley is used.

**Measurements:** all dimensions, straightness and actual mass; 20 upward/downward
slow traverses per sample over the entire 40 mm working stroke. Horizontal
force measurement isolates guide friction; vertical differential weights verify
gravity return. Record peak breakaway and sliding force separately. Repeat at
fixture tilt 0°, 1°, 3° in both axes and guide offsets 0/0.05/0.10 mm. The
0.10 mm offset is a failure search, not the intended assembly tolerance.
Test clean as printed first, then one documented deburr-only cleanup. No
individual polishing to a matched mate.

**Continue:** 30 interchangeable sets, intact webs, no custom fitting, maximum
drag+uncertainty <0.5×measured weight, all returns settled ≤0.4 s at up to 3°
fixture tilt and 0.05 mm relative-guide offset. Record any weaker declared
installation envelope as a design change, not a pass. Otherwise stop gravity
scale-up. A narrowed body is a new geometry revision with new mass and fill.
Record hands-on minutes/scrap to expose manufacturing burden.

### B — passive six-cell full-pitch mechanism

**Make:** six each `passive_rotor`, `passive_follower`, `passive_follower_guide`,
two qualified `fit_tile_0.1` guide tiers, eight `bearing_half` pieces and one
`passive_lift_plate`. The fit
tiles have the same six guide apertures as the historical tiers, with a wider
outer border for clamping; this adds fixture margin without changing pitch.
`passive_body_guide.stl` is retained as a historical geometry comparison, not
the recommended fragile clamping edge. STLs use assembly coordinates, not automatic print orientation;
lower each part to the bed and inspect slicing. Rotor shaft is fragile in either
orientation; compare upright and side variants with documented support removal.

**Fixture:** use a rigid laboratory clamping frame around the 15.24×10.16 mm
active rectangle; rotor centers are `(5.08*x-0.3,5.08*y)`, x=0..2, y=0..1.
Use the **three-journal `bearing_half`**, not the oversized single-motor journal
ears. Mirror two halves across y=0 to form one row; duplicate at y=5.08 for two
rows. Assemble upper/lower decks around the captive shafts before clamping the
outer x ends to the jig. Upper deck z=-2.05 to -0.05 supports the rotor bases;
lower deck z=-12.95 to -10.95 traps the integral drive discs below it. This
provides nominal 0.10 mm total end play; measure and shim to 0.05–0.10 mm and
verify the wheel at z=-10 to -8.5 remains clear. The two decks use eight halves
total. Do not glue the turning journals to the shafts. Any hand finishing is
recorded and is not evidence of scalable cell bearings. For a reproducible
lab support, use three 0.10 mm steel shim fins at x=2.50+5.08*x_cell, extending
in y from -5 to 10 mm and z from 4 to 84 mm. Bond the backs of the two slotted
guides in each column to its fin with a controlled thin adhesive layer; clamp
the fins' y-end margins to external rigid angle brackets. The fin plus adhesive
must stay below 0.15 mm thick, leaving at least 0.09 mm nominal clearance to
the next body's x=2.74 boundary. Measure this clearance through every height;
if it cannot be maintained, stop and redesign the fixture. The original lift
slot ends at x=2.65 in each cell: fin/adhesive also needs positive **measured**
clearance there through the entire lift (nominal margin only 0–0.05 mm). A rub
invalidates the jig; do not diagnose column friction using that contaminated
force measurement. Fin/frame compliance
must be measured under load, not assumed absent. This purchased lab jig is not
a scalable printed guide solution: adopting metal backing in the product needs
a new cost and packing assessment. Set upper guide tiers
at **z=110.2–114.2 and 118.2–122.2 mm** with a height gauge, preserving hole
alignment. Clamp only external margins; no clamp may intrude into a column
opening. The jig is lab tooling, not a proven full-scale cartridge. Record a
dimensioned jig sketch/photo and dial-indicator alignment for reproducibility.

Lift plate occupies z=42–44 mm at bottom and translates **41 mm** on a screw
stage; cam bases z=0–2 mm. Independently rotate cams by hand while fully raised,
then lower without nudging the columns. For initial height-support tests, hold
rotor angle using external shaft clamps below the plate. These clamps replace
neither the detent test nor the automatic programmer; they isolate return and
contact. Keep rotor axial position fixed. No motor is required.

**Instruments:** Stage A equipment, height gauge, small load cell/weights, camera,
micrometer lift stage. Measure a named representative miniature from base bottom
to highest normal body/head feature and actual usable column travel.

**Sequence:** all 25 old/new level pairs on each cell, 20 repeats per pair,
distributed as four repeats each with neighbors low/high, inverse checkerboard,
isolated-high, isolated-low and mixed levels. Cycle 1000 times first; if sound continue to **10,000** on
each cell. Every 1000 inspect wear and repeat drag tests. Apply a controlled
1 mg of sieved PLA debris (record particle range, e.g. 50–150 µm, distribution
and photo) to each guide set and run 100 cycles before cleaning. This is a
repeatable contamination challenge, not a claim to represent all household dust.
Repeat drag and height measurements after cleaning and after wear.

Test 1 N vertical load for 24 h at each level (separate specimens may run in
parallel); test 5 N for 10 s on sacrificial specimens. At maximum height with
neighbors high/low apply 0.1 N then 1 N lateral force; record deflection and
post-unload behavior. Expect possible failure: historical ideal cam buckling
is already below 5 N. Do not proceed by ignoring the failed abuse gate.

**Continue:** U01 drag/settle gate; every height within ±0.25 mm; neighbors shift
≤0.10 mm; no crack, unintended drop or permanent set >0.25 mm; min unload gap
≥0.5 mm; no residual lateral-load jam; usable travel ≥40 mm and exceeds the
measured miniature. Any unmet criterion stops Stage C as a validation of this
geometry (isolated motor research may still proceed, labelled accordingly).

### C — one motor, retained rotor, home stop and replaceable detent

**Make:** `wheel_4/5/6` and `leaf`, `bench_base`, `home_wheel`, `home_stop`,
`motor_cradle`, two pairs `journal_half`, two pairs `collar_half`, `coupler`.
Use a new sacrificial Test08 rotor for the final loaded coupling test. The flat
leaf/wheel bench isolates torque and wear; it cannot fit adjacent cells and is
not a full-pitch head design. First compare the legacy notched wheel with the
scalloped five-level wheel. Four/six compare angular behavior only until matched
cam geometry is separately qualified.

**Bench assembly:** wheel at z=3.2 above base, leaf at z=3.45, leaf clamp centered
at (3,12.5) with M2 screw/washer and a shim supporting its underside. Rotor axis
at (0,0). Wheel's 1.3 mm bore mounts on a measured 1.1 mm gauge shaft, bonded
only at the hub for this bench test. Ream/bond is recorded. The nib is nominally
0.05 mm preloaded at the valley; measure actual preload rather than trusting
the STL. Home wheel adds a lug above the leaf plane; clamp the separate stop
so only the lug meets it. Adjust stop angular datum so the five operating
positions cover 0–288° without an intervening collision; verify by hand over
the entire sweep. Stop, clamp and wheel are bench parts, not a packed cell.

Mount motor vertically below the shaft in the cradle on an external guided
linear stage. An external compression spring provides measured 0.1/0.2/0.5/1 N
face force; a micrometer sets travel 0.5–1 mm. `coupler` needs its bore set from
the **measured motor shaft**, not the default gauge diameter. Glue a measured
friction pad in the shallow end recess; record material/thickness/adhesive. Two
journals plus collars take axial thrust so it cannot displace the rotor. Use
an indexed paper disk/microscope video fiducial on the rotor as independent
angle observation, never infer rotor angle from commanded motor pulses.

**Buy only a sample:** identified motor, suitable dual bridge, current-limited
supply, controller and sensor/temperature probes. Supplier list/lead-time
confirmation is needed; no order has been placed. Buy more motors only after
a same-part delivered batch quote can fit a revised product BOM.

**Instruments:** oscilloscope or logic analyzer, current probe/shunt, temperature
probe, optical angular measurement ≤1° uncertainty, low-force gauge and known
10 mm torque arm (0.15 mN m corresponds to 15 mN force), axial dial indicator.
Measure unloaded bearing torque and detent torque-angle hysteresis separately.
Then measure the coupled assembly under its actual load, not a no-load motor.

**Trials:** 100 home/write cycles per combination of 100/200/300/400/600/800 pps
and five target states, stop on thermal or destructive failure. At each rate
test both directions, cold and after 30 min maximum update duty. Randomize
initial rotor angle and electrical phase; intentionally slip by 9°, 18°, 36°
and a non-step offset, then rehome. Compare first reversal pulse motion.
Measure all transaction intervals individually and READY time. Log failure and
recovery even when a retry succeeds.

For passive detent capture, release from ±6/9/18/24/30° around every valley,
20 repeats each, unpowered. Run **10,000** cycles, remeasure curve every 1000,
then hold preloaded 24 h at 20°C and 35°C. Vibrate 5–50 Hz at measured 0.2 g
for 10 min per axis, with unloaded and 1 N-supported terrain; record actual
excitation. This is a screening environment, not a universal vibration rating.

**Continue:** seated angle+uncertainty ≤6°, always captures ±18° correctly,
no lost level, restoring torque retains ≥80%, no crack/creep; axial play ≤0.1 mm
under twice normal engagement thrust; loaded running torque ≥0.15 mN m at
chosen rate and ≥2× measured mechanism torque. Motor within supplier rating,
PLA mount ≤40°C. Non-slip writes and controlled home slip must coexist. Replay
measured conservative intervals at 80×80 must be ≤27 s. If not, redesign or
reject; raising motor voltage beyond its rating is not a timing fix.

### D — eight channels, not eighty

**Make:** an eight-channel 4×2 output head at 5.08 mm pitch, with staggered motor
ranks, individual spring compliance, qualified retained rotors and independent
detents. Stage C's flat bench leaf cannot simply be tiled: first detail a
vertical leaf cartridge, thrust housing and home lug, and check continuous
neighbor sweeps in CAD. That integration is an explicit **future gate**, not an
included production head STL. Use the measured sample dimensions for shafts.
Rigid lab XY and engagement stages are acceptable fixtures but their timings
must be replaced by product-axis measurements before full-scale qualification.

**Instruments:** C equipment plus simultaneous current/voltage capture at all
drivers, high-speed video of eight couplers, and planned optical inspection.

Run ≥10,000 randomized operations/channel (≥80,000 cell operations), adversarial
high/low and one-high-per-group maps. Record row event IDs to preserve correlated
failure information. Add controlled height offsets up to measured tolerance
stack and worn/dust states. Load the supply with equivalent 80-channel electrical
demand while exercising eight; this tests power, not 80-channel alignment.
Measure loom drag, moving mass and simultaneous engagement force. Do not
extrapolate a 4×2 span's stiffness to a 406 mm head without a separate beam test.

Inject **100 faults of each class**: stuck follower, intentional rotor slip,
partial coupling, rail dropout and module skew; test power cuts in each motion
phase. Validate detection, false alarms and READY suppression. Save optical
traces showing why the detector recognized each fault. A camera bought within
an allowance is not proof that all 6400 columns can be inspected in 1 s.

**Continue:** zero unexplained spontaneous failures, all injected faults
detected, measured conservative full-map replay ≤27 s including inspection and
bounded automatic recovery policy, and revised quoted BOM ≤$500 incl contingency.
Any silent fault, unbounded repair, electrical dropout or expensive necessary
hardware stops scale. 80,000 operations still do not establish production
reliability; use `reliability.csv` bounds and do not pool correlated events.

### E — representative lift/structure, independent of a successful small head

Start with two `beam_half` pieces, two `splice` plates and four M3 through-bolts,
washers and internal crush spacers at the splice. Two plates bridge the joint
on upper/lower faces; holes lie 10/25 mm from each mating end. Use separate
end supports, no glue credited as a rigid joint. Compare unspliced 203.2 mm
span with 406.4 mm midspan-jointed span under eight-beam-equivalent distributed
load; measure deflection and joint rotation. Print on side/flat and record
orientation; internal cavity bridging must be inspected in the slicer and part.

Then assemble a **406.4×406.4 mm dummy platen**, box-grid modules and 4 synchronized
screws first, or a revised 9-node design if beam tests reject corner support.
Dummy weights represent **13.24 kg columns + actual weighed structure**; add
measured aggregate friction allowance, not only static weight. Do not build
6400 columns to perform this test. Include guide rails, actual screw thrust
bearings, belt/tensioners and normally engaged brake/catch. Requote if support
count changes. Dimensions alone do not establish platen rigidity.

Use five dial indicators (four corners/center), distributed test weights,
torque/current logging, temperature and high-speed video. Load evenly, then
concentrate half the load in one quadrant. Run **1000** 41 mm lift/lower cycles
at intended speed, record torque and screw rpm, check flatness every 100. Hold
maximum load 24 h at 20°C and 35°C. Deliberately introduce belt phase errors
and one sticky guide; test fault detection before damage. First power-cut tests
use catch blocks less than 1 mm below the platen; expand only after controlled
braking is demonstrated. Test ten power cuts at each of bottom/midstroke/top.

**Continue:** measured deflection+racking ≤0.25 mm, unload gap-uncertainty ≥0.5 mm,
2× loaded torque reserve at operating rpm, no permanent set or lost synchronization,
power-cut descent ≤0.5 mm, restart requires reference and invalidates READY.
Any unmet result rejects that support/drive configuration. Add the working
structure/brake to BOM and measured lift times to the timing replay.

### Recording and decision closure

Fill `timing.csv` with one conservative **combined qualification observation**
per run: measured per-row event durations from C/D plus the selected measured
axis/lift envelope from E. `trace_path` points to a manifest containing all
contributing traces, units, phase boundaries and stage run IDs. Include cold,
warm, worn and misaligned condition rows. Motor home/program pulse durations
are derived from the recorded rate and home count, so do not duplicate those
durations in the settle columns. Reference includes reset/controller setup;
inspection includes final state verification; recovery includes the entire
bounded retry. Zero recovery is only valid for explicitly fault-free runs, not
as proof that faults require no time. The aggregate model cannot certify recovery
coverage; review injected-fault traces separately. If no bounded recovery exists,
record the failure in reliability and mark U19/U25 failed rather than entering 0.

Run `python 06-experiments/test09_test08_validation/qualify.py --timing PATH_TO_COPY`.
Header-only shipped data produces `NOT_MEASURED`; missing traces, invalid
numbers and duplicate run IDs are rejected. Stage A–E gates remain manual
engineering decisions with linked records; a timing-only flag cannot override
friction, load, cost, miniature travel or reliability failures.

Final decision requires all gates on the **same configuration**. At present,
only Stage A printing is the next recommended build. Stage C motor research and
Stage E beam coupons may be useful independently, but neither licenses a full
head after a passive-mechanism failure.

## Sourcing ledger

No orders placed, supplier contacted, delivered quotation obtained, or physical
motor measured. USD list prices are **sourced**; they are not delivered prices.
The BOM separates sourced entries from **engineering allowances** and
**speculative bulk targets** in each row. Shipping, import/currency exposure and
20% contingency are additional, separate allowances. Requote before purchase.

| ID | Primary source and observed fact | Qualification limit |
|---|---|---|
| M1 | [MOONS PM catalogue](https://www.moonsindustries.com/c/permanent-magnet-stepper-motors-a0208): 8PM020S1-02001, 8 mm class, 8.5 mm length, 18°, bipolar, 0.25 A, 0.4 mN m **holding** torque, $40 list | Listed product, delivery/stock unconfirmed. No usable loaded speed curve or shaft drawing retrieved. Rated voltage, shaft diameter/length and winding resistance must be confirmed. 80 cost $3200 before anything else. |
| M2 | [DFRobot FIT0708](https://www.dfrobot.com/product-2199.html): $12.90 single, $11.90 at ten; 10 mm linear motor, 18°, 20 ohm ±10%, 3.3–5 V, 1500 pps auto-start specification | Different assembly, no loaded rotary torque guarantee; requires removal/adaptation of screw slider and dimensional inspection. Cannot be substituted for an 8 mm PM08 motor. 80 cost $952 before delivery. Use dual bridges; do not infer GPIO drive suitability from sales wording. |
| M3 | [Archived PM08-2](../legacy/test00_pneumatic_multiplexer/docs/micro-stepper-datasheet.pdf) | Historical 3.3 V, 40 ohm, 18°, 8 mm, 5 gf cm pull-in torque; >800 pps is no-load. Historical €0.52/pair is not a current price. Test09 has no matched current low-cost offer. |
| D1 | [LCSC DRV8833PWR C544801](https://www.lcsc.com/product-detail/C544801.html): retrieved search snapshot displayed 566 stock; $2.3734 single, $1.8005 at 30, $1.5752 at 100 | Dynamic price table was not exposed on subsequent direct-page retrieval; these are sourced cached listing values, not a confirmed checkout. For 80 use 30 tier; 100 costs $157.52 versus 80×$1.8005=$144.04. PCB/passives additional. |
| D2 | [TI DRV8833](https://www.ti.com/product/DRV8833): two bridges drive one bipolar stepper, 2.7–10.8 V supply; PW package 500 mA RMS per bridge | Electrical architecture reference only. Choose current limit from the actual motor, check rail drop and fault output; chip fault cannot detect every missed step. |
| D3 | [Pololu 2130 carrier](https://www.pololu.com/product/2130): $10.95 single, $9.27 at 25; backorders allowed in retrieved listing | Practical one-motor bench driver if obtainable; 80 carriers $741.60. This carrier cost is **not** the bare-IC BOM. |
| S1 | [Adafruit 2776](https://www.adafruit.com/product/2776): $4.95 single, $4.46 at 10–99, $3.96 at 100+; displayed in stock; 5 V, 1.1 A, 3 mm throw, 12.6 g | Multi-row conservative $4.46 means sourced 100+ price plus $0.50 driver allowance for 320/400 channels. Smaller banks retain $4.46 as a rough allowance; shipping and loaded response unqualified. The lightweight 3 g selector mass is a custom-selector hypothesis, not this solenoid. |
| F1 | [Project X1C context](../../02-design-criteria/README.md), with [manufacturer specifications](https://eu.store.bambulab.com/products/x1-carbon-3d-printer) | 256 mm build volume, PLA baseline, 0.4/0.2 mm nozzles. Direct manufacturer retrieval failed during Test09; no new dimensional tolerance claimed. |

Search also covered 8 mm/18° surplus and linear motors. Aggregator prices and
unidentified marketplace motors were not promoted to qualified quotes. This is
not proof that cheap motors do not exist. It is a procurement gate: obtain one
traceable sample and an 80+spares delivered quote with the same winding, shaft,
step angle and production lot; measure that sample, then several lot samples.

At historical PM08 electrical assumptions, each phase draws 82.5 mA and an
80-channel two-phase head dissipates 43.56 W (13.2 A at 3.3 V). FIT0708 at 3.3 V
would instead nominally dissipate 87.12 W for 80; MOONS current cannot be combined
with the PM08 resistance. Driver wiring, thermal test and supply BOM must follow
the selected winding. No-load frequency, holding torque and pull-in torque are
three different specifications; none establishes 400 pps loaded running torque.

Blank `measurements/procurement.csv` records source/date, matched part, quantities,
unit currency, conversion, shipping, taxes and delivered USD. Update the BOM and
rerun before authorizing scale. Bench instruments and the existing printer are
test equipment, excluded from the product BOM; brake, sensors and permanent
structural hardware are included. No purchased part is hidden under printing.
