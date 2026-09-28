# Test 08 — full-scale architecture search and programmed rotary stops

**Outcome: no product-qualified architecture.** Strongest next experiment:
passive five-level stepped cams, an 80-channel PM-stepper programming head and
a common lifting platen. Full-scale timing is conditionally 26.25 s; the working
purchased BOM is $432, or $518.40 with 20% contingency. Return friction, reliable
angular memory, head coupling, structural support and sourcing remain gates.

Start with the [engineering report](../../07-evidence-and-decisions/).
Supporting documentation is consolidated below. Machine-readable configuration remains in `params.json` and purchased BOM allowances in `bom.csv`.

## Reproduce

From repository root, Python 3.11+, standard library only for analysis/checks:

```text
python 06-experiments/test08_architecture_search/analysis.py
python 06-experiments/test08_architecture_search/checks.py
```

Optional variable-section cam buckling screen (tested with NumPy 1.26.3):

```text
python -m pip install numpy==1.26.3
python 06-experiments/test08_architecture_search/cam_strength.py
python 06-experiments/test08_architecture_search/cam_strength.py --core-radius 0.45
```

This solver checks itself against the closed-form uniform cantilever result and
records cross-section and element-count convergence. It is a structural screen,
not a material qualification or rated load. Output is `results/cam_strength.json`;
the override preserves a separate file documenting the rejected thin-core case.

Optional report figure: `python 06-experiments/test08_architecture_search/plots.py`
(matplotlib 3.8.2). It writes `results/engineering_summary.png` and `.svg` from
the current metrics and sensitivity sweep, without another simulation.

For actual parametric CSG/STL exports and scoped interference checks, install/use
OpenSCAD (tested with the installed Windows command-line program):

```text
python 06-experiments/test08_architecture_search/cad_check.py --render
```

The CAD command can take several minutes. It fails on compiler warnings, errors,
missing exports or nonempty interference solids. It queries five supported
states and twenty raised rotation angles. Continuous radial clearance is also
bounded analytically. It does not check the omitted head/frame/retention system.

`params.json` is the dimensional source; `analysis.py` emits
`results/parameters.scad` for `coupon.scad`. Run analysis before opening the SCAD
file. `part` selects rotor, follower, follower_guide, body_guide, lift_plate,
assembly or section. The baseline coupon is 3×2, at final horizontal pitch.
Its fixture, detent spring and drive head are not an assembled print-ready kit.
Upper guide heights derive from body length; follower-guide and lift coordinates
implement the 40 mm baseline. A different stroke requires updating and validating
the whole stack, not just `travel_mm`.

## Generated evidence

All generated files stay in ignored `results/` and are reproducible:

- `metrics.json`: configuration hash, timing, force, geometry, mass variants,
  cost and reliability bounds. There is deliberately no blanket mechanical pass.
- `worst_schedule.json`: complete ordered events, including reset and every home.
- `timing_sweep.csv`: 48 combinations of head count, motor rate and coupling time.
- `timing.svg`: six full-map cases with the 30 s boundary.
- `parameters.scad`, `assembly.csg`, five part STLs, `cad_checks.json` and three
  PNG renders after the CAD command.

The independent unit checks validate acceleration formulas, all-cell coverage,
adversarial maps, partial-width head groups, invalid height encoding and known
mechanical/cost failures. Historical files and the template are unchanged.

## Important interpretation

This is an analytical/event model plus real solid geometry, not rigid-body
physics. Height support and successful detent seating are conditional states.
No ideal-lock flags or zero-collision constants are offered as measurements.
The initial unsupported follower failed its load screen; initial full-width
guides had zero wall thickness; the first short follower guide lost contact at
full extension; nine cam levels fail angular clearance; a
40-channel head fails full-map timing. Those failures informed the revised
candidate rather than being hidden by a pleasing render.

The 40 mm stroke has not been checked against a measured named miniature. No
physical measurements, completed procurement, printed prototype or lifetime
validation are claimed.

## Architecture families and rejection / iteration log

All times below concern a complete adversarial map, not sparse edits. Rough
screening estimates are not contact simulations. Counts include the expensive
actuation; thousands of printed memory parts remain real assembly work. 40 mm
travel is the common provisional assumption. Price ranges are engineering
allowances unless the source ledger identifies a listing.

