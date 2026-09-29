<!-- © 2024 Sander Van Damme - All Rights Reserved. -->

# SHA-22 A1 local-update and board-update time characterization

> **Evidence class.** Everything here is **CALCULATION over sourced limits
> plus CAD**, executed by
> `08-integrated-designs/a1-reliability-first/analysis/a1_update_times.py`
> (`--gate`: 13/13), which reuses the SHA-7 timing decomposition
> (`a1_promotion_timing.py`, 7/7) and the SHA-9 regional model
> (`a1_regional_update.py`, 13/13) without re-deriving them. **No print, no
> purchase, no measurement** ([DND-27](/DND/issues/DND-27)). Nothing here is
> physical validation. S5-R and S6-LC are untouched.

SHA-7 promoted A1 measurement-gated with a worst-case full-board number
(19.63 s sustained) but no numeric local-update time was fixed yet
(02-design-criteria sets no stricter local target than "below 30 s and
ideally scaling with region size"). This note fixes both numbers, checks
their sensitivity, and writes the coupon test plan that must confirm them.

## 1. Full-board update-time model vs the 30 s requirement — PASS

Authoritative worst case is the SHA-7 decomposition (8 heads, 1.0 m/s,
snap-trigger actuation, 1 % miss): **19.6252 s sustained, margin
10.3748 s — PASS**. Visible transition equals sustained (mask generation
0.00 s, no hidden prep). The fraction-scaled model below is a conservative
upper bound (write pass scaled by changed fraction f; FULL verify pass and
full per-line ramp always charged; retry scaled with f·6400). At f = 1.0 it
reproduces the SHA-7 number exactly (gated assert).

| Changed fraction | Changed cells | Total (s) | Margin (s) | Clears 30 s? |
|---|---|---:|---:|---|
| 1.00 (worst case) | 6,400 | **19.6252** | 10.3748 | **YES** |
| 0.50 | 3,200 | 16.0196 | 13.9804 | YES |
| 0.25 | 1,600 | 14.2168 | 15.7832 | YES |
| 0.10 | 640 | 13.1351 | 16.8649 | YES |

Scaling is monotonic (gated) and every fraction clears: the ~12.4 s fixed
floor (transport 2.0 + reset 3.0 + full verify 5.86 + settle 1.5 + map 0.05)
dominates small fractions, which is why local updates use the addressed-cell
model of §2 rather than this bound.

## 2. Small-region local-update time model and behaviour

Times reuse the SHA-9 addressed-cell model (slew 0.20 s + n·write/engaged +
n·verify/engaged + 1 % retry + 0.10 s settle; engaged = min(8, tile cols)):

| Reveal | Changed cells | Heads engaged | Time (s) |
|---|---|---:|---:|
| Single cell | 1 | 1 | **0.3124** |
| 5×5 tile | 25 | 5 | 0.3661 |
| 10×10 tile | 100 | 8 | **0.4730** |
| Room 12×12 | 144 | 8 | 0.5492 |
| Corridor 40×4 | 160 | 8 | 0.5769 |
| 20×20 tile | 400 | 8 | 0.9922 |
| Full row (80) | 80 | 8 | 0.4384 |
| **3 separated 10×10** | 300 | 8 | **1.2190** |
| **Room + corridor** | 304 | 8 | **1.0260** |

All locals clear 30 s by more than an order of magnitude and scale with
region size, as the criteria ask. Multi-region totals charge one slew per
region plus a single settle share.

**Does a small change disturb the rest of the surface?** In the rigid-body
model: **no.** Only differing cells are toggled (cell granularity); there
is no shared platen move and no full-board reset, so modelled rigid-body
neighbour displacement is **0.00 mm** against the Q5 proposal gate of
**0.10 mm**. Every write-path clearance is positive (placed CAD): writer
excursion inside owned half-lane +0.09 mm, shutter sweep vs neighbour
+0.280 mm, read spot vs neighbour +0.353 mm (gated). The elastic half —
loaded-neighbour motion under tabletop load, miniature tipping on a region
boundary, hinge-wear drift — is **not** modelled and stays open as coupon B
measurement (SHA-9 R6b, DND-27).

## 3. Sensitivity to write-path assumptions

Sustained full-board (f = 1.0, 8 heads) across gantry speed × actuation
model, plus head-count and miss-rate sweeps:

| Gantry speed | Snap-trigger (primary) | Pessimistic full-sweep |
|---|---|---|
| 0.5 m/s (X1C-sourced) | 26.7532 s (margin 3.25) | 29.0252 s (margin 0.97) |
| **1.0 m/s (credible)** | **19.6252 s (margin 10.37)** | 25.9612 s (margin 4.04) |
| 1.5 m/s (repo-prior) | 17.9158 s (margin 12.08) | 25.6065 s (margin 4.39) |

| Heads (1.0 m/s, snap) | 4 | 8 (adopted) | 12 | 16 |
|---|---|---|---|---|
| Sustained (s) | **31.3532 FAIL** | 19.6252 | 15.7160 | 13.7612 |

| Miss rate (8 heads) | 1 % nominal | 5 % stress |
|---|---|---|
| Sustained (s) | 19.6252 | 25.0140 PASS |

Reading: **the whole assumption box clears 30 s at 8 heads** (gated; worst
corner 29.03 s at slow gantry + pessimistic actuation, margin 0.97 s).
Speed helps only to ~17.9 s because the fixed floor (~12.4 s) dominates;
actuation model matters more than gantry speed above 1.0 m/s. Head count
remains load-bearing (4 heads fail at 31.35 s — the SHA-9 8-head-minimum
design rule stands). Miss rate 1→5 % costs ~5.4 s; the 500-cell retry cap
never binds below 5 % (320 expected misses at 5 %).

## 4. Coupon measurement / test plan (future physical work)

These coupons are a handoff specification, not authorisation to build
(DND-27: no print tests in this program). Coupon identity follows
[SHA-13](sha13-a1-coupon-readiness.md) (A: single cell, B: 5×5 array,
C: bank/module).

- **T1 — per-cell write time (coupon A, single cell at true pitch).**
  Measure gantry traverse per 5.08 mm pitch at the adopted speed, latch
  snap-trigger time, and hard-stop settle; confirm write_cell ≤ 6.08 ms
  (the §1 model input) with a stated spread. Kills the rate bound if the
  mean exceeds the 13 ms pessimistic corner with margin exhausted.
- **T2 — full-line traverse + reversal overhead (coupon C or a rail rig).**
  Measure per-line accel/reversal time at 1.0 m/s; confirm the 1.0 s/pass
  ramp allowance. A 2× overshoot reopens the head-count rule.
- **T3 — regional reveal time + disturbance (coupon B, 5×5, loaded
  neighbour + representative miniature).** Run 10×10-equivalent and
  20×20-boundary-equivalent reveals; measure wall time against §2
  (0.47 s / 0.99 s predictions) AND peak neighbour motion against the
  0.10 mm Q5 proposal plus miniature tip-over. This is the elastic R6b
  half that analysis cannot retire.
- **T4 — retry-loop convergence (coupon B with a deliberately stuck cell).**
  Measure first-try miss rate q against the 1 % nominal / 5 % stress
  assumptions and confirm re-drive + re-verify closes the error.
  q > 7.8 % (the 500-cell cap) reopens the retry budget.
- **T5 — multi-region independence (coupon B/C).** Reveal two separated
  regions in one cycle; confirm total ≈ sum of singles (no shared-platen
  coupling) and that the untouched gap meets the Q5 gate.

Pass criteria are the numbers in §1–§3 with their margins; any coupon that
misses by more than the stated margin reopens this note, not the
architecture silently.

## Verdict

- **Full-board: 19.6252 s sustained vs 30 s — PASS** (margin 10.37 s;
  whole sensitivity box clears at 8 heads; 4 heads fail, rule stands).
- **Local-update: numeric times fixed** — single cell 0.31 s, 10×10
  0.47 s, 20×20 0.99 s, 3 separated 10×10 1.22 s; rigid-body disturbance
  0.00 mm vs 0.10 mm proposal; elastic half stays coupon-B measurement.
- **Residual uncertainty:** gantry as-built speed/registration, latch snap
  force/spread, optical constants, hinge wear, and all elastic disturbance
  are assumption-class or measurement-only (DND-27). Nothing analytic
  remains on the timing axis — the next step is coupons T1–T5.

## Reproduce

```bash
python 08-integrated-designs/a1-reliability-first/analysis/a1_update_times.py --gate  # 13/13 (new)
python 08-integrated-designs/a1-reliability-first/analysis/a1_promotion_timing.py --gate    # 7/7 (unchanged)
python 08-integrated-designs/a1-reliability-first/analysis/a1_regional_update.py --gate     # 13/13 (unchanged)
git status --short  # S5-R (08-integrated-designs/s5r-*) and S6-LC untouched
```
