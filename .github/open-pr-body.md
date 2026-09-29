# DND-111: analytic bound on the A1 writer/reader rate + single-cell read

## What changed

Replaces the DND-104 **unconstrained placeholder** in
`10-reliability-mask/analysis/reliability_mask.py`:

```python
HEAD_RATE_CELLS_S = 1000.0   # 1 ms/cell per head
```

with a first-principles derivation from **sourced component-class kinematics +
the placed A1 CAD** (the [DND-54] pattern: when the only residual is a printed
coupon that [DND-27] forbids, replace it with an analytic + CAD model).

- `10-reliability-mask/analysis/a1_writer_rate.py` **(new)** — the derivation,
  the outcome, and a JSON CLI.
- `10-reliability-mask/scad/a1_reader_head.scad` **(new)** — reader-head optical
  geometry with single-cell read-resolution self-checks.
- `10-reliability-mask/analysis/render_a1_cad.py` — also render + mesh-validate
  the reader head and assert the spot fits the column top face.
- `10-reliability-mask/analysis/reliability_mask.py` — `HEAD_RATE_CELLS_S` now
  derived; A1 timing stages 8.8/8.8 → 4.864/4.864; full cycle 24.15 s → 16.278 s;
  decisive falsifier re-stated as the registration tolerance.
- `10-reliability-mask/analysis/reliability_mask_checks.py` — 10 new DND-111
  checks (50/50 total).
- `10-reliability-mask/README.md`, `07-evidence-and-decisions/README.md`,
  new ADR `07-evidence-and-decisions/dnd111-writer-rate-bound.md`,
  `07-evidence-and-decisions/dnd104-reliability-mask.md` (supersede note).
- `.github/workflows/ci.yml` — DND-111 step.
- `08-current-design/` and `09-low-cost-variant/` **untouched**.

## Engineering question addressed

Is A1's decisive number — the writer/reader rate — credible, or is it a bare
assumption? And can a single wrong cell among 6,400 be resolved? Decide both
**analytically**, with no print or measurement ([DND-27]).

## Evidence (CALCULATION over sourced limits + CAD)

**The rate is traverse/actuation-bounded, ~164 cells/s/head.**

| Kinematics | cells/s/head | Note |
|---|---:|---|
| Stop-and-go @ 20 m/s² (sourced X1C accel) | 30 | **excluded** |
| Stop-and-go @ 100 m/s² | 90 | **excluded** |
| Fly-over 1.0 m/s + snap-trigger toggle | **164.5** | **primary** |
| Fly-over 1.5 m/s + snap-trigger | 228 | optimistic |
| Fly-over 1.0 m/s + full-sweep toggle | 71.4 | pessimistic |

The placeholder **overstated the rate by 4.4–14×**. Stop-and-go is excluded at
5.08 mm pitch: a 1,000 cells/s step rate needs ~5.08 m/s (a 20T GT2 pulley at
~7,620 rpm).

**The full cycle still clears < 30 s including verification.**

| Stage | s |
|---|---:|
| digital map | 0.05 |
| mask generation | 0.00 (no mask) |
| mask transport | 2.00 |
| reset | 3.00 |
| write | 4.864 |
| settle | 1.50 |
| verify | 4.864 |
| **total** | **16.278** |

Head sweep @ 1.0 m/s (write + verify + reset + settle): 4 heads → 26.0 s;
8 heads → 16.28 s. Pessimistic full-sweep toggle: 8 heads → 22.61 s. Heads are
cheap printed bodies, so the honest rate is bought back with parallelism.

**Single-cell read resolution** is photometrically trivial (SNR ~1,460 at 50 µs,
gate 5) but geometrically a **±0.264 mm head-to-cell registration tolerance**
(2 mm aperture, 2 mm gap → 3.072 mm spot on a 3.60 mm top face; worst-case corner
reach 2.172 mm). CAD: `scad/a1_reader_head.scad`, `cad/stl/reader_head.stl`.

## Outcome recorded

**Outcome (a) BOUNDED.** The decisive number is now a bounded calculation, not an
unconstrained placeholder. The decisive residual narrows to **as-built gantry
registration (±0.26 mm over 406 mm)**, which is a position-repeatability coupon
question under DND-27, **not the rate question**. The next CEO terminal call for
the reader/retry architecture is SUCCESS-eligible on the rate axis.

## Assumptions / uncertainty

- Reflectance pair (0.80/0.15), aperture, LED power and ambient are
  assumption/sourced-class, not measured.
- Sourced component-class limits (X1C 0.5 m/s, NEMA17-class speed) are
  representative of the class, not a selected part.
- Latch snap-trigger pulse (3 ms) is device-class; the full-sweep (13 ms) is the
  conservative bound and the design clears even that.
- As-built registration and as-printed snap force remain unmeasured (DND-27).
- **Nothing here is physical validation.**

## Most informative next test

An independent adversarial audit (Falsifier) of the new decisive number, then an
as-built gantry position-repeatability measurement (blocked by DND-27) that
bounds the ±0.26 mm registration the single-cell read needs.

## Reproduce

```bash
python 10-reliability-mask/analysis/a1_writer_rate.py
python 10-reliability-mask/analysis/reliability_mask_checks.py   # 50/50
export PATH="$HOME/.local/bin:$PATH"
python 10-reliability-mask/analysis/render_a1_cad.py
python 07-evidence-and-decisions/falsifier_dnd104_checks.py \
    --model 10-reliability-mask/analysis/audit_view_a1.py
```
