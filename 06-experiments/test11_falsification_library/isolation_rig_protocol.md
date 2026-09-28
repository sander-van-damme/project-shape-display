# J2 — shared isolation-rig protocol (research question Q5)

**Status: PROTOCOL ONLY. Nothing has been printed or measured.** Every
threshold below is a proposed pass/fail gate, not a result. This document is
written so that a CTO or human operator can build and run the same rig, obtain
the same numbers, and compare every architecture against one protocol.

## Why this rig exists

Q5 in [`05-research-questions/`](../../05-research-questions/README.md) is the
single discriminator that decides whether **regional updates** are real. S1, S2
and S4 all claim that one module/tile can reset or swap while its loaded
neighbour stays put. None has measured the disturbance. Without a number, the
product requirement "unchanged cells should remain mechanically supported and
should not be disturbed" cannot be pass/failed, and tile-size choice (5×5 vs
10×10 vs 20×20) floats on opinion.

The rig is deliberately **architecture-agnostic**. It provides:

- two adjacent loaded cell arrays (the "target" and the "untouched neighbour");
- interchangeable **drive fixtures** so S1 (threshold strip), S2 (planar tile),
  S4 (shared bus) and S5 (rotor row) can each drop into the same frame;
- one **representative miniature** interface so "does the figure move/tip" is a
  first-class measured outcome.

The same rig also serves the S2-B and CROSS-D register rows.

## What it is not

- It does not validate a full 80×80 board.
- It does not establish that a jam is contained at scale, only within the two
  tiles tested.
- A pass is a **gate to the next coupon**, never a product qualification.

## Rig layout

Two identical tile holders, side by side, sharing one rigid base rail. Only the
target holder is actuated; the neighbour holder is mechanically independent
except through the shared base.

```text
        fastened rigid base rail (aluminium extrusion or thick printed spine)
  +---------------------+   gap   +---------------------+
  |  TARGET tile holder | <-----> | NEIGHBOUR holder    |
  |  (interchangeable   |  seam   | (loaded, passive)   |
  |   drive fixture)    |         |                     |
  +---------------------+         +---------------------+
        ^ actuated here                 ^ dial indicators + miniature
```

### Key dimensions (coupon scale)

| Item | Value | Note |
|---|---|---|
| Cell pitch | 5.08 mm | full-scale pitch; do not scale down |
| Tile sizes under test | 5×5 (25.4 mm), 10×10 (50.8 mm), 20×20 (101.6 mm) | three separate holder pairs |
| Adjacent tile gap (seam) | 0.40 mm nominal | same order as cell-to-cell gap |
| Base rail | ≥ 12 mm thick, or clamped to a granite/steel bench | prevents rig flex masquerading as isolation |
| Holder wall | ≥ 2.0 mm | must not deflect under 1 N lateral |

The 20×20 pair exceeds the X1C 256 mm build volume only if printed monolithically;
print each holder in two halves on the 203.2 mm split and bolt on a printed
splice. The 5×5 and 10×10 pairs print in one piece.

### Printed parts per holder pair (J2)

- 2 × tile holder frame (accepts interchangeable drive fixture)
- 2 × cell-array coupon body for the architecture under test
- 2 × miniature base adapter (a shallow tray that centres a real figure base and
  prevents it sliding independently of the tile)
- 2 × dial-indicator mounting bracket
- 1 × shared base rail / spine
- seam shim set: 0.20/0.30/0.40/0.50 mm

### Purchased parts

- Two 0.01 mm dial indicators (vertical on neighbour tile; lateral on neighbour
  tile edge).
- One 240 fps phone camera or better, on a fixed tripod, framing both the
  neighbour tile and the miniature.
- Calibrated masses covering 1 g to 100 g, and a force gauge resolving ≤ 1 mN.
- One representative D&D miniature (28–35 mm humanoid), base measured and
  recorded.
- Optional: accelerometer taped to the neighbour tile (records vibration when a
  dial indicator is too slow).

### Interchangeable drive fixtures

| Fixture ID | For survivor | What it does in the rig |
|---|---|---|
| FX-S1 | S1 threshold/ratchet | fires one common 10 mm stroke on the target 2×5 strip |
| FX-S2 | S2 planar tile | lifts and drops/swaps the target 5×5/10×10 planar stack |
| FX-S4 | S4 shared bus | engages the target tile's clutch on the shared bus |
| FX-S5 | S5 rotor row | runs the target Test09 rotor row and lowers it |

Each fixture bolts to the target holder with the same four M3 interfaces so the
neighbour readings are comparable across architectures.

## Procedure

