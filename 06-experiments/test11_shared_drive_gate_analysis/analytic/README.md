# T11-A analytic gate package (DND-28)

**This directory replaces the physical T11-A print/measure gate of
[DND-21](/DND/issues/DND-21) with analytic + simulation evidence.** No physical
print tests are performed (board policy [DND-27](/DND/issues/DND-27)).

## What is here

| File | Type | Purpose |
|---|---|---|
| `t11a_analytic_gate.py` | calculation + simulation | Sourced-FDM printability screen, worst-case + Monte Carlo tolerance stack-up, analytic run-record emitter |
| `runs/t11a_analytic_measurements.csv` | **analytic run record** | Two rows (0.4 mm / 0.2 mm) in the exact `t11a_fit_check.py` schema, with `evidence=CALCULATION` |

## How it is consumed

The existing CI-tested gate engine reads the analytic record directly:

```bash
python ../t11a_fit_check.py --validate
python ../t11a_fit_check.py --input runs/t11a_analytic_measurements.csv
python t11a_analytic_gate.py --report      # full analysis
python t11a_analytic_gate.py --selftest    # asserts the analysis is sane
python t11a_analytic_gate.py --emit-record # regenerate the record
```

The engine refuses to silently call a row `MEASURED`: it reads the `evidence`
column and prefixes the disposition action with `[ANALYTIC SCREEN, NOT A PRINT]`
when the input is not a measurement.

## What the analysis found

- **Sourced FDM limits** (labelled `sourced fact` vs `assumption` in the code):
  min vertical wall ~1.05x nozzle (0.42 mm at 0.4 mm; 0.21 mm at 0.2 mm), min
  slot/through-feature ~1x nozzle (0.40 mm / 0.20 mm), plus assumed free-gap and
  pivot-definition floors.
- **Designed values vs limits:** web 0.47 mm, notch 0.55 mm, lateral clearance
  3.48 mm, pivot definition 0.80 mm — all clear the sourced floors.
- **Worst-case tolerance stack-up:** min web margin **+0.11 mm** (thin but
  positive); lateral clearance **+3.09 mm**; bbox **+4.96 mm**. Land reach
  worst case is **−0.05 mm** (the ±0.20 mm land window is itself the bound).
- **Monte Carlo (200k, sigma = half_range/√3):** min-web pass fraction 1.0000,
  lateral 1.0000, land reach 0.9077.
- **Pivot free play (M3) is NOT resolved analytically.** The coupon prints its
  pivot in place with **no designed radial clearance**, so whether it frees is a
  slicer/print-bias question. The analytic record deliberately leaves `M3_pivot`
  blank so the engine returns `INCONCLUSIVE` rather than a false pass or kill.
- **Disposition from the engine:** `INCONCLUSIVE_RUN_A4` with an explicit
  analytic-evidence warning. The decision tree cannot reach
  `S3_DENSITY_PRINTABLE` without an M3 answer.

## Residual uncertainty (vs a physical coupon)

This is **not a print**. The analytic gate cannot see fusion, stringing, layer
adhesion, elephant-foot, warp, or whether the printed-in-place pivot actually
frees. It bounds the *dimensional* stack-up only. The highest-value cheap
follow-up is an explicit **designed pivot clearance** added to the SCAD, which
would convert M3 from unmodelled to analytic.

## FDM limit sources

The minimum-feature rules used here are the standard slicer conventions
(documented in Prusa/Bambu slicer knowledge bases): a vertical wall thinner than
~1 extrusion width under-extrudes, and a vertical slot below ~1 nozzle diameter
bridges or fuses. Repeated as `sourced fact` values with a stated conservative
margin. The free-gap and pivot-definition floors are **assumptions** and are
labelled as such in `FDM_LIMITS`.
