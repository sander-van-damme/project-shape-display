# DND-124: close DND-121 as superseded; disclose the shutter crosstalk modelling-convention residual

## Context

[DND-124](/DND/issues/DND-124) closes [DND-121](/DND/issues/DND-121) as **superseded by
[DND-119](/DND/issues/DND-119)** (independently verified by the [DND-122](/DND/issues/DND-122)
audit). Reconciling the closure surfaced one honesty item declared landed but not on `main`:
the crosstalk **modelling-convention residual**.

The earlier DND-124 branch was built on pre-DND-123 `9b406f3` and, if merged as-is, would have
**reverted the DND-123 crosstalk fix** (re-landed `6.37×`, deleted the DND-123 entry). This PR is
**rebased onto `main` (`8fa3b92`)** and carries only the ADR caveat + register note. The DND-123
fix is preserved.

## What changed (ADR prose + register only; **no geometry, no code, no gated-numeric change**)

- `07-evidence-and-decisions/dnd115-a1-state-encoding-shutter.md` §3a — adds a **residual
  modelling-convention caveat**. The neighbour crosstalk term `rho·A_nb/g_nb²` is area-scaled,
  while the vane signal `rho·A_vane/g_vane²` is area-scaled against a chosen vane area reference.
  Using the **full vane face** (`0.704 mm²`, main's own `vane_region`) gives **4.6% / 5.95×**
  (shipped); clipping the vane to the read spot (`0.608 mm²`) gives **5.35% / 5.75×`; scaling by
  the **whole read spot** (`1.550 mm²`, 3.2× the 0.44 mm vane width) gives `2.10% / 6.78×`, which
  is not physical (the vane and neighbour patches do not both fill the spot).
- `07-evidence-and-decisions/README.md` — new **DND-124** register entry recording the same, plus
  the blocker correction (stale branch reverted DND-123; rebased).

## Engineering question

Is the DND-123 area-consistent crosstalk figure (`4.6% / 5.95×`) sensitive to the choice of vane
area reference — and if so, does any defensible convention threaten the 2× gate?

## Findings

- The ratio is **mildly convention-dependent** (≈4.6–5.4% / **5.6–6.0×** across defensible vane
  references), but **every** defensible convention leaves the on/off ratio far above the 2× gate.
  No gate outcome or design decision changes. The shipped full-vane-face convention is retained.
- The `whole-spot` variant (`2.1% / 6.78×`) is **not physical**: `A_spot` cancels only if both
  patches fill the spot, which they do not (the spot is 3.2× the vane width).

## Evidence produced (CALCULATION + CAD only, [DND-27](/DND/issues/DND-27))

| Vane area in the denominator | neighbour/vane | gated on/off | note |
|---|---:|---:|---|
| full vane face `0.704 mm²` (**shipped**) | 4.6% | **5.95×** | main's own `vane_region`; defensible |
| vane clipped to the read spot `0.608 mm²` | 5.35% | 5.75× | most physical |
| whole read spot `1.550 mm²` | 2.10% | 6.78× | **wrong** (spot 3.2× the 0.44 mm vane width) |

## Gates run on the rebased branch (all green)

- `falsifier_dnd115_a1_shutter_audit.py --gate` → **CLEAN 14/14** (A13 `MATCH`: ADR 4.6% / 5.95×)
- `falsifier_dnd115_checks.py --gate` → CLEAN 12/12
- `falsifier_dnd114_checks.py --gate` → 7/7; `falsifier_dnd112_checks.py --gate` → 11/11
- `reliability_mask_checks.py` → 78/78; `a1_writer_rate.py` exit 0

## Assumptions / residual uncertainty

- CALCULATION + CAD only. No print, no purchase, no measurement (DND-27). No board contact (DND-32).
- The residual is **presentational**: it changes no gate outcome. Assumption-class optical constants
  remain unmeasured (DND-27).

## Most informative next test

None required on this axis. The DND-115 read axis is closed at CAD + calculation; the live main
tree is CLEAN 14/14. Physical single-cell A1 coupon measurement is not an available evidence class
(DND-27).
