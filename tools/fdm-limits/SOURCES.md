# Sourced FDM process limits — citations

Companion to [`fdm_process_limits.py`](fdm_process_limits.py) and the analytic
checker [`../validate/analytic_printability.py`](../validate/analytic_printability.py).

Every limit is labelled **sourced fact**, **assumption**, or **calculation** so a
reader can see how much weight it carries. No value here is a measurement of a
printed part; the program performs no physical print tests (board directive
[DND-27](/DND/issues/DND-27)).

## Target process

Declared in the T11 coupon SCAD headers and
[`06-experiments/test11_falsification_library/PRINTABILITY_REPORT.md`](../../06-experiments/test11_falsification_library/PRINTABILITY_REPORT.md):

| Parameter | Value |
|---|---|
| Printer | Bambu Lab X1C |
| Build volume | 256 × 256 × 256 mm |
| Material | PLA |
| Nozzle | 0.4 mm |
| Layer height | 0.20 mm |
| Perimeters | 3 |

## Limits and sources

| Rule | Limit (0.4 mm nozzle) | Class | Source |
|---|---:|---|---|
| Extrusion width (one printed line) | ≈ 0.44 mm | sourced fact | Standard FDM behaviour: a 0.4 mm nozzle lays a line ~1.0–1.25× the nozzle; 1.1× used here. Vendor slicers default to ~0.42–0.45 mm for a 0.4 mm nozzle. See note below. |
| Minimum standalone feature | 0.44 mm | sourced fact | A feature narrower than one extrusion line cannot be formed reliably (the line has nowhere to bond). |
| Minimum robust wall (infill-free) | 0.88 mm | calculation | 2 × extrusion width. One line is a fragile waver; two lines bond into a solid wall. |
| Recommended load-bearing wall | 1.32 mm | calculation | `perimeters × extrusion width` = 3 × 0.44 mm, matching the declared 3-perimeter profile. |
| Max unsupported overhang | 45° | sourced fact | Protolabs Network (Hubs), *How to design parts for FDM 3D printing*: "an overhang can usually be printed up to 45° without compromising quality … Above 45°, support is required." <https://www.hubs.com/knowledge-base/how-design-parts-fdm-3d-printing/> |
| Max clean bridge span | 5 mm | sourced fact | Same guide: "if the bridge is less than 5 mm" it prints cleanly; longer bridges sag or need support. |
| Minimum reliable printed pin diameter | 5 mm | sourced fact | Same guide: pins under 5 mm print with only perimeters, a weak discontinuity, and may not print at all. For critical small pins, print a hole and insert an off-the-shelf pin. |
| Dimensional accuracy per axis | ±0.1 mm | **assumption** | A generic X1C-class figure, **not** vendor-quoted in this repo and **not** measured here. Used only for worst-case clearance stack-ups; small holes print undersize by more. |

### Note on the extrusion-width figure

The 1.1 × nozzle rule is an engineering convention rather than a single quoted
datasheet number. It is the value used by common slicers for a 0.4 mm nozzle and
is conservative (the true line is between 0.4 and 0.5 mm). Because the verdicts
that depend on it are all *robustness* (RISK) judgements rather than hard
go/kill gates, the sensitivity is small: shifting the assumption to 1.0× would
lower the robust-wall target to 0.80 mm and leave the coupon's 0.47 mm web as a
RISK either way.

## How the check is used

`analytic_printability.py` reads the coupon's constants straight from the
`.scad` source and compares each printed feature against these limits:

- **FAIL** — below a hard floor (one extrusion line). The feature is not
  reliably printable as designed.
- **RISK** — printable but below the robustness target (e.g. a 1-line wall).
  Expect fragility and inspect the design intent.
- **PASS** — at or above the robustness target.

## Residual uncertainty (explicit)

This is a **calculation over CAD-declared parameters**. It is *not* a slicer and
*not* a print. It does not model seam placement, thin-wall detection, bridging
parameters, machine calibration, filament lot, or moisture. It retires
geometry-vs-process risk only; it does not validate function or fit.
