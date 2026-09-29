# DND-59 — S5-R residual retirement: the last agent-reachable residuals

## What changed

Retires/bounds the five **agent-reachable** S5-R residuals left by
[DND-57](/DND/issues/DND-57), on the evidence classes [DND-27](/DND/issues/DND-27)
allows only: **CAD + CALCULATION + sourced listings; no print, no purchase, no
measurement**.

- **`06-experiments/test12_winner_convergence/s5r_residuals.py`** (new) + **`s5r_residuals_checks.py`**
  (new, 12 gates) — the residual-retirement model.
- **`s5r_register.py` / `s5r_register.scad` / `s5r_register_checks.py`** — keeper
  re-profile (0.45 → 0.90 mm, 2 lines), keeper moved to the row (Y) axis, hard
  compression shoulder, two-axis cell-fit.
- **`s5r_bank.py` / `s5r_bank.scad` / `s5r_bank_checks.py`** — keeper modelled in
  +Y; comber tine-gap and keeper-clearance updated.
- **`tools/validate/analytic_printability.py`** — register branch is now two-axis
  and checks the keeper shoulder.
- **`07-evidence-and-decisions/dnd59-s5r-residual-retirement.md`** (new ADR);
  residual registers in the DND-54/55/58 ADRs and `08-current-design/README.md`
  updated with a **consolidated S5-R residual registry**.
- **`.github/workflows/ci.yml`** — adds the DND-59 residual + register-printability
  steps.

> Branched from `main` (DND-54 / DND-55 / DND-58 present).

## The call

After [DND-58](/DND/issues/DND-58), can every **agent-reachable** S5-R residual be
retired or usefully bounded without a print, so the CEO can make the terminal call
on [DND-57](/DND/issues/DND-57) and leave only a measurement-only residue?

## Result

| Residual | New status | Evidence |
|---|---|---|
| R-DND54-KEEPER (keeper leaf 1 line RISK) | **closed** — 0.45 → 0.90 mm (2 lines); hold moved to a hard compression shoulder (144–324×); register printability **RISK → PASS** | CAD + calc |
| R-DND54-6 (writer force unconfirmed) | **closed agent-side** — bottom-up **0.2425 N**; sourced 5 V push-solenoid **1.20 N** clears 4.95× | calc + sourced |
| R-DND54-5 (missed set = silent row error) | **bounded agent-side** — q ≤ **1.57e-6**/keeper for a 99 % map; per-group verify+retry relaxes **2–10×**, writer redundancy 2× **~798×** | calc |
| R-DND54-3 (crank 720 deg/s, settle 0.05 s) | **bounded agent-side** — break-evens **468 deg/s** / **0.084 s**; sourced NEMA17 class clears (2.15× torque) | calc + sourced |
| R-DND55-1 (bar eccentricity e) | **closed for the steel rod** — 0.0052 mm skew at extreme e (33× inside gate; break-even e ≈ 201 mm) | calc |

**Key finding:** re-profiling the keeper to 2 lines in the pitch (X) band would
consume the cell clearance (worst-case gap 0.02 mm). The keeper is therefore moved
into the **row (Y)** axis beside the pawl (X gap 0.98 mm, Y gap 0.28 mm) and its
**holding** function is decoupled from the tolerance-critical over-centre offset by
a hard printed shoulder in compression — a Monte-Carlo over the sourced print
tolerance shows the old bending-only hold fails in a meaningful fraction of builds,
the shoulder does not.

**Remaining residue (measurement-only, un-retirable under DND-27):** as-printed
pawl/keeper friction μ and gate/tip sharpness; printed-leaf creep/fatigue; as-printed
per-set reliability q; the loaded NEMA17 speed/torque curve.

## Verification

- `python s5r_register.py` / `s5r_register_checks.py` — **20 OK**
- `python s5r_bank.py` / `s5r_bank_checks.py` / `s5r_bank.py --cad` — **17 OK**; 6
  positives render, **5/5 interference queries empty**
- `python s5r_residuals.py` / `s5r_residuals_checks.py` — **12 OK**
- `tools/validate/analytic_printability.py s5r_register.scad` — **PASS** (was RISK)
- `tools/validate/validate_geometry.py --require-openscad` — **HARNESS OK**
- Full test08–test13 engineering checks green.

## Assumptions / uncertainty

Sourced printed-PLA compression yield (20–45 MPa) and modulus (1500 MPa); the
actuator class figures are sourced-class allowances, **sample-confirmed only at
purchase** (forbidden now). No physical validation is claimed.
