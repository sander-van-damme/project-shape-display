# Ordered physical validation — no measurements yet

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

## A — process and return calibration, before purchasing a motor

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

## B — passive six-cell full-pitch mechanism

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

## C — one motor, retained rotor, home stop and replaceable detent

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

## D — eight channels, not eighty

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

## E — representative lift/structure, independent of a successful small head

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

## Recording and decision closure

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

Run `python experiments/test09_test08_validation/qualify.py --timing PATH_TO_COPY`.
Header-only shipped data produces `NOT_MEASURED`; missing traces, invalid
numbers and duplicate run IDs are rejected. Stage A–E gates remain manual
engineering decisions with linked records; a timing-only flag cannot override
friction, load, cost, miniature travel or reliability failures.

Final decision requires all gates on the **same configuration**. At present,
only Stage A printing is the next recommended build. Stage C motor research and
Stage E beam coupons may be useful independently, but neither licenses a full
head after a passive-mechanism failure.
