# 04 — Architecture candidates

This stage records Shape Display system hypotheses, not preferred mechanisms.
The fresh search below deliberately starts from functions and scale rather than
from Test08's rotary stop. No candidate is product-qualified.

## Functional decomposition and accounting rules

Every architecture must allocate ten jobs: (1) map representation, (2)
selection, (3) power delivery, (4) vertical positioning, (5) state retention,
(6) tabletop load support, (7) lowering/reset, (8) regional isolation, (9)
programming and (10) detection/recovery. Combining jobs is allowed, but unnamed
"selectors" or "clutches" still need a count, price, pitch and transaction rate.

The common screen is 80×80 = **6,400 cells**, 5.08 mm pitch, five useful height
states across 40 mm, a strict <30 s end-to-end full update, arbitrary regional
updates, and <$500 purchased parts. Five-state terrain contains at least 14,860
bits; a purely serial writer needs >213 finished cells/s before overhead. These
are calculated bounds from [Test10](../06-experiments/test10_broad_architecture_screen/),
not measured performance.

## Broad explored solution space

The following are materially different allocations of the system functions.
“Drop” means do not prototype at present, not that every conceivable descendant
has been disproved.

| # | Architecture topology | Full-scale sanity check and disposition |
|---:|---|---|
| 1 | Motor and lead screw in every cell | 6,400 motors/drivers; even $0.50 per axis is $3,200. Excellent local updates and passive screw hold; **drop on bought count/cost**. |
| 2 | Solenoid per cell plus latch | 6,400 coils, switches and wires; latch reduces hold power but not selection cost. **Drop**. |
| 3 | Cylinder per cell with valves/check valves | 6,400 seals and independently metered states; manifolding does not remove local hold/measurement. Legacy Test00 did not validate seals. **Drop**. |
| 4 | Thermal/SMA/wax cell plus passive lock | Cooling and 6,400 heaters/switches dominate; no credible <30 s reset or thermal-isolation bound. **Drop pending a radically shared thermal selector**. |
| 5 | Electrostatic or dielectric-elastomer cell | High voltage, 40 mm stroke amplification, load support and 6,400 electrodes remain separate. **Drop for this fabrication baseline**. |
| 6 | One XYZ pick/push writer with local latches | Cheap active hardware and good local access, but 6,400 serial services require >213/s; Test08's modeled version took about 76 min. **Drop for visible full-map writing**. |
| 7 | One 80-column travelling row head | Eighty cells per dwell gives only 0.375 s/row including all reset/travel; Test10's illustrative 0.40 s dwell is already 32 s. **Drop as baseline, retain only with overlapping work**. |
| 8 | Full-width 4–5-row travelling programmer | 320–400 simultaneous channels and 16–20 stations; 0.40 s/station is 6.4–8 s before reset. **Survivor S3**, if channels are passive/shared rather than bought actuators. |
| 9 | Global lift plus per-cell bistable latch | Long stroke is shared and loads are passive; selection/reset of 6,400 latches is the real architecture. **Retain only when coupled to broadcast pattern media (S1)**. |
| 10 | Global incremental strokes plus cell ratchets | Four 10 mm broadcast strokes can create five levels; each stroke needs an arbitrary 6,400-bit threshold mask and selective release. **Survivor S1**; [Test11](../06-experiments/test11_threshold_ratchet_s1/) shows density passes but a single all-armed stroke needs ~2.4 kN, and mask writing needs ≥500 channels or an off-line writer. |
| 11 | Row/column coincidence clutch matrix | ~160 edge controls look cheap, but one row/column pair selects one intersection; arbitrary masks can require thousands of coincidences unless intersections store a broadcast mask. **Drop as sole programmer; retain inside tiles**. |
| 12 | Jacquard/punched threshold cards plus common strokes | Passive bitmap selection gives massive read parallelism; four binary threshold layers imply 25,600 decisions. Rewriting and alignment, not actuation, dominate. **S1/S2 ingredient**. |
| 13 | Stacked perforated first-stop plates | Height is external planar geometry; one lift reads all cells and the stop carries load. Four planes plus bottom encode five levels. **Survivor S2**, tiled for local change; [Test11](../06-experiments/test11_threshold_ratchet_s1/) leaves S2 valid only with off-line writing and double buffering. |
| 14 | Reprogrammable shutter/aperture planes | Avoids consumable cards, but 25,600 shutters cannot each have a bought actuator. **S2 variant** only with a shared off-line writer. |
| 15 | Double-buffered full-board map cartridge | Slow writing can be hidden and swap can be fast; unexpected local reveal and 400 mm registration are poor. **Drop monolithic form; retain tile cartridges in S2**. |
| 16 | Shared rotating shaft with per-cell clutches | Motors are shared but 6,400 dense, non-slipping clutches remain. Module-level coupling is plausible; **move clutch from cell to tile in S4**. |
| 17 | Tendon/Bowden power bus with cell catches | Routes power away from pitch, but 6,400 cables create friction, stretch and assembly work. **Drop per-cell topology; retain short printable tile tendons as an implementation option**. |
| 18 | Shared screw-driving matrix | Passive screw memory is strong, but 40 mm at 2 mm lead is 20 turns/cell; row-parallel Test08 baseline exceeded time and needs couplings. **Drop baseline**. |
| 19 | Magnetic latch plus swept magnetic writer | Contactless selection is attractive, but individually selective 5 mm sites require 6,400 magnetic bits or a serial field head; miniatures may contain steel. **Drop until a parallel rewritable medium exists**. |
| 20 | Vacuum/granular-jamming height field | Few pumps and passive freeze, but cannot guarantee independently square 5.08 mm columns or deterministic 40 mm levels. **Drop on product geometry**. |
| 21 | 10×10-cell tile elevators | Only 64 actuators and excellent isolation, but moving a whole tile represents 64 cells as one and loses required resolution. **Drop alone; use tile actuation only to read local cell memory**. |
| 22 | Manually swapped sculpted/preprinted terrain tiles | Fast visible swap and low hardware, but not arbitrary independently represented cells and requires map inventory/manual intervention. **Drop as primary product; useful fallback mode**. |
| 23 | Telescoping nested segments with printable snap states | Packages 40 mm stroke above/below the board and holds passively; selection still scales per cell and segment walls consume pitch. **Retain as a cell coupon, not an architecture**. |
| 24 | Rotary stepped stop plus wide travelling head | Separates programming, lifting and support. Test08 gives conditional 26.25 s and $432 working BOM; Test09 leaves sourcing, detent, return and structure unverified. **Reference S5, no longer presumptive leader**. |
| 25 | Orthogonal wedge/height strips whose displacements sum | Only O(160) controls, but representable height fields are separable row+column functions, not arbitrary maps. **Drop except as coarse base layer beneath fine cells**. |
| 26 | Inflatable common bladder plus local escapements | Shared pressure supplies stroke while mechanical catches store levels. Avoids metered cell pneumatics, but a 5 mm-pitch restraint/selector and controlled lowering remain. **S1 power-source variant**. |
| 27 | Fluidic decoder/network | Few electrical valves can address many branches, but arbitrary parallel states still need thousands of fluidic memory valves and leak-free printed paths. **Drop**. |
| 28 | Profile belts/drums, one encoded strip per row | Eighty replaceable profiles can support 80 columns in parallel and carry load; dynamic rewriting is off-board and row exchange disturbs a long region. **Retain as S2 media variant**. |
| 29 | Sixty-four autonomous 10×10 tiles with synchronized shared drive | Tile-local memory/decoder plus common shaft or lift offers full-board parallelism and local isolation. Replicated active hardware can still cost too much. **Survivor S4**. |
| 30 | Coarse active underlay plus fine passive residual layer | A 10–20 mm module elevator supplies bulk height while short-stroke cell memory adds detail, reducing local stroke but adding two state systems and seams. **Retain as S4 variant; reject if maps need arbitrary 40 mm neighbor steps**. |

