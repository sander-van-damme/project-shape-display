<!-- © 2024 Sander Van Damme - All Rights Reserved. -->

# SHA-27 A1 vs S6-LC convergence decision + measurement gate

> **Evidence class: CALCULATION + CAD only** (DND-27). This note prints,
> purchases, and measures nothing. Nothing here is physical validation.
> S5-R, A1, and S6-LC packages are untouched (additive note only).
> Inputs: SHA-22 A1 update-time PASS, SHA-23 cost audit, SHA-14 hardening,
> SHA-13 coupon readiness. No new divergent seeds (SHA-25 pause stands).

## 1. Decision

**A1 is the exploitation baseline-to-beat** (architecture PROMOTED, build
MEASUREMENT-GATED on coupon A — [SHA-7](sha7-a1-promotion-decision.md)).
**S6-LC stays alive on a single narrow gate: G8 per-cell reliability via
printed coupon C1, plus closing the $13.05 delivered-cost overrun.** All
other lanes are parked, rejected, or paused (§4).

Why A1, on the joint cost/quality mandate ([SHA-11](/SHA/issues/SHA-11)):

- **Cheapest measured-convention cost:** $181 purchased (IDEAL) / $209.96
  delivered; hostile+fallback $218.40 (ACCEPTABLE), $281.60 under the $500
  ceiling ([SHA-14](sha14-a1-hardening.md) §3, gate 13/13 re-verified this
  heartbeat).
- **Only zero-silent architecture:** reader verifies every cell; every other
  lane carries ~6,400 silent cells (A1 README §3–5).
- **Timing clears with margin:** 18.278 s bare / **19.63 s sustained +
  retry** (SHA-22 PASS), 10.37 s margin; sub-second tile-local reveals
  (0.31–0.99 s, [SHA-9](sha9-a1-gate-residuals-regional.md)).
- S6-LC beats A1 on raw speed (11.96 s) and actuator count (3 vs 4) but
  loses on cost, reliability structure, and regional granularity — speed
  alone does not satisfy the joint mandate.

## 2. Comparable cost table (repository evidence; estimates marked)

| Dimension | A1 | S6-LC | S5-R (provenance) |
|---|---|---|---|
| Purchased parts | **$181.00** IDEAL (`bom_a1.csv`; SHA-14 §3) | **$226.77** G5 PASS (`bom_s6lc.csv`, DND-98 ratified) | $348.79 (model `s5r_register.py`) |
| Delivered (×1.16) | **$209.96** PASS | **$263.05** G6 FAIL (+$13.05) | $404.60 |
| Hostile + fallback | $218.40 ACCEPTABLE (SHA-14 §3) | scenarios $199.79–$300.58 parts (ratified CSV note) | band $387–$422 |
| Full-map time | 18.28 s bare / **19.63 s** sustained | **11.96 s** (off-line mask caveat) | 24.615 s |
| Regional update | cell-granular, sub-second | bank-local replay; surprise maps mask-set-bound | bank-scoped |
| Silent cells | **0** (reader + retry) | 6,400 (G8 UNRESOLVED) | 6,400, no readback |
| Bought actuators | 4 | 3 | 42 (2 bank + 40 solenoids) |
| Repeated part types | 5 (column, latch, cradle, vane, shutter) | column/rack, pawl, mask strip, release comb | 14-part set, 25,661 pcs |
| Printed mass | ~2.4 g/cell → **~15 kg ESTIMATE** (SHA-14 §2; method: solid-equiv bbox × PLA 1.24 × 0.40 infill; **±50–60 %**, slicer/infill unmeasured) | ESTIMATE-class (unbounded here; §5 T1–T2 measures it) | mesh-manifested (S5-R `print_manifest.json`, mesh-sourced) |
| Print time | **~111 single-X1C days ESTIMATE** (SHA-14 §2; 25 min/cell-set order class; **±50–60 %**) | ESTIMATE-class (§5 measures) | manifested per-part hours (mesh + rate model) |
| Assembly | ~25.6k placements (4 ops/cell) + 4 subassemblies; L1–L3 elimination levers (SHA-14 §2) | banked combs + mask setting (off-line labour uncosted) | manifests + route in `fabrication/` |
| Fabrication burden | modular 2×2 tiles + 210 mm rail segs; 4 feats at 0.44 floor; pin rule FAIL→R2 (SHA-14) | owned-lane fit PASS; pawl/release measurement-only (DND-97) | full FDM-limit PASS, slicer-ready |

**Cost-down posture (elimination-first):** A1's cheapest lever is L3
dovetails (−$10–14) + 5→3 limit switches (−$2); band already IDEAL so the
lever buys fallback headroom, not a band change. S6-LC's lever is the
delivered overrun: −$13.05 via bought-line repricing or mask-medium
simplification — costed analytically before any CAD.

## 3. What keeps S6-LC alive

Exactly two things, both gated:

