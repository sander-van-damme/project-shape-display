# DND-56: Independently ratify the DND-54 S5-R delivered BOM ($397.53)

Advances [DND-56](/DND/issues/DND-56), for [DND-54](/DND/issues/DND-54). The S5-R pivot was
promoted on a **$397.53 delivered** figure computed from point-in-time actuator-class
*allowances* ($12/motor, $2.50/writer) plus the no-channel E1–E6 base ($218.70) — the same
class of untraced price that produced the S5 incumbent's K7 cost cliff. This PR re-derives the
BOM from first principles and traces the two allowances to orderable listings.

**Evidence class: CALCULATION over sourced listings and stated assumptions. No purchase, print
or physical measurement** ([DND-27](/DND/issues/DND-27)).

## What changed

- `06-experiments/test12_winner_convergence/s5r_bom_ratify.py` — the independent ratification.
  Does **not** import `s5r_register.bom()` for its own arithmetic; re-enters the E1–E6 fixed-line
  prices by hand, re-derives the BOM, and `--selftest` reconciles against the committed
  `cost_closure.py` (and `s5r_register.py` when present).
- `s5r_bom_ratify_checks.py` — 11 regression + honesty gates (no-channel identity, claim
  reproduction, additive uplift, sourced labelling, channel pricing, scenarios, break-evens).
- `s5r_bom_ratified.csv` — the working-scenario purchased BOM, one labelled row per line.
- `07-evidence-and-decisions/dnd54-s5r-bom-ratification.md` — the ratified note.
- `06-experiments/test12_winner_convergence/README.md` — run section.
- `.github/workflows/ci.yml` — runs the new module + checks in the stdlib-only job.

- `06-experiments/test12_winner_convergence/s5r_register.py` — mechanism definition +
  static/kinematic model (cell fit, neighbour cross-talk, writer force, bank drive
  force, service-load inheritance, endurance, timing, BOM, sensitivity, verdict).
- `s5r_register_checks.py` — 15 regression + honesty gates (CI).
- `s5r_register.scad` — CAD unit cell (housing, rotor, printed pawl, over-centre
  keeper, toothed drive bar).
- `07-evidence-and-decisions/dnd54-s5r-register-latch.md` — the ADR.
- `08-current-design/README.md` and the DND-52 ADR updated to promote S5-R.
- `tools/validate/analytic_printability.py` gains a register-cell branch;
  `validate_geometry.py` and `render_winner_cad.py` render the register cell;
  `.github/workflows/ci.yml` runs the model checks, the printability table and the CAD
  render.

| Question | Result |
|---|---|
| Does $342.70 parts / **$397.53 delivered** reproduce? | **YES, exactly**; margin $102.47 |
| No-channel base + driver identity? | **$218.70 + $63.64 = $282.34** — holds, **no double-count** |
| Uplift convention? | additive **×1.16** (DND-41), not the DND-37 ×1.166 |
| Are the $12 / $2.50 prices traced? | **Allowances**, sourced to **$12.39 / $2.20** (±$0.40) |

**One material finding:** the S5-R `bom()` prices the **actuator block's own channels at zero**.
The 80-channel TB6612 block leaves *with* the 80 motors, but the 2 bank motors and 40 writer
solenoids still need channels: 2 bank H-bridge ICs + 5 ULN2803-class writer switches = **$3.09
parts**.

| Scenario | Delivered | vs $500 | vs <$400 |
|---|---:|---:|---:|
| Optimistic (sourced units, 1 bank IC) | **$387.18** | −$112.82 | **−$12.82** |
| Working (allowances + channels) | **$401.12** | −$98.88 | **+$1.12** |
| High (premium NEMA17 + premium writer) | **$421.51** | −$78.49 | +$21.51 |
| DND-54 claim (channels unpriced) | $397.53 | −$102.47 | −$2.47 |

**Break-even for the $500 ceiling (working channel cost):** bank motor **$54.62/ea**, writer
solenoid **$4.63/ea** — 4.5× and 1.85× the allowances. **No line dies on cost.**

DND-52's option-1 timing replaced the whole 80-column step time with a token
"20 stations × 0.3 s" and did not model a per-row cycle. Counted honestly, a
**single-row** bank (R=1) needs 80 groups and is **≥36 s even at an aggressive
3 rev/s crank**. The real lever is that the bank bar can span **R rows in depth at
no pitch penalty** (row pitch is independent of the in-row column pitch), so one
bank pass writes R rows at once.

**RATIFIED WITH ONE MATERIAL FINDING.** The claim is correct and reproducible; the S5-R BOM is
**not** double-counting the driver block; the two actuator allowances are credible against
sourced listings. The honest end-to-end working total is **$401.12 delivered** — solidly under
the $500 ceiling, but **$1.12 outside the ideal <$400 band**, so the DND-54 "inside the ideal
band" phrasing should read "optimistic scenario; ~$1 over in the working scenario." Remaining
cost residual is the writer solenoid's **force** (not published by any listing) and the absence
of a 2-piece contract quote — both measurement/procurement-gated under
[DND-27](/DND/issues/DND-27). No board contact ([DND-32](/DND/issues/DND-32)).