## Promising survivors

### S1 — Broadcast threshold memory + global incremental lift

- **Topology:** each column has a printable ratchet/escapement and four threshold
  enables. Four board- or tile-wide 10 mm strokes advance exactly the cells whose
  encoded target exceeds each threshold.
- **Selection/programming:** a removable punched film, sliding shutter sheet or
  tile-local Jacquard layer supplies four arbitrary masks. It is passive during
  readout; a separate writer may prepare it off-board.
- **Power/state/load:** one global platen, cam, bladder or a few tile lifts provide
  motion. Ratchet teeth store height and carry downward play load; the selector
  need only gate an event, not lift a miniature.
- **Reset/region:** release combs are segmented by 10×10 tile or row. A local tile
  is unloaded/released and replayed through four strokes while other ratchets stay
  engaged; a truly global platen must not lift untouched loaded cells, so tile
  clutches or non-engaging lost motion are mandatory.
- **Scale/timing/cost:** four broadcast cycles are attractive—at an assumed 1 s
  per cycle plus 4 s reset/settle, readout is about 8 s—but mask installation or
  programming is outside that estimate. Bought hardware could be 1–4 drives plus
  64 tile couplers; the 25,600 threshold decisions must be printable media, not
  purchased solenoids.
- **Failure and sensing:** a missed ratchet step is local but not self-revealing;
  use a datum check or camera/top-height scan after programming rather than 6,400
  sensors.