| Family | Actuators / purchased count at full scale | Full-map time and parallelism | Purchased cost / update power | Pitch, travel, fabrication and verdict |
|---|---|---|---|---|
| Motor per cell, screw memory | 6400 motors + 6400 drivers, ≥25600 motor wires | ~1–3 s with all cells parallel | Even $1 per complete axis is $6400; ≥6.4 kW at 1 W/axis | Remote fanout can provide pitch and stroke but enormous wiring/repair burden. Reject cost; passive holding alone does not fix it |
| One XYZ writer | 3 axes, ~30–80 motion/electrical parts | At 150 mm/s Z and 4000 mm/s²: 2×0.304 s stroke + 0.071 s index + 0.04 s contact ≈4570 s for 6400 | ~$150–300; ~30–100 W | Can fit square columns and 40 mm stroke. Hobby-buildable and repairable, but cannot approach 213 cells/s. Reject speed |
| Row bank of independent full-stroke pushers | 80 Z drives + scanner + release; 80 feeders/encoders | Same motion bound gives ≥54 s plus reset; legacy 40 mm/s is >160 s | ~$400–1000; ~100–400 W | 80-way parallelism insufficient at these stroke speeds. Fanout, buckling and per-cell detents required. Reject present implementation |
| Multiple independent row writers | 160–240 Z drives plus scanners | Two banks still ~30 s including reset; three ~21–25 s | ~$700–2000; ~200–800 W | Meets timing only by exceeding purchased budget and increasing wiring/assembly. Reject |
| Shared screw-driving row head | 80 rotary motors + coupling/index axes; 6400 printed screws | 40 mm / 2 mm lead = 20 turns: at 3000 rpm, 32 s rotation alone, ~42 s with indexing | ~$350–700; ~50–150 W | Fast loaded screw rotation, engagement, 6400 thread fits and self-locking lead tradeoff unresolved. Reject baseline; changing to large lead loses holding margin |
| Serial pneumatic aperture selector | ~16 plate axes + pump + valves; 6400 sealed sliding interfaces | Even 20 ms per cell gives 128 s before reset | ~$200–500 optimistic; ~50–200 W | Printed sealing, leakage and passive holding unproven. More channels needed; reject serial speed |
| Row-parallel pneumatic sample/hold | ~80 proportional valves + 80 row selections; 6400 non-return/hold elements | 80 rows × 0.25 s = 20 s ideal; filling/reset/locking plausibly 30–60 s | >$1000 at modest valve costs; ~100–500 W | 6400 seals and height control defeat hobby assembly/cost. A check valve is not a position measurement. Reject |
| Jacquard-style global motion with scanned binary catches | 80 binary selectors + lift + scanner; 6400 independent bistable catches | Eight 400 mm passes at 200 mm/s ≈16 s + reversals/reset/settling ≈20–30 s; requires ~25 ms selection windows | 80 sourced solenoids $356.80 alone; full system >$550, up to 440 W selectors | Potentially good timing. Catch access paths around lift/column array, gravity return and 6400 bistable mechanisms unresolved. Retain only as a custom-selector research fallback |
| Mechanical row/column coincidence addressing | ~80 column selectors + ~80 row inputs, 6400 clutches | Eight levels ×80 rows ×0.10 s =64 s; must get complete row transaction below ~40 ms | ~$300–700 conjectural; ~50–250 W | Dense clutches and cross-talk; long row shafts deflect. Cheap hardware does not establish independence. Reject baseline |
| Binary weighted height memory | 80 writers; 4 bits/cell =25600 stored mechanical bits for ≥9 levels | Four scans ×80 ×80 ms =25.6 s before ~10 s of indexing/lifting; fast 25 ms transactions could rescue timing | ~$300–650; ~50–150 W | Replaces electrical cost with four mechanisms in each 5 mm cell and potentially hundreds of assembly hours. Reject present complexity |
| Thermal/SMA/wax cells | 6400 thermal elements/switches or shared heating scanner | No credible end-to-end <30 s cooling/reset bound established for 40 mm load-bearing stroke | At merely 0.2 W/cell, 1.28 kW; hardware price not established | Thermal isolation and passive terrain holding need another mechanism. Reject without qualified thermal cycle, not on an invented cooling number |
| Passive mold/swap board/granular surface | 0–3 drives; small purchased count | Could be quick for pre-made maps; arbitrary-map preparation not bounded | ~$20–300; 0–100 W | Manual preparation, membranes or material coupling lose independently controlled narrow walls and complete arbitrary-map timing. Reject product mismatch |
| Programmed stepped rotary stops + common lift | 80 small PM motors + 3 motion axes; 6400 passive rotors, guides and detents | Explicit simulator: 26.25 s at 400 pps, 33.85 s at 200 pps; 40-channel alternative fails even at 800 pps | Detailed BOM in `bom.csv`; ~119 W including powered platen holding | Removes 40 mm actuator motion from each write. Five levels; hard stops support terrain without power. Strongest next experiment, not an approved product architecture |

