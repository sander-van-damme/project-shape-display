<!-- © 2024 Sander Van Damme - All Rights Reserved. -->

# SHA-9 A1 GATE execution — analytic residuals (R5–R6) + regional evidence

> **Evidence class.** Everything here is **CALCULATION over sourced limits
> plus CAD**, executed by
> `08-integrated-designs/a1-reliability-first/analysis/a1_regional_update.py`
> (`--gate`: 13/13). **No print, no purchase, no measurement**
> ([DND-27](/DND/issues/DND-27)). Nothing here is physical validation.
> S5-R and S6-LC are untouched.

SHA-7 ([`sha7-a1-promotion-decision.md`](sha7-a1-promotion-decision.md))
returned **GATE**: promote the architecture, gate the build on coupon A,
with residuals R1–R6. R1–R4 are measurement-only and stay open. This note
attacks the two analytic residuals (R5–R6) and adds the A1 regional-update
evidence SHA-9 criterion 3 requires.

## 1. R5 — 4-head boundary → RETIRED as an 8-head-minimum design rule

R5 stated: the 4-head configuration sits on the 30 s boundary, so head
count is load-bearing. Attack: re-derive the head sweep in **both**
actuation corners from the bounded rate (`a1_writer_rate.py`).

| Heads | Snap (primary) full cycle | Pessimistic full-sweep | Clears 30 s? |
|---:|---:|---:|---|
| 4 | 30.006 s (bare) / **31.35 s** (sustained + retry) | 42.678 s | **NO / NO** |
| **8 (adopted)** | 18.278 s (bare) / **19.63 s** (sustained + retry) | **24.61 s** | **YES / YES** |

- Minimum heads to clear 30 s is **8 in both corners** (gated asserts).
- 8-head sustained margin is **10.37 s** (gated asserts > 10 s).
- 4-head sustained **fails** (31.35 s), confirming the count is
  load-bearing — and the adopted build carries twice the failing count.

**Verdict: R5 is retired analytically.** It was never a measurement
question; it is now a stated design rule — **no A1 build with fewer than
8 heads** — enforced by the gate, not by prose. No coupon can reopen it
unless the bounded rate itself is revised.

## 2. R6 — regional disturbance → PARTIALLY retired (geometry yes, elastic no)

R6 stated: regional disturbance 0.00 mm is modelled while the Q5 0.10 mm
limit is still a proposal. Attack in two halves:

**Half (a) — rigid-body / geometry: retired.** A1 has no shared platen:
the writer addresses only changed cells, so the modelled rigid-body
neighbour displacement is **0.00 mm** against the Q5 proposal of
**0.10 mm**. Every geometric clearance that could convert a write into
neighbour contact is positive (placed CAD):

| Clearance | Value | Margin |
|---|---|---:|
| Writer excursion (0.65 mm) vs owned half-lane (0.74 mm) | inside lane | +0.09 mm |
| Swept shutter flap vs neighbour body (DND-115) | clears | +0.280 mm |
| Read spot half-width vs neighbour body (DND-115) | clears | +0.353 mm |
| Regional update needs full-board reset? | **no** (cell granularity) | — |

**Half (b) — elastic / loaded: unattackable analytically, stays open.**
What calculation cannot supply: loaded-neighbour elastic motion under
tabletop load (3.27 N service + miniature mass) while an adjacent tile
toggles, miniature tip-over on a 20×20 boundary sweep, and hinge-wear
drift across cycles. These need **coupon B** (5×5 cycling rig with a
loaded untouched neighbour + miniature). DND-27 forbids it; no further
analysis retires it.

**Verdict: R6 is half-retired.** The geometry half is gated analytic
evidence; the elastic half is recorded as coupon-B measurement with the
missing piece stated below (§4), not hidden.

## 3. Regional-update evidence (criterion 3): tile-local reveal

Time model: `slew (0.20 s) + n·write/head + n·verify/head + retry(n) +
settle share (0.10 s)`, per-cell times from the bounded rate, engaged
heads = min(8, tile columns), retry = SHA-7 1 % budget. No reset term:
binary-latch regional updates toggle only differing cells.

| Reveal | Changed cells | Heads engaged | Time |
|---|---|---:|---:|
| Single cell | 1 | 1 | **0.31 s** |
| 5×5 tile | 25 | 5 | **0.37 s** |
| 10×10 tile | 100 | 8 | **0.47 s** |
| 20×20 tile | 400 | 8 | **0.99 s** |
| Full row (80) | 80 | 8 | **0.44 s** |

Disturbance for every row above: modelled rigid-body neighbour motion
**0.00 mm** vs the Q5 proposal **0.10 mm** — PASS on the modelled half,
with the elastic half open per §2(b).

## 4. Missing piece (stated, not hidden)

Coupon B must measure, on a 5×5 full-pitch array with a loaded untouched
neighbour tile and a representative miniature: peak vertical/lateral
neighbour motion across a 20×20-boundary-equivalent sweep, residual height
error, and miniature tip-over — against the 0.10 mm proposal. Until then,
A1's regional-update claim is **geometry + timing evidence only**, and the
build stays MEASUREMENT-GATED.

## 5. Reproduce

```bash
python 08-integrated-designs/a1-reliability-first/analysis/a1_regional_update.py --gate
```