- **Why investigate / likely killer:** uniquely combines extreme parallelism with
  passive support. It dies if four reliable threshold gates plus a ratchet cannot
  fit at 5.08 mm, or if updating a mask takes serial visible time.
- **Cheapest rejection:** a 2×5 full-pitch strip with two independently patterned
  thresholds, shared stroke and adjacent loaded cells; measure missed/double
  steps, release force and disturbance.

#### S1-B — banked broadcast ratchet (Test11 variant)

[Test11](../06-experiments/test11_threshold_ratchet_s1/) shows the un-banked S1
force gate fails only for a worst-case all-armed stroke. Splitting the board into
**8 banks of 10 rows (800 cells)** bounds one stroke's release force to ~296 N at
0.37 N/pawl and gives ~17.6 s for four strokes across all banks — still inside
30 s. It does **not** fix the mask-write problem: 12,800 unary decisions still
need ≥500 parallel channels or an off-line double-buffered medium. S1-B is
therefore a *force-feasibility* variant, not an independence fix.

### S2 — Independently swappable planar-memory tiles

- **Topology:** divide the surface into 64 nominal 10×10-cell tiles. In each tile,
  perforated first-stop layers, shutter layers, profile films or row strips encode
  height outside the moving column. A local platen raises the tile and followers
  settle onto hard stops.
- **Selection/programming:** selecting a tile needs only 64 addresses. Cell state
  is written into removable media by a slow off-board punch/shutter writer; a
  second cartridge may be prepared while the current tile remains visible.
- **Power/state/load:** a shared X/Y service head or common shaft couples to one
  tile for regional work; an all-tile bus reads a prepared full map in parallel.
  Stop plates, not the writer, bear miniature loads.
- **Reset/region:** isolate, lift and exchange/rewrite only affected tiles. The
  10×10 choice is a sweep point, not a decision: 8×8 cells yields 100 tiles;
  20×20 yields 16 but coarser disturbance. Seam caps must remain independently
  supported.
- **Scale/timing/cost:** full readout could be one 40 mm lift/lower operation,
  plausibly seconds, but there is no valid <30 s claim until cartridge insertion,
  registration and tile coupling are timed. Likely purchased items are 1–4
  motors, shafts/belts, controller and perhaps 64 cheap mechanical couplers—not
  6,400 cell actuators.
- **Failure and sensing:** bad media corrupt one tile; keyed insertion, fiducials
  and a height image can localize faults. The writer may be slow only when the
  next map is known; surprise reveals require stocked/prewritten tiles or a fast
  small-tile writer.
- **Why investigate / likely killer:** it externalizes precision and makes slow
  programming concurrent with play. It dies if multilayer registration catches
  followers, if tile exchange disturbs miniatures, or if arbitrary surprise data
  cannot be written quickly enough.
- **Cheapest rejection:** two adjacent loaded 5×5 tiles and two media patterns;
  exchange/read one 100 times while measuring untouched-cell displacement,
  insertion force, seam height and misreads.

### S3 — Multi-row mechanical DMA head + local passive memory

- **Topology:** a carriage spans all 80 columns and four or five rows. A common
  short stroke or rotating bus drives 320–400 printable selectors that write
  ratchets, latches or stops; the head never carries play load.
- **Selection/power:** electronics send a bitmap to the head; a small number of
  motors powers common cams/shafts while printable shutters/clutches fan out the
  choice. This is not viable if "channel" means one bought actuator.
- **State/load/reset:** local teeth or stops retain height. Reset is row/tile
  segmented, allowing the head to rewrite only an affected band.