### Search after the first promising candidate failed its initial checks

1. Plain stepped cam under a full-width column: tall unselected sectors collide
   with the column. Move the body above all sectors and add an offset follower.
2. Unsupported printed follower: Euler screening fails a 1 N load by almost an
   order of magnitude. Add a continuous slotted guide, retaining a short unsupported toe.
3. Nine cam levels at the proposed toe width: 20° half-sector is smaller than
   the 23.50° toe envelope. It can land on a neighboring higher step. Reject this
   geometry. Five levels leave 12.50° nominal angular margin. Four levels buy
   more angular margin at the cost of 13.33 mm height increments.
4. Cheap high-ratio servo head: 45° input mapped to 288° output makes timing
   plausible but multiplies deadband/backlash by 6.4. Sourced servos also exceed
   budget. Replace with 18° PM motors; 72° levels are four full steps apart.
5. Forty PM channels: re-running the complete schedule, including sideways
   repositioning and every row's home, gives 39.72 s even at 800 pps. Reject the
   appealing half-cost version rather than quoting only its rotation time.
6. Hollow lightweight columns: CAD-derived mass reduces gravity-return margin.
   Compare solid printed columns before adding 6400 springs or ballast pieces.
   Springs would add cell hardware or flexure life risk, and a 0.1 N spring per
   cell adds 640 N to the reset load. A global platen cannot pull individual
   stuck columns down once other columns have stopped.
7. Commercial binary solenoids: revisit the Jacquard branch instead of forcing
   the cam concept. The sourced selector bank alone consumes most of the budget;
   homemade electromagnetic selectors are a new validation project, not free
   reliable parts. No superior qualified replacement emerged from this search.
8. Rendered guided follower at maximum height: the first fixed guide was too
   short and lost the stem. Extend it to z=84 mm, relieve the lower body and
   lift plate, and connect the body to the stem through the open slot. Increase
   body length to 80.2 mm so a full 40 mm square upper segment hides this relief
   beside lower terrain. Rerun solid intersections and mass/load estimates;
   larger mass helps return but increases lift torque and overall height.
9. Expanded collision checks find that a high toe intersects the lowered lift
   plate. Extend its clearance window left to include the complete toe envelope.
   A separate cam-beam buckling screen finds only 2.45 N ideal critical load with
   the original 0.45 mm core radius. Increasing the core to 1.0 mm raises it to 4.96 N
   without nominal toe contact. This improves the design but still does not
   establish the 5 N handling gate.

The bottleneck has shifted from gross timing to printed sliding reliability,
passive angular retention, low-cost qualified actuators and structural support.
More animated CAD cannot resolve those uncertainties.

## Historical audit

Inspected 2026-09-27: root README, design target, test guide, template source and
parameters, framework tests, all test00–07 READMEs and mechanism source files,
archived document/spreadsheet content, and the archived micro-stepper datasheet.
Historical experiments were not modified. These are designs, not physical test
records: there are no measured friction, cycle-life, full-map timing or procurement
results establishing product compliance in the inspected files.

