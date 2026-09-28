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
  positive); lateral clearance **+3.09 mm**; bbox **+4.96 mm**. Land reach is a
  finger *angular-throw* margin derived from the CAD land height
  (`LAND_H_NOMINAL = 0.90 mm` → 16.3°; low extreme 0.65 mm still seats):
  worst case **+0.35 mm** (DND-4 follow-up; the earlier −0.05 mm compared the
  land against an arbitrary ±0.20 mm window around a 0.50 mm artefact and was a
  modelling error, not a design failure).
- **Monte Carlo (200k, sigma = half_range/√3):** min-web pass fraction 1.0000,
  lateral 1.0000, land reach **1.0000** (min margin +0.087 mm).
- **Pivot free play (M3) is now resolved analytically (DND-4).** The coupon was
  changed from a printed-in-place pivot (no designed clearance) to a **designed
  journal fit**: the finger boss (`PIVOT_D = 0.80`) turns in a base socket bore
  `PIVOT_SOCKET_D = 0.80 + 2×0.20 = 1.20 mm`. The diametral free play is a
  CAD-set **0.40 mm**; worst-case boss-high/socket-low tolerance leaves
  **+0.08 mm** margin over the 0.20 mm free-gap floor, and the Monte Carlo pass
  fraction is **0.99998** (200k samples; the tiny tail is normal-distribution
  beyond the bounded ±0.06 tolerance, not a design boundary).
- **Disposition from the engine:** `S3_DENSITY_PRINTABLE` on the `A1-ANALYTIC`
  0.4 mm baseline row, with the explicit `[ANALYTIC SCREEN, NOT A PRINT]`
  warning. The decision tree reaches a pass on M1–M6 analytically once M3 is a
  designed fit.

## Residual uncertainty (vs a physical coupon)

This is **not a print**. The analytic gate cannot see fusion, stringing, layer
adhesion, elephant-foot, warp, or how the printed-in-practice boss/socket pair
deviates from the modelled tolerance class. It bounds the *dimensional* stack-up
only. With the designed clearance, M3 is no longer an unmodelled slicer unknown,
but the printed journal fit is still a **permanent qualitative risk** (ADR-001
§5.2). M4 land reach is now closed analytically as an angular-throw margin
(worst case **+0.35 mm**, MC pass **1.0000**); the remaining qualitative risk is
whether the as-printed land height and throw track the modelled tolerance class.

## FDM limit sources

The minimum-feature rules used here are the standard slicer conventions
(documented in Prusa/Bambu slicer knowledge bases): a vertical wall thinner than
~1 extrusion width under-extrudes, and a vertical slot below ~1 nozzle diameter
bridges or fuses. Repeated as `sourced fact` values with a stated conservative
margin. The free-gap and pivot-definition floors are **assumptions** and are
labelled as such in `FDM_LIMITS`.
