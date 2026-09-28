# Architecture screening at 80×80

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

## Search after the first promising candidate failed its initial checks

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