| Experiment | Actual mechanism/evidence | Useful contribution | Scaling issue |
|---|---|---|---|
| 00 pneumatic multiplexer | SolidPython generates binary-pattern aperture layers; 80 mm module, 16×16 outlets at 5 mm | Binary addressing and low-cost motor research | Apertures are not sealed, qualified valves; no pressure dynamics, leakage, cell locking or full-map schedule |
| 01 threaded rods | OpenSCAD/BOSL2 screw/nut variants: 2–4 mm diameters, 1–2 mm lead, 50–70 mm length | Passive screw memory, calibration geometry | Thousands of drives or a slow shared drive; printed fine threads and thrust support unqualified |
| 02 Python cubes | 4×4 SolidPython geometry, nominal 5 mm pitch, 50 mm sliders, dimensional sweep | Explicit clearance coupons | No actuation, holding or reset mechanism |
| 03 threaded actuator | 4 mm screw, 2 mm lead, 6 mm body, slotted drive head; frames/calibration parts | Shared screwdriver interface | Body alone exceeds pitch; engagement and complete update time absent |
| 04 plain cubes | 4.64 mm columns and 0.44 mm guide walls at 5.08 mm, 45×45 frame; pump-pressure coupon | Earlier work already targets appropriate pitch | No complete actuated/locked system; pump coupon is not a measured seal result |
| 05 grid/cubes/rod | 4.4 mm hollow body, 3.2 mm screw, 3 mm lead; 45×45 grid | Screw variant near target density | Nut wall/clearance and shared drive not qualified; no full-scale timing |
| 06 sandwich detent | 1×5, 8.5 mm pitch, 6 mm columns, 30 mm stroke, 5 mm steps, one sliding comb | Flat load-bearing tooth, common release | One rising column cams the entire comb: other cells on that comb can release; shrinking pitch is not a scale transform |
| 07 capped grid/caddy | 5×5 at 8.5 mm pitch; one comb per row; flexible rods; schematic feeders; two servo ranks | Separates large actuators from cell pitch; accessible row modules | Per-row comb isolates other rows, NOT other columns within the same row. Two ranks at target pitch provide 10.16 mm against 12.6 mm servo width; need ≥3. Tube OD is 5.1 mm against 5.08 mm pitch. No closed-loop rod-length measurement |
| template | Serial XY–Z travel sum, ideal discrete heights | Reproducible lightweight framework | No retraction, physical reset, acceleration or contact solver. `all_columns_locked`, zero error and zero collisions are assigned. Optional backends only import/version-check packages |

The three archived `shape-display-dev.odt` files have identical content XML
(SHA256 `e0376492ffa31e80114bf9cef9332680fca1fbe16fe3ede2a7372dc09f575c0d`).
The three `multiplexing-layout.ods` files also match
(`4c054428c527fa63efcdafc9e96f41ceceae5367213e21c8e6c8085ad0176ee1`).
They contain the earlier architecture comparison and bit-selection layouts,
not three independent experimental validations. Old 50 cm / 200×200 / four-hour
assembly aspirations are superseded by the current target and current request.

The archived PM08-2 datasheet says 8 mm diameter, 18° steps, 3.3 V, 40 ohm phases,
5 gf·cm pull-in torque, and response above 800 pulses/s **without load**. The
components note instead suggests 5–6 V and 0.12 A. Use the datasheet's 3.3 V
for this hypothesis; do not silently combine voltage, price and torque claims
from possibly different surplus motors. The quoted old €0.52/pair is not a
2026 delivered-price guarantee.

Retain: passive memory, square tiling, calibration coupons and shared actuation.
Discard as evidence: render appearance, ideal simulator flags and unsupported
claims that a comb or feeder “works well.”

## External source ledger

Checked 2026-09-27. USD unless specified. These sources bound the search; none
qualifies the proposed assembly. Bulk allowances in `bom.csv` are deliberately
labelled unquoted. Printed parts and fabrication time are excluded from the
purchased-hardware total; purchased stock, electronics and fasteners are included.

