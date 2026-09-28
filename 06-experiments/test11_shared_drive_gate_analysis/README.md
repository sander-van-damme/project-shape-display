# Test11 — shared-drive family system analysis and rejection gates

**Question.** For the shared-drive / multi-row survivors S3 (multi-row mechanical
DMA head), S4 (distributed passive tiles on a shared bus) and the rotary-stop
reference S5, can complete machines be specified with real component counts, and
what is the cheapest test that would reject each one?

**Answer (one line).** A concrete S3 machine can be specified and survives its
arithmetic; its selector fan-out gate is now an **analytic `S3_DENSITY_PRINTABLE`**
after the pivot was redesigned with a designed journal clearance
([DND-4](#s3--multi-row-mechanical-dma-head--local-passive-memory-invented-machine));
S4 is only viable with a *printed* tile clutch and its dominant risk is correlated
multi-tile backlash; S5's five named gates remain **open** and the $1.25 motor
allowance does not fit the $500 ceiling with contingency. No physical measurement
exists in this folder.

**Evidence level.** Everything here is **calculated** on **assumed** inputs, with
sources cited where used, except `coupon_geometry.py` (calculated fit screen),
`selector_fanout_coupon.scad` (readable parametric CAD) and the **generated,
mesh-verified STLs**. There are no printed or measured results: the STL files
exist so T11-A is ready to fabricate, not because it has been fabricated. This
folder does not qualify any architecture.

## Reproduce

```bash
cd 06-experiments/test11_shared_drive_gate_analysis
python model.py                       # system arithmetic for S3/S4/S5
python checks.py                      # asserts the rejection thresholds below
python coupon_geometry.py             # calculated fit screen for the S3 coupon
python make_coupon_stl.py             # stdlib STL generation (no OpenSCAD needed)
python verify_coupon_stl.py           # mesh + X1C-envelope check on the STLs
python t11a_fit_check.py --selftest   # synthetic exercise of the M1-M6 gate engine
python t11a_fit_check.py --validate   # check the runs/ measurement schema
python t11a_fit_check.py --predict    # CALCULATED expected coupon dimensions
# DND-4 analytic selector fan-out gate (replaces the forbidden physical print):
python analytic/t11a_analytic_gate.py --report      # printability + stack-up
python analytic/t11a_analytic_gate.py --selftest    # asserts the analysis is sane
python analytic/t11a_analytic_gate.py --emit-record # regenerate the analytic record
python t11a_fit_check.py --input analytic/runs/t11a_analytic_measurements.csv
# optional, if OpenSCAD 2021.01 is on PATH:
openscad -o selector_fanout_coupon.stl selector_fanout_coupon.scad
```

All scripts are Python 3.11+ standard library only. `checks.py` exits non-zero if
an assumption drifts into a regime the candidate cannot survive.

**T11-A print package.** `make_coupon_stl.py` emits `coupon_assembled.stl`,
`coupon_finger.stl`, `coupon_bank.stl` and `coupon_base.stl`; `verify_coupon_stl.py`
confirms each is well-formed and fits the 256 mm X1C envelope. The fabricate-and-
measure steps and pass/kill thresholds are in
[`T11A_PRINT_PROTOCOL.md`](T11A_PRINT_PROTOCOL.md). The notched finger is emitted
as a mesh with a notch cue rather than a volumetric boolean subtraction, so the
notch opening must be confirmed in the slicer and on the print, not from the STL.

**T11-A runnable scoring.** [`t11a_fit_check.py`](t11a_fit_check.py) is the
executable half of the protocol: it reads the human-entered table in
[`runs/t11a_measurements.csv`](runs/t11a_measurements.csv), applies the M1–M6
pass/kill gates, and resolves the protocol decision tree across the 0.4 mm
baseline and the 0.2 mm fallback (`--selftest` exercises every branch
synthetically; `--predict` prints the calculated coupon dimensions). **No row is
filled: nothing has been printed.** The package is ready to score a physical run,
not a substitute for one.

---

## S3 — multi-row mechanical DMA head + local passive memory (invented machine)

This is a concrete mechanism, not a relabelled "selector". The key invention is
to make the head a **bit-plane cam programmer**, so a station services 320 cells
with `increments` (4) *global sweeps* instead of 320 transactions.

### Arrangement

- A carriage spans all 80 columns and dwells over 4 rows. 20 stations cover 80
  rows (`stations = 80 / 4`).
- Each column has a **passive ratchet/rack memory** (backlog R04): a printed
  pawl holds one of five height increments. The head never carries play load.
- Two **cam banks per station** (one per column side) rotate under the column
  field. Each bank has four independent 5.08 mm-pitch cam planes; a plane
  corresponds to one of the four 10 mm height increments.
- Above each column, **four hinged selector fingers** (one per row claimed by
  this station) ride the bank. A finger with a printed notch engages its plane;
  a finger without a notch rides the raised land and is skipped. One bank sweep
  therefore advances **all 80 columns of one row that need that increment**, in
  parallel.
- Electronics stream a 320-bit bitmap into the head while it indexes; a small
  number of head motors drive the banks. There is **no bought per-channel
  selector**.

### Ten system functions

| Function | S3 allocation |
|---|---|
| Visible moving element | 6400 printed square columns (4.6 mm) + printed ratchet racks |
| State storage | printed ratchet/pawl, one of five increments, no power |
| Selection | 4 hinged printed selector fingers per column per station; notch present/absent decides write |
| Power distribution | 2 head cam-bank motors per station + 1 carriage index motor, shared across 80 columns |
| 40 mm motion | column rides a shared **global lift platen** (41 mm clear) then settles onto its ratchet step |
| Retention | passive ratchet tooth; load path is column → rack tooth → frame, not the head |
| Lowering / reset | global platen down; one release comb per row band lifts pawls for affected band |
| Full-map update | 20 stations × (engage + 4 write sweeps + disengage) + travel + verify |
| Regional update | head indexes only affected row band; release comb is row-segmented |
| Jam handling | per-bank friction coupling limits torque; post-write height scan flags band and retries |
| Power loss | ratchets hold; platen needs a brake/self-locking drive (shared with S5) |
| Assembly | 20 head cartridges + 6400 cell/rack prints + row release combs |
| Active / passive count | **41 head motors**, 6400 passive ratchets, 0 bought selectors |
| Purchased BOM (allowance) | ~$94 (41 motors + 41 drivers + controller + rails), no delivered quotes |
| End-to-end timing (calculated) | **25.20 s** at the stated inputs, 4.80 s margin |

### S3 timing schedule (`model.py`)

| Term | s |
|---|---:|
| global release + settle (`reset_s`) | 3.00 |
| 20 station index moves @0.30 | 6.00 |
| 20 dwells: 0.05 engage + 4×0.12 write + 0.05 disengage | 11.60 |
| 20 verify steps @0.20 | 4.00 |
| park | 0.60 |
| **Total** | **25.20** |

Sensitivity is the real story: this is a **budget**, not a measurement. If a
write sweep costs 0.18 s instead of 0.12 s the total is 30.0 s; if station index
is 0.40 s and write is 0.15 s it is 31.6 s. The 4.8 s margin must be protected by
measured Stage-B numbers before a head is trusted.

### S3 failure modes we are hostile to

1. **Printable fan-out pitch.** Four rows share one 5.08 mm band → **1.27 mm per
   row**. A 0.8 mm finger leaves a 0.47 mm web; on a 0.4 mm nozzle that is barely
   one extrusion. This is the single most likely killer and the reason T11-A is
   first. If the web fuses, S3 must drop to 2–3 rows/station and re-pay timing.
2. **Cumulative force.** Checkerboard = 40 engaged fingers × 0.03 N friction =
   1.2 N per bank at assumed μ=0.30, 0.1 N preload. A real cam-land crush force
   (not modelled) could multiply this. T11-C sweeps engaged fraction and looks
   for a nonlinear rise.
3. **Moving mass.** Four-row 5.08 mm head at assumed 15 g/axis plus frame is
   ~5–6 kg (Test09). At 4 m/s² that is 20–24 N before rail drag; the carriage
   axis is not free.
4. **Loaded dwell.** The model assumes 0.12 s per write sweep; that is a
   guess. The rejection test measures a complete loaded dwell, not unloaded
   motor speed.

### Cheapest rejection tests for S3

- **T11-A, analytic form (DND-4):** fan-out fit coupon. Under board policy
  [DND-27](/DND/issues/DND-27) the physical print is not run; the analytic gate
  [`analytic/t11a_analytic_gate.py`](analytic/t11a_analytic_gate.py) evaluates the
  as-designed geometry against sourced FDM limits plus a tolerance stack-up. The
  **pivot was redesigned** from printed-in-place to a designed journal fit
  (`PIVOT_CLR = 0.20 mm/side`, socket bore 1.20 mm), so protocol gate M3 is now
  analytic. The engine returns **`S3_DENSITY_PRINTABLE`** on the 0.4 mm baseline
  (analytic screen, not a print). The remaining thin term is M4 land reach
  (−0.05 mm worst case).
- **T11-A, physical form (deferred, not permitted under DND-27):** the printed
  coupon package (STLs + [`T11A_PRINT_PROTOCOL.md`](T11A_PRINT_PROTOCOL.md)) is
  ready to fabricate if the policy changes. It would kill S3 density if the
  fingers fuse (web < 0.20 mm).
- **T11-B (≈3 h):** 2×4 loaded engage/write/disengage dwell, all 256 binary
  masks, neighbour-release count.
- **T11-C (≈1.5 h):** full 80-column single-row bank, engaged fraction sweep,
  look for stall/skip onset.

---

## S4 — distributed passive tiles on a shared power bus (invented machine)

### Arrangement

- 64 tiles of 10×10 cells. Each tile carries its own printed decoder (a 4-plane
  index drum) and cell-level passive ratchet memory.
- One **rotating shaft bus** runs under the whole board. Four bus revolutions
  (one per bit-plane) let every tile read its programmed pattern in parallel.
- A **printed dog/index clutch per tile** couples the tile's local input to the
  bus only when that tile is selected. This is the only new bought boundary —
  and the arithmetic says it must be **printed**, not bought.

### Ten system functions

| Function | S4 allocation |
|---|---|
| Visible moving element | 6400 printed square columns |
| State storage | per-cell printed ratchet, same as S3 |
| Selection | 4-plane index drum per tile + printed dog clutch per tile |
| Power distribution | one common shaft bus, ~600 rpm assumed |
| 40 mm motion | shared bus drives a local tile lift/ratchet cycle; large stroke is shared |
| Retention | passive ratchet |
| Lowering / reset | reverse bus direction / release comb per tile |
| Full-map update | 4 bus revolutions + warm + settle |
| Regional update | engage 1..N tile clutches only |
| Jam handling | clutch **fails open**; per-tile slip before bus stall |
| Power loss | ratchets hold; bus is not self-locking by itself |
| Assembly | 64 tile cartridges on a common frame/shaft line |
| Active / passive count | 1 bus motor (few), 64 printed clutches, 0 bought cell selectors |
| Purchased BOM | bus motor + bearings + frame + controller, **plus no bought clutches** |
| End-to-end timing (calculated) | **1.10 s** bus sweep at 600 rpm (excluding full reset/lower) |

### S4 arithmetic shock: the clutch is the whole problem

`model.py` shows 64 tiles × $6 absolute allowance = **$384** bought clutches
*before the rest of the machine*. At the $3 ideal it is $192. **A bought clutch
consumes the entire S4 budget**, so S4's real gate is whether a printed dog
clutch can transmit the tile torque, disengage under load and fail open. That is
a mechanical coupon (T11-D), not a sourcing exercise.

### S4 failure modes we are hostile to

1. **Correlated bus fault.** A common shaft means one backlash stack. At 1°/joint
   random-walk over 10 joints the calculated last-tile height error is 0.088 mm,
   inside a 0.25 mm decoder margin — but at 3°/joint it is 0.264 mm and fails.
   T11-E measures phase lag vs joint count.
2. **Torque accumulation.** Simultaneous tile engagement on a shared bus sums
   load; a jam in one tile must not stall the bus. The clutch must slip first.
3. **Decoder vs clutch blur.** If the tile "decoder" is really 100 clutches, S4
   recreates the per-cell problem. The 4-plane drum must genuinely read 100 cells
   in parallel.
4. **Phase/registration.** The large shared stroke still has to settle each
   ratchet on its tooth; a skipped tooth is a silent one-level error across a
   whole tile.

### Cheapest rejection tests for S4

- **T11-D (≈2 h):** two 2×4 tiles, one bus, printed clutches, engage one then
  both, forced jam. Kills S4 if a jam propagates or the clutch can't disengage.
- **T11-E (≈1.5 h):** 2/4/6/8-joint bus, measure accumulated backlash.

---

## S5 — rotary stepped stops + travelling programmer (gate closure)

S5 is the existing reference. Test08 gave 26.25 s and a $432 working BOM;
Test09 left five gates open. This test adds an explicit, testable status per gate
and reproduces the cost boundary.

| Gate | Status | Smallest coupon that qualifies or kills it | Kill threshold |
|---|---|---|---|
| low-cost qualified motor supply | **OPEN** | buy ONE traceable 8 mm PM sample + delivered 80+spares quote (T11-F) | no same-part quote ≤$1.06 delivered |
| detent / coupling reliability | **OPEN** | flat leaf/wheel bench, 10k cycles, ±18° unpowered capture (T11-G) | capture fails or torque <80% |
| return-friction margin | **OPEN** | 30 interchangeable cells, 0/1/3° tilt, drag+unc <0.5×weight (T11-H) | any set fails |
| structural frame | **OPEN** | 203.2 mm beam + splice + 406.4 mm dummy platen under 8-beam load (T11-I) | deflection+racking >0.25 mm |
| regional isolation | **OPEN** | two adjacent 5×5 tiles, one resets while neighbour + miniature loaded (T11-J) | neighbour motion >0.10 mm or tip |

### Cost boundary reproduced

Test08's working non-motor allowance is **$332**. To finish under $500 **with
20% contingency**, the 80 motors must average **≤ $1.058** each
(`500/1.2 − 332)/80`). Test08 allowed $1.25. **The allowance does not fit.**
Removing another ~$99 from the $332 base is the alternative. `checks.py` asserts
this inequality so it cannot be quietly forgotten.

### Regional isolation note

S5's regional update still requires clearing the affected band and settling it,
which is weaker than S4's tile-level isolation. The honest disposition: S5 can
still be a valid **full-map** machine if its five gates pass, but it should not
be preferred for fog-of-war reveals until T11-J passes.

---

## Evidence boundaries

| Claim | Type | Status |
|---|---|---|
| S3 25.20 s schedule | calculated | at assumed sweep/index/verify inputs |
| S3 1.27 mm row land, 0.47 mm web | calculated geometry | from the coupon parameters |
| S3 coupon is printable on 0.4 mm nozzle | **assumed** | not rendered here, not printed |
| S4 1.10 s bus sweep | calculated | assumes 600 rpm, no reset/lower |
| S4 64×$6 = $384 clutch cost | calculated + sourced tier | $6 is the project's absolute per-channel ceiling |
| S5 five gates open | project status | inherited from Test09, unchanged |
| S5 $1.058 motor ceiling | calculated | reproduces Test08 totals |

## Decision

- **S3:** retain. It is the only family here that needs **zero bought
  per-channel selectors** and has a printable mechanical fan-out. Its survival
  depends entirely on T11-A (pitch) and T11-B (loaded dwell).
- **S4:** retain **only** with a printed clutch. Its distinct risk is correlated
  bus backlash, not selection cost.
- **S5:** do **not** scale. Run T11-F and T11-G first; the motor cost boundary
  currently fails.

None of this promotes an architecture into `08-current-design/`.