Record every run with: date, fixture ID, survivor, tile size, part revision,
slicer project/3MF, nozzle/layer, PLA lot, operator, instrument IDs and
calibration. Copy the `measurements/isolation.csv` header into a dated run
directory; do not overwrite the shipped blank.

### J2-0 — rig-qualification (run once, before any survivor)

1. Clamp the base rail to a rigid bench. Mount both holders with the 0.40 mm
   seam shim.
2. Install the dial indicators on the neighbour. Zero them.
3. Apply a **known** 0.05 mm shim under the target holder base. Confirm the
   neighbour vertical indicator does **not** read this (rig decoupling check:
   expect < 0.01 mm).
4. Load the neighbour tile with a known mass (representing columns + miniature).
5. Record the rig's own noise floor: tap the bench, read neighbour noise over
   10 s. **If rig noise > 0.02 mm, fix the rig before measuring anything.**

### J2-1 — disturbance during a target reset (the core measurement)

For each survivor × tile size:

1. Set the neighbour tile to a **non-flat** state (e.g. half the cells at
   mid-height, half low) and load it with the representative miniature plus a
   20 g mass.
2. Zero both dial indicators and start the 240 fps camera.
3. Run **one** target regional reset/update using the fixture.
4. Stop the camera; read peak vertical and lateral neighbour displacement from
   both the indicators and the video.
5. Score whether the miniature moved or tipped. "Moved" = base centre shifted
   > 0.5 mm. "Tipped" = base tilts enough to lift one edge > 0.5 mm.
6. Repeat 10 times. Record the maximum, not the mean.

### J2-2 — seam behaviour at maximum adjacent height difference

Raise target cells to maximum and neighbour cells to maximum independently so
the seam carries the largest step. Photograph the seam; measure seam step with
the vertical indicator across the seam. Load the seam with 1 N and re-measure.

### J2-3 — repeated exchange/update

Run 100 target update cycles with the neighbour continuously loaded. Every
10 cycles re-zero and record neighbour drift. **Cumulative drift** is a
separate failure mode from peak disturbance; both are gates.

### J2-4 — optional timing capture

Time one regional clear+settle from controller start to "neighbour and target
settled". This feeds CROSS-D and the `regional_update_seconds` model in
`reliability.py`. Time a 10×10 reveal and a 20×20 reveal separately.

## Pass/fail gates (proposed)

These match the register rows S2-B and CROSS-D. They are **inconclusive**
between pass and fail; record intermediate values honestly.

| Measurement | Pass | Fail | Units |
|---|---|---|---|
| Neighbour peak vertical displacement | ≤ 0.10 | > 0.25 | mm |
| Neighbour peak lateral displacement | ≤ 0.10 | > 0.25 | mm |
| Miniature base movement | ≤ 0.50 | > 0.50 | mm |
| Miniature tipping (edge lift) | ≤ 0.50 | > 0.50 | mm |
| Seam step at max adjacent heights | ≤ 0.25 | > 0.50 | mm |
| Cumulative drift over 100 cycles | ≤ 0.20 | > 0.50 | mm |
| Rig noise floor | ≤ 0.02 | — | mm |
| Regional clear+settle (10×10) | ≤ 5.0 | ≥ full-map | s |
| Regional clear+settle (20×20) | ≤ 8.0 | ≥ full-map | s |

The regional time gates are derived from the screening model in
`reliability.py`: fixed overhead plus a fraction of the modelled full-map time.
They give the architecture the benefit of the doubt (perfect scaling); if even
that fails, a measurement cannot rescue it.

## Why a 5×5 or 6-cell demo cannot answer this

The reliability arithmetic in `reliability.py` shows that at a 0.01% per-cell
error rate, a 6400-cell map is correct only 52.7% of the time. A six-cell coupon
has a 99.94% chance of being perfect even at that failing rate. **The coupon that
demonstrates one clean reset proves almost nothing about the board.** The rig
therefore must report counted disturbances and cycle drift, not a single
"it worked" video.

## What to hand to the CTO

The protocol above is buildable as-is. The CTO (or a human operator) needs to:

1. Approve the print set and PLA/0.4 mm baseline for the rig parts and the first
   survivor fixture (S5/Test09 Stage A is the most specified).
2. Approve purchase of the two dial indicators, force gauge and calibrated
   masses (test equipment; excluded from the product BOM).
3. Run J2-0 before any survivor, then J2-1..J2-4 per survivor.

No agent can perform the physical measurement in this environment. The
deliverable from this agent is the protocol, the register and the coupon CAD;
the physical run is a human/external step owned by the CTO.
