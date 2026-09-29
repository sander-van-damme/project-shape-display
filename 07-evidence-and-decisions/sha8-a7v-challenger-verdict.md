# SHA-8 challenger verdict — A7-V verified camshaft: REJECT on cost ceiling

> Status: REJECTED (challenger). A1 remains the reliability-first candidate.
> Evidence class: CALCULATION over sourced-class BOM + DND-111 rate + CAD
> priors. No print, purchase or measurement (DND-27). Ranges with stated
> confidence; residual uncertainty explicit.

## Chosen challenger

**A7-V — shared-camshaft bank (A7, $158 / 1 actuator / 13.05 s) + A1-class
cell-resolving reader + retry.** The single most promising challenger because
it has the largest cost headroom vs A1 ($181): $23. All other screen bases
leave less (A4 $10, A6 $2, A3/A5/A2 negative) and S1-B/S2/S3/S4 carry prior
kills (mask-write ≥500 channels, surprise media, 1.27 mm land, 64×$6 clutch).

## Kill criteria (up front)

K1 cost (beat $181) · K2 zero-silent (cell-resolving read, ≥2× contrast) ·
K3 timing (<30 s incl. verify) · K4 density (80 lobes/shaft, ≤0.1 mm).

## Quantitative screen (binding gate = K1 cost ceiling)

| Quantity | Value | Basis / confidence |
|---|---|---|
| A1 purchased | $181.0 | sourced-class BOM (medium) |
| A7 base purchased | $158.0 | sourced-class sketch (medium-low; sketch, not line BOM) |
| Headroom | **$23.0** | calc (high confidence on arithmetic, medium on inputs) |
| Reader head add | +$12 | A1 sourced-class line (medium) |
| Scan motion add | +$38–49 | stepper $14 + rail $16–22 + belt $8 + switches/loom share (medium) |
| **A7-V total** | **$208–219** | calc → **$27–38 OVER A1** |
| Reuse-credit floor (share reset rail, still need belt/switches/loom ~$20) | ~$190 | optimistic low → still **+$9 over A1** |
| Hostile +35% soft lines | gap +$19.0 | convention from DND-104 A7 audit (kills robustly) |

Cheapest rejecting analysis is this ceiling math — no CAD needed. K1 KILLS
A7-V: adding the very reader that earns "zero silent errors" reintroduces the
gantry/scan cost A7 was avoiding.

Timing (K3): A7-V with 8-head verify = 13.05 + 5.864 ≈ **18.9 s PASS**; with a
single scan row = 13.05 + 6400/164.5 ≈ **52 s FAIL**. So timing passes only in
the 8-head configuration whose cost is counted above — no escape.

Silent structure (K2): full scan → silent 0 (same structure as A1, reusing the
DND-114/115 common-height target); bank-coarse readback → 6,392 silent (A5
pattern) → fails the SHA-8 "zero silent" constraint. The affordable variant
fails K2; the compliant variant fails K1.

Density (K4, secondary): 80 lobes on a 406.4 mm shaft = ≥2 printed segments;
≤0.1 mm lobe repeatability against joint backlash + PLA torsion is unproven
and a second independent kill risk. Not pursued once K1 kills.

## Comparison vs A1

| Dimension | A1 (reliability-first) | A7-V (challenger) |
|---|---|---|
| Purchased cost | **$181** / $210 delivered | $208–219 (~$190 floor) — LOSES |
| Silent-error structure | 0 silent; cell-local re-drive | 0 silent only with full scan; retry is bank-global re-home (800 cells, lift carries minis) — EQUAL on count, WORSE on blast radius |
| Full-map timing | 18.28 s incl. verify | ~18.9 s (8-head) — EQUAL; 52 s single-row — LOSES |
| Regional update | cell-granular, no reset | bank-only (800 cells), needs bank reset — LOSES |
| Unresolved risks | latch snap force, gantry registration, hinge wear (coupon/measurement) | all of A1's reader risks PLUS cam-joint backlash/torsion, shaft-segment wear, bank-retry disturbance — MORE |

## Decision

**REJECT A7-V.** Evidence that killed it: K1 cost-ceiling math ($23 headroom <
$12 reader + $38–49 scan; even the $20 reuse floor totals ~$190 > $181, hostile gap +$19). Recorded as engineering knowledge: broadcast-write families
cannot buy cell-resolving verification for less than the gantry they delete.

## Next cheapest test (if ever revisited)

Only if a scan-motion design under ~$10 total (e.g. reader riding the
existing reset carriage with zero added rail/belt/loom — currently uncosted
and unproven) is drawn and costed: then re-run K1, then a 1×5 cam-lobe
repeatability coupon (K4) at true pitch. No CAD/BOM work is justified before
that. Owner: Mechanism Explorer. No follow-up issue created — the family is
parked, not queued.

## Reproduce

```bash
python 06-experiments/test15_a7v_challenger_screen/screen_a7v.py
python 08-integrated-designs/a1-reliability-first/analysis/reliability_mask.py convergence | head -40
```
