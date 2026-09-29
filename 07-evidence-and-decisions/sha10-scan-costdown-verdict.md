# SHA-10 scan/verify motion cost-down verdict — A7-V stays REJECTED (parked)

> Status: search COMPLETE. 4 full topologies + 1 screen surveyed, verdicts per
> topology below, SHA-8 K1 re-run explicit. A1 ceiling stands; sub-$10 trigger
> NOT met; A7-V does NOT reopen.
> Evidence class: CALCULATION over sourced-class prices (2026-09 web sweep,
> ranges not quotations) + DND-111 reader rate. No print, purchase or
> measurement (DND-27). Ranges with stated confidence; residual uncertainty
> explicit. Reproduce: `python 06-experiments/test16_scan_costdown/scan_costdown.py --gate` (10/10).

## Kill criteria (up front)

| ID | Gate | Kill line |
|---|---|---|
| KC1 cost | verify subsystem inside the **$23.00** headroom (A7 $158 vs A1 $181); named trigger = **sub-$10 scan motion**; A1 reader ≤ **$30.99** | nominal-over, or margin with no robustness |
| KC2 timing | verify ≤ **8 s** nominal; sustained full-map **< 30 s** | nominal verify > 10 s, or any total > 30 s |
| KC3 disturbance | non-contact, or bounded ≤ **0.10 mm** neighbour motion (Q5) | contact force can unlatch/drag a settled column |
| KC4 complexity | ≤ 2 added purchased lines, ≤ 1 added actuator (0 preferred) | new precision axis (rail+belt+motor+loom) for A7-V |

Cheapest-rejecting-analysis-first throughout: timing kills before costing where
applicable (T4), premise checks before BOMs (T1), fork kills before detail (T3).

## Survey (80×80 = 6400 cells; DND-111 rate 164.5 cells/s/head, band 71–228)

**T1 — piggyback travelling row: REJECT for A7-V.** The reuse premise fails on
inspection: A7 writes with rotary camshafts in place and HAS no linear
travelling carriage, so marginal cost collapses to a full new axis
($33–49 scan + $12 reader → A7-V ≈ $203–219 > $181; KC1 + KC4 kill). Side
result for the A1 track: A1's gantry already exists, so its marginal scan is
$0 — the $12 reader and the $30.99 ceiling stand unchallenged.

**T2 — overhead camera, zero motion: ADVANCE to analytic K2 test only.** One
ESP32-CAM-class module ($8–12; Waveshare $7.99–8, Amazon 2-pack ~$11/ea) +
illumination ($2–4) + mount/loom ($2–4) = **$11–18 nominal $14**, replacing the
$12 head. Beats the $30.99 ceiling on paper; scan motion is $0 but this is
sensing, not scan-motion, so the sub-$10 trigger is honestly NOT claimed.
Cycle ≈ 13.05 + 3.5 ≈ 16.6 s nominal (KC2 pass, kill line 10 s verify; KC3/KC4
pass). K2 zero-silent is **assumption-class**: top-down single view has ~0
geometric height cue (20 px/cell but coplanar tops); 45° oblique occludes ~8
cells behind each tall column. Next cheapest test (no CAD/BOM/procurement
before it): pinhole-occlusion calc + CAD render at 2 angles, kill line ≥2×
contrast on 100% of cells, 0 occluded. Owner: Mechanism Explorer.

**T3 — bank-parallel fixed sensing: REJECT both forks.** (a) Cell-resolving
fixed array = 6400 × $0.25–0.60+ ≈ **$1600+**, KC1 kills by ~70×. (b) Row-coarse
(8 bank sensors/chains, ~$11) leaves up to **6392 silent** cells (A5 pattern),
failing the SHA-8 zero-silent constraint. A 640-sensor partial row reads only
fixed points — full-field read without motion is geometrically impossible.

**T4 — cheap serial probe (28BYJ-class axis, $6–12): REJECT on KC2.** Single-row
serial read needs 6400/164.5 = **38.9 s alone** (band 28–90 s); A7-V cycle
≈ 54 s nominal, never clearing 30 s at any band corner. Proves there is no
cheap serial escape; cost is irrelevant once timing kills.

**T5 — ToF zone array (screen): REJECT on KC1.** 8×8-zone VL53-class modules
($8–15) cover one 8×8-cell patch each → 100 modules → **$800–1500**.

## SHA-8 K1 re-run (explicit, per acceptance criterion 3)

K1: "A7-V beats A1 ($181)". Cheapest paper verify (T2, $11–18) → A7-V
$170–178, nominal $174 → **nominal PASS by $7** (paper only). Hostile
convention (SHA-8): gap −$17.3 (passes arithmetically). **A7-V does NOT
reopen**: K1 pass is necessary but not sufficient — K2 camera proof is
assumption-class, K4 camshaft density risk (80 lobes/shaft, ≤0.1 mm) still
open, the A7 $158 base is sketch-class with a paper-thin $3–11 margin, and the
literal sub-$10 scan-motion trigger is unmet. Contingent path only: T2 passes
its analytic K2 test AND a line-BOM reprices A7 with margin. No follow-up
issue created — the family stays parked, not queued.

## Comparison (ranges; confidence in parentheses)

| Dimension | A1 (record) | Best challenger (A7-V + T2 camera, paper) |
|---|---|---|
| Verify subsystem | $12 reader, marginal scan $0 (high) | $11–18 camera (medium-low; K2 unproven) |
| Full purchased | **$181** IDEAL (medium) | $170–178 nominal (low-medium; sketch base) |
| Verify timing | 5.864 s proven-rate calc | ~2–5 s analytic allowance (assumption) |
| Silent structure | 0 silent, cell-local re-drive (calc) | 0 silent CLAIMED, proof pending |
| Regional update | cell-granular | bank-global re-home (SHA-8; unchanged) |
| Unresolved risks | R1–R6 coupon-gated (SHA-7) | all of A1's reader risks + occlusion/contrast + cam-joint/torsion + sketch BOM |

## Residual uncertainty

Sourced-class prices are point-in-time equivalents, not quotations; A7 base
confidence is medium-low (sketch, not line BOM); T2 timing/decode and contrast
are assumption-class pending the analytic K2 test. Nothing here is physical
validation. S5-R, A1, S6-LC packages untouched.