- **Scale/timing/cost:** 4 rows produce 20 stations; an illustrative complete
  0.40 s dwell gives 8 s before travel/reset. A credible schedule may allocate
  12 s programming, 5 s carriage travel, 5 s reset and 5 s verification = 27 s,
  but every term is an unverified budget. At $0.50 each, 320 bought selectors
  cost $160 before drives; printed fan-out is therefore central.
- **Regional/failure:** excellent random regional access, though a failed common
  shaft can affect a band. Encoder plus post-write height scan can retry locally.
- **Why investigate / likely killer:** it handles surprise terrain without
  prewritten media and concentrates maintainable hardware. It dies on selector
  pitch, cumulative force, moving mass or inability to complete a loaded dwell
  in roughly 0.4–0.6 s.
- **Cheapest rejection:** a 2×4 head section at final pitch with adversarial
  checkerboard selection, one shared drive and loaded passive latches. Measure a
  complete engage/write/disengage dwell, not unloaded motor speed.
- **First cheap result ([Test11](../06-experiments/test11_selector_coupon/README.md),
  calculated/CAD only):** the printable sliding-gate latch inherited from legacy
  Test07 survives as a body but not as a linear gate at 5.08 mm pitch — the
  0.20 mm inter-cell band cannot host the 1.60 mm slot+walls, and a 1.2 mm
  one-blade rotary gate crosses 1.10 mm into the occupied neighbour channel. A
  one-per-column electronic gate on a 2-wire bus takes 0.72 s and 7.2 A to
  address 80 columns, above the 0.60 s dwell. The surviving S3 topology is
  therefore an **axis-centred drum gate addressed as a banked loaded register**,
  not a gate per column powered during the write. The shared stroke is only
  25% of 40 mm (4 strokes), independent of column count. Nothing here changes
  S3's "drop until quantified" disposition; it redirects the next coupon.

### S4 — Distributed passive tiles on a shared power bus

- **Topology:** 64 10×10 tiles each contain a small printable decoder and local
  cell memory. A common shaft, belt, reciprocating rail or pneumatic bladder
  supplies energy to all tiles; one inexpensive tile clutch isolates regional
  work.
- **Selection/state/load:** tile selection is electrical or mechanical; within a
  tile, row/column coincidence or threshold masks select cells. Local ratchets or
  stops hold load after the bus stops.
- **Reset/region:** engage all tiles for full map; engage one or several for local
  reset/replay. Fault propagation is bounded if clutches fail open and each tile
  has overload protection.
- **Scale/timing/cost:** 64 active couplers are potentially affordable only if
  each complete channel averages below about $3 to preserve room under $200, or
  $6 under the absolute $500 ceiling before the rest of the machine. Full-map
  time depends on four/five synchronized broadcast cycles, not 6,400 services.
- **Why investigate / likely killer:** module isolation directly compensates for
  global-motion weakness and matches the X1C build envelope. It dies if the tile
  decoder merely hides 100 costly clutches, or shaft torsion/backlash causes
  correlated missed states.
- **Cheapest rejection:** two 2×4-cell tiles on one bus; cycle one while the other
  supports a load, then both together. Measure clutch cost, torque, phase error,
  neighboring displacement and jam propagation.

### S5 — Rotary stops + travelling programmer (reference survivor)

This remains a useful control against new ideas: height and load live in 6,400
printed stepped rotors, a platen provides 40 mm motion, and an 80-channel head
programs rows. Test08 calculated 26.25 s and a $432 working BOM; Test09 has not
qualified the motor source, detent/coupling, return friction or structure. Its
regional update requires lifting/clearing affected cells and is weaker than S2–S4.
Do not spend on a larger build until its existing Test09 coupon gates pass.

### Test11 refinement of S3, S4 and S5

[Test11](../06-experiments/test11_shared_drive_gate_analysis/) converts S3/S4
from analogies into concrete machines and gives S5 an explicit gate list. It is
**calculated, not measured**; no coupon has been printed.