1. **G8 per-cell reliability is the life-gate.** `(1−q)^6400` needs
   q ≤ 1.57e-6 for a 99 % map; S6-LC has no per-cell feedback, so every
   miss is silent. Evidence path is **printed coupon C1** (DND-91 §6:
   4×4 true-pitch block + single cell; 100 cycles/cell × 4 cells ×
   3 coupons; kill lines: zero neighbour contact, release within 2×
   model, hold ≥ design load, 100 % engage, spread sd ≤ 9 %).
   **C1 fail → S6-LC parked. C1 pass → full-machine print question opens.**
2. **Delivered-cost overrun must close.** Mission gate (purchased < $250)
   PASSES at $226.77; the repo's stricter delivered convention FAILS at
   $263.05. A1's delivered ($209.96) beats S6-LC's by $53.09 — S6-LC
   cannot win exploitation on cost without closing this.

S6-LC's retained upside if both gates clear: fastest visible map
(11.96 s), fewest actuators (3), conventional broadcast mechanism.

## 4. Kill / park / continue per lane

| Lane | Disposition | Rationale |
|---|---|---|
| **A1** | **CONTINUE — baseline-to-beat** | Gated promotion stands; exploit via coupons A/B/C (SHA-13 ready) + L1–L3 |
| **S6-LC** | **CONTINUE-GATED (C1 + cost)** | Alive only through §3 gates; any full build waits on C1 PASS |
| **S5-R** | **PARK (provenance)** | Slicer-ready package preserved untouched; superseded on cost ($404.60) + silent structure; no further spend unless A1 and S6-LC both fail |
| **A7-V** | **REJECT stands** | K1 cost kill ($208–219 vs $181); T2 camera K2 killed (SHA-10/12); contingent path only (sub-$10 scan + K2 proof) |
| **A2–A6, T1/T3–T5, M/D/E/F/G seeds** | **PARKED / PAUSED** | Prior kills stand; SHA-25 principled pause holds — resume only on stated triggers (M2/D2/E3 media, ≥10× transducer quantity, requirement/process change, SHA-24 delta) |
| **New divergent seeds** | **NONE** | SHA-25 pause stands; capacity to exploitation |

## 5. Single gated measurement plan: weigh-one-tile + coupons T1–T5

One physical session (DND-27 handoff — agent-runnable prep only) converts
the ±50–60 % printed-mass/time ESTIMATES to measured and advances both
lanes' life-gates. Print **one tile per lane** (A1: 5×5 full-pitch cell
block per SHA-13 coupon-B geometry; S6-LC: 4×4 block per DND-91 C1),
then:

| Test | Measures | Procedure / instruments | Kill / convert line |
|---|---|---|---|
| **T1 mass** | printed mass/tile → full-field kg | digital scale ±0.1 g; weigh tile as-printed (record slicer, infill, PLA lot) | replaces 0.40-infill assumption; re-scales §2 ESTIMATES to measured ±5 % |
| **T2 time** | print time/tile → full-field days | log slicer wall time + filament used for the same tile | replaces 25 min/cell-set order class with measured rate |
| **T3 assembly** | placements + fit per tile | time 4-ops/cell assembly on the tile; caliper lane/fit checks | converts 25.6k-op class to timed rate; fit FAIL → D1/D2 or pawl re-budget |
| **T4 coupon A** (A1 life-gate) | snap force + read contrast | push-pull gauge (0–20 N); 30 snaps ≥3 prints; 30 reads/state at fixed standoff | PASS iff mean ≤ 7.14 N, no snap > 10 N, on/off ≥ 2× (ideal + crosstalk-corr.); else writer/shutter redesign |
| **T5 coupon C1** (S6-LC life-gate) | engage reliability + force spread | 100 cycles/cell × 4 cells; gauge release/hold; spread sd | PASS per DND-91 §6 lines (100 % engage, sd ≤ 9 %, hold ≥ load); else S6-LC parked |

**Order is cheapest-first:** T1–T3 ride free on the same prints as T4/T5
(no extra machine time). T4 and T5 run in parallel on their own tiles.
**Next action (CTO/board handoff):** print the two tiles on an X1C-class
machine (PLA, 0.4 mm nozzle, 0.2 mm layers) and execute T1–T5; agents
cannot execute under DND-27. No CAD/BOM edits are authorised before
results land.

## 6. Reproduce / verify (this heartbeat)

```bash
python 08-integrated-designs/a1-reliability-first/analysis/a1_hardening.py --gate  # 13/13
python 08-integrated-designs/s6lc-low-cost/analysis/s6lc_checks.py                  # 48/48
python 08-integrated-designs/a1-reliability-first/analysis/a1_regional_update.py --gate  # 13/13
python 08-integrated-designs/a1-reliability-first/analysis/a1_coupon_readiness.py --gate # 32/32
git status --short  # S5-R / A1 / S6-LC packages untouched; this note additive only
```