| Source | Fact used | Limits |
|---|---|---|
| [Archived PM08-2 datasheet](../test00_pneumatic_multiplexer/docs/micro-stepper-datasheet.pdf) | 18° step, 3.3 V, 40 Ω, 8 mm body, 5 gf·cm = 0.490 mN·m pull-in torque; >800 pps no-load response | No loaded torque/speed curve; surplus identification and price unresolved; not a verified production supply |
| [FEETECH FS90 manufacturer datasheet hosted by Pololu](https://www.pololu.com/file/0J1435/FS90-specs.pdf) | 0.12 s/60° at 4.8 V, 0.10 at 6 V, 120° commanded range, 120 mA no-load and 800 mA stall at 6 V | No-load timing, not loaded positioning time; analog deadband and coupling error matter |
| [Pololu FS90 listing](https://www.pololu.com/product/2818) | $8.40 single / $7.90 at five | 80 × $7.90 = $632 before other hardware; no inferred cheaper 80-piece tier |
| [Tower Pro SG90](https://towerpro.com.tw/product/sg90-7/) | 23 × 12.2 × 29 mm, 0.1 s/60° at 4.8 V | Speed/dimensions reference, not a quote for unbranded clone performance |
| [Adafruit mini solenoid 2776](https://www.adafruit.com/product/2776) | $4.46 at 10–99; 5 V, 1.1 A, 3 mm throw | 80 selectors alone cost $356.80 and could draw 440 W; mechanical response not specified |
| [DFRobot FIT0708](https://www.dfrobot.com/product-2199.html) | 18° PM motor, 1500 pps minimum no-load auto-start specification; $11.90 at ten | Linear assembly, different motor: evidence for the motor class only, not a drop-in torque guarantee or qualifying BOM |
| [MOONS permanent-magnet motors](https://www.moonsindustries.com/c/permanent-magnet-stepper-motors-a0208) | 8 mm 18° motor listed at 0.4 mN·m holding torque / $40 | Industrial retail is far outside budget; holding torque is NOT running torque |
| [MIT inFORCE](https://tangible.media.mit.edu/project/inforce/) | Individually driven 10×5 closed-loop force display | Supports the direct-actuation family; does not establish low-cost 6400-cell feasibility |
| [Reconfigurable discrete pin tooling research](https://research.sabanciuniv.edu/16383/1/Design_and_analysis_of_a_reconfigurable_discrete_pin_tooling_system_for_molding_of_three-dimensional_free-form_objects.pdf) | Research precedent for passive self-locking pin tooling | Not evidence that this project's density, price or update time is attained |

Engineering assumptions, not sourced measurements: 400 pulses/s loaded PM motor
operation; 25 ms engagement and 25 ms disengagement; 15 ms motor/detent settling;
250 mm/s carriage with 4000 mm/s² acceleration; 35 mm/s lift; 1.5 GPa effective
printed modulus; 1.24 g/cm³ solid polymer density; 5 mN guide drag. These must be
tested together. The sensitivity sweep includes slower motors and slower couplers.

No representative miniature has been physically measured in this investigation.
40 mm usable travel is a provisional design envelope, not a claim that the
authoritative miniature-height requirement has been verified.

## Smallest physical prototype and decision criteria

### Print the six-cell passive coupon first

Use the **3×2 geometry at full 5.08 mm pitch**, not an enlarged demonstration.
It is the smallest useful coupon with an interior column in a row, both lateral
neighbors, a neighboring row, different heights, and guide-wall interactions. The active
rectangle is 15.24×10.16 mm; allow an external fixture for clamping the guide
tiers at their documented heights. Print six solid followers, six rotors, six
slotted follower guides, the two upper guide tiers and the lift plate. Default
STLs come from `cad_check.py`. The guide tiers are separate solids in one export;
split them in the slicer and preserve z=110.2–114.2 /118.2–122.2 on assembly.

**These are contact/guide coupons, not an assembled automated printer.** The
fixture must hold rotor axes and guide tiers square. Support rotors in reamed
printed bushes, rotate them by hand without lifting their shafts, and raise
the common plate with a micrometer or an external screw stage. A final thrust
retainer, brake, detent leaf and motor head are not included in these STLs.
Do not interpret their omission as proof that those parts fit or work.

Suggested first fabrication: a 0.2 mm nozzle / fine layer process for the 0.2 mm
upper-guide walls, with the follower printed on its side and the toe layer
orientation recorded. If the walls cannot be printed reliably, that is a
geometry failure, not a reason to quietly enlarge the pitch. Resin is a second
process experiment, not an assumed tool already available to the builder.
Use a 0.01 g balance or better, calipers, a dial indicator, calibrated small
weights, a camera, and a low-range force measurement setup. An ordinary luggage
scale cannot resolve the critical millinewton friction.

Record the printer, nozzle, layer height, material/lot, orientation and every
manual reaming/sanding operation. First run as printed; then document a single
controlled cleanup method. Keep failed coupons and dimensions.

| Measurement | Method | Continue / abandon gate |
|---|---|---|
| Miniature travel requirement | Identify one actual representative D&D miniature, including its base; measure maximum height and record identity/photo | 40 mm stroke must exceed measured height. If not, enlarge stroke and rerun density, timing and load calculations before any compliance claim |
| Sliding return | Weigh each follower; measure breakaway force across entire stroke, all orientations, clean and with realistic dust; repeat after cycles | Maximum downward drag < half the measured weight (nominal solid-body gate **10.1 mN**). Every column must follow lowering and settle in the allotted 0.4 s. Any persistent stick fails |
| Independent heights | Exercise all 25 old/new height combinations and all neighboring low/high patterns; measure final tops | Within ±0.25 mm, no neighbor displaced by >0.1 mm, no extra operator nudge |
| Load support | 1 N on one cell at each height for 24 h; 5 N for 10 s; observe toe, sector and guide | No level change, crack or permanent displacement >0.25 mm. 5 N is a screening abuse load, not a whole-hand safety certification |
| Lateral handling | Apply 0.1 N then 1 N at maximum extension with neighboring cells low/high | Quantify deflection. No permanent jam or unintended level change after unloading; establish an honest permitted side load |
| Clearance under reset | Measure minimum gap between lifted toe/body and every rotating sector under representative platen deflection | ≥0.5 mm everywhere; baseline nominal is 1 mm |
| Process viability | Log hands-on time and scrap over at least 30 cell sets | If each assembly needs bespoke sanding or matching, stop full-scale fabrication and redesign guidance |

The cam-beam model predicts only 4.96 N ideal critical load even after the core
revision. Use a sacrificial coupon for the 5 N test; expect that a support or
material redesign may be necessary. A passed miniature-weight demonstration
must not override this failure gate.

For friction, a calibrated 0.1 g mass provides roughly 0.98 mN. Small differential
weights or a calibrated compliant force gauge can resolve the requirement.
The full device may not rely on added miniature weight to make columns return.

### Only after that passes: one driven cam, then an eight-channel head

The passive coupon does not test mechanical memory under vibration. Print and
test a replaceable detent leaf around the modeled wheel: starting hypothesis
10 mm free length, 0.45 mm thickness, 1 mm width, 0.2 mm deflection. The beam
estimate is only 6.8 mN and 0.135% surface strain. Add an individual angular
home stop and a thrust retainer; measure their space and loads. These details
are intentionally not treated as solved by the sector model.

Use one actual candidate PM motor, dual H bridge, thrust-retained rotor and
spring-loaded friction face coupling. Record part identity, delivered price,
voltage, coil resistance, loaded torque/speed, temperature and supply current.
Do **not** substitute the DFRobot no-load speed or the old surplus price for
measurements on the bought motor.

The qualification transaction is: engage; home 22 steps; settle; write up to
16 steps; settle; disengage; detent-seat. Nominal durations in `params.json`
must hold together. After random starting angles and intentional slips, require
the seated rotor angle within **±6°**, not merely an apparently correct motor
step count. The complete 80-channel extrapolation must stay below 27 s using
measured conservative durations, leaving at least 3 s for variability. The motor
must supply at least **0.15 mN·m running torque at 400 pps** for the initial
hypothesis, with measured total rotor/coupler friction less than half that.
If it cannot, rerun at measured rate: 200 pps already fails the full-map limit.

An eight-channel, two-row head then tests simultaneous engagement, shaft fan-in,
80-channel electrical extrapolation, neighboring selection and row motion. Use
at least 10,000 randomized operations per cell, including power cuts during
homing and disengagement. Zero failures at this stage permits a larger test;
it does not establish full-system reliability. No per-cell indexing feedback
exists in the current cost model, so a plan to detect silent miswrites must be
priced and timed if required to meet reliability.

Separately test a full-width dummy platen with the predicted 13.24 kg column
mass plus structure, four synchronized screws and deliberately uneven loading.
Require <0.25 mm flatness change, no racking, an adequate torque-speed margin and
controlled behavior on power loss. Small coupons cannot validate that structure.

### Stop criteria

- Abandon the current five-level cam geometry if it cannot retain/seat within
  ±6° without power or if a single-step error escapes the detent's correction.
- Abandon gravity return if the measured drag gate fails after controlled
  cleanup, wear or dust. Adding 6400 return springs is a new architecture/cost
  assessment, not a minor fix.
- Reject any purchased BOM above $500 delivered, including required braking,
  sensing, better motors and spares. Seek $400 or less; the current working BOM
  plus contingency fails this gate.
- Reject if conservative full-map timings reach 30 s, or if readiness requires
  manual fault repair. Never remove homing/reset from the timing to obtain a pass.
- Abandon ordinary-FDM fabrication at this geometry if guide-wall yield and
  surface tolerance cannot be maintained across multiple print batches.

Continuation needs **all** timing, cost, pitch, measured travel, holding and
return gates. If they fail, revisit the Jacquard/custom-selector branch with
its own measured actuator and catch coupon; do not finish the cam head on faith.

### Measurement record

Copy `physical_measurements.csv` per build. Empty cells deliberately mean “not
measured.” Do not replace them with simulated values. Record every failure,
including its recovery time; report full-map readiness separately from command
completion.