- **S3 machine.** A carriage dwells over 4 rows (20 stations). Two per-station
  cam banks with four independent 5.08 mm-pitch planes each program 80 columns
  per sweep; four sweeps per station cover the four height increments. Selector
  fingers are **printed, not bought**, so bought per-channel count is zero. The
  calculated schedule is **25.20 s** (3 s reset, 6 s travel, 11.6 s writes,
  4 s verify, 0.6 s park) with a lean allowance near $94.
  - Hardest gate: **four rows share one 5.08 mm band = 1.27 mm per row**. A
    0.8 mm finger leaves a 0.47 mm web on a 0.4 mm nozzle — one extrusion.
    Rejection is a single fit-coupon print (T11-A). If it fuses, drop to 2–3
    rows/station and re-pay the timing.
  - Second gate: cumulative engaged-finger friction at 320 channels (T11-C) and
    a complete loaded dwell (T11-B).
- **S4 machine.** 64 tiles read 4 bus revolutions; the tile coupler must be a
  **printed dog clutch** because 64 bought clutches at the $6 ceiling are $384
  before the rest of the machine. The distinct failure mode is **correlated bus
  backlash** (T11-E): at 1°/joint over ~10 joints the calculated last-tile height
  error is 0.088 mm, within a 0.25 mm margin, but 3°/joint fails.
- **S5 gates.** All five remain **open** (motor supply, detent/coupling, return
  friction, structure, regional isolation). The cost boundary is reproduced:
  $332 working non-motor leaves a **$1.058/motor** ceiling against Test08's $1.25
  allowance. `checks.py` asserts this so it cannot be forgotten.

## Comparative decision frame

| Direction | Visible full-map parallelism | Surprise regional update | Bought cell-level parts | Passive load path | Dominant uncertainty |
|---|---|---|---|---|---|
| S1 threshold/ratchet | four broadcast cycles | good only with tile isolation | none intended | ratchet | 5.08 mm gate density and mask writing |
| S2 planar tiles | tile/all-board parallel read | medium; writer/media dependent | none intended | stop planes | registration and fast surprise media |
| S3 multi-row DMA | 320 bits/sweep × 4 planes/station | strong | **zero** (printed fingers) | local ratchet | 1.27 mm row land and loaded dwell |
| S4 shared-bus tiles | 64 tiles in parallel | strong | printed clutch (bought fails at 64×$6) | local ratchet | correlated bus backlash |
| S5 rotary reference | 80 cells/station | weak/medium | 80 motors/drivers | rotor stop | five open Test09 gates; $1.058 motor ceiling |

The search does **not** justify promotion into `08-current-design/`. S1–S4 are
architecture hypotheses whose fastest falsification tests should precede detailed
CAD or BOM optimization. [Test11](../06-experiments/test11_shared_drive_gate_analysis/)
supplies the ordered rejection tests and 3D-printable coupon for S3/S4 plus the
S5 gate list; it is calculated evidence and has not been printed or measured.

> **Update ([DND-35](/DND/issues/DND-35), ADR-002):** the survivor field is now
> converged. **S5 is promoted to [`08-current-design/`](../08-current-design/README.md)**
> as the single buildable winner; S1/S2/S4 are parked and S3 is killed, each with recorded
> evidence in
> [`07-evidence-and-decisions/convergence-decision-2026-09-b.md`](../07-evidence-and-decisions/convergence-decision-2026-09-b.md).
> This candidate table is preserved as the search record.

## Test11 refinement — September 2026

[Test11](../06-experiments/test11_threshold_ratchet_s1/) is the first hostile
arithmetic pass against S1/S2. It does not change the survivor list but sharpens
each verdict:

- **Density is not the killer.** A pawl + gate fits in 2.28 mm beside a 2.0 mm
  mechanism shaft; a 1.2 mm rack pocket leaves a 1.76 mm rail. The original
  "gate cannot fit at 5.08 mm" fear is unsupported at the arithmetic level.
- **Force is the S1 killer.** An all-high map arms all 6,400 pawls in one stroke
  (~2.4 kN at 0.37 N/pawl; break-even 0.234 N/cell). Fix by banking → **S1-B**.
- **Mask writing is the shared S1/S2 killer.** 12,800 unary decisions need
  ≥500 parallel writer channels (~9 s) or an off-line writer (~56 s) hidden by
  double buffering. Nothing cheap writes 6,400-bit masks serially in 30 s.
- **Print variation needs margin, not sorting.** Across 6,400 printed pawls the
  safe release window survives only to ~9% force sd; per-cell calibration is not
  affordable.
- **S2 survives as a system, not a mechanism.** Reading is ~2 s; the entire hard
  problem moves to the off-line writer and tile exchange. Surprise maps and
  exchange disturbance remain named product risks.
